# Document 2 — Knowledge architecture (current)

**Supersedes:** `02_current_minimal_knowledge_ir_proposal.md`, `03_previous_typed_hypergraph_proposal.md`,
and `crypto_axiomatic_teaching_framework_current.md` (all three archived at
[`archive/knowledge-graph/`](archive/knowledge-graph/) — kept for the design-rationale trail, not
deleted). This document states which parts of those three proposals are adopted, and points to the
already-implemented schema rather than restating it.

## 1. Object model

Five object kinds, following the axiomatic proposal's framing:

```text
TERM
DEFINITION
ASSUMPTION
CONSTRUCTION
PROPOSITION
```

Mapped onto real files, not a hypothetical schema:

- **TERM + DEFINITION** → [`definitions/precise-definitions.md`](definitions/precise-definitions.md)
  (306 entries, arity-1: states only what a term *means*).
- **PROPOSITION** (and everything relational) → [`knowledge-graph/facts-tree.md`](knowledge-graph/facts-tree.md)
  (arity-2+: a concept connected to a target via a named relation), converted mechanically to
  [`knowledge-graph/facts-data.yaml`](knowledge-graph/facts-data.yaml). The arity test that draws this
  line is [`knowledge-graph/logic.md`](knowledge-graph/logic.md) §1.

## 2. ASSUMPTION and CONSTRUCTION — already handled, not new additions

The axiomatic proposal treats `ASSUMPTION` and `CONSTRUCTION` as object kinds distinct from
`DEFINITION`/`PROPOSITION`. Checking against the live schema before adding anything found both
already covered, under different names, by considered decisions already made in `logic.md`:

- **ASSUMPTION** is already a categorical type (`logic.md` §2a: *"a condition a construction's
  security rests on"*, e.g. `DH security assumes CDH is hard`), and every fact already carries a
  stable `id` (§4), so an assumption fact is already independently citable as a premise by other
  facts via `composite-facts.yaml`'s `premises.refs: [fact_id, ...]` (§3a case 3). No schema change
  needed — this is a naming/framing difference, not a missing capability.
- **CONSTRUCTION** was deliberately *not* split into its own fact type. `logic.md` §1's corollary:
  *"most of 'how a construction works internally' ... is arity-1 and belongs in the definition, not
  a separate fact — even though it feels 'technical.' Only promote it to a fact if it makes a claim
  connecting the concept to a genuinely separate one."* CTR's `KS_i = E_K(nonce||counter_i)` formula
  lives inside CTR's own definition; `CTR depends_on nonce_uniqueness` is the separate fact. Adding a
  `construction` categorical type now would re-litigate an already-settled call without a concrete
  example showing it's insufficient.

## 3. Relation vocabulary — kept as-is, not migrated to the minimal 5

`logic.md` §3 already has a canonical relation vocabulary: `depends_on`, `defined_from`, `is_a`,
`part_of`, `precedes`, `performed_by`, `assumes`, `implies`, `enables`, `motivates`, `condition_for`,
`satisfies`, `prevents`, `example_of`, `differs_from`, `vulnerable_to`, `best_practice`, `pitfall`,
`counterexample_of`, `equivalent_to` — about 20 named relations, populated across ~505 audited fact
edges in `facts-tree.md`.

Docs 02/03 (archived) proposed collapsing this to 5 core relations (`IS_A`, `HAS_PROPERTY`,
`DEPENDS_ON`, `IMPLIES`, `COMPARES`) plus a `kind` qualifier. The critique behind that proposal is
valid in the abstract — most of the 20 relations really are "`DEPENDS_ON`/`IMPLIES` + a specific
kind" underneath. But logic.md's named relations already **are** that pattern, pre-expanded into
self-documenting names (`best_practice`/`pitfall` is more legible on sight than
`HAS_PROPERTY(kind=best_practice)`), and the 505 edges are already collected, direction-checked, and
externally audited once. Migrating relation *names* to save qualifier bookkeeping, at the cost of
re-touching every audited edge, is not worth it without a concrete case the current vocabulary can't
express — none has come up yet.

## 4. Provenance, qualifiers, derived views — already implemented

No changes here; these are exactly what docs 01/02 asked for, already built:

- Provenance/trust (`source`, `status`, `rationale`, per-content-type source authority) — `logic.md` §2c.
- Selection fields (`functional_role`, `demonstrable`, `teaching_priority`) — `logic.md` §2d.
- One canonical source, everything else a derived projection — `facts-tree.md` is hand-edited;
  `facts-data.yaml` is generated from it and never hand-edited; the six §3c candidate pools
  (design-rationale chains, usage/pitfall pairs, tradeoffs, concrete instantiations, bare
  consequences, counterexamples) are mechanically pulled from `facts-data.yaml` — see `logic.md` §7
  and [`DOCUMENTATION.md`](DOCUMENTATION.md) for the full file list.
- N-ary conjunctive implications (`A ∧ B ⟹ C`, with `combinator: all|any` and
  `claim_mode: sufficient|necessary|equivalent`) — `logic.md` §3a, derived from real cases
  (Encrypt-then-MAC, RSA-OAEP, Bellare–Namprempre composition) the archived proposals never
  encountered.
- The named-artefact namespace split (AES/RSA aren't `precise-definitions.md` entries but must still
  be fact subjects via `example_of`) — `logic.md` §4, another real problem the archived proposals
  don't mention.

## 5. What's still open

`logic.md` itself flags the next phase: the §6 activity/task layer — turning
`demonstrable: true` + `teaching_priority: core|recommended` facts into actual exercises,
demonstrations, and assessments — is explicitly **not yet built**. That's the subject of
[`03_pedagogical_engine.md`](03_pedagogical_engine.md).
