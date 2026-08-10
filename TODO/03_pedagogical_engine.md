# Document 3 — Pedagogical engine (current)

**Supersedes:** `pedagogical_engine_preliminary_summary.md` (archived at
[`archive/pedagogy/`](archive/pedagogy/), kept for the design-rationale trail).

**Status:** design only, matching `knowledge-graph/logic.md`'s own statement that its §6
activity/task layer is *"not yet done, and out of scope for [the completed] phase."* This document
is that next phase's spec, not yet built.

## 1. Core idea

Domain knowledge (`facts-tree.md`) says what is true. A separate pedagogical engine decides what is
worth deriving from it for teaching — explanation, comparison, demonstration, practical application,
attack, measurement, exercises, and assessment. The engine should not compute every possible logical
consequence; it performs goal-directed pedagogical derivation, filtered to `demonstrable: true` and
`teaching_priority: core|recommended` facts per `logic.md` §7's own workflow.

## 2. Operator vocabulary, mapped onto what already exists

Each operator is a transformation from domain facts to a teaching artefact. Most already have a home
in `logic.md`'s existing machinery — the table below is the actual design work: confirming which
operators are new versus already covered, so nothing gets rebuilt.

| Operator | Produces | Existing home in `logic.md` / `knowledge-graph/` |
|---|---|---|
| `COMPARE` / `CONTRAST` | structured comparison table | `differs_from` facts + [`tradeoff-comparisons.yaml`](knowledge-graph/tradeoff-comparisons.yaml) (§3c-2) |
| `EXPLAIN_WHY` | a why-chain | [`design-rationale-chains.yaml`](knowledge-graph/design-rationale-chains.yaml) (§3b): `Design-element —(part_of\|is_a\|enables)→ Property —(prevents\|vulnerable_to\|satisfies)→ Attack-or-goal` |
| `VIOLATE` + `ATTACK` | failure demonstration, attack exercise | a design-rationale chain's second hop, plus [`counterexamples.yaml`](knowledge-graph/counterexamples.yaml) (§3c-5) |
| `DEMONSTRATE` | a runnable observation | the `demonstration_sketch` field already present in all six §3c pools |
| `APPLY` / `TRANSFER` | practical/new-context exercise | [`usage-pitfall-pairs.yaml`](knowledge-graph/usage-pitfall-pairs.yaml) (§3c-1), `best_practice`/`pitfall` facts |
| `DEFINE` / `DECOMPOSE` | definition-dependency breakdown | `definition_uses`-equivalent: `depends_on(kind=definition)` edges in `facts-tree.md`, already generating the definition-dependency graph |
| `TRACE` | step-by-step derivation | a walked chain of already-existing binary edges (§3b's own definition of a chain) |
| **`BRIDGE`** | known-concept → target-concept teaching path | **genuinely new** — see §3 below |
| **`REPAIR`** | fix-and-reverify exercise | **genuinely new** — not yet a §3c pattern; closest existing shape is the usage/pitfall pair, but repair needs a *sequence* (break → fix → reverify), not a static contrast |
| **`MEASURE`** | benchmark/scaling exercise | **genuinely new as a distinct output kind** — `logic.md` §7 (doc 01) lists measurable dimensions (runtime, throughput, overhead) as pedagogically demonstrable, but no §3c pool currently collects "measurable" facts the way it collects comparisons or consequences |
| `PREDICT` | prediction-then-verify exercise | not a new fact type — a presentation mode applied to any `demonstrable: true` fact (ask for the outcome before running the demonstration) |

Three operators (`BRIDGE`, `REPAIR`, `MEASURE`) are the actual gap. Everything else is a presentation
layer over facts and pools that already exist.

## 3. `BRIDGE` — the one operator that needs new machinery

Given a target concept a student doesn't know and a known concept they likely do, find:

```text
maximal shared structure + minimal conceptual difference
```

This is structurally a `COMPARE` between two concepts **chosen for pedagogical adjacency to a
specific student**, not for definitional similarity — the search needs a "what does this student
already know" input that the other operators don't. Not yet built; first candidate slice is Seminar
1's `encoding-and-stream-ciphers.py`, which already has this exact worked path in the notebook (see
§8 below).

**Full worked example — encoding → Caesar → encryption**, kept in full because the notation
progression is the actual pedagogical content, not just the three labels:

