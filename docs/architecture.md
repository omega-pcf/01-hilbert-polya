# Architecture

## Stack

- **release-it**: Semantic versioning + GitHub releases.
- **@release-it/bumper**: Synchronizes version `package.json` → `CITATION.cff`, `.zenodo.json`.
- **TypeScript + tsx**: Orchestration scripts.
- **Docker** (`kjarosh/latex:2024.4-full`): Reproducible LaTeX compilation.
- **Zenodo webhook**: Automatic integration from GitHub.

## Flow

```
pnpm run release
  → @release-it/bumper: updates versions in package.json, CITATION.cff, .zenodo.json
  
  → after:bump: pnpm run build
    → cleanup: removes previous document-v*.pdf
    → citation: updates date-released
    → compile: Docker with SOURCE_DATE_EPOCH (git commit timestamp)
    → checksums: SHA256 of the PDF
  
  → Git: commit + tag v${version} + push (release-it stages automatically with addUntrackedFiles)
  
  → GitHub: Release with assets (PDF, checksums)
  
  → Zenodo: automatic webhook → new version + DOI
```

## Reproducibility

**SOURCE_DATE_EPOCH:** Extracted from `git log -1 --pretty=%ct`.

**LaTeX primitives:** `\pdfinfoomitdate=1`, `\pdftrailerid{}`, etc. (see `main.tex`).

**Docker pinned:** `kjarosh/latex:2024.4-full` (explicit version).

Same commit = same PDF hash (guaranteed).

## Structure

```
scripts/
├── build.ts              # Independent build (hook after:bump)
├── tasks/                # Atomic tasks
│   ├── checksums.ts
│   ├── citation.ts
│   ├── cleanup.ts
│   └── compile.ts
├── types.ts              # TypeScript types
└── utils/
    └── git.ts            # Git utilities (getCommitEpoch)
```

## Metadata

**Source of truth:** `package.json` version.

**Automatic Synchronization:**
- `CITATION.cff` version (via @release-it/bumper).
- `.zenodo.json` version (via @release-it/bumper).
- `CITATION.cff` date-released (via hook after:bump → build.ts).

**Zenodo:** Reads `.zenodo.json` from the tag, creates a version under the same Concept DOI.
