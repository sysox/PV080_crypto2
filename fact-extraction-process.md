# Fact-extraction process

How [`facts-ciphers.md`](facts-ciphers.md) actually got built, not how it was originally planned to
be built — the plan was "facts first, chains later" (see [`logical-chain.md`](logical-chain.md)'s open
question); what actually worked was several rounds of draft → external review → fix, and the review
rounds caught the same *kinds* of problems repeatedly. This document is that pattern, written down so
the next domain (hash functions, MAC, signatures, key agreement, ...) can either follow it directly or
skip straight to the checklist below instead of rediscovering it by trial and error.

## 1. The pipeline, as it actually happened

1. **Confirm what's already defined.** Check `definitions/pv080-definitions.md` (or
   `precise-definitions.md`) for every term the domain touches before writing a single fact. Facts add
   *relations between* terms, never redefine them. (Caught early: the domain had far more coverage
   already than expected — block cipher, stream cipher, trapdoor one-way function, confusion/diffusion
   were all already precisely defined before any fact-writing started.)
2. **Draft atomic facts from discussion**, one true sentence each, loosely grouped by topic, tagged
   `core`/`recommended`/`optional` (reusing `activity-model.md`'s existing importance scale rather than
   inventing a new one). Cite fact IDs when one fact depends on another, so dependency is traceable, not
   just implied by ordering.
3. **External review, repeated until it stops finding new categories of problem.** Four rounds here
   (see §2 for the prompt, §3 for what each round actually caught). Rounds 2–3 trended toward
   precision/qualification rather than new gaps — but round 4 broke that trend and found genuine
   factual errors (RSA's hardness misattributed to factoring rather than the RSA problem; ElGamal's
   confidentiality misattributed to CDH rather than DDH; DES's weakness misattributed to key
   unpredictability rather than keyspace size; a numerically wrong key-size comparison) plus a real
   missing fact (stream-cipher keystream pseudorandomness, distinct from nonce uniqueness). **Don't
   assume review has converged just because the last round or two trended toward precision-only —
   check every round on its own merits; a later round can still surface a first-order correctness bug
   a domain expert would catch immediately, especially around named concrete constructions where exact
   claims (which hard problem, which numbers) are easy to get subtly wrong even when the general shape
   of the fact is right.**
4. **Comparisons pass**, once the base facts are stable: explicitly look for terms close enough in
   meaning or surface shape that students conflate them, and for each pair/trio, state the *one
   dimension* that actually distinguishes them — not "they're different." (`/home/sysox/Projects/
   PV080_crypto/knowledge-graph/facts-tree.md`, an earlier and more complex version of this project,
   turned out to have well-reasoned `differs_from` entries worth reusing as a style reference even
   though its surrounding YAML/hypergraph pipeline was abandoned as overbuilt.)
5. **Concrete/named-instance pass**, with an explicit scope check per candidate: does this named thing
   actually belong to the domain being written (ciphers), or does it belong to a neighboring domain
   that hasn't been started yet (DH/DSA/ECDSA → key agreement/signatures, deliberately excluded)?
6. **Not yet done for this domain:** takeaways (capability-tagged claims about what a student should be
   able to *do*, cited to fact IDs) and pedagogical task chains per takeaway. Facts, comparisons, and
   named instances were judged a stable enough base to stop and document process before continuing.

## 2. The external-review prompt (reusable template)

Ask a second model (or a second pass of the same one, cold) to audit a facts file against four fixed
questions, with the domain's deliberate scope exclusions stated up front so the reviewer doesn't flag
intentionally-deferred content as a gap:

```
Audit ONLY for:
1. Missing concepts/facts: within the stated scope, what's simply absent that a student would
   need before the next layer makes sense?
2. Missing logical links: are there two facts that each assume something true which is never
   itself stated as a fact?
3. Broken/skipped reasoning: any fact that jumps a step, or overclaims/underclaims relative to
   what's actually true?
4. Structural issues: is the section grouping logically sound, or should anything move/merge/split?
```

