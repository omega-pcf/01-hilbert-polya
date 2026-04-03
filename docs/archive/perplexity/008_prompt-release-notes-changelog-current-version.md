# Prompt para Investigación: Changelog Solo de Versión Actual en Release Notes

## Contexto Completo del Proyecto

### Stack Tecnológico Actual (YA IMPLEMENTADO)

**NO estamos buscando cambiar el stack, solo resolver el problema del changelog:**

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
CHANGELOG.md                # Generado por @release-it/conventional-changelog
scripts/
├── build.ts                # Genera PDF con versión correcta
└── ...
```

### Problema Específico

**Situación actual:**
- `@release-it/conventional-changelog` genera correctamente `CHANGELOG.md` con solo los cambios de la versión actual
- El archivo `CHANGELOG.md` se actualiza correctamente (solo añade la nueva versión al inicio)
- **PERO**: En las GitHub Release Notes se muestra TODO el historial del changelog, no solo los cambios de la versión actual

**Configuración actual en `.release-it.ts`:**
```typescript
github: {
  release: true,
  releaseName: 'v${version}',
  autoGenerate: false,
  assets: ['build/document-v*.pdf', 'checksums.txt'],
  releaseNotes:
    'cat CHANGELOG.md && printf "\\n\\n## Files\\n\\n- **PDF**: `build/document-v${version}.pdf` - Compiled preprint document\\n\\n## DOI\\n\\nDOI: 10.5281/zenodo.17619486"',
},
plugins: {
  '@release-it/conventional-changelog': {
    preset: {
      name: 'conventionalcommits',
    },
    infile: 'CHANGELOG.md',
  },
},
```

**El problema:**
- `cat CHANGELOG.md` lee TODO el archivo, que contiene el historial completo
- Necesitamos solo la sección de la versión actual (la primera sección del changelog)

**Ejemplo de `CHANGELOG.md` actual:**
```markdown
# Changelog

## [1.2.1](///compare/v1.2.0...v1.2.1) (2025-11-18)

## [1.2.0](///compare/v1.1.3...v1.2.0) (2025-11-18)

### Features

* **release:** add dotenv-cli to load GITHUB_TOKEN from .env f52be09

## [1.1.3](///compare/v1.1.2...v1.1.3) (2025-11-18)

### Bug Fixes

* **release:** remove redundant GitHub Action and use shell string for release notes 5fd2f0f

## [1.1.2](///compare/v1.1.1...v1.1.2) (2025-11-18)
...
```

**Lo que queremos en Release Notes:**
```markdown
## [1.2.1](///compare/v1.2.0...v1.2.1) (2025-11-18)

## Files

- **PDF**: `build/document-v1.2.1.pdf` - Compiled preprint document

## DOI

