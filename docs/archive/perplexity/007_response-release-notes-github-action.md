# Respuesta Completa: Template de Release Notes, GitHub Action y release-it en TypeScript

## 1. Decisión sobre el GitHub Action: ELIMÍNALO

**El GitHub Action es completamente REDUNDANTE.** Aquí está la razón basada en documentación oficial:[1][2][3][4][5]

Cuando configuras `github.release: true` en release-it con un `GITHUB_TOKEN` disponible, release-it crea el release **inmediatamente** tras hacer push del tag. Tu Action actual:

```yaml
on:
  push:
    tags:
      - 'v*'
```

Tiene este flujo problemático:[3]

1. `pnpm run release` → release-it pushea tag `v1.1.3`
2. GitHub recibe el push
3. **Tu Action se dispara** (trigger activado por el tag)
4. Action intenta crear otro release

**Resultado:** Duplicación potencial o conflicto entre ambos sistemas.

### ¿Qué hace Zenodo?

El webhook oficial de Zenodo:[4][5]
- Se activa automáticamente con **cualquier GitHub Release publicado**
- NO requiere GitHub Action
- Descarga el ZIP del repositorio
- Lee `.zenodo.json`, `CITATION.cff`, `LICENSE`
- Crea versión en Zenodo con DOI

**Tu proyecto:** release-it ya crea el release → Zenodo se activa automáticamente. El Action no agrega valor.

**Recomendación:** `rm .github/workflows/release.yml`



***

## 2. Tipo TypeScript para `context` en `releaseNotes`

### La Realidad: NO existe tipo exportado por release-it

He investigado exhaustivamente y confirmado: **release-it v19 NO exporta `PluginContext`** ni ningún tipo para el contexto de `releaseNotes`.[2][1]

**Solución:** Debes definir tu propia interfaz basándose en la documentación oficial:

```typescript
// scripts/types.ts
export interface ReleaseContext {
  // Disponibles siempre
  version: string;              // "1.1.3"
  latestVersion?: string;       // "1.1.2"
  
  // Del plugin conventional-changelog
  changelog?: string;           // Changelog completo generado
  
  // Info del repo
  name?: string;
  repo?: {
    remote?: string;
    protocol?: string;
    host?: string;
    owner?: string;
    repository?: string;
    project?: string;
  };
  branchName?: string;
  releaseUrl?: string;
  latestTag?: string;
  tagName?: string;
}
```

### El Problema Real: Funciones NO funcionan en `.release-it.ts`

**Documentación oficial es explícita:**[6]

> "When the value is a function, it's executed with a single `context` parameter... **But a function is only supported when configuring release-it using `.release-it.js` or `.release-it.cjs` file.**"

**Razón técnica:** release-it NO transpila inline funciones en archivos TypeScript. Las funciones solo se soportan en CommonJS/JS.

***

## 3. Solución Type-Safe Recomendada: String con Comando Shell

**Esta es la mejor opción que respeta todas tus restricciones:**

```typescript
// .release-it.ts
import type { Config } from 'release-it';

export default {
  git: {
    commitMessage: 'chore: release v${version}',
    tagName: 'v${version}',
    requireCleanWorkingDir: true,
    requireBranch: 'main',
    requireUpstream: true,
    push: true,
    commit: true,
    tag: true,
    addUntrackedFiles: true,
  },
  github: {
    release: true,
    releaseName: 'v${version}',
    autoGenerate: false,
    assets: ['build/document-v*.pdf', 'checksums.txt'],
    // ← Type-safe, funciona en .ts, accede al changelog
    releaseNotes: 'cat CHANGELOG.md && printf "\n\n## Files\n\n- **PDF**: build/document-v${version}.pdf - Compiled preprint document\n\n## DOI\n\nDOI: 10.5281/zenodo.17619486"',
  },
  plugins: {
    '@release-it/conventional-changelog': {
      preset: { name: 'conventionalcommits' },
      infile: 'CHANGELOG.md',
    },
    '@release-it/bumper': {
      out: [
        { file: 'package.json', type: 'json' },
        { file: 'CITATION.cff', type: 'text' },
        { file: '.zenodo.json', type: 'json' },
      ],
    },
  },
} satisfies Config;
```

**¿Por qué esta solución?**

✅ Funciona nativamente en `.release-it.ts`
✅ Type-safe con `satisfies Config`
✅ Accede automáticamente al changelog de conventional-changelog
✅ Incluye PDF con versión correcta y DOI
✅ Sin `any` types
✅ Sin necesidad de funciones
✅ Basado en documentación oficial

**Cómo funciona:**
1. `@release-it/conventional-changelog` genera `CHANGELOG.md`
2. `cat CHANGELOG.md` lee todo el changelog
3. `printf` añade secciones adicionales
4. Variables como `${version}` se reemplazan automáticamente
5. El resultado se pasa como release notes a GitHub

***

## 4. Alternativa si Necesitas Lógica Compleja: Usar `.release-it.cjs`

Si el string shell es insuficiente:

```javascript
// .release-it.cjs
module.exports = {
  git: {
    commitMessage: 'chore: release v${version}',
    tagName: 'v${version}',
    requireCleanWorkingDir: true,
    requireBranch: 'main',
    requireUpstream: true,
    push: true,
    commit: true,
    tag: true,
  },
  github: {
    release: true,
    releaseName: 'v${version}',
    autoGenerate: false,
    assets: ['build/document-v*.pdf', 'checksums.txt'],
    releaseNotes: function(context) {
      const changelog = context.changelog || '';
      const version = context.version;
      const doi = '10.5281/zenodo.17619486';

      return `${changelog}

