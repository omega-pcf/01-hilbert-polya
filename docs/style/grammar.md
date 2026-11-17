# GRAMMAR AND USAGE — rules of human language for mathematical prose

| Field | Value |
|---|---|
| **Document** | `docs/style/grammar.md` |
| **Status** | In force |
| **Version** | 1.0 (extracted from `style-guide.md` §1.5) |
| **Date** | 2026-11-16 |
| **Language** | English; worked examples in Spanish, English, French, Italian |
| **Scope** | Grammar and register of the texts this family writes — language-neutral rules; each language's own normative authority governs its own cases |

**Objective**: state the grammar rules that make formal prose **correct, didactic and
succinct**, as rules of *human language* rather than of Spanish: the Spanish material
that used to live in `style-guide.md` §1.5 is kept here as one worked language of the
family, not as the frame.

**Why the rules pay** (the reason each one is kept, not its tradition):

- **Correctness**: a grammatically complete, agreeing, unambiguous sentence admits one
  reading; an omitted function word or a dangling reference admits several, and the
  reader must choose.
- **Didacticity**: the reader of a definition or a proof is following an argument, not
  reconstructing it — every elision the language permits is a step the reader must
  invent.
- **Succinctness**: the savings come from cutting *filler*, not from cutting *structure*.
  Dropping a preposition saves four characters and costs a reread; dropping an empty
  modifier saves a word and costs nothing (§G7).

**Fundamental principle**: mathematical abstraction and linguistic elegance are
complementary, not antagonistic. The artificial habit of omitting prepositions,
conjunctions or determiners under the banner of "mathematical concision" creates
ambiguity, hinders reading, and contradicts the goal it claims to serve.

**Register, not law**: §G8 is a convention of scientific register. It governs the texts
this family writes; it is not a rule of the language and it is not a rule about
conversation.

---

## G1. Complete structure

Every sentence carries the function words its language requires: conjunctions,
prepositions, determiners, and the connective that ties it to what precedes.

- ❌ ES `corresponde a rotación hiperbólica` (after an equation, the connection is missing)
- ✅ ES `y que corresponde a rotación hiperbólica`
- ❌ EN `corresponding to a hyperbolic rotation` (sentence fragment after the display)
- ✅ EN `and that it corresponds to a hyperbolic rotation`

## G2. Prepositions state the relation

A preposition is the relation between two concepts; dropping it leaves the concepts
adjacent and the relation unstated.

- ❌ ES "El mapa preserva estructura algebraica mediante isomorfismo grupo de Lorentz"
- ✅ ES "El mapa preserva la estructura algebraica mediante isomorfismo entre el grupo de Lorentz y..."
- ❌ EN `The map preserves algebraic structure via isomorphism Lorentz group`
- ✅ EN `The map preserves the algebraic structure by an isomorphism between the Lorentz group and …`

## G3. Agreement

Subject and verb agree in number and person; determiners agree with their nouns. The
agreement is imposed by the subject, not by the nearest noun or by an intervening
prepositional phrase.

- ❌ ES `El conjunto de los resultados se publican en la sección 4` (the subject is `el conjunto`)
- ✅ ES `El conjunto de los resultados se publica en la sección 4`
- ❌ EN `The set of results are published in section 4`
- ✅ EN `The set of results is published in section 4`

## G4. Clear reference

Every pronoun, demonstrative and ellipsis resolves to exactly one antecedent, and the
antecedent is introduced **before** it is used. Three failure modes: no antecedent at
all, two possible antecedents, and several pronoun/antecedent pairs in one sentence.
This is the grammar half of the discourse rule in `style-guide.md` §7.2.

- ❌ ES `El operador actúa sobre la base y su espectro es real. Se muestra acotado.` (`Se muestra` has no subject here)
- ✅ ES `El operador actúa sobre la base y su espectro es real. El operador se muestra acotado.`
- ❌ EN `When the flag is set and the buffer is full, it must be flushed` (two candidates for `it`)
- ✅ EN `When the flag is set and the buffer is full, the buffer must be flushed`