DOI: 10.5281/zenodo.17619486
```

**NO queremos:**
- Todo el historial de versiones anteriores
- Solo los cambios de la versión actual

### Lo que Ya Intentamos

**Intento 1: Leer archivo completo**
```typescript
releaseNotes: 'cat CHANGELOG.md && printf ...'
```
**Resultado:** Muestra todo el historial ❌

**Intento 2: Extraer solo primera sección con `sed` o `awk`**
```bash
# Intentamos algo como:
sed -n '/^## \[/,/^## \[/p' CHANGELOG.md | head -n 20
```
**Problema:** Esto es un hack, no la forma estándar. Además, puede ser frágil si el formato cambia.

**Intento 3: Usar función en `.release-it.ts`**
```typescript
releaseNotes: function(context) {
  const changelog = context.changelog || '';
  // ...
}
```
**Problema:** Las funciones NO funcionan en `.release-it.ts`, solo en `.release-it.js` o `.release-it.cjs` (según documentación oficial).

### Información Relevante de Documentación

**Según la respuesta anterior de Perplexity:**
- `context.changelog` contiene el changelog generado por `@release-it/conventional-changelog`
- `context.changelog` debería contener **solo los cambios de la versión actual**, no el historial completo
- El orden de ejecución es:
  1. Plugin conventional-changelog se ejecuta
  2. Lee commits desde el último tag
  3. Genera `CHANGELOG.md` (añade nueva versión al inicio)
  4. Almacena resultado en memory como `context.changelog`
  5. Se llama a `releaseNotes()` (función o comando shell)
  6. Accede a `context.changelog` disponible
  7. GitHub Release se crea con el resultado

**Propiedades disponibles en context:**
- `version` - Nueva versión
- `latestVersion` - Versión anterior
- `changelog` - Changelog generado (de conventional-changelog) - **¿Solo versión actual o todo?**
- `repo.owner`, `repo.repository` - Info del repo
- `branchName`, `releaseUrl`, `latestTag`, `tagName`

### Dudas Específicas

1. **¿Qué contiene exactamente `context.changelog`?**
   - ¿Solo los cambios de la versión actual?
   - ¿O todo el historial del `CHANGELOG.md`?
   - ¿Cómo se genera exactamente?

2. **¿Cómo acceder a `context.changelog` desde un comando shell?**
   - ¿Se expone como variable de entorno?
   - ¿Hay alguna forma nativa de accederlo?
   - ¿O solo está disponible en funciones?

3. **¿Cuál es la forma estándar según la documentación oficial?**
   - ¿Cómo lo hacen otros proyectos?
   - ¿Hay ejemplos oficiales de release notes con solo versión actual?
   - ¿Qué recomienda la documentación de release-it?

4. **¿Hay opciones de configuración en `@release-it/conventional-changelog`?**
   - ¿Alguna opción para controlar qué se incluye en `context.changelog`?
   - ¿Alguna opción para generar solo la versión actual?

5. **¿Deberíamos usar `autoGenerate: true`?**
   - ¿Qué hace exactamente `autoGenerate: true`?
   - ¿Genera solo la versión actual o todo el historial?
   - ¿Podemos personalizarlo?

6. **¿Hay alguna forma de extraer solo la primera sección del changelog de forma estándar?**
   - ¿Algún comando o herramienta estándar para esto?
   - ¿O debemos usar funciones (y por tanto cambiar a `.release-it.cjs`)?

### Restricciones Críticas (NO NEGOCIABLES)

1. **NO hacks:** Debe ser la forma estándar y recomendada
2. **NO adivinar:** Basado en documentación oficial o código fuente
3. **Preferir TypeScript:** Si es posible mantener `.release-it.ts`
4. **Si es necesario cambiar a `.release-it.cjs`:** Aceptable si es la forma estándar
5. **Usar `@release-it/conventional-changelog`:** No cambiar de plugin
6. **Mantener funcionalidad actual:** PDF, DOI, assets deben seguir funcionando

### Lo que Necesito Saber Exactamente

1. **¿Qué contiene `context.changelog` exactamente?**
   - Documentación oficial o código fuente que lo confirme
   - Ejemplos reales de su contenido

2. **¿Cómo acceder a `context.changelog` desde shell?**
   - Variable de entorno disponible
   - Forma nativa de acceso
   - O confirmación de que solo está disponible en funciones

3. **¿Cuál es la forma estándar recomendada?**
   - Ejemplos de la documentación oficial
   - Ejemplos de proyectos reales que usan release-it
   - Mejores prácticas según la comunidad

4. **¿Hay opciones de configuración que resuelvan esto?**
   - Opciones de `@release-it/conventional-changelog`
   - Opciones de `github.releaseNotes`
   - Opciones de `github.autoGenerate`

5. **Si necesitamos usar funciones, ¿cómo hacerlo correctamente?**
   - Cambiar a `.release-it.cjs` (si es necesario)
   - Tipo correcto para el context
   - Ejemplo completo funcional

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
- `CHANGELOG.md` (generado por conventional-changelog)
- `package.json` (versión source of truth)

**Comportamiento esperado:**
Cuando ejecuto `pnpm run release`, el release de GitHub debe tener:
- **Solo** los cambios de la versión actual (no todo el historial)
- Nombre correcto del PDF: `build/document-v${version}.pdf`
- DOI: `10.5281/zenodo.17619486`
- Todo en un template limpio y bien formateado

### Preguntas Específicas para Resolver

1. ¿Qué contiene exactamente `context.changelog` generado por `@release-it/conventional-changelog`?
2. ¿Cómo acceder a `context.changelog` desde un comando shell en `releaseNotes`?
3. ¿Cuál es la forma estándar recomendada por la documentación oficial?
4. ¿Hay opciones de configuración que resuelvan esto sin hacks?
5. ¿Deberíamos usar `autoGenerate: true` en lugar de `releaseNotes` personalizado?
6. ¿Si necesitamos funciones, cuál es la forma correcta de implementarlo?

**Por favor, proporciona:**
- Respuestas basadas en documentación oficial o código fuente de release-it y @release-it/conventional-changelog
- Referencias específicas a documentación (URLs, secciones)
- Ejemplos de código completos y funcionales
- Ejemplos de proyectos reales que resuelven esto correctamente
- **NO adivinar, solo información verificable**
- **NO hacks, solo formas estándar y recomendadas**

