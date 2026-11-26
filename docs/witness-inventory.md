# Witness inventory — 01-hilbert-polya

> **GENERATED** — `pnpm run witness:inventory` (`scripts/tasks/witness-inventory.ts`) rewrites
> this file from the working tree; `pnpm run inventory:check` (inside `validate`) fails with
> a diff when it drifts. Do not edit by hand.

Measured over the tracked manuscript sources (`main.tex` and `src/**/*.tex`) — 13 files. TeX comments (a line whose first non-space character is `%`) and the lines that *define* a counted macro are excluded; nothing here is copied from an older document. The form taxonomy is the one of `docs/witness-contract.md` §6.1.

## Marks

| form | count |
|---|--:|
| `\tier[ids]{P}` | 0 |
| `\tier[ids]{N}` | 0 |
| `\tier{P}` (bare) | 0 |
| `\tier{N}` (bare) | 0 |
| own-line `\witness{P}{…}` | 0 |
| own-line `\witness{N}{…}` | 0 |
| mid-line `\witness{…}` (no block) | 0 |
| `\tier[\testref{…}]{N}` marks | 0 |

Ids carried by `N` marks: **0 ids over 0 distinct**.

## Decoration and accounting macros

| macro | occurrences in the manuscript |
|---|--:|
| `\LeanInline` | 0 |
| `\LeanStar` | 0 |
| `\LeanTally` | 0 |
| `\LeanCW` | 0 |
| `\leanline` | 0 |
| `\code` | 104 |
| `\testref` | 0 |
| `\witness` | 0 |

## Gates measured here

| gate | result |
|---|---|
| citation-key lint (no key, no `\cite` inside a tag) | **0 failures** |
| stars (`\LeanStar` body uses) | **0** |
| `Tier` column in a table | **0** |
| `pending(D7)` markers | **0** |
| `\tier[…]` id parts that are neither a `\testref`, a snake_case id nor a qualified declaration | **0** |
| open sites (`(open;`) | **0** |

## Per-file marks

| file | `\tier[…]` + `\tier{…}` marks |
|---|--:|

Re-generate with `pnpm run witness:inventory`; a hand-edited figure is a defect.
