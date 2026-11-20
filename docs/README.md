# Project Documentation

This directory contains technical documentation for the manuscript, its build and release pipeline,
and the family style guide as it applies here.

## Structure

```
docs/
├── README.md          # This file
├── architecture.md    # Release system architecture
├── citations.md       # CSL single-source citation pipeline + witness (tier) contract (§1–§8)
├── figures.md         # Deterministic figure pipeline
├── installation.md    # Prerequisites and setup
├── style-guide.md     # Family style guide v2.2 (port of `05-kkgt/docs/style-guide.md`)
├── style/
│   └── grammar.md     # Grammar and usage rules of human language (ES/EN/FR/IT examples)
├── usage.md           # Build, release, commit and version conventions (semver + Zenodo)
├── witness-contract.md # Why the marks exist (portable rationale of the witness device, EN)
└── reports/           # Specific, repository-tied reports (dated, id'd)
    └── README.md      # Reports convention (template) + index of this repository's reports
```

`docs/` itself stays generic (rules and rationale, portable across the
sibling repositories); anything tied to one repository state — per-site
inventories, decision logs, verdict tables — goes to `docs/reports/`.

## Contents

- **architecture.md**: Tech stack, execution flow, reproducibility measures, scripts structure.
- **citations.md**: How `citation.csl.json` drives the bibliography, CITATION.cff and .zenodo.json
  (§1–§7); §8 is the family witness (tier) contract — grammar, writing rules, alphabet and the
  quantified inline / own-line criterion. This repository's manuscript currently renders no
  witness marks; the contract is the family standard, not an applied state.
- **figures.md**: What `pnpm run generate:figures` guarantees and why (byte-stable, text-extractable PDFs).
- **installation.md**: Prerequisites and setup instructions.
- **style-guide.md**: The family style guide (v2.2), a port of `05-kkgt/docs/style-guide.md`:
  editorial rules (§1–§12), including the rigorous IMRAD structure of §7; the software-quality
  doctrine D1–D7 (§13); the TeX/proofreading pipeline with its cited sources (§14). Generic across
  the family: this repository's own conventions are linked, never copied — the family documents it
  links (`citations.md` §8, `witness-contract.md`, `style/grammar.md`, `reports/`) are propagated
  here, so every link is local.
- **style/grammar.md**: The grammar and usage rules extracted from `style-guide.md` §1.5 —
  language-neutral (complete structure, agreement, clear reference, voice, punctuation, economy),
  worked in Spanish, English, French and Italian, with the RAE-checked Spanish `se` verbs and their
  sources.
- **usage.md**: Daily workflow, conventional commits, the version standard (semver + Zenodo), build and release commands.
- **witness-contract.md**: The rationale of the witness marks — why they exist, the inline /
  own-line shape rule, the compactness method, the colour and accessibility rules, and what the
  marks do not assert. Portable across the family; the applied state of a repository lives in its
  `docs/reports/`.
- **reports/**: Specific reports — per-site inventories, decision logs, verdict tables and
  incidents. The convention (naming, ISO header, index format) and the index of this repository's
  reports are in `reports/README.md`; this repository has no report yet.

## Conventions

Commits follow [Conventional Commits](https://www.conventionalcommits.org/);
format, common types, examples and the English-subject rule:
[usage.md](usage.md) §Commits.
