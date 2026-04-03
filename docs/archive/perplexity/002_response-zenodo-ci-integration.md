# Arquitectura backwards-first: GitHub → Zenodo determinístico

Automatización completa para publicación reproducible de documentos LaTeX en Zenodo vía GitHub Releases, con versionado semántico y compilación determinística.

## Flujo de ejecución: desde Zenodo hacia atrás

La arquitectura se construye **backwards** desde Zenodo como destino, garantizando que cada paso anterior prepara exactamente lo que el paso siguiente requiere.

### Zenodo como punto final: lo que realmente necesita

Zenodo recibe webhooks de GitHub cuando se publica un release. **El momento crítico**: Zenodo descarga el repositorio en el estado exacto del git tag, no el estado actual del branch. Esta distinción es fundamental para toda la arquitectura.

**Webhook que Zenodo consume:**
- Evento: `release` con `action: "published"`
- Payload incluye: `tag_name`, `tarball_url`, `zipball_url`, metadata del repositorio
- Zenodo descarga snapshot del repo en estado del tag (no clona git, descarga tarball)

**Lectura de metadatos con prioridad estricta:**
1. `.zenodo.json` en repository root (máxima prioridad)
2. `CITATION.cff` si existe (complementa campos faltantes)
3. GitHub API metadata (contributors, topics, descripción)
4. Valores por defecto (upload_type: "software")

**Comportamiento de versionado automático:**
- Primera release: crea registro Zenodo + Concept DOI + Version DOI
- Releases subsecuentes: crea NUEVA versión bajo mismo Concept DOI
- Cada versión obtiene su propio Version DOI único
- **NO falla** si detecta contenido similar - siempre crea nueva versión
- Versiones ordenadas por fecha de creación (no por número de versión semántica)

**Límites técnicos de Zenodo:**
- 50 GB total por depósito (expandible bajo solicitud)
- 100 archivos máximo por depósito
- Solo procesa releases publicados (drafts ignorados)
- No hay endpoint de pre-validación para .zenodo.json

### Schema .zenodo.json: campos exactos que Zenodo valida

**Campos esenciales:**
```json
{
  "title": "string",
  "upload_type": "software|publication|poster|dataset|image|video|...",
  "description": "string (HTML permitido)",
  "creators": [
    {
      "name": "Apellido, Nombre",
      "affiliation": "string (opcional)",
      "orcid": "string (opcional)"
    }
  ],
  "access_right": "open|embargoed|restricted|closed",
  "license": "string (ej: 'MIT', 'cc-by-4.0')"
}
```

**Campo version (tipo y validación):**
- Tipo: `string` sin restricciones de formato
- Acepta cualquier valor: `"1.0.0"`, `"2.1.5-beta"`, `"21.10 (Impish)"`
- Zenodo NO parsea semver automáticamente
- Zenodo NO extrae language codes del version string

**Campo language (crítico):**
- Tipo: `string` con código ISO 639-2 o 639-3 (3 letras)
- Ejemplo: `"eng"` para inglés (no `"en"`)
- Divergencia con CITATION.cff que acepta ISO 639-1 (2 letras)
- **Campo separado** - no se parsea desde version string

**Campos opcionales con condicionales:**
- `publication_type`: requerido si `upload_type: "publication"`
- `image_type`: requerido si `upload_type: "image"`
- `embargo_date`: requerido si `access_right: "embargoed"`
- `license`: requerido si `access_right` es `"open"` o `"embargoed"`

**Grants y communities:**
```json
{
  "grants": [
    {"id": "10.13039/501100000780::283595"}
  ],
  "communities": [
    {"identifier": "community-id"}
  ]
}
```

**Schema completo:** https://github.com/zenodo/zenodo/blob/master/zenodo/modules/deposit/jsonschemas/deposits/records/legacyrecord.json

**Validación local (workaround para falta de endpoint oficial):**
```bash
pip install check-jsonschema
check-jsonschema --schemafile \
  https://raw.githubusercontent.com/zenodo/zenodo/master/zenodo/modules/deposit/jsonschemas/deposits/records/legacyrecord.json \
  .zenodo.json
```

### Schema CITATION.cff: especificación completa

**Campos requeridos (mínimo viable):**
```yaml
cff-version: "1.2.0"
message: "If you use this software, please cite it as below."
title: "Software Title"
authors:
  - family-names: "Apellido"
    given-names: "Nombre"
```

**Campo version (sin restricciones):**
- Tipo: `string` o `number`
- Pattern: Sin validación de formato específico
- Ejemplos válidos: `version: "1.2.0"`, `version: 2.1`, `version: "0.3.12-rc"`