## G5. Punctuation for clarity

Commas separate items of an enumeration, semicolons separate related but independent
clauses, a colon introduces an enumeration or an explanation — each language's own
rules, applied to keep one reading.

- ❌ ES `La sección define el operador, su espectro y se demuestra la unicidad`
- ✅ ES `La sección define el operador y su espectro; después se demuestra la unicidad.`
- ❌ EN `The section defines the operator its spectrum and proves uniqueness`
- ✅ EN `The section defines the operator and its spectrum; it then proves uniqueness.`

## G6. Voice marks how an object is expressed

When the sentence says **how** an object is written, defined, characterized or
computed, the object is the subject and the verb must not cast it as an agent: an
abstract object does not write, define or identify anything. Each language marks this
its own way — English with the passive or `is defined as`, French and Italian with
their reflexive constructions, Spanish with the **reflexive passive** (`se` + active
verb, agreement with the patient subject).

**Practical test**: if the object is the **subject** and the verb describes *how that
object is expressed, structured, defined or characterized*, use the language's
non-agentive marking; if the object is the **active agent** acting on something else,
use the plain active verb.

- ❌ ES "La representación algebraica escribe $\mathbb{C} = ...$" (it suggests the representation actively "writes")
- ✅ ES "La representación algebraica se escribe como $\mathbb{C} = ...$" (it indicates how the representation is expressed)
- ❌ ES "La representación polar descompone $\mathbb{C} \cong ...$" (it suggests active action)
- ✅ ES "La representación polar se descompone como $\mathbb{C} \cong ...$" (it indicates how the representation is structured)
- ❌ ES "La representación euclidiana identifica $\mathbb{C} \cong ...$" (the representation is not an agent that "identifies")
- ✅ ES "En la representación euclidiana, $\mathbb{C}$ se identifica con ..." (it indicates how the identification is established)
- ❌ ES "La función define..." (when the function is the object being defined)
- ✅ ES "La función se define como..." (when the function is being defined)
- ❌ ES "La transformación preserva..." (it can be correct if the transformation is the active subject)
- ✅ ES "La transformación se preserva bajo..." (when speaking of a property that is maintained)
- ❌ EN `The algebraic representation writes $\mathbb{C} = \dots$`
- ✅ EN `The algebraic representation is written as $\mathbb{C} = \dots$`
- ❌ FR `La représentation algébrique écrit $\mathbb{C} = \dots$`
- ✅ FR `La représentation algébrique s'écrit $\mathbb{C} = \dots$`
- ❌ IT `La rappresentazione scrive $\mathbb{C} = \dots$`
- ✅ IT `La rappresentazione si scrive come $\mathbb{C} = \dots$`

**Avoid** the object as subject of an agentive transitive verb (`identifica`,
`define`, `construye`): write `En X, Y se identifica con …`, `Mediante X, Y se define
como …`, or `X establece la identificación de …`.

### G6.1 Spanish: the `se` verbs, checked against the RAE

Selection criterion (not an inventory): the RAE states that the reflexive passive *solo
se da con verbos transitivos* — a verb that cannot take a direct object cannot appear
in it. Any transitive verb of expression, structure, definition or calculation
qualifies; the list below is representative, and the criterion, not the list, is the
rule.

- **Kept** (transitive in the DLE): `se escribe`, `se define`, `se descompone`,
  `se caracteriza`, `se parametriza`, `se clasifica`, `se identifica`, `se representa`,
  `se expresa`, `se formula`, `se construye`, `se establece`, `se determina`,
  `se calcula`, `se evalúa`, `se resuelve`, `se aplica`, `se utiliza`, `se emplea`,
  `se preserva`, `se mantiene`, `se conserva`, `se genera`, `se produce`, `se obtiene`,
  `se muestra`, `se revela`.
