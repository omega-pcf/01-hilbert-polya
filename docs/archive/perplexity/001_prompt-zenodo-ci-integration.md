# Prompt: Evaluar toolchain para automatizar releases GitHub → Zenodo con PDFs y metadatos

Quiero que actúes como un investigador técnico especializado en pipelines de publicación científica (LaTeX → PDF) y sincronización GitHub–Zenodo. Necesito una recomendación exhaustiva de herramientas existentes (GitHub Actions ya mantenidas, CLIs, librerías) para automatizar TODA la cadena de release sin escribir scripts personalizados. Mi prioridad es usar software “battle tested”, con soporte activo, que reduzca al máximo código propio. Contexto y requisitos:

## Contexto del repositorio
- Proyecto: preprint matemático (LaTeX, clase LaPreprint).
- Lenguajes: español (v1.0.x ya publicado con DOI `10.5281/zenodo.17619486`), próximo release en inglés.
- PDF compilado con `pdflatex` (puede tardar ~1 min). Tenemos Docker (`nanozoo/pdflatex`) como opción para builds reproducibles.
- Actualmente: workflow manual (compilamos local, subimos PDF, creamos release, Zenodo integra via webhook).

## Objetivos
1. **Automatizar pipeline por completo** (CI/CD):
   - Commit/push → pipeline genera PDFs ES/EN, produce metadatos, crea release GitHub con assets, dispara Zenodo.
   - Preferimos GitHub Actions que ya realicen el tagging, release drafting, attachment de artefactos.
2. **Metadatos consistentes**:
   - Usar `.zenodo.json` o `CITATION.cff` (o ambos) para mapear autores, ORCID, afiliaciones, keywords, DOI previos, Colab notebook, idioma.
   - Evitar mantener metadatos en múltiples archivos; ideal que el workflow o la action los actualice automáticamente (versioning).
3. **PDF principal como release asset**:
   - El artefacto principal en Zenodo debe ser el PDF compilado, no solo el ZIP de GitHub.
4. **Múltiples idiomas**:
   - Releases diferenciados (ES vs EN). Necesitamos que las herramientas permitan etiquetar/nombrar assets y metadatos según idioma.
5. **Minimizar código propio**:
   - Si existe un CLI o action que ya hace (a) build LaTeX, (b) update `.zenodo.json`, (c) crear release, preferimos usarlo.

## Preguntas específicas para investigar
1. **GitHub Actions existentes**:
   - ¿Cuáles son las mejores actions mantenidas para compilar LaTeX? (Docker-based, caching, soporte multi PDF).
   - Actions para gestionar release tags automáticamente (Release Drafter, release-it, semantic-release, etc.).
   - Actions para subir archivos y metadatos a Zenodo (`upload-to-zenodo`, `zenodo-upload`, etc.). Pros/Contras, requerimientos de autenticación (`ZENODO_TOKEN`, sandbox).
   - Actions que actualicen `.zenodo.json` o `CITATION.cff` basadas en tag semver (ej. release-it plugins, python utilities).
2. **Herramientas CLI/Frameworks**:
   - `release-it` (JS/TS), `semantic-release`, `standard-version`, `changesets`.
   - Alternativas en Python (al menos 5): e.g., `hatch`, `poetry-plugin`, `bump2version` con plugins, `towncrier`, `cz-cli` (commitizen) adaptado.
   - Herramientas en Go u otros lenguajes (ej. `goreleaser`) que soporten pipelines multi-asset y hooks para generar metadata.
3. **Autenticación & tags**:
   - ¿Conviene generar tags dentro de Actions con `GITHUB_TOKEN` (transport-based release) o usar release-it local?
   - Implicaciones de usar la integración oficial Zenodo ↔ GitHub vs. actions que suben a Zenodo vía API.
   - Mejores prácticas para sandbox/testing (evitar DOIs permanentes durante pruebas).
4. **Localización**:
   - ¿Hay tooling para publicar releases multi-idioma (naming, assets, metadata) sin duplicar workflows?
   - ¿Cómo mapear `language` en `.zenodo.json` y mantener versiones `es`/`en` coherentes?
5. **Costos/tiempos**:
   - Recomendaciones para optimizar minutos de Actions (caching TeX, runners self-hosted, etc.).

## Resultado esperado
- Tabla comparativa de acciones/CLI/herramientas con:
  - Autor/mantenedor, popularidad, última actualización.
  - Funcionalidad cubierta (build LaTeX, release tagging, metadata Zenodo).
  - Requerimientos (tokens, configuración).
  - Ventajas/desventajas en nuestro caso (repos público, multi-idioma, PDF pesado).
- Recomendación concreta de stack minimalista (p.ej., `release-it` + `github-tag-action` + `upload-to-zenodo` + `latex-action`).
- Pasos sugeridos para integrar herramientas seleccionadas (orden secuencial, hooks principales, cómo acoplar con `.zenodo.json`/`CITATION.cff`).

## Estilo de respuesta
- Muy detallado, técnico, con referencias a repos/actions oficiales (URLs, issues relevantes).
- Enfocado en reducir código custom: priorizar librerías declarativas antes de sugerir “escribir script Python”.
- Estructura clara (tables, bullets, pasos).

Gracias. Quiero basar toda la implementación en estas recomendaciones sin reinventar la rueda.

