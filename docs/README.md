# Project Documentation

This directory contains technical documentation for the manuscript, its build and release pipeline,
and the family style guide as it applies here.

## Structure

```
docs/
├── README.md          # This file
├── architecture.md    # Release system architecture
├── citations.md       # CSL single-source citation pipeline (§1–§7)
├── figures.md         # Deterministic figure pipeline
├── installation.md    # Prerequisites and setup
├── style-guide.md     # Family style guide v2.2 (port of `05-kkgt/docs/style-guide.md`)
└── usage.md           # Build and release commands
```

## Contents

- **architecture.md**: Tech stack, execution flow, reproducibility measures, scripts structure.
- **citations.md**: How `citation.csl.json` drives the bibliography, CITATION.cff and .zenodo.json
  (§1–§7). The family witness contract is §8 of `05-kkgt`'s `citations.md`; it is referenced from
  `style-guide.md`, not copied here.
- **figures.md**: What `pnpm run generate:figures` guarantees and why (byte-stable, text-extractable PDFs).
- **installation.md**: Prerequisites and setup instructions.
- **style-guide.md**: The family style guide (v2.2), a port of `05-kkgt/docs/style-guide.md`:
  editorial rules (§1–§12), including the rigorous IMRAD structure of §7; the software-quality
  doctrine D1–D7 (§13); the TeX/proofreading pipeline with its cited sources (§14). Generic across
  the family: this repository's own conventions are linked, never copied — links whose target this
  repository does not have (witness contract `citations.md` §8, `witness-rationale.md`,
  `style/grammar.md`, `reports/`) resolve to `05-kkgt` on GitHub.
- **usage.md**: Daily workflow, conventional commits, build and release commands.

## Conventions

All commits follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>
```

**Common types:** `feat`, `fix`, `docs`, `refactor`, `chore`.
