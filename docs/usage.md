# Build and Release Workflow

## Daily Development

**Workflow:** LaTeX Workshop (James Yu) in VS Code
- Automatically compiles to `build/main.pdf`.
- Real-time preview on save.

**Build:**
```bash
pnpm run build
```

## Counts

The numbers the documentation states about the repository — the figure
inventory of `images/` and the Lean source statistics — are **measured,
never typed** (family mechanism ported from `05-kkgt`, whose `CVR-001` §5
named the stale counts):

```bash
pnpm run counts         # rewrite the marked regions and regenerate docs/counts.md
pnpm run counts:check   # fail, with a diff, when either has drifted
```

`counts:check` runs inside `validate`, after `parity`. The mechanism follows
the `selfcitations` precedent (the family SPEC-001 §5.2): a region is delimited
by `<!-- counts:begin id="..." -->` … `<!-- counts:end id="..." -->` in prose,
and by `# counts:begin id="..."` … `# counts:end id="..."` on lines of their
own inside a code fence, where an HTML comment would print as text.
`pnpm run build` calls `syncCounts()` next to `syncSelfCitations()`, before
the render, so the PDF can never print a stale count.
`docs/counts.md` is regenerated in full and lists every counter with the
command that measures it and the regions that quote it. This repository has
no pytest suite, so it declares no suite counter.

Dated reports (`docs/reports/`) are snapshots of a moment: they are corrected
by hand with the reason recorded, never rewritten by the task.

## Shared files

Most of the build pipeline is shared by **byte, not by copy**: the five
repositories of the family (`01-hilbert-polya`, `02-odd-zeta`,
`03-crystalline-worldsheet`, `04-mersenne-cr`, `05-kk-golden-throat`) carry the
same `scripts/tasks/*.ts`, `scripts/types*`, `scripts/schemas/*`,
`scripts/utils/git.ts`, `tsconfig.json`, `.latexmkrc` and the toolchain pins.
What must stay identical is pinned in
[`scripts/shared-files.json`](../scripts/shared-files.json) — one SHA-256 per
file — and verified by `scripts/tasks/manifest.ts`:

```bash
pnpm run manifest         # rewrite the pinned hashes from the working tree
pnpm run manifest:check   # fail, naming the file and both digests, when one drifted
```

`manifest:check` runs inside `validate`, right after `counts:check`. A listed
file is a **family** file: changing it in one repository only fails the gate.
A deliberate change is ported to every repository, `pnpm run manifest`
refreshes the manifest in each one, and the refreshed manifest is committed
together with the change; a file that legitimately stops being shared moves to
the manifest's `excluded` table with its reason, again in all five
repositories, so the manifest itself stays byte-identical family-wide.

The `excluded` table is part of the contract, not a footnote: `package.json`
and `CITATION.cff` are per-repository identity roots (asserted by `parity`),
`pyproject.toml` and `uv.lock` are the per-repository dependency sets,
`scripts/tasks/counts.ts` is a per-repository counter table by design, and
the manifest never lists itself. Each exclusion names its measured reason
where a file was evaluated and rejected. `scripts/build.ts` joined `files`
when the two sides were unified (2026-11-21): `01`–`04` now call
`syncCounts()` beside `syncSelfCitations()` exactly as `05` does, so the
entry point is byte-identical family-wide and pinned like the rest.

The design follows the checksum-manifest pattern (`sha256sum -c` over a
versioned list) and the lockfile philosophy — pin the bytes, fail loudly on
drift, update the pin in the same commit as the change — rather than a runtime
integrity layer: background and sources are recorded in
the family SPEC-004
§3.1 (`05-kkgt/docs/specs/20261120_SPEC-004_family_build_alignment_and_version_scheme.md`).

## Commits