**Campo languages (array separado):**
```yaml
languages:
  - "en"   # ISO 639-1 (2 letras) recomendado
  - "haw"  # O ISO 639-2/3 (3 letras) también válido
```
- Pattern regex: `^[a-z]{2,3}$`
- Campo INDEPENDIENTE de version
- No hay parsing automático de language codes desde version string

**Campo date-released (crítico):**
```yaml
date-released: "2024-01-15"  # Formato YYYY-MM-DD (ISO 8601)
```
- **NO actualizado automáticamente** por release-it o @release-it/bumper
- Debe actualizarse en hook `after:bump` con script custom

**Campos opcionales importantes:**
```yaml
doi: "10.5281/zenodo.1234567"  # DOI sin URL prefix
repository-code: "https://github.com/user/repo"
license: "MIT"  # SPDX identifier o array para múltiples
keywords: ["keyword1", "keyword2"]
abstract: "Descripción del software"
commit: "abc123def456"  # Git commit hash
```

**Objetos person con detalles:**
```yaml
authors:
  - family-names: "Doe"
    given-names: "Jane"
    orcid: "https://orcid.org/0000-0002-1825-0097"
    affiliation: "Institution Name"
    email: "jane@example.com"
```

**Schema oficial:** https://citation-file-format.github.io/1.2.0/schema.json

**Validación con cffconvert:**
```bash
pip install cffconvert
cffconvert --validate
```

### GitHub Release API: requisitos exactos

**Endpoint:** `POST /repos/{owner}/{repo}/releases`

**Único campo requerido:**
- `tag_name`: String con nombre del tag (ej: "v1.0.0")

**Campos opcionales clave:**
- `name`: Nombre del release (default: usa tag_name)
- `body`: Release notes en markdown
- `draft`: Boolean (default: false) - Drafts NO trigger Zenodo webhook
- `prerelease`: Boolean (default: false)
- `target_commitish`: Branch o SHA (default: default branch)

**Asset upload constraints:**
- Endpoint separado: `POST https://uploads.github.com/repos/{owner}/{repo}/releases/{release_id}/assets`
- Tamaño máximo por asset: **2 GB**
- Cantidad máxima de assets: **1,000 por release**
- Sin límite en tamaño total acumulado
- Content-Type debe especificarse (ej: "application/pdf")

**Rate limits relevantes:**
- Authenticated: 5,000 requests/hora
- GitHub Actions (GITHUB_TOKEN): 1,000 requests/hora por repo
- **Límite secundario**: Creating releases genera notificaciones, sujeto a rate limiting adicional
- Content creation: 80 requests/minuto, 500 requests/hora

**Tag format para Zenodo:**
- Zenodo acepta cualquier tag pattern
- Convención recomendada: `v{MAJOR}.{MINOR}.{PATCH}` (ej: v1.0.0)
- Pre-releases aceptados: `v1.0.0-beta.1`, `v2.0.0-rc.3`
- **Zenodo solo procesa published releases**, no drafts

### release-it hooks: orden de ejecución exacto

**Lifecycle completo (orden cronológico):**

```
1. init()              → Todos los plugins en orden
2. getName()           → Primer plugin que retorna valor
3. getLatestVersion()  → Primer plugin que retorna valor
4. beforeBump()        → Todos los plugins en orden
5. bump()              → Todos los plugins en orden
6. beforeRelease()     → Todos los plugins en orden
7. release()           → Todos los plugins en ORDEN REVERSO
8. afterRelease()      → Todos los plugins en ORDEN REVERSO
```

**Hooks disponibles con namespace:**
```json
{
  "hooks": {
    "before:init": "comando",
    "after:init": "comando",
    "before:bump": "comando",
    "after:bump": "comando",
    "before:git:release": "comando",
    "after:git:release": "comando",
    "before:github:release": "comando",
    "after:github:release": "comando",
    "before:release": "comando",
    "after:release": "comando"
  }
}
```

**Variables disponibles en hooks (excepto init):**
- `${version}` - Nueva versión calculada
- `${latestVersion}` / `${previousVersion}` - Versión anterior
- `${changelog}` - Changelog generado
- `${name}` - Nombre del package/proyecto
- `${branchName}` - Branch actual de git
- `${repo.repository}` - Nombre del repo (owner/repo)
- `${repo.owner}` - Owner del repositorio
- `${releaseUrl}` - URL del release creado

**Capacidades de hooks:**
- ✅ Pueden leer archivos (cualquier comando shell)
- ✅ Pueden escribir archivos (cualquier comando shell)
- ✅ Pueden ejecutar arrays de comandos
- ✅ Si comando falla (exit code ≠ 0), release-it aborta
- ✅ Hooks subsecuentes no ejecutan si uno anterior falla

