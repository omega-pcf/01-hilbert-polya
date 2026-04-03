# Prompt para Investigación: Template de Release Notes en release-it con TypeScript

## Contexto Completo del Proyecto

### Stack Tecnológico Actual (YA IMPLEMENTADO)

**NO estamos buscando cambiar el stack, solo resolver el template de release notes:**

- **release-it v19.0.6**: Configurado en `.release-it.ts` (TypeScript)
- **@release-it/conventional-changelog v10.0.2**: Genera changelog automático en `CHANGELOG.md`
- **@release-it/bumper v7.0.5**: Sincroniza versiones en `package.json`, `CITATION.cff`, `.zenodo.json`
- **TypeScript v5+**: Configuración en `.release-it.ts` con `satisfies Config`
- **pnpm v9+**: Gestor de paquetes
- **GitHub Releases**: Automatizados vía release-it

**Estructura actual:**
```
.release-it.ts              # Configuración TypeScript
scripts/
├── release-notes-template.ts  # Template de release notes (NUEVO, con error de tipos)
├── build.ts                   # Genera PDF con versión correcta
└── ...
```

### Problema Específico

**Situación actual:**
- Release-it crea releases en GitHub pero el template es incorrecto
- Muestra `build/main.pdf` en lugar de `build/document-v${version}.pdf`
- No incluye el changelog generado por `@release-it/conventional-changelog`
- No incluye el DOI (`10.5281/zenodo.17619486`)

**Lo que necesito:**
1. Template personalizado de release notes que:
   - Use el changelog generado por `@release-it/conventional-changelog`
   - Incluya el nombre correcto del PDF: `build/document-v${version}.pdf`
   - Incluya el DOI: `10.5281/zenodo.17619486`
   - Sea configurado en TypeScript (`.release-it.ts`)

### Lo que Ya Intenté

**Intento 1: Función inline en `.release-it.ts`**
```typescript
github: {
  releaseNotes(context: any) {
    // ...
  } as any,
}
```
**Error:** TypeScript no acepta `any` y el tipo no coincide.

**Intento 2: Función en archivo separado**
```typescript
// scripts/release-notes-template.ts
import type { PluginContext } from 'release-it';

export function generateReleaseNotes(context: PluginContext): string {
  // ...
}
```
**Error:** `Module '"release-it"' has no exported member 'PluginContext'`.

### Configuración Actual

**`.release-it.ts`:**
```typescript
import type { Config } from 'release-it';
import { generateReleaseNotes } from './scripts/release-notes-template.js';

export default {
  github: {
    release: true,
    releaseName: 'v${version}',
    autoGenerate: false,
    assets: ['build/document-v*.pdf', 'checksums.txt'],
    releaseNotes: generateReleaseNotes,  // ← AQUÍ ESTÁ EL PROBLEMA
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
import type { PluginContext } from 'release-it';  // ← TIPO NO EXISTE

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

### Documentación Revisada

**GitHub Releases docs:** https://github.com/release-it/release-it/blob/HEAD/docs/github-releases.md

**Información clave encontrada:**
- `github.releaseNotes` puede ser:
  - String (comando shell)
  - Function (solo en `.release-it.js` o `.release-it.cjs`)
  - Object con templates

**Ejemplo de función en la documentación:**
```javascript
{
  github: {
    release: true,
    releaseNotes(context) {
      return context.changelog.split('\n').slice(1).join('\n');
    }
  }
}
```

**Nota importante:** La documentación dice "When the value is a function, it's executed with a single `context` parameter that contains the plugin context. The function can also be `async`. Make sure that it returns a string value."

### Dudas Específicas

1. **Tipo TypeScript correcto:**
   - ¿Qué tipo tiene el `context` en `releaseNotes(context)`?
   - ¿Existe un tipo exportado por release-it para esto?
   - ¿Debo definir mi propia interfaz basándome en las propiedades que uso (`changelog`, `version`)?

2. **Soporte de funciones en TypeScript:**
   - La documentación menciona que funciones solo funcionan en `.release-it.js` o `.release-it.cjs`
   - ¿Funciona en `.release-it.ts` también?
   - Si no, ¿cómo hacerlo funcionar con TypeScript?

3. **Propiedades del context:**
   - ¿Qué propiedades tiene el `context`?
   - ¿`context.changelog` contiene el changelog generado por `@release-it/conventional-changelog`?
   - ¿`context.version` contiene la nueva versión?
   - ¿Hay otras propiedades útiles?

4. **Alternativas si funciones no funcionan en TS:**
   - ¿Puedo usar un string con comando shell que lea el changelog?
   - ¿Puedo usar el objeto template con placeholders?
   - ¿Cómo acceder al changelog generado por conventional-changelog desde un comando shell?

5. **Integración con conventional-changelog:**
   - ¿El changelog generado está disponible en `context.changelog` automáticamente?
   - ¿O necesito leerlo del archivo `CHANGELOG.md` manualmente?

### Restricciones Críticas (NO NEGOCIABLES)

1. **NO cambiar a JavaScript:** Debe funcionar en `.release-it.ts`
2. **NO usar `any`:** Tipos correctos y type-safe
3. **NO adivinar:** Basado en documentación oficial o código fuente
4. **Template separado:** No inline en `.release-it.ts`
5. **Usar changelog automático:** Del plugin `@release-it/conventional-changelog`

### Lo que Necesito Saber Exactamente

1. **Tipo TypeScript correcto para `context` en `releaseNotes`:**
   - Definición exacta del tipo
   - Si no existe, cómo definir una interfaz correcta
   - Propiedades disponibles en el context

2. **Soporte de funciones en `.release-it.ts`:**
   - ¿Funciona nativamente?
   - Si no, ¿cómo hacerlo funcionar?
   - Alternativas type-safe

3. **Propiedades del context:**
   - Lista completa de propiedades disponibles
   - Cómo acceder al changelog de conventional-changelog
   - Cómo acceder a la versión

4. **Ejemplo funcional completo:**
   - Código TypeScript completo que funcione
   - Con tipos correctos
   - Sin `any`
   - Template separado en archivo propio

### Información Adicional

**Versiones:**
- release-it: 19.0.6
- @release-it/conventional-changelog: 10.0.2
- TypeScript: 5.x
- Node.js: 20+

**Archivos relevantes:**
- `.release-it.ts` (configuración principal)
- `scripts/release-notes-template.ts` (template actual con error)
- `CHANGELOG.md` (generado por conventional-changelog)
- `package.json` (versión source of truth)

**Comportamiento esperado:**
Cuando ejecuto `pnpm run release`, el release de GitHub debe tener:
- Changelog completo del `@release-it/conventional-changelog`
- Nombre correcto del PDF: `build/document-v1.1.3.pdf` (ejemplo)
- DOI: `10.5281/zenodo.17619486`
- Todo en un template limpio y bien formateado

### Preguntas Específicas para Resolver

1. ¿Cuál es el tipo TypeScript correcto para el parámetro `context` en `releaseNotes`?
2. ¿Cómo hacer que funciones funcionen en `.release-it.ts` (no solo `.js`)?
3. ¿Qué propiedades tiene el `context` y cómo acceder al changelog?
4. ¿Hay un ejemplo completo funcional de esto en TypeScript?
5. ¿Cuál es la mejor práctica según la documentación oficial?

**Por favor, proporciona:**
- Respuestas basadas en documentación oficial o código fuente de release-it
- Ejemplos de código TypeScript completos y funcionales
- Referencias a documentación específica
- NO adivinar, solo información verificable

