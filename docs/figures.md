# Figure pipeline: deterministic, text-extractable PDFs

`pnpm run generate:figures` runs `scripts/figures/main.py`, which executes the
generators of `scripts/figures/generators/` into `images/` (PDF + SVG).

The chain table (generator → `images/` → verification) is
[`architecture.md` §Sources of truth](architecture.md#sources-of-truth).

## What it guarantees

1. **The text in the PDFs is extractable.** Every generated PDF carries a
   `/ToUnicode` CMap, so `pdftotext` reads `σ`, `φ`, `↑` back instead of
   junk.
2. **Two consecutive runs are byte-identical.** `SOURCE_DATE_EPOCH` is pinned
   (PDF `/CreationDate`) and `svg.hashsalt` is set (the SVG backend otherwise
   mints a fresh `uuid4` per render), so `git status --porcelain images/`
   does not change between runs.
3. **No host font is a prerequisite.** The typography is pinned in
   `scripts/figures/utils/__init__.py` (DejaVu Serif, bundled with
   matplotlib); a machine-local `matplotlibrc` cannot change the output.

## Settings (all in `scripts/figures/utils/__init__.py`)

| Setting | Value | Reason |
| --- | --- | --- |
| `pdf.fonttype` | `42` | On matplotlib 3.10.x (the version in `uv.lock`) the default `3` embeds Type 3 fonts **without** `/ToUnicode`. Type 42 embeds the same TrueType outlines as CID fonts **with** `/ToUnicode`. |
| `svg.hashsalt` | `omega-pcf-figures` | Without a salt every SVG render got new ids → 27 figures changed on every run. |
| `SOURCE_DATE_EPOCH` | `1794274263` | The timestamp of the figure round that produced `images/` (2026-11-09 19:31:03 -06:00). Honoured by the pdf, ps and svg backends; an explicitly exported value still wins. |

## Verifying

```bash
pnpm run generate:figures          # run once
sha256sum images/* > /tmp/a
pnpm run generate:figures          # run twice
sha256sum images/* > /tmp/b && diff /tmp/a /tmp/b   # must be silent

pdffonts images/towers_comparison.pdf    # emb sub uni: yes yes yes
pdftotext images/towers_comparison.pdf - # reads Rσ, φ, ↑ …
```

Docker (`kjarosh/latex`) is not involved in figure generation: it is only the
LaTeX engine of `pnpm run build`.
