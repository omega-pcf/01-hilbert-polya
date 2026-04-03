# Especificación: Releases Automáticos Zenodo con release-it

## Stack Tecnológico

- **release-it**: Versionado semántico + GitHub releases
- **@release-it/bumper**: Sincronización multi-archivo (package.json → CITATION.cff, .zenodo.json)
- **TypeScript + tsx**: Scripts de orquestación
- **Docker (nanozoo/pdflatex)**: Compilación LaTeX determinística
- **Zenodo webhook**: Integración automática (no requiere Actions adicionales)

## Flujo de Release

```
npm run release
  → release-it prompt versión
  → @release-it/bumper actualiza version en package.json, CITATION.cff, .zenodo.json
  → after:bump hook:
    - Actualiza date-released en CITATION.cff
    - Compila PDF con SOURCE_DATE_EPOCH desde git commit
    - Genera checksums SHA256
    - git add archivos modificados
  → Git commit + tag v${version}
  → Git push commits + tag
  → GitHub Release con PDF como asset
  → Zenodo webhook automático → descarga ZIP del tag → lee .zenodo.json → crea versión + DOI
```

## Estructura de Archivos

```
project/
├── .release-it.json          # Config release-it
├── package.json              # Source of truth para versión
├── CITATION.cff              # Metadata académica (actualizado por bumper)
├── .zenodo.json              # Metadata Zenodo (actualizado por bumper)
├── main.tex                  # LaTeX source (v1 español, v2 inglés)
├── build/main.pdf            # PDF compilado (renombrado a document-v${version}.pdf)
├── scripts/
│   └── release-orchestrator.ts  # after:bump hook script
└── .github/workflows/
    └── (solo si necesario para validación pre-release)
```

## Configuración release-it

```json
{
  "git": {
    "commitMessage": "chore: release v${version}",
    "tagName": "v${version}",
    "requireCleanWorkingDir": false,
    "requireBranch": "main"
  },
  "github": {
    "release": true,
    "releaseName": "v${version}",
    "assets": ["build/document-v*.pdf", "checksums.txt"]
  },
  "hooks": {
    "after:bump": "npx tsx scripts/release-orchestrator.ts ${version}"
  },
  "plugins": {
    "@release-it/bumper": {
      "in": "package.json",
      "out": [
        { "file": "CITATION.cff", "path": "version", "type": "text/yaml" },
        { "file": ".zenodo.json", "path": "version", "type": "application/json" }
      ]
    }
  }
}
```

## Script Orchestrator (after:bump)

**Responsabilidades:**
1. Actualizar `date-released` en CITATION.cff (bumper no lo hace)
2. Compilar PDF con SOURCE_DATE_EPOCH desde `git log -1 --pretty=%ct`
3. Renombrar `main.pdf` → `document-v${version}.pdf`
4. Generar `checksums.txt` (SHA256)
5. `git add` todos los archivos modificados

**Compilación determinística:**
```bash
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
docker run --rm \
  -v $(pwd):/workdir -w /workdir \
  -e SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH \
  -e LC_ALL=C -e LANG=C -e TZ=UTC \
  registry.gitlab.com/islandoftex/images/texlive:TL2024-2024-03-15-full \
  latexmk -pdf -interaction=nonstopmode main.tex
```

## Schema .zenodo.json

**Campos críticos:**
- `upload_type: "publication"` (no "software")
- `publication_type: "preprint"`
- `language: "spa"` (ISO 639-2, 3 letras) para v1 español
- `version: "1.0.0"` (string, sin "v" prefix)
- `creators`: array con `name`, `orcid`, `affiliation`
- `related_identifiers`: GitHub release URL (`isSupplementTo`), Colab (`isDocumentedBy`)

**Validación:**
```bash
check-jsonschema --schemafile \
  https://raw.githubusercontent.com/zenodo/zenodo/master/zenodo/modules/deposit/jsonschemas/deposits/records/legacyrecord.json \
  .zenodo.json
```

## Schema CITATION.cff

**Campos mínimos:**
- `cff-version: "1.2.0"`
- `title`, `version`, `date-released` (actualizado en after:bump)
- `authors`: `family-names`, `given-names`, `orcid`, `affiliation`
- `languages: ["es"]` (ISO 639-1, 2 letras)

**Validación:**
```bash
pip install cffconvert
cffconvert --validate
```

## Interdependencias Críticas

1. **@release-it/bumper ejecuta ANTES de after:bump** → version ya actualizada
2. **after:bump ejecuta ANTES de git commit** → permite modificar archivos + git add
3. **.zenodo.json actualizado ANTES de git tag** → tag apunta a commit con metadata correcta
4. **Git tag ANTES de GitHub Release** → release requiere tag existente
5. **GitHub Release published ANTES de Zenodo webhook** → solo published releases (no drafts)

## LaTeX Primitives para Reproducibilidad

Agregar al inicio de `main.tex`:
```latex
\pdfinfoomitdate=1
\pdftrailerid{}
\pdfsuppressptexinfo=15
\pdfminorversion=5
```

**NO usar:** `\today` (usar fecha fija), paths absolutos, random sin seed.

## GitHub Actions (Opcional - Solo Validación)

Si se requiere validación pre-release:
```yaml
name: Validate Release
on:
  pull_request:
    paths: ['.zenodo.json', 'CITATION.cff', 'main.tex']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate schemas
        run: |
          check-jsonschema --schemafile <zenodo-schema> .zenodo.json
          cffconvert --validate
```

**No se requiere Action para releases** - release-it + Zenodo webhook son suficientes.

## Criterios de Aceptación

- ✅ `npm run release` ejecuta flujo completo sin intervención manual (excepto prompt versión)
- ✅ PDF compilado es reproducible (mismo commit = mismo SHA256)
- ✅ .zenodo.json y CITATION.cff sincronizados con versión
- ✅ GitHub Release incluye PDF como asset
- ✅ Zenodo crea versión automáticamente con metadata correcta
- ✅ DOI generado y visible en GitHub Release

## Plan de Implementación

1. **Setup inicial:**
   - `npm install release-it @release-it/bumper tsx typescript yaml`
   - Crear `.release-it.json`
   - Crear `scripts/release-orchestrator.ts`
   - Template `.zenodo.json` y `CITATION.cff`

2. **Testing:**
   - Dry run: `npx release-it --dry-run`
   - Validar schemas localmente
   - Test en branch separado antes de main

3. **Primer release:**
   - `npm run release` → `v1.0.3`
   - Verificar GitHub Release + Zenodo record

4. **v2 inglés:**
   - Migrar `main.tex` a inglés
   - Actualizar `.zenodo.json` `language: "eng"`
   - Release `v2.0.0`