Every repository of the family follows [Conventional Commits](https://www.conventionalcommits.org/)
with **English subject lines** (the documentation-language rule is
`docs/citations.md` §6):

```
<type>(<scope>): <description>
```

**Types used in the family:**

| type | meaning | example from this repository |
|---|---|---|
| `feat` | new content or capability | `feat(ci): add Zenodo upload workflow via REST API` |
| `fix` | a defect: manuscript markup, frontmatter, scripts, figures | `fix(frontmatter): group amsart address and email blocks by institution` |
| `docs` | documentation only — reports, specs, guides | `docs: propagate the family witness contract, rationale and grammar` |
| `test` | the suite: tests and their fixtures | — |
| `refactor` | structure changes with no behaviour change | `refactor(metadata): centralized abstracts in package.json and removed script-based sanitization` |
| `style` | formatting that changes no rendered meaning | `style(bibliography): uniform initial-form author names in references (giveninits)` |
| `chore` | tooling, metadata, dependencies | `chore: release v2.5.4` |
| `revert` | reverts | `revert(ci): remove GitHub Actions Zenodo upload workflow` |

**Scopes** name the surface that changed: `manuscript`/`tex` (the manuscript
body), `frontmatter` (title block, dates, authors), `citation`/`citations`/`bib`
(the bibliography and its metadata), `tests`, `figures`, `metadata`, `lean`,
`build`/`pipeline`/`scripts`, `ci`/`zenodo`/`release`. The type must match the
content: `docs` never carries a manuscript edit, `fix` never carries new
content — a wrong type is a defect of the record, not a style preference.

**Rules:** subject in English, imperative, no trailing period; the body
explains *why*; `!` after the type or scope marks a breaking change
(`feat(api)!: …`); one concern per commit, with the gates green at every
commit.

**Version bump mapping** — which commit cuts a release is decided in
`.release-it.ts` by the official [`conventionalcommits` preset]
(`bumpStrict: true` plus the per-type `hidden` flag), never by a
hand-written table:

| commit shape | bump |
|---|---|
| `feat!`, `feat(<scope>)!`, or a `BREAKING CHANGE:` / `BREAKING-CHANGE:` footer on any type | **major** |
| `feat`, `feature` | **minor** |
| `fix` | **patch** |
| `docs`, `chore`, `test`, `build`, `refactor`, `perf`, `ci`, `style`, `revert` | **no release** — the commits stay in git history, and the same `hidden` flag keeps them out of `CHANGELOG.md` |
| no commits since the last tag | **no release** |
| a type outside the convention | **patch**: the preset counts any undeclared type as a possible fix |

[`conventionalcommits` preset]: https://www.npmjs.com/package/conventional-changelog-conventionalcommits

`hidden` is a single preset flag serving both the recommendation and the
changelog, so the sections a release renders are `Features` and `Bug Fixes`
(a `BREAKING CHANGE` commit is rendered whatever its type carries). Worked
example: the v168 merge commit `feat(paper)!:` carrying a `BREAKING CHANGE:`
footer is a **major**.

**Changelog:** `@release-it/conventional-changelog` renders `CHANGELOG.md`
from these subjects at each release.

## Versioning

- **Standard:** [Semantic Versioning](https://semver.org) — `vX.Y.Z`
  (major.minor.patch), where `feat` → minor, `fix` → patch,
  `BREAKING CHANGE`/`!` → major, as declared in the commit subjects above,
  and **every other type (`docs`, `chore`, `test`, `build`, `refactor`,
  `perf`, `ci`, `style`, `revert`) cuts no release at all** — the bump is
  read from `.release-it.ts` (official `conventionalcommits` preset) by the
  table in §Commits, not from a hand-written mapping.
- **Single source:** the `version` field of `package.json`.
- **Synchronization chain:** `release-it` bumps `package.json` →
  `@release-it/bumper` writes the same value into `CITATION.cff` →
  `citation.ts` regenerates `.zenodo.json` from the CFF → the GitHub release
  carries the tag → **Zenodo archives exactly this version** under the
  repository's Concept DOI (one DOI per version, one Concept DOI for all of
  them). Zenodo therefore consumes the same string the repository declares;
  the pipeline detail lives in [architecture.md](architecture.md), and the
  row-by-row chain (source → generator → derived file) in
  [architecture.md §Sources of truth](architecture.md#sources-of-truth).
- **The paper prints it.** The page-1 footnote of the family is standardised
  as:

  ```latex
  \renewcommand{\datename}{\textbf{Received:}}
  \date{<Month D, YYYY>; \textbf{Last modified:} \today; \textbf{Version:} \texttt{vX.Y.Z}}
  ```

  which renders `Received: <Month D, YYYY>; Last modified: <today>; Version:
  vX.Y.Z.` — with only the identifier in monospace: the labels stay
  `\textbf`, `Version: ` itself is not typed, and the token sits inside
  `\texttt{…}`. The first label lives in `\datename` because amsart prefixes
  the footnote with it (its own default would read `Date: Received: …`). The
  version token mirrors the `version` field of `package.json` (v2.5.4), so
  the printed version, the committed version and the version archived by
  Zenodo cannot diverge; `pnpm run selfcitations:check` (and `parity`) fails
  when the token sits outside `\texttt{…}`, and `pnpm run selfcitations`
  wraps it back.

## Release

```bash
pnpm run release         # Full release: bump → build → tag → GitHub → Zenodo
pnpm run release:dry-run # Preview without changes
```

## Installation

```bash
pnpm install
```

**Requirements:** Node.js 20+, pnpm 9+, Docker.