Keep the scope-exclusion note explicit and specific each time (e.g. "concrete named algorithms aren't
added yet, don't flag their absence" / "DH/DSA/ECDSA are out of scope, this file is encryption only") —
without it, review rounds waste turns re-litigating already-made scope decisions instead of finding new
problems.

## 3. Checklist of problems actually caught — watch for these proactively next time

Grouped by kind, each with the concrete instance from the ciphers pass as a worked example, so this
reads as "what to check for" rather than an abstract warning.

**Overclaiming / absolute vs. computational**
- "Not invertible" stated where "computationally infeasible to invert" was meant (F1→F2 fix) —
  confusing information-theoretic and computational security by accident.
- "Possible only when X exists" stated where "commonly built from X, not the only foundation" was true
  (F9) — necessary-vs-only-known-sufficient-condition confusion.
- "Regardless of the schemes combined" stated where "given these stated assumptions" was the actual
  claim (F44→F46) — a conditional result presented as unconditional.

**Missing foundational facts before derived reasoning**
- Jumped straight to "why block ciphers are iterated" (a fairly deep why-chain) without first stating
  that a block cipher is an invertible keyed permutation at all. A new foundations section had to be
  inserted *before* the existing "why iterate" section, not appended after.

**An entire knowledge dimension absent, not just one fact**
- Practicality (throughput, latency, memory, parallelism, overhead — the vision doc's own §5 table) was
  essentially unrepresented after the first full drafting pass, because the discussion that produced
  the facts was security/design-flavored throughout and practicality never came up naturally. Check
  coverage against the full dimension table explicitly, don't rely on the drafting conversation to
  surface every dimension on its own.

**Implicit premises a fact silently depends on**
- A fact claimed a composition was safe (Encrypt-then-MAC) without stating the preconditions doing the
  actual work: independent keys, verify-before-release ordering, an unforgeable MAC, no side channels.
  Each precondition that was pulling real weight got its own fact (or an explicit qualifying clause);
  the alternative — an unbounded regress of ever-more-specific preconditions — was avoided by folding
  minor ones into the dependent fact's own wording instead of minting a new ID for every single one.

**Terminology precision**
- ECB described as "no mode" when it's actually a degenerate mode of operation — a real terminological
  inconsistency, not just a style nitpick, since "requires a mode" (true) and "ECB has no mode" (false)
  would otherwise directly contradict each other in the same file.

**Apparent internal contradictions between adjacent facts**
- One fact said tamper detection needs "a separate mechanism"; the next fact introduced AEAD as an
  *integrated* mechanism. Not actually contradictory, but read as one on a fast pass — fixed by having
  the first fact explicitly forward-reference the integrated alternative rather than leaving "separate"
  unqualified.

**Scope drift, both directions**
- Content that belongs to a neighboring domain sneaking in because it's needed to state a limitation of
  the current domain (MAC/signature facts in a ciphers file, needed to explain "confidentiality doesn't
  imply integrity") — kept deliberately, flagged explicitly, rather than either silently left in or
  reflexively cut.
- Named concrete algorithms (RSA, AES, ECC) appearing as one-word illustrative examples inside generic
  facts *before* the dedicated concrete-instance layer officially existed — an external review flagged
  this as scope creep; judged worth keeping anyway (a concrete example makes a fact easier to verify)
  but the judgment call itself got written down in the Flags section rather than silently overridden.
- The file re-violated a scope rule it had already written down for itself: the Flags section stated
  "MAC/signature facts appear only where needed to state a limitation of encryption alone," but two
  later-added comparison facts (MAC vs. signature, keyed hash vs. MAC) compared properties *within*
  the MAC/signature family rather than stating a limitation of encryption — drift back into scope
  already fixed once, not new scope creep. Worth periodically re-checking new facts against rules the
  file already states for itself, not just against the domain boundary in the abstract.

## 4. Editorial judgment calls worth carrying forward (not obviously right/wrong, but decided)

- Keep single-word illustrative named-algorithm mentions inside generic facts, even before those
  algorithms get their own dedicated facts — verifiability for the human reviewer outweighs strict
  layering purity.
- When a fact accumulates many preconditions across review rounds, fold minor ones into that fact's own
  wording rather than minting a new fact ID per precondition — reserve new IDs for preconditions that
  are themselves reusable claims other facts might also cite.
- When restructuring requires inserting a section before existing content, renumber the whole file
  rather than leaving gaps or using sub-numbering (`D2`-style) — a flagged awkwardness the first time,
  fixed by renumbering the second time.
- Deliberately stub out adjacent-domain concerns with a one-line note plus "(Stub: full treatment
  belongs to a [future file], not expanded here)" rather than either fully expanding them inline or
  omitting them silently — keeps the current file honest about what it's not covering, without turning
  it into scope creep.

## 5. Open question for reuse in other domains

This process assumed a domain (ciphers) with unusually thorough existing definitions already in place.
A domain with thinner existing definitions might need a definitions-gap-filling pass *before* step 1
of §1, rather than being able to assume "every term already exists, only relations are missing." Worth
checking explicitly at the start of the next domain rather than assuming this pipeline transfers
unchanged.
