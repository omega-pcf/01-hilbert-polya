# STYLE GUIDE - Internal Formal Coherence

**Objective**: Establish internal coherence in formal language, notation, and structure. It is NOT about imitating Elsevier. It is about being **extremely serious** without being forced into an artificial box.

**FUNDAMENTAL EDITORIAL PRINCIPLE**: This guide is **editorial**, not **authorial**. Its function is to:
- ✅ Prescribe **style, format, notation coherence, and presentation structure**
- ✅ Ensure **clarity, formal rigor, and consistency** in writing
- ❌ **NOT** prescribe specific mathematical content (concepts, theorems, constructions)
- ❌ **NOT** add concepts not present in the original text without explicit verification
- ❌ **NOT** make mathematical claims that require technical justification

**When a mathematical content suggestion is encountered**: Verify first against the original text. If it is not grounded, maintain fidelity to the original and only improve the formal presentation.

---

## 1. VOICE AND TONE

### Principle
- **Formal**: No casualness. Rigorous academic.
- **Direct**: Explain something once, well. No repetition.
- **Intellectually honest**: If it contradicts orthodoxy, say so explicitly (not hidden).
- **Unapologetic**: This is what it is. If it's unusual, it's because the structure requires it.

### Audience
- **Expert scientific public**: The paper is addressed to scientists with advanced training in mathematics, but its multi-domain scope requires familiarity with number theory, complex analysis, Hermitian operators, quantum physics, geometry, and computational verification. The artificial separation of mathematics into "departments" does not reflect the interdisciplinary nature of the problems addressed.
- **Do not sacrifice readability "foolishly"**: Do not use less clear or concise words just to make the text sound less dense or specialized. The expert audience expects and appreciates technical precision and appropriate terminology. Avoid periphrasis that seeks to "soften" content at the expense of clarity.
- **Clarity over artificial simplicity**: Prefer precise and concise technical terms over unnecessary periphrasis. Readability comes from structure, coherence, and precision, not from avoiding specialized terminology. The paper addresses deep mathematical problems that require a multi-domain approach; the writing must reflect this complexity without artificiality.

### Paragraph Structure
- **Topic + Justification + Consequence**
- No: "This is A, which is important because B, also it's C, and also D, finally E."
- Yes: "This is A. Due to [technical reason], this implies B and C. This differs from [orthodoxy] because [geometric/structural explanation]."

### Avoid
- Unnecessary mechanical enumerations when it can be written fluidly (but enumerations are valid when they improve clarity or structure).
- Bullet lists with short phrases + repetitive subsequent amplification (AI-pattern).
- "Observe that", "It is important to note that", "It is worth mentioning that".
- Repetition of the same idea with different notation.

---

## 2. UNIFIED NOTATION

### Notation Macros (Defined in `main.tex`)

**Principle**: Only use macros for document-specific notation that:
- Repeats frequently
- Is complex or long to write
- Might change or need global adjustments

**Available Macros:**
- `\omegapcf` → `\Omega_{\text{PCF}}` (PCF operator - document-specific notation)
- `\omegahat` → `\hat{\Omega}` (generator matrix - useful if used frequently)

**Standard Notation (DO NOT use macros):**
- ✅ Directly use `\mathbb{C}`, `\mathbb{R}`, `\mathbb{Z}`, `\mathbb{Q}`, `\mathbb{N}` (standard, well-known)
- ✅ Directly use `\varphi` for the golden ratio (standard)
- ✅ Directly use `\mathcal{C}`, `\mathcal{H}`, etc. (standard)

**Reason**: Macros for standard notation add unnecessary complexity without real benefit. They only make sense for document-specific notation that repeats a lot.

### Cross-Reference Macros (Defined in `main.tex`)

For consistent references to mathematical constructions:

- `\tref{label}` → "Theorem X.Y.Z"
- `\dref{label}` → "Definition X.Y.Z"
- `\pref{label}` → "Proposition X.Y.Z"
- `\lref{label}` → "Lemma X.Y.Z"
- `\cref{label}` → "Construction X.Y.Z"
- `\oref{label}` → "Observation X.Y.Z"

**Recommended Usage:**
- ✅ Use these macros instead of manually writing "Theorem~\ref{...}"
- ✅ Example: `As shown in \pref{prop:rotational-invariance}...` instead of `As shown in Proposition~\ref{prop:rotational-invariance}...`
- ✅ This ensures consistent formatting and facilitates global changes.

