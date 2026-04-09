#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
CHAPTERS_DIR = SRC_DIR / "chapters"
TMP_DIR = PROJECT_ROOT / "tmp"
OUTPUT_FILE = TMP_DIR / "manuscript_unified.tex"

# Chapter order as defined in main.tex
CHAPTERS = [
    "abstract",
    "introduction",
    "background",
    "methods",
    "results",
    "categorical",
    "squeeze",
    "discussion",
    "conclusions",
    "disclosure",
    "acknowledgments",
    "appendix"
]

PREAMBLE_TEMPLATE = r"""\documentclass[11pt,fleqn]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amsthm}
\usepackage{mathtools}
\usepackage{amssymb}
\usepackage{tikz-cd}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{graphicx}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage[capitalize,nameinlink]{cleveref}
\usepackage{setspace}
\usepackage{geometry}
\geometry{margin=1in}

% Sigma class emulators
\newcommand{\Abstract}[1]{\begin{abstract} #1 \end{abstract}}
\newcommand{\Keywords}[1]{\par\vspace{1em}\noindent\textbf{Keywords:} #1}
\newcommand{\Classification}[1]{\par\vspace{0.5em}\noindent\textbf{AMS Classification:} #1}
\newcommand{\ShortArticleName}[1]{}
\newcommand{\ArticleName}[1]{\title{#1}}
\newcommand{\Author}[1]{\author{#1}}
\newcommand{\AuthorNameForHeading}[1]{}
\newcommand{\Address}[1]{\date{#1}}
\newcommand{\EmailD}[1]{}
\newcommand{\ArticleDates}[1]{\date{#1}}
\newcommand{\LastPageEnding}{}
\newcommand{\FirstPageHeading}{}
\newcommand{\PaperNumber}[1]{}

% Macros from main.tex
\newcommand{\cat}[1]{\mathcal{#1}}
\newcommand{\Set}{\mathbf{Set}}
\newcommand{\Hilb}{\mathbf{Hilb} }
\newcommand{\Met}{\mathbf{Met} }
\newcommand{\ob}[1]{\mathrm{ob}(#1)}
\newcommand{\norm}[1]{\|#1\|}
\newcommand{\abs}[1]{|#1|}
\newcommand{\Zmod}[1]{\mathbb{Z}/{#1}\mathbb{Z}}
\newcommand{\Ztwenty}{(\mathbb{Z}/20\mathbb{Z})^\times}
\newcommand{\Rpcf}{R_{\mathrm{PCF}}}
\newcommand{\Ecube}{E^3}
\newcommand{\golden}{\varphi}
\newcommand{\OmH}{\widehat{\Omega}}
\newcommand{\lean}[1]{\nolinkurl{#1}}
\newcommand{\pcfrepo}{https://github.com/omega-pcf/01-hilbert-polya}
\newcommand{\mail}[1]{\href{mailto:#1}{#1}}

% Theorems for article class
\newtheorem{Theorem}{Theorem}[section]
\newtheorem*{Theorem*}{Theorem}
\newtheorem{Corollary}[Theorem]{Corollary}
\newtheorem{Lemma}[Theorem]{Lemma}
\newtheorem{Proposition}[Theorem]{Proposition}
\newtheorem{Conjecture}[Theorem]{Conjecture}
\newtheorem{Observation}[Theorem]{Observation}

\theoremstyle{definition}
\newtheorem{Definition}[Theorem]{Definition}
\newtheorem{Note}[Theorem]{Note}
\newtheorem{Example}[Theorem]{Example}
\newtheorem{Remark}[Theorem]{Remark}

\title{The Hilbert--P\'{o}lya Operator and the Primitive Structure of the Complex Plane: Between $\mathbb{F}_1$, String Theory, and Ancient Geometry}
\author{Jorge Armando Gonz\'{a}lez Garc\'{i}a et al.}
\date{\today}

\begin{document}
\maketitle

\tableofcontents
\newpage

"""

def get_chapter_content(chapter_name):
    path = CHAPTERS_DIR / f"{chapter_name}.tex"
    if not path.exists():
        print(f"Warning: Chapter {chapter_name} not found at {path}")
        return f"%% MISSING CHAPTER: {chapter_name}\n"
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ensure images path is correct
    content = content.replace("src/images/", "images/")
    return content

def generate_unified():
    TMP_DIR.mkdir(exist_ok=True)
    
    full_latex = PREAMBLE_TEMPLATE
    
    for chapter in CHAPTERS:
        full_latex += f"\n%% ================= CHAPTER: {chapter} =================\n"
        full_latex += get_chapter_content(chapter)
        full_latex += "\n"
    
    # Add bibliography with absolute path or verifiable relative path
    # We copy the bib file to tmp to avoid path issues with bibtex
    bib_src = SRC_DIR / "bibliography.bib"
    bib_dest = TMP_DIR / "bibliography.bib"
    if bib_src.exists():
        import shutil
        shutil.copy2(bib_src, bib_dest)
    
    full_latex += r"""
\bibliographystyle{plain}
\bibliography{bibliography}
\end{document}
"""
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_latex)
    
    print(f"Unified TeX generated at {OUTPUT_FILE}")

def run_cmd(args, cwd=None, ignore_error=False):
    print(f"Running: {' '.join(args)}")
    res = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0 and not ignore_error:
        print(f"Error running command: {res.stderr}")
    return res

def compile_pdf():
    print("Compiling PDF...")
    # 1. First pdflatex (ignore errors as they might be solved by bibtex/later runs)
    run_cmd(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(TMP_DIR), str(OUTPUT_FILE)], ignore_error=True)
    
    # 2. Bibtex
    aux_file = OUTPUT_FILE.with_suffix(".aux").name
    run_cmd(["bibtex", aux_file], cwd=TMP_DIR)
    
    # 3. pdflatex again x2
    run_cmd(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(TMP_DIR), str(OUTPUT_FILE)], ignore_error=True)
    run_cmd(["pdflatex", "-interaction=nonstopmode", "-output-directory", str(TMP_DIR), str(OUTPUT_FILE)], ignore_error=True)
    
    target_pdf = OUTPUT_FILE.with_suffix(".pdf")
    if target_pdf.exists():
        print(f"Success! PDF generated at {target_pdf}")
    else:
        print("Final PDF not found. Check log files in tmp/")

if __name__ == "__main__":
    generate_unified()
    compile_pdf()