- **Cut** (intransitive in the DLE, so they cannot form the reflexive passive):
  `se resulta`, `se surge`, `se emerge`, `se aparece`. Write `resulta`, `surge`,
  `emerge`, `aparece` — or name the subject: `La función resulta acotada`,
  `El error surge de …`. The old list also carried `se establece` twice.

## G7. Economy of the sentence

One idea per sentence; every word must earn its place.

- Cut empty modifiers (`really`, `very`, `totally`, `muy`, `realmente`) and doublets
  (`due and payable` → `due`; `knowledge and information` → either one).
- Reduce prepositional padding (`a number of` → `several`; `at this point in time` →
  `now`; `en este momento` → `ahora`).
- Keep the structure: an omitted preposition is not economy, it is a reread (§G2).

- ❌ EN `It is important to note that, at this point in time, the map is able to preserve the structure`
- ✅ EN `The map preserves the structure`
- ❌ ES `Se puede observar que, en este momento, el mapa es capaz de preservar la estructura`
- ✅ ES `El mapa preserva la estructura`

## G8. Register: impersonal, non-deictic third person

For the documents this family writes: no second-person inflection (`tú`, `tuyo`, `te`,
`ti`; `you`, `your`), no addressing the reader as the subject, no praise, blame or
other mark of subjectivity — the discourse is centred on the object of work, with
impersonal constructions (`se`, the reflexive passive), the periphrastic passive and
substantivizations. This is **scientific positivism as a register convention**: the
datum, the theorem and the artifact exist independently of who produced them, and a
value judgment is noise. It is a convention of the written product, not a rule about
conversation.

---

## Improvement example

- ❌ ES `La transformación preserva estructura, métrica, simetrías mediante isomorfismo grupo Lorentz corresponde rotación hiperbólica`
- ✅ ES `La transformación preserva la estructura, la métrica y las simetrías mediante un isomorfismo entre el grupo de Lorentz y las transformaciones conformes, y que corresponde a una rotación hiperbólica`
- ❌ EN `The transformation preserves structure metric symmetries via isomorphism Lorentz group corresponds hyperbolic rotation`
- ✅ EN `The transformation preserves the structure, the metric and the symmetries by an isomorphism between the Lorentz group and the conformal transformations, and it corresponds to a hyperbolic rotation`

## Sources (all retrieved on 2026-11-16)

- RAE — *Diccionario panhispánico de dudas*, «se», §2.1b (reflexive passive with transitive verbs only): https://www.rae.es/dpd/se
- RAE — *Diccionario panhispánico de dudas*, «concordancia»: https://www.rae.es/dpd/concordancia
- RAE — *Nueva gramática básica de la lengua española*, 23.6 *La pasiva refleja*: https://www.rae.es/gram%C3%A1tica-b%C3%A1sica/oraciones-activas-pasivas-impersonales-y-medias/la-pasiva-refleja
- RAE — *Diccionario de la lengua española*, transitiveness of the cut verbs: https://dle.rae.es/resultar · https://dle.rae.es/surgir · https://dle.rae.es/emerger · https://dle.rae.es/aparecer
- RAE — *Diccionario de la lengua española*, transitiveness of the kept verbs: https://dle.rae.es/mostrar · https://dle.rae.es/revelar
- *The Chicago Manual of Style*, 17th ed., §5.28 *Antecedents of pronouns*: https://www.chicagomanualofstyle.org/book/ed17/part2/ch05/psec028.html
- *The Chicago Manual of Style*, 17th ed., chapter 5 contents (§5.42 agreement of the personal pronoun): https://www.chicagomanualofstyle.org/book/ed17/part2/ch05/toc.html
- Digital.gov (GSA), *Writing for understanding* — active voice, hidden verbs: https://digital.gov/guides/plain-language/writing
- GSA/plainlanguage.gov, *Be concise* — one idea per sentence, doublets, modifiers (sources listed there: Garner 2001, Kimble 2006, SEC *Plain English Handbook* 1998): https://github.com/GSA/plainlanguage.gov/blob/main/_pages/guidelines/concise/index.md