### Complex Numbers
- **Modulus**: always `|z|` in algebraic context, "magnitude" in geometric context.
- **Complex variable**: `z = x + iy` in the first definition, then just `z`.
- **Euler**: `e^{i\theta}` (not `exp(i\theta)` variations).

### Spaces
- **Complex plane**: `\mathbb{C}`
- **Real numbers**: `\mathbb{R}`
- **Integers**: `\mathbb{Z}`
- **Hilbert**: `\mathcal{H}` or `H` (CHOOSE ONE per section and maintain).
- **Sobolev/L² Spaces**: `L^2(\text{domain})` - be explicit about the domain.

### Operators
- **PCF Operator**: `\Omega` (use `\omegapcf` for `\Omega_{\text{PCF}}`).
- **Generator Matrix**: `\hat{\Omega}` (use `\omegahat` if it repeats a lot, or directly `\hat{\Omega}`).
- **Fourier**: `\mathcal{F}`
- **Integral**: always `\int_X f(x) dx` with clear limits.

### Golden Ratio
- **Symbol**: `\varphi` (not variations).
- **Value**: `\varphi \approx 1.618...` (if numerical is needed) or just `\varphi` (algebraic).
- **Powers**: `\varphi^\sigma` or `\varphi^n` - be consistent with the index.

---

## 3. STRUCTURE OF DEFINITIONS

### Standard Format
```latex
\begin{definition}[Descriptive Name]
[CONCISE STATEMENT IN ONE SENTENCE]

For [elements involved], [fundamental property]:
\[
[main formula]
\]

[CONTEXT/MEANING: 1-2 paragraphs maximum explaining what it means, why it matters, how it relates to the previous content]
\end{definition}
```

---

## 4. EQUATIONS AND FORMULAS

### Rule: **Equation ↔ Text**
Every formula must be integrated with text, never isolated.

#### BAD
```latex
The operator is defined as:
\[
\hat{\Omega} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}
\]
```

#### GOOD
```latex
The operator $\hat{\Omega}$ is a linear transformation represented in the standard basis as:
\[
\hat{\Omega} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}
\]
where $a, b, c, d$ are coefficients satisfying [property]. This diagonal form reveals that $\hat{\Omega}$ acts as [geometric interpretation].
```

---

## 5. PROPOSITIONS, THEOREMS, COROLLARIES

### Structure
```latex
\begin{theorem}[Descriptive Name]\label{thm:...}
[FORMAL STATEMENT IN ONE OR TWO LINES]

If [hypothesis], then [conclusion]:
\[
[concise formula]
\]
\begin{proof}
[Main argument in prose, logically structured]
[If there are key algebraic steps, show ONE or TWO]
[Conclusion: "Therefore, [conclusion of the theorem]"]
\end{proof}
\end{theorem}
```

### Difference: Theorem vs. Proposition vs. Lemma
- **Theorem**: MAIN result. Can change an entire perspective.
- **Proposition**: IMPORTANT but subordinate result. Tool for theorems.
- **Lemma**: Necessary TECHNICAL result. Not interesting on its own.

If it's not clear which one it is, err towards **Proposition** (it's the most flexible).

### Observation vs. Remark
- **Observation**: Geometric or structural insight that follows NATURALLY from the theorem.
- **Remark**: Technical clarification or context about notation/convention.

### Line Breaks in Environments
Use `\par` explicitly to force paragraph breaks within `theorem`, `proposition`, `definition`, etc.

---

## 6. AVOID AI PATTERNS

- **Repetitive Enumeration**: Avoid "First, A. Second, B. Third, C." if it doesn't add clarity.
- **Bullet List + Repetitive Amplification**: Avoid listing features and then repeating them in the following text.
- **Filler Phrases**: Avoid "Observe that", "It is important to note that". Let the logic speak for itself.

---

## 7. PROACTIVE DETECTION OF INCONSISTENCIES

The AI should act as a proactive editor: detecting mathematical, logical, or stylistic inconsistencies, even when not explicitly requested.

### Protocol
1. **Detect**: Identify inconsistency, ambiguity, or error.
2. **Evaluate**: Strong (clear error), Moderate (ambiguity), Weak (stylistic).
3. **Present**: Specific analysis + options before or after the task.

---

## 8. COMPARISON OF SECTIONS (paper.md vs src/chapters)

### ⚠️ CRITICAL RULE: DO NOT EDIT paper.md
`paper.md` is the original source document and MUST NOT be modified. All updates must be made in the `.tex` files in `src/chapters/`.

**Purpose**: Generate concise reports of differences between the original `paper.md` and the current transcribed chapters when requested.
