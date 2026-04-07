# Installation and Requirements

This document outlines the software requirements and steps to setup the environment for compiling the manuscript and running the verification suite.

## Prerequisites

To perform the full build process, formal verification, and numerical analysis, your system requires the following tools:

1. **[Node.js](https://nodejs.org/) & [pnpm](https://pnpm.io/)**
   - Required for managing project scripts, the release pipeline, and TypeScript wrappers.
   - Install `pnpm` globally via `npm install -g pnpm`.

2. **[uv](https://github.com/astral-sh/uv) (Python package manager)**
   - Used for the python-based numerical verification (`mpmath`, `numpy`, `matplotlib`) and figure generation.
   - `uv` provides extremely fast virtual environment creation and package resolution.

3. **[Docker](https://www.docker.com/)**
   - Required for the deterministic and reproducible LaTeX build process.
   - We use the `kjarosh/latex:2024.4-full` image.

4. **[Lean 4 & Elan](https://leanprover.github.io/lean4/doc/setup.html)** *(Optional but recommended)*
   - Required to build and execute the categorical proofs in the `lean/` directory.

---

## Setup Instructions

### 1. Clone the repository

Clone the official metadata-synchronized repository and navigate into it:

```bash
git clone https://github.com/omega-pcf/01-hilbert-polya.git
cd 01-hilbert-polya
```

### 2. Install Node dependencies

Use `pnpm` to install all necessary TypeScript tools and release binaries defined in `package.json`:

```bash
pnpm install
```

### 3. Initialize Python (via `uv`)

To generate figures or run the numerical verification scripts locally, Python is managed by `uv`. The `pnpm` scripts automatically prefix the Python commands with `uv run`, which will automatically install the necessary Python environment based on the `requirements` specifications.

To manually sync or fetch Python dependencies for the figures:

```bash
cd scripts/figures
uv sync
cd ../..
```

---

## Executing the Workflow

Once the installation is complete, you can use the built-in commands:

- **Build the LaTeX Manuscript:**

  ```bash
  pnpm run build
  ```

  *(Downloads the required LaTeX Docker image if absent and compiles standard `.tex` sources to `.pdf`)*

- **Generate Figure Placeholders & Compile Full Package:**

  ```bash
  pnpm run build:full
  ```

- **Run all Numerical Verifications:**

  ```bash
  pnpm run verify:py
  ```

- **Run Formal Proof Verifications (Lean 4):**

  Through the `pnpm` wrapper:

  ```bash
  pnpm run verify:lean
  ```

  Or verify natively without `pnpm` using `lake`:

  ```bash
  cd lean
  lake build
  ```
