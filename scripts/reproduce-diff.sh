#!/usr/bin/env bash
# scripts/reproduce-diff.sh
# Usage: ./scripts/reproduce-diff.sh [ORIGINAL_FILE] [OUTPUT_HTML]

set -e

# Default original file path from the user's request
ORIGINAL_MANUSCRIPT="${1:-/home/aficio/Downloads/V11_paper_v10(1).tex}"
FINAL_REPORT="${2:-tmp/manuscript_diff.html}"

# 1. Modular Order of Reconstruction
CHAPTERS=(
    "src/chapters/abstract.tex"
    "src/chapters/introduction.tex"
    "src/chapters/background.tex"
    "src/chapters/methods.tex"
    "src/chapters/results.tex"
    "src/chapters/categorical.tex"
    "src/chapters/squeeze.tex"
    "src/chapters/discussion.tex"
    "src/chapters/conclusions.tex"
    "src/chapters/disclosure.tex"
    "src/chapters/acknowledgments.tex"
    "src/chapters/appendix.tex"
)

OUT_TEX="tmp/reconstructed_v11.tex"
mkdir -p tmp

echo "--- Reconstructing current manuscript into $OUT_TEX ---"

# We include the current Sigma preamble from main.tex to provide structure
head -n 114 main.tex > "$OUT_TEX"

for CHAPTER in "${CHAPTERS[@]}"; do
    if [ -f "$CHAPTER" ]; then
        echo "Appending $CHAPTER..."
        echo -e "\n% --- CHAPTER START: $CHAPTER ---\n" >> "$OUT_TEX"
        cat "$CHAPTER" >> "$OUT_TEX"
        echo -e "\n% --- CHAPTER END: $CHAPTER ---\n" >> "$OUT_TEX"
    else
        echo "Warning: $CHAPTER not found, skipping."
    fi
done

# Append the bibliography and closing commands from main.tex
tail -n +137 main.tex >> "$OUT_TEX"

echo "Reconstruction complete."

# 2. High-Performance Visual Diff (ANSI -> HTML)
# --no-index: Compares files outside git repo status
# --color=always + aha: Generates the visual HTML
# --histogram: Better for comparing text blocks
# -w / -b: Ignores space changes (useful for modularization indentation shifts)
# --color-moved=zebra: Highlights moved blocks differently

echo "Generating visual diff report..."
git diff --no-index --color=always --histogram -w \
    --color-moved=zebra \
    "$ORIGINAL_MANUSCRIPT" "$OUT_TEX" | aha --black --title "Manuscript Progress Diff" > "$FINAL_REPORT"

echo "Success! Report saved to $FINAL_REPORT"
echo "TIP: You can preview it interactively with fzf --ansi before generating the HTML report."