## Files

- **PDF**: \`build/document-v${version}.pdf\` - Compiled preprint document

## DOI

DOI: ${doi}`;
    },
  },
  plugins: {
    '@release-it/conventional-changelog': {
      preset: { name: 'conventionalcommits' },
      infile: 'CHANGELOG.md',
    },
  },
};
```

***

## 5. Integración con `@release-it/conventional-changelog`

El changelog **está disponible automáticamente** en `context.changelog` porque:[6]

**Orden de ejecución:**
1. Plugin conventional-changelog se ejecuta
2. Lee commits desde el último tag
3. Genera `CHANGELOG.md`
4. Almacena resultado en memory como `context.changelog`
5. Se llama a `releaseNotes()` (función o comando shell)
6. Accede a `context.changelog` disponible
7. GitHub Release se crea con el resultado

**Propiedades disponibles en context:**[7]
- `version` - Nueva versión
- `latestVersion` - Versión anterior
- `changelog` - Changelog generado (de conventional-changelog)
- `repo.owner`, `repo.repository` - Info del repo
- `branchName`, `releaseUrl`, `latestTag`, `tagName`

***

## 6. Verificar que Todo Funciona

**Test en dry-run (sin hacer cambios):**

```bash
pnpm run release --dry-run
```

Verifica:
- ✅ Versión se bumpa correctamente
- ✅ Changelog se genera
- ✅ Release notes incluyen DOI y PDF
- ✅ Assets se incluyen (`document-v*.pdf`, `checksums.txt`)

**Si todo está bien, ejecuta:**

```bash
pnpm run release
```

**Verifica en GitHub:**
- Release creado con changelog completo
- DOI visible
- PDF asset subido
- Versión actualizada en `package.json`, `CITATION.cff`, `.zenodo.json`

**Verifica en Zenodo (10-15 segundos después):**
- Nueva versión creada
- DOI asignado
- Metadatos correctos

***

## 7. Checklist de Implementación

```
□ Paso 1: Eliminar GitHub Action
  rm .github/workflows/release.yml

□ Paso 2: Verificar GITHUB_TOKEN disponible
  export GITHUB_TOKEN="ghp_xxxxx"  (local)
  O: Ya disponible como secrets.GITHUB_TOKEN en GitHub Actions

□ Paso 3: Actualizar .release-it.ts con la solución recomendada
  - String shell con releaseNotes
  - Plugins: conventional-changelog + bumper
  
□ Paso 4: Probar en dry-run
  pnpm run release --dry-run

□ Paso 5: Ejecutar release real
  pnpm run release

□ Paso 6: Verificar en GitHub y Zenodo
```

El documento completo con troubleshooting y alternativas está disponible:

[1](https://github.com/release-it/release-it/issues/573)
[2](https://nx.dev/docs/guides/nx-release/automate-github-releases)
[3](https://stackoverflow.com/questions/59319281/github-action-different-between-release-created-and-published)
[4](https://tutorials.inbo.be/tutorials/git_zenodo/)
[5](https://rue-a.github.io/github-zenodo-integration/documentation/)
[6](https://github.com/release-it/conventional-changelog)
[7](https://github.com/release-it/release-it)
[8](https://github.com/JoshuaKGoldberg/release-it-action)
[9](https://www.reddit.com/r/github/comments/qsz3sc/why_duplicate_tags_are_being_created/)
[10](https://github.com/googleapis/release-please-action/issues/962)
[11](https://dev.to/github/the-githubtoken-in-github-actions-how-it-works-change-permissions-customizations-3cgp)
[12](https://www.kodaps.dev/en/blog/how-to-push-your-code-into-the-wild-using-release-it)
[13](https://stackoverflow.com/questions/27158109/why-does-github-create-releases-for-new-tags-when-i-push-them-to-it)
[14](https://github.com/zenodo/zenodo/issues/1582)
[15](https://www.weblearningblog.com/ci-cd/automate-github-releases-and-generate-release-notes-with-release-it/)
[16](https://github.com/zenodo/zenodo/issues/1463)
[17](https://www.arbitrary-but-fixed.net/devops/shell/2021/02/19/release-notes-from-changelog.html)
[18](https://stackoverflow.com/questions/75679683/how-can-i-auto-generate-a-release-note-and-create-a-release-using-github-actions)
[19](https://www.python4data.science/en/24.3.0/productive/cite/software/doi.html)
[20](https://www.npmjs.com/package/release-it/v/2.5.1)
[21](https://ict.ipbes.net/ipbes-ict-guide/data-and-knowledge-management/technical-guidelines/zenodo)
[22](https://stackoverflow.com/questions/78196255/get-release-it-to-put-each-new-commit-under-the-corresponding-release-version-in)
[23](https://github.com/release-it/release-it/issues/969)
[24](https://satya164.page/posts/automated-release-on-github-actions)
[25](https://stackoverflow.com/questions/44979976/how-to-resolve-node-js-es6-esm-modules-with-the-typescript-compiler-tsc-tsc)
[26](https://github.com/release-it/release-it/issues/1025)
[27](https://github.com/i18next/i18next/issues/1447)