**Hook crítico para arquitectura Zenodo:**
```json
{
  "hooks": {
    "after:bump": [
      "npx tsx scripts/update-citation-date.ts",
      "npx tsx scripts/compile-pdf.ts ${version}",
      "sha256sum document-v${version}.pdf > checksums.txt",
      "git add CITATION.cff document-v${version}.pdf checksums.txt"
    ]
  }
}
```

**Timing crítico:** `after:bump` ejecuta DESPUÉS de actualizar versiones pero ANTES de git commit/tag, permitiendo:
1. Modificar archivos adicionales basados en nueva versión
2. Stagear archivos con `git add` para incluirlos en el commit
3. Garantizar que el tag apunta a commit con TODOS los archivos actualizados

### release-it bumper plugin: capacidades multi-archivo

**Funcionalidad principal:** Leer y/o escribir versión en múltiples archivos de cualquier tipo.

**Configuración para caso Zenodo + CITATION.cff:**
```json
{
  "plugins": {
    "@release-it/bumper": {
      "in": "package.json",
      "out": [
        {
          "file": "CITATION.cff",
          "path": "version",
          "type": "text/yaml"
        },
        {
          "file": ".zenodo.json",
          "path": "version",
          "type": "application/json"
        }
      ]
    }
  }
}
```