```text
encoding:    E(m)          — publicly determined transformation, goal is representation
Caesar:      E_k(m)        — a keyed instance of the same shape, still publicly invertible if k is guessed/known
encryption:  Enc_k(m)      — keyed, goal is confidentiality, inversion by non-key-holders infeasible
```

Caesar is the actual bridge step, not a distraction: it has a key, so it looks like encryption, but
brute-forcing 26 keys is trivial, so it doesn't yet deliver on encryption's requirement. Walking a
student through *why* Caesar isn't "real" encryption is what motivates the requirement. This is also
where the engine's iterative gap-discovery shows up concretely: a first-pass distinction like
"reversible vs. not reversible" is too coarse (both encoding and Caesar are reversible by *someone*)
— the engine should discover it needs the finer distinction **publicly reversible** vs. **reversible
only with secret information**, and propose that as a new `status: candidate` fact for review rather
than silently using the coarse version. That refinement-discovery step, not just the final
three-way comparison, is what `BRIDGE` actually needs to do.

## 4. Provenance — every derivation should answer "why do we claim this"

A concrete derivation (not the domain model as a whole, which may contain cycles via `implies`/
`enables` chains) is a DAG: premises feed a conclusion, which may itself feed a further conclusion.
The engine should be able to answer, for any generated explanation or exercise:

```text
Why do we claim E?
Which definitions and facts were used?
Which assumption is responsible?
```

Concretely, this is not new machinery — a design-rationale chain (§3b) already *is* a two-node
provenance path, and a composite fact's `premises.refs: [fact_id, ...]` (§3a case 3) already records
exactly this for conjunctive claims. What's new is treating provenance as a first-class *output*
property of anything the engine generates: every generated explanation, comparison, or exercise
should carry the list of `fact_id`s it was built from, not just read naturally from prose. This is
close to a Euclidean proof style — each step traceable to a definition, an explicit assumption, or a
previously derived fact — and it's what makes "why is this exercise testing what it claims to test"
a checkable question rather than an editorial judgment call.

## 5. Capability vocabulary, and when a comparison is worth generating

A takeaway is not a fact restated — it's a statement of what the student should be able to *do* with
it. Useful capability vocabulary: `RECALL, EXPLAIN, DISTINGUISH, TRACE, PREDICT, CHOOSE, APPLY,
IMPLEMENT, DEBUG, ATTACK, DESIGN, JUSTIFY`. This is the target-capability input every operator in §2
needs (e.g. `EXPLAIN_WHY` targets `EXPLAIN`/`JUSTIFY`; `VIOLATE`+`ATTACK` targets `ATTACK`/`DEBUG`;
`APPLY`/`TRANSFER` targets `APPLY`/`DESIGN`) — the same underlying fact produces a different exercise
depending on which capability is being targeted, which is the actual mechanism behind §6's
"Exercise Generation" idea in the preliminary doc.

`COMPARE`/`CONTRAST` specifically needs a filter, or it produces meaningless output: comparing two
concepts just because both exist in the knowledge base is not useful (`hash function vs. certificate`
— no shared pedagogical context). A comparison is worth generating only when the pair shares one of:
same broad purpose, same use case, same category, alternative constructions for the same problem,
similar interface, similar visible behaviour, or is a documented commonly-confused pair. `hash vs.
MAC`, `MAC vs. digital signature`, `CTR vs. CBC`, `nonce vs. IV`, `OTP vs. stream cipher` all pass
this filter; most arbitrary pairs of definitions don't. In terms of existing machinery: a `COMPARES`/
`differs_from` fact with a real, populated `dimension` already implies this filter was satisfied by
whoever wrote it (§3c-2); the engine needs to apply the same filter when *proposing* a new comparison
that isn't in `tradeoff-comparisons.yaml` yet.

## 6. Demonstration archetypes and the full generation pipeline

Useful demonstration archetypes to check a fact against before calling it `demonstrable: true`:
function usage, vary-one-input, controlled comparison, requirement violation, failure demonstration,
attack, attack scaling, benchmark/resource usage, size/overhead measurement, tampering, security
game, toy-version break, parameter sweep, API misuse. Typical observables: output, intermediate
values, runtime, memory, output length, success/failure, verification result, Hamming distance.

