# Prompt para Investigación: Template de Release Notes y GitHub Action en release-it

## Contexto Completo del Proyecto

### Stack Tecnológico Actual (YA IMPLEMENTADO)

**NO estamos buscando cambiar el stack, solo resolver el template y conciliar con GitHub Action:**

- **release-it v19.0.6**: Configurado en `.release-it.ts` (TypeScript)
- **@release-it/conventional-changelog v10.0.2**: Genera changelog automático en `CHANGELOG.md`
- **@release-it/bumper v7.0.5**: Sincroniza versiones en `package.json`, `CITATION.cff`, `.zenodo.json`
- **TypeScript v5+**: Configuración en `.release-it.ts` con `satisfies Config`
- **pnpm v9+**: Gestor de paquetes
- **GitHub Releases**: Automatizados vía release-it
- **Zenodo webhook oficial**: Ya habilitado en GitHub (integración automática)

**Estructura actual:**
```
.release-it.ts              # Configuración TypeScript
.github/workflows/
└── release.yml             # GitHub Action que se ejecuta en push de tags v*
scripts/
├── release-notes-template.ts  # Template de release notes (con error de tipos)
├── build.ts                   # Genera PDF con versión correcta
└── ...
```

### Problema Específico

**Situación actual:**
1. **Release-it crea releases automáticamente** cuando ejecuto `pnpm run release`
2. **GitHub Action también crea releases** cuando se hace push de un tag `v*` (trigger: `on.push.tags: ['v*']`)
3. **Conflicto/duplicación**: Ambos están creando releases, posiblemente duplicados o conflictivos
4. **Template incorrecto en Action**: El Action tiene template hardcodeado que menciona `build/main.pdf` en lugar de `build/document-v${version}.pdf`
5. **Template en release-it**: Intentamos configurar `github.releaseNotes` como función TypeScript pero hay problemas de tipos

**Lo que necesito:**
1. **Decidir si el GitHub Action es necesario:**
   - release-it ya crea releases automáticamente
   - Zenodo webhook oficial ya está habilitado (no necesita Action)
   - ¿El Action es redundante o tiene un propósito específico?
   - ¿Debo eliminarlo o modificarlo?

2. **Template correcto de release notes:**
   - Usar el changelog generado por `@release-it/conventional-changelog`
   - Incluir el nombre correcto del PDF: `build/document-v${version}.pdf`
   - Incluir el DOI: `10.5281/zenodo.17619486`
   - Configurado en TypeScript (`.release-it.ts`) sin errores de tipos

### GitHub Action Actual

**`.github/workflows/release.yml`:**
```yaml
name: Create Release with PDF

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Get tag name
        id: tag
        run: echo "TAG_NAME=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
      
      - name: Extract version number
        id: version
        run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT
      
      - name: Check if PDF exists
        id: check_pdf
        run: |
          if [ -f "build/main.pdf" ]; then
            echo "exists=true" >> $GITHUB_OUTPUT
            echo "PDF found at build/main.pdf"
          else
            echo "exists=false" >> $GITHUB_OUTPUT
            echo "Warning: PDF not found at build/main.pdf"
          fi
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: ${{ steps.tag.outputs.TAG_NAME }}
          name: Release ${{ steps.version.outputs.VERSION }}
          body: |
            ## Release ${{ steps.version.outputs.VERSION }}
            
            This release includes the compiled PDF of the preprint.
            
            ### Files
            - **PDF**: `build/main.pdf` - Compiled preprint document
            
            ### DOI
            DOI: [10.5281/zenodo.17619486](https://doi.org/10.5281/zenodo.17619486)
          files: |
            build/main.pdf
          draft: false
          prerelease: false
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Problemas identificados:**
- Busca `build/main.pdf` pero el PDF real es `build/document-v${version}.pdf`
- Template hardcodeado, no usa el changelog automático
- Se ejecuta cuando release-it ya creó el release (duplicación potencial)

### Configuración release-it Actual

**`.release-it.ts`:**
```typescript
import type { Config } from 'release-it';
import { generateReleaseNotes } from './scripts/release-notes-template.js';

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
    releaseNotes: generateReleaseNotes,  // ← PROBLEMA: tipo incorrecto
  },
  plugins: {
    '@release-it/conventional-changelog': {
      preset: { name: 'conventionalcommits' },
      infile: 'CHANGELOG.md',
    },
  },
} satisfies Config;
```

**`scripts/release-notes-template.ts`:**
```typescript
import type { PluginContext } from 'release-it';  // ← ERROR: tipo no existe