**Tipos de archivo soportados:**
- JSON (application/json) - navegación con dot notation
- YAML (text/yaml) - navegación con dot notation
- TOML (text/toml, application/toml)
- XML (text/xml, application/xml) - navegación con CSS selectors
- INI (text/x-properties)
- Plain text (text/plain, text/*, cualquier extensión)

**Navegación de paths para nested fields:**
```json
{
  "out": {
    "file": ".zenodo.json",
    "path": "metadata.version",  // Dot notation para nested
    "type": "application/json"
  }
}
```

**Modo consumeWholeFile para archivos simples:**
```json
{
  "out": {
    "file": "VERSION",
    "type": "text/plain",
    "consumeWholeFile": true  // Sobrescribe archivo completo con solo version
  }
}
```

**Lo que bumper HACE:**
- ✅ Actualiza campo `version` en todos los archivos `out`
- ✅ Preserva resto del contenido y formato
- ✅ Soporta arrays de archivos para actualizar múltiples simultáneamente

**Lo que bumper NO HACE:**
- ❌ NO actualiza campos de fecha (date-released en CITATION.cff)
- ❌ NO actualiza language fields
- ❌ NO valida schemas
- ❌ NO parsea language codes desde version strings
- ❌ NO hace transformaciones custom de versión

**No hay plugins específicos para .zenodo.json o CITATION.cff** - @release-it/bumper es la solución oficial recomendada.

### Reproducibilidad determinística: especificación completa

**SOURCE_DATE_EPOCH: cuándo aplica exactamente**

Soporte desde pdfTeX ≥ 1.40.17 (mayo 2016, TeX Live 2016):

**Aplica automáticamente a:**
- ✅ PDF CreationDate key
- ✅ PDF ModDate key  
- ✅ PDF trailer /ID (usa SOURCE_DATE_EPOCH como seed en lugar de timestamp actual)
- ✅ Todos los modos de output (PDF y DVI)

**NO aplica por defecto a:**
- ❌ TeX primitives `\year`, `\month`, `\day`, `\time` (siguen usando tiempo actual)
- ❌ `\pdffilemoddate` (usa modification time real del archivo)
- ❌ Build path incluido en trailer ID

**Override con FORCE_SOURCE_DATE=1:**
```bash
export FORCE_SOURCE_DATE=1
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
pdflatex document.tex
```
Fuerza `\year`, `\month`, `\day`, `\time` a usar SOURCE_DATE_EPOCH. **NO recomendado** excepto para casos especiales.

**Formato requerido:**
- Integer ASCII sin componente fraccional
- Segundos desde Unix epoch (1970-01-01 00:00:00 UTC)
- Ejemplo: `1609459200` (2021-01-01 00:00:00 UTC)

**Uso correcto:**
```bash
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
```

**pdfTeX primitives para determinismo completo:**

Agregar al inicio de `main.tex`:
```latex
\pdfinfoomitdate=1        % Omite dates del PDF info dictionary
\pdftrailerid{}           % Trailer ID vacío (omite por completo)
\pdfsuppressptexinfo=15   % Suprime metadata PTEX.* (bitmask: 1+2+4+8)
\pdfminorversion=5        % Versión PDF explícita (1.5)
```

**Evitar elementos no-determinísticos:**
- ❌ `\today` command - usar fecha fija: `\date{2024-01-01}`
- ❌ Random number generation sin seed - usar `\pdfrandomseed`
- ❌ Absolute file paths - afectan trailer ID
- ❌ Compression level variable - mantener `\pdfcompresslevel` constante

**Variables de entorno críticas:**
```bash
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
export LC_ALL=C           # Locale consistente
export LANG=C
export TZ=UTC             # Timezone consistente
export PYTHONHASHSEED=0   # Si se usan scripts Python
export PERL_HASH_SEED=0   # Si se usan scripts Perl
```

**Docker image pinning strategy:**

Usar **date-tagged images**, NO `latest`:
```dockerfile
FROM registry.gitlab.com/islandoftex/images/texlive:TL2024-2024-03-15-full
```

Tag format: `TL{RELEASE}-{YYYY}-{MM}-{DD}-{scheme}`

**Por qué pinning es crítico:**
- `latest` tag se actualiza continuamente con nuevas versiones de packages
- Cambios en packages pueden alterar output incluso con mismo source
- Date-pinned images garantizan paquetes idénticos años después
- Permite reproductor exacta del build en futuro

**Alternativas de imágenes:**
- Island of TeX (recomendado): `registry.gitlab.com/islandoftex/images/texlive`
- Dante-ev: `danteev/texlive:YYYY-MM-DD`
- Docker Hub oficial: `texlive/texlive` (menos opciones de pinning)

**latexmk garantías de reproducibilidad:**

latexmk NO produce outputs diferentes cuando:
- ✅ SOURCE_DATE_EPOCH está configurado consistentemente
- ✅ Dependencies no han cambiado
- ✅ Build environment es idéntico

**Convergencia determinística:**
- latexmk compara MD5 hashes de auxiliary files entre runs
- Recompila hasta que hashes se estabilicen
- Típicamente 2-3 runs para documentos simples
- Hasta 4+ runs para cross-references complejos
- Detección automática de convergencia

**Configuración .latexmkrc para reproducibilidad:**
```perl
$pdf_mode = 1;
$postscript_mode = $dvi_mode = 0;
$pdflatex = 'pdflatex -interaction=nonstopmode -recorder %O %S';
$bibtex_use = 1;
$out_dir = '_build';
```

**Validación de reproducibilidad:**

Script de validación completo:
```bash
#!/bin/bash
set -e

# Build 1
rm -rf build1 && mkdir build1 && cd build1
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
latexmk -pdf ../main.tex
HASH1=$(sha256sum main.pdf | cut -d' ' -f1)
cd ..

# Build 2 (clean)
rm -rf build2 && mkdir build2 && cd build2
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
latexmk -pdf ../main.tex
HASH2=$(sha256sum main.pdf | cut -d' ' -f1)
cd ..

# Compare
if [ "$HASH1" = "$HASH2" ]; then
    echo "✓ REPRODUCIBLE: $HASH1"
    exit 0
else
    echo "✗ NOT REPRODUCIBLE"
    diffoscope build1/main.pdf build2/main.pdf
    exit 1
fi
```

**Herramientas de comparación:**
- `sha256sum` - Hash rápido para verificación básica
- `diffoscope` - Análisis detallado de diferencias (estructura PDF, metadata, fonts)
- `cmp -s` - Comparación byte-a-byte
- `pdfinfo` - Inspección de metadata PDF

### TypeScript integración con release-it

**Ejecutar TypeScript desde hooks: métodos disponibles**

**Método 1: tsx (recomendado 2025):**
```json
{
  "hooks": {
    "after:bump": "npx tsx scripts/update-all.ts ${version}"
  }
}
```
- ✅ Más rápido (usa esbuild)
- ✅ Zero config
- ✅ Soporte ESM/CJS seamless
- ❌ No hace type checking (ejecutar `tsc --noEmit` separadamente)

**Método 2: ts-node (tradicional):**
```json
{
  "hooks": {
    "after:bump": "npx ts-node scripts/update-all.ts ${version}"
  }
}
```
- ✅ Puede hacer type checking
- ❌ Más lento (full TypeScript compilation)
- ⚙️ Requiere configuración en tsconfig

**Método 3: Compiled TypeScript:**
```json
{
  "scripts": {
    "build:scripts": "tsc --project tsconfig.scripts.json",
    "prerelease": "npm run build:scripts"
  },
  "hooks": {
    "after:bump": "node dist/scripts/update-all.js ${version}"
  }
}
```
- ✅ Type-safe (errores en compile time)
- ✅ Más rápido en runtime
- ❌ Extra build step

**Pattern recomendado:**
```json
{
  "scripts": {
    "type-check": "tsc --noEmit",
    "release": "npm run type-check && release-it"
  },
  "hooks": {
    "after:bump": "npx tsx scripts/orchestrator.ts ${version}"
  }
}
```

**Custom plugin architecture:**

Para lógica compleja o reutilizable:
```typescript
// plugins/academic-metadata-plugin.ts
import { Plugin } from 'release-it';
import * as fs from 'fs';
import YAML from 'yaml';

interface AcademicMetadataOptions {
  updateCitationDate?: boolean;
  updateZenodo?: boolean;
}

class AcademicMetadataPlugin extends Plugin<AcademicMetadataOptions> {
  async afterBump() {
    const version = this.config.getContext('version');
    
    if (this.options.updateCitationDate) {
      await this.updateCitationDate();
    }
    
    if (this.options.updateZenodo) {
      await this.updateZenodoMetadata(version);
    }
  }
  
  private async updateCitationDate() {
    const cffPath = 'CITATION.cff';
    const cff = YAML.parse(fs.readFileSync(cffPath, 'utf8'));
    cff['date-released'] = new Date().toISOString().split('T')[0];
    fs.writeFileSync(cffPath, YAML.stringify(cff));
    this.log.info('Updated date-released in CITATION.cff');
  }
  
  private async updateZenodoMetadata(version: string) {
    // Custom logic
  }
}

export default AcademicMetadataPlugin;
```

Configuración:
```json
{
  "plugins": {
    "./plugins/academic-metadata-plugin.ts": {
      "updateCitationDate": true,
      "updateZenodo": true
    }
  }
}
```

**Patrón arquitectónico recomendado:**

**Single orchestrator para workflows complejos:**
```typescript
// scripts/release-orchestrator.ts
import { updateCitationDate } from './tasks/update-citation';
import { compilePDF } from './tasks/compile-pdf';
import { generateChecksums } from './tasks/checksums';
import { stageFiles } from './tasks/git-stage';

async function main() {
  const version = process.argv[2];
  
  try {
    await updateCitationDate();
    await compilePDF(version);
    await generateChecksums(version);
    await stageFiles(['CITATION.cff', `document-v${version}.pdf`, 'checksums.txt']);
    
    console.log(`✓ Release preparation completed for v${version}`);
  } catch (error) {
    console.error('✗ Release preparation failed:', error);
    process.exit(1);
  }
}

main();
```

**Scripts separados para tareas independientes:**
```json
{
  "hooks": {
    "after:bump": [
      "npx tsx scripts/update-citation-date.ts",
      "npx tsx scripts/compile-pdf.ts ${version}",
      "npx tsx scripts/generate-checksums.ts ${version}",
      "git add CITATION.cff document-v${version}.pdf checksums.txt"
    ]
  }
}
```

## Arquitectura completa: configuración final

Integrando todos los componentes anteriores en una solución completa y determinística.

**Estructura de proyecto:**
```
project/
├── .release-it.json          # Configuración release-it
├── .latexmkrc                # Configuración latexmk
├── Dockerfile                # Docker build reproducible
├── Makefile                  # Build automation
├── main.tex                  # LaTeX source con primitives determinísticos
├── CITATION.cff              # Metadata académica
├── .zenodo.json              # Metadata Zenodo
├── package.json              # Node.js config
├── scripts/
│   ├── release-orchestrator.ts
│   ├── tasks/
│   │   ├── update-citation-date.ts
│   │   ├── compile-pdf.ts
│   │   └── generate-checksums.ts
│   └── utils/
│       └── helpers.ts
└── validate-reproducibility.sh
```

**Configuración release-it completa (.release-it.json):**
```json
{
  "git": {
    "commitMessage": "chore: release v${version}",
    "tagName": "v${version}",
    "requireCleanWorkingDir": false,
    "requireBranch": "main",
    "requireUpstream": true,
    "push": true,
    "commit": true,
    "tag": true
  },
  "github": {
    "release": true,
    "releaseName": "v${version}",
    "autoGenerate": false,
    "assets": ["document-v*.pdf", "checksums.txt"]
  },
  "npm": {
    "publish": false
  },
  "hooks": {
    "before:init": [
      "npm run lint",
      "npm test",
      "tsc --noEmit"
    ],
    "after:bump": "npx tsx scripts/release-orchestrator.ts ${version}",
    "after:release": "echo Successfully released v${version}"
  },
  "plugins": {
    "@release-it/bumper": {
      "in": "package.json",
      "out": [
        {
          "file": "CITATION.cff",
          "path": "version",
          "type": "text/yaml"
        },
        {
          "file": ".zenodo.json",
          "path": "version",
          "type": "application/json"
        }
      ]
    }
  }
}
```

**Script orchestrator completo (scripts/release-orchestrator.ts):**
```typescript
#!/usr/bin/env tsx
import { execSync } from 'child_process';
import * as fs from 'fs';
import YAML from 'yaml';

function updateCitationDate() {
  const cffPath = 'CITATION.cff';
  const cff = YAML.parse(fs.readFileSync(cffPath, 'utf8'));
  cff['date-released'] = new Date().toISOString().split('T')[0];
  fs.writeFileSync(cffPath, YAML.stringify(cff));
  console.log(`✓ Updated date-released to ${cff['date-released']}`);
}

function compilePDF(version: string) {
  const commitEpoch = execSync('git log -1 --pretty=%ct', { encoding: 'utf8' }).trim();
  
  const dockerCmd = `docker run --rm \
    -v $(pwd):/workdir \
    -w /workdir \
    -e SOURCE_DATE_EPOCH=${commitEpoch} \
    -e LC_ALL=C \
    -e LANG=C \
    -e TZ=UTC \
    registry.gitlab.com/islandoftex/images/texlive:TL2024-2024-03-15-full \
    latexmk -pdf -interaction=nonstopmode main.tex`;
  
  execSync(dockerCmd, { stdio: 'inherit' });
  
  // Rename with version
  if (fs.existsSync('main.pdf')) {
    fs.renameSync('main.pdf', `document-v${version}.pdf`);
    console.log(`✓ Compiled document-v${version}.pdf with SOURCE_DATE_EPOCH=${commitEpoch}`);
  } else {
    throw new Error('PDF compilation failed - main.pdf not found');
  }
}

function generateChecksums(version: string) {
  const pdfFile = `document-v${version}.pdf`;
  const hash = execSync(`sha256sum ${pdfFile}`, { encoding: 'utf8' });
  fs.writeFileSync('checksums.txt', hash);
  console.log(`✓ Generated checksums.txt`);
}

function stageFiles(version: string) {
  const files = [
    'CITATION.cff',
    '.zenodo.json',
    `document-v${version}.pdf`,
    'checksums.txt'
  ];
  
  execSync(`git add ${files.join(' ')}`, { stdio: 'inherit' });
  console.log(`✓ Staged files for commit: ${files.join(', ')}`);
}

async function main() {
  const version = process.argv[2];
  
  if (!version) {
    console.error('Error: Version argument required');
    process.exit(1);
  }
  
  try {
    console.log(`\n🚀 Preparing release v${version}...\n`);
    
    updateCitationDate();
    compilePDF(version);
    generateChecksums(version);
    stageFiles(version);
    
    console.log(`\n✅ Release preparation completed successfully for v${version}\n`);
  } catch (error) {
    console.error(`\n❌ Release preparation failed:`, error);
    process.exit(1);
  }
}

main();
```

**LaTeX source con primitives determinísticos (main.tex):**
```latex
% Primitives para reproducibilidad determinística
\pdfinfoomitdate=1
\pdftrailerid{}
\pdfsuppressptexinfo=15
\pdfminorversion=5

\documentclass{article}

% NO usar \today - fecha fija
\date{2024-01-01}

% Packages
\usepackage[utf8]{inputenc}
\usepackage{hyperref}

\title{Reproducible LaTeX Document}
\author{Author Name}

\begin{document}

\maketitle

\section{Introduction}

Content here...

\end{document}
```

**Dockerfile para builds reproducibles:**
```dockerfile
FROM registry.gitlab.com/islandoftex/images/texlive:TL2024-2024-03-15-full

ARG SOURCE_DATE_EPOCH
ENV SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH}

WORKDIR /workdir

# Set consistent environment
ENV LC_ALL=C
ENV LANG=C
ENV TZ=UTC

CMD ["latexmk", "-pdf", "-interaction=nonstopmode"]
```

**Makefile para local builds:**
```makefile
COMMIT_EPOCH = $(shell git log -1 --pretty=%ct)
VERSION = $(shell node -p "require('./package.json').version")

.PHONY: all clean build validate release

all: build

build: document-v$(VERSION).pdf

document-v$(VERSION).pdf: main.tex
	SOURCE_DATE_EPOCH=$(COMMIT_EPOCH) \
	LC_ALL=C LANG=C TZ=UTC \
	latexmk -pdf main.tex
	mv main.pdf document-v$(VERSION).pdf
	sha256sum document-v$(VERSION).pdf > checksums.txt

clean:
	latexmk -C
	rm -f document-*.pdf checksums.txt

validate:
	./validate-reproducibility.sh

release:
	npm run release
```

**Script de validación (validate-reproducibility.sh):**
```bash
#!/bin/bash
set -e

echo "Validating reproducible build..."

# Clean
make clean

# Build 1
echo "Build 1..."
make build
cp document-*.pdf build1.pdf
HASH1=$(sha256sum build1.pdf | cut -d' ' -f1)

# Clean and build 2
echo "Build 2..."
make clean
make build
cp document-*.pdf build2.pdf
HASH2=$(sha256sum build2.pdf | cut -d' ' -f1)

# Compare
echo ""
if [ "$HASH1" = "$HASH2" ]; then
    echo "✓ REPRODUCIBLE BUILD VERIFIED"
    echo "  SHA256: $HASH1"
    rm build1.pdf build2.pdf
    exit 0
else
    echo "✗ BUILDS NOT REPRODUCIBLE"
    echo "  Build 1: $HASH1"
    echo "  Build 2: $HASH2"
    
    if command -v diffoscope &> /dev/null; then
        echo ""
        echo "Running diffoscope analysis..."
        diffoscope build1.pdf build2.pdf || true
    fi
    
    exit 1
fi
```

**CITATION.cff template:**
```yaml
cff-version: "1.2.0"
message: "If you use this software, please cite it using these metadata."
title: "Your Project Title"
version: "1.0.0"
date-released: "2024-01-01"
authors:
  - family-names: "Doe"
    given-names: "Jane"
    orcid: "https://orcid.org/0000-0002-1825-0097"
    affiliation: "Institution Name"
repository-code: "https://github.com/user/repo"
license: "MIT"
keywords:
  - "keyword1"
  - "keyword2"
languages:
  - "en"
```

**.zenodo.json template:**
```json
{
  "title": "Your Project Title",
  "version": "1.0.0",
  "upload_type": "software",
  "description": "Project description with <em>HTML</em> allowed.",
  "creators": [
    {
      "name": "Doe, Jane",
      "affiliation": "Institution Name",
      "orcid": "0000-0002-1825-0097"
    }
  ],
  "access_right": "open",
  "license": "MIT",
  "language": "eng",
  "keywords": [
    "keyword1",
    "keyword2"
  ],
  "related_identifiers": [
    {
      "identifier": "https://github.com/user/repo",
      "relation": "isSupplementTo",
      "scheme": "url"
    }
  ]
}
```

**GitHub Actions CI workflow (.github/workflows/release.yml):**
```yaml
name: Release
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  validate-reproducibility:
    runs-on: ubuntu-latest
    container:
      image: registry.gitlab.com/islandoftex/images/texlive:TL2024-2024-03-15-full
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Validate reproducibility
        run: ./validate-reproducibility.sh
      
      - name: Upload PDF
        uses: actions/upload-artifact@v4
        with:
          name: document-pdf
          path: document-*.pdf

  release:
    needs: validate-reproducibility
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch'
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: npm run release
```

**package.json scripts:**
```json
{
  "scripts": {
    "type-check": "tsc --noEmit",
    "lint": "eslint .",
    "test": "jest",
    "build:pdf": "make build",
    "validate": "./validate-reproducibility.sh",
    "release": "release-it"
  },
  "devDependencies": {
    "@release-it/bumper": "^6.0.0",
    "release-it": "^17.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.0.0",
    "yaml": "^2.0.0"
  }
}
```

## Flujo de ejecución paso a paso

Cuando se ejecuta `npm run release`:

**Paso 1: Inicialización**
- release-it detecta versión actual de package.json
- Hooks `before:init` ejecutan: lint, tests, type-check
- Usuario prompted para nueva versión (o auto-increment)

**Paso 2: Version bump**
- @release-it/bumper actualiza:
  - `package.json`: `"version": "1.1.0"`
  - `CITATION.cff`: `version: "1.1.0"`
  - `.zenodo.json`: `"version": "1.1.0"`

**Paso 3: Hook after:bump**
- Orchestrator ejecuta con `${version}` = "1.1.0"
- `updateCitationDate()`: CITATION.cff `date-released: "2024-11-17"`
- `compilePDF()`: 
  - SOURCE_DATE_EPOCH desde último commit
  - Docker build con imagen pinned
  - Genera `document-v1.1.0.pdf` determinístico
- `generateChecksums()`: SHA256 en `checksums.txt`
- `stageFiles()`: `git add CITATION.cff .zenodo.json document-v1.1.0.pdf checksums.txt`

**Paso 4: Git commit y tag**
- Commit message: "chore: release v1.1.0"
- Commit incluye TODOS los archivos staged
- Tag: `v1.1.0` apuntando a este commit
- **CRÍTICO**: Tag apunta a commit con .zenodo.json y CITATION.cff actualizados

**Paso 5: Git push**
- Push commits a GitHub
- Push tag v1.1.0 a GitHub

**Paso 6: GitHub Release**
- release-it crea GitHub Release vía API
- Release name: "v1.1.0"
- Release body: Changelog generado
- Assets uploaded: `document-v1.1.0.pdf`, `checksums.txt`

**Paso 7: Zenodo webhook (automático)**
- GitHub envía webhook a Zenodo
- Zenodo descarga repo en estado del tag v1.1.0
- Zenodo lee `.zenodo.json` con version "1.1.0"
- Zenodo crea nueva versión en su sistema
- Zenodo genera nuevo Version DOI
- Release ahora citeable con DOI permanente

## Interdependencias críticas

**Estas dependencias DEBEN cumplirse:**

1. **@release-it/bumper ANTES de after:bump hook**
   - Version ya actualizada en archivos antes de orchestrator
   - Variable `${version}` disponible en hook

2. **after:bump hook ANTES de git commit**
   - Permite modificar archivos adicionales
   - `git add` stagea archivos para el commit
   - Commit incluye TODOS los cambios

3. **.zenodo.json actualizado ANTES de git tag**
   - Tag apunta a commit con metadata correcta
   - Zenodo lee repo en estado del tag
   - Cambios post-tag NO visibles para Zenodo

4. **Git tag ANTES de GitHub Release**
   - Release requiere tag existente
   - Assets asociados al release, no al tag directamente

5. **GitHub Release published ANTES de Zenodo webhook**
   - Solo published releases (no drafts) triggean Zenodo
   - Webhook automático de GitHub a Zenodo

6. **SOURCE_DATE_EPOCH desde git commit**
   - Garantiza timestamp reproducible
   - Mismo commit = mismo SOURCE_DATE_EPOCH = mismo PDF hash

7. **Docker image pinned**
   - Versión exacta de TeX Live
   - Reproducibilidad garantizada años después

## Validación y troubleshooting

**Validar configuración antes del primer release:**

```bash
# 1. Validar schemas localmente
cffconvert --validate  # CITATION.cff
jq . .zenodo.json      # JSON syntax

# 2. Validar reproducibilidad PDF
./validate-reproducibility.sh

# 3. Dry run de release
npx release-it --dry-run

# 4. Check git status
git status  # Debe estar limpio antes de release
```

**Problemas comunes y soluciones:**

**"Working directory not clean" durante release:**
- Causa: Archivos sin commitear
- Solución: Commitear cambios o desactivar check con `git.requireCleanWorkingDir: false`

**Zenodo no recibe webhook:**
- Verificar repo habilitado en https://zenodo.org/account/settings/github/
- Verificar webhook en GitHub Settings → Webhooks
- Check que release sea "published", no "draft"

**PDF no reproducible:**
- Verificar SOURCE_DATE_EPOCH configurado
- Check primitives en main.tex (\pdfinfoomitdate, etc.)
- Verificar Docker image pinned (no usar :latest)
- Check que no uses \today en LaTeX

**.zenodo.json con versión vieja en Zenodo:**
- Causa: .zenodo.json no actualizado antes del tag
- Solución: Verificar que @release-it/bumper está en plugins
- Verificar que after:bump hook ejecuta git add

**GitHub Release sin assets:**
- Verificar path en `github.assets` config
- Check que archivos existen antes de release
- Verificar que nombres de archivo coinciden con pattern

**Type errors en scripts TypeScript:**
- Ejecutar `npm run type-check` antes de release
- Agregar a hooks `before:init` para prevención

## Conclusiones y garantías

Esta arquitectura garantiza:

✅ **Versionado semántico automático** en package.json, CITATION.cff, y .zenodo.json simultáneamente

✅ **Compilación PDF determinística** reproducible bit-a-bit con mismo SOURCE_DATE_EPOCH

✅ **Metadata académica sincronizada** entre CITATION.cff, .zenodo.json y GitHub

✅ **Pipeline completamente automatizado** desde version bump hasta Zenodo DOI

✅ **Type-safety** en scripts TypeScript con validación pre-release

✅ **Reproducibilidad a largo plazo** mediante Docker image pinning

✅ **Zero dependencias manuales** - todo automatizado en release-it

**Flujo completo end-to-end:**
```
npm run release
  → User prompt para versión
  → @release-it/bumper actualiza version fields
  → after:bump hook:
    - Actualiza date-released en CITATION.cff
    - Compila PDF con SOURCE_DATE_EPOCH desde git
    - Genera checksums SHA256
    - Stage archivos con git add
  → Git commit con todos los cambios
  → Git tag apuntando a commit con metadata correcta
  → Git push commits + tag
  → GitHub Release creation con assets
  → Zenodo webhook automático
  → Zenodo crea versión y genera DOI
  → Release citeable con DOI permanente
```

Todos los archivos en el repositorio en estado del tag v${version} tienen metadata consistente y PDF reproducible verificado por checksums.