**Full pipeline, one worked example end to end** (this is the shape every generated unit should have,
tying together §2's operators, §4's provenance, and §5's capability targeting):

```text
Outcome (capability target):
    Understand why encoding is not encryption.

Derivation (provenance — §4):
    encoding  —[fact: transforms data, representation goal, no secret required]
    encryption —[fact: transforms data, confidentiality goal, uses key material]
    shared: transformation of data
    distinguishing dimensions: purpose, keying, security guarantee

Demonstration (DEMONSTRATE):
    Base64(message)  vs.  Encrypt(key, message)

Transfer question (APPLY/TRANSFER, targeting JUSTIFY):
    A developer says a sensitive token is secure because it is Base64-encoded. Assess the claim.
```

Every stage traces back to the same one or two domain facts — nothing here is invented at the
demonstration or question stage that wasn't already in the derivation.

## 7. Review status: BASE / DERIVED / PROPOSED — reconciled with existing `status`

The preliminary doc proposed a three-way status (`BASE` = curated, `DERIVED` = reconstructed from
base, `PROPOSED` = discovered missing and awaiting review) for content the engine produces while
trying to build an explanation. `logic.md` §2c already has
`status: candidate | reviewed | conflicting | external_needed` on every fact. These are the same
axis, not two parallel ones:

- `PROPOSED` ≈ `status: candidate`, specifically candidates the *engine* surfaces while generating
  (as opposed to candidates found during manual extraction) — same field, different discovery route,
  worth a provenance note but not a new field.
- `BASE` ≈ `status: reviewed`.
- `DERIVED` content (a generated explanation, a comparison table) is not stored as a fact at all —
  it's a projection, matching `logic.md` §7's "derived views, not separately maintained knowledge"
  principle. Only genuinely new facts the engine surfaces (a missing distinction, a missing
  definition) get a `status: candidate` fact entry for review.

## 8. Validation slice: the seminars, not an invented one

The archived proposals recommended validating the schema against an invented slice (OTP → stream
cipher → block cipher → AES → ECB/CBC/CTR → nonce → MAC → AEAD). That slice already exists here, for
real, with real student tasks: [`seminars/notebooks/`](seminars/notebooks/) plus
[`seminars/seminar-task-categorization.md`](seminars/seminar-task-categorization.md), which sorts
every existing seminar task into one of six example-pattern types — `DRC` (design-rationale chain),
`PIT` (usage/pitfall pair), `TRD` (tradeoff), `INST` (concrete instantiation), `CEX`
(counterexample), `CONS` (bare consequence) — or flags it `MECH` (skill practice, no new concept).

These six labels **are** `logic.md` §3c's five example-pattern types plus §3b's design-rationale
chain — the seminar-categorization pass and this engine design are the same taxonomy, found
independently from two directions (top-down from the fact base, bottom-up from real notebooks), now
formally the same thing. The engine's job on this slice is not to invent new pedagogy but to
mechanize what the categorization pass already did by hand.

## 9. Open work — first concrete tasks

Three real examples the categorization pass found in the notebooks but that aren't yet in the §3c
YAML pools (`seminars/seminar-task-categorization.md`, "Open items"):

1. **Nonce → keystream uniqueness** (Seminar 1, §25) → candidate for `design-rationale-chains.yaml`.
2. **AES vs. RSA speed** (Seminar 5, Task 3.1) → candidate for `tradeoff-comparisons.yaml`, likely
   stronger than the existing ECC-vs-RSA entry given how central it is to motivating hybrid
   encryption.
3. **Certificate binding vs. impersonation** (Seminar 7, Task 1.2) → candidate for
   `design-rationale-chains.yaml`.

Folding these three in — by hand, following §3b/§3c's existing shape — is the smallest possible next
step, and a natural first test of whether `BRIDGE`/`REPAIR`/`MEASURE` are actually needed before
building them: Seminar 1's encoding→Caesar→keyed-cipher progression (§3 above) is the first real
`BRIDGE` candidate; Seminar 6's MAC ladder (unkeyed hash → XOR encryption → XOR checksum → real MAC,
each broken then fixed) is the first real `REPAIR` candidate; Seminar 5's AES-vs-RSA timing task is
the first real `MEASURE` candidate.