export function generateReleaseNotes(context: PluginContext): string {
  const changelog = context.changelog || '';
  const doi = '10.5281/zenodo.17619486';
  const pdfName = `document-v${context.version}.pdf`;
  
  return `${changelog}

## Files

- **PDF**: \`build/${pdfName}\` - Compiled preprint document

## DOI

DOI: ${doi}`;
}
```

**Error TypeScript:**
```
Module '"release-it"' has no exported member 'PluginContext'.
```

### Flujo Actual de Release

**Cuando ejecuto `pnpm run release`:**
1. release-it ejecuta hooks y plugins
2. release-it hace git commit + tag + push
3. release-it crea GitHub Release automáticamente (si `GITHUB_TOKEN` está configurado)
4. **GitHub Action se dispara** porque se hizo push de tag `v*`
5. Action crea otro release (o actualiza el existente) con template hardcodeado

**Problema:** Duplicación o conflicto entre release-it y Action.

### Zenodo Integration

**Zenodo webhook oficial de GitHub:**
- Ya está habilitado en el repositorio
- Se activa automáticamente cuando se publica un GitHub Release
- Descarga el ZIP del tag
- Lee `.zenodo.json` del tag
- Crea versión en Zenodo con DOI

**No requiere GitHub Action** - funciona automáticamente con releases de GitHub.

### Dudas Específicas

1. **¿Es necesario el GitHub Action?**
   - release-it ya crea releases automáticamente
   - Zenodo webhook funciona con releases de GitHub (no necesita Action)
   - ¿El Action tiene algún propósito que release-it no cubre?
   - ¿Debo eliminarlo completamente o modificarlo?

2. **Tipo TypeScript correcto para `releaseNotes`:**
   - ¿Qué tipo tiene el `context` en `releaseNotes(context)`?
   - ¿Existe un tipo exportado por release-it?
   - ¿Debo definir mi propia interfaz?
   - ¿Cómo hacerlo type-safe sin `any`?

3. **Soporte de funciones en `.release-it.ts`:**
   - La documentación menciona funciones solo en `.release-it.js` o `.release-it.cjs`
   - ¿Funciona en `.release-it.ts` también?
   - Si no, ¿cómo hacerlo funcionar con TypeScript?
   - ¿Alternativas type-safe?

4. **Propiedades del context:**
   - ¿Qué propiedades tiene el `context`?
   - ¿`context.changelog` contiene el changelog de `@release-it/conventional-changelog`?
   - ¿`context.version` contiene la nueva versión?
   - ¿Hay otras propiedades útiles?

5. **Integración con conventional-changelog:**
   - ¿El changelog está disponible en `context.changelog` automáticamente?
   - ¿O necesito leerlo de `CHANGELOG.md` manualmente?

6. **Alternativas si funciones no funcionan en TS:**
   - ¿Puedo usar string con comando shell?
   - ¿Puedo usar objeto template con placeholders?
   - ¿Cómo acceder al changelog desde shell?

### Restricciones Críticas (NO NEGOCIABLES)

1. **NO cambiar a JavaScript:** Debe funcionar en `.release-it.ts`
2. **NO usar `any`:** Tipos correctos y type-safe
3. **NO adivinar:** Basado en documentación oficial o código fuente
4. **Template separado:** No inline en `.release-it.ts`
5. **Usar changelog automático:** Del plugin `@release-it/conventional-changelog`
6. **Minimalismo:** Solo lo indispensable, eliminar redundancias

### Lo que Necesito Saber Exactamente

1. **¿Eliminar o modificar el GitHub Action?**
   - ¿Es redundante con release-it?
   - ¿Tiene algún propósito específico que release-it no cubre?
   - ¿Cómo conciliar ambos si ambos son necesarios?

2. **Tipo TypeScript correcto para `context` en `releaseNotes`:**
   - Definición exacta del tipo
   - Si no existe, cómo definir una interfaz correcta
   - Propiedades disponibles en el context

3. **Soporte de funciones en `.release-it.ts`:**
   - ¿Funciona nativamente?
   - Si no, ¿cómo hacerlo funcionar?
   - Alternativas type-safe

4. **Propiedades del context:**
   - Lista completa de propiedades disponibles
   - Cómo acceder al changelog de conventional-changelog
   - Cómo acceder a la versión

5. **Ejemplo funcional completo:**
   - Código TypeScript completo que funcione
   - Con tipos correctos
   - Sin `any`
   - Template separado en archivo propio
   - Integrado con conventional-changelog

### Información Adicional

**Versiones:**
- release-it: 19.0.6
- @release-it/conventional-changelog: 10.0.2
- @release-it/bumper: 7.0.5
- TypeScript: 5.x
- Node.js: 20+
- pnpm: 9+

**Archivos relevantes:**
- `.release-it.ts` (configuración principal)
- `.github/workflows/release.yml` (Action actual)
- `scripts/release-notes-template.ts` (template con error de tipos)
- `CHANGELOG.md` (generado por conventional-changelog)
- `package.json` (versión source of truth)

**Comportamiento esperado:**
Cuando ejecuto `pnpm run release`, debe:
1. release-it crea el release de GitHub con:
   - Changelog completo del `@release-it/conventional-changelog`
   - Nombre correcto del PDF: `build/document-v${version}.pdf`
   - DOI: `10.5281/zenodo.17619486`
   - Assets: PDF y checksums.txt
2. Zenodo webhook automático crea versión en Zenodo
3. **NO debe haber duplicación o conflicto con GitHub Action**

### Preguntas Específicas para Resolver

1. ¿El GitHub Action es necesario o debe eliminarse?
2. ¿Cuál es el tipo TypeScript correcto para el parámetro `context` en `releaseNotes`?
3. ¿Cómo hacer que funciones funcionen en `.release-it.ts` (no solo `.js`)?
4. ¿Qué propiedades tiene el `context` y cómo acceder al changelog?
5. ¿Hay un ejemplo completo funcional de esto en TypeScript?
6. ¿Cuál es la mejor práctica según la documentación oficial?
7. ¿Cómo conciliar release-it con GitHub Action si ambos son necesarios?

**Por favor, proporciona:**
- Respuestas basadas en documentación oficial o código fuente de release-it
- Ejemplos de código TypeScript completos y funcionales
- Referencias a documentación específica
- Recomendación clara sobre el GitHub Action (eliminar, modificar, o mantener)
- NO adivinar, solo información verificable

