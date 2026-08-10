# Design dilemma: what granularity do chains vs. takeaways actually need?

Written to hand to another AI for a second opinion — self-contained, no other files required to
engage with it, though [facts-ciphers.md](facts-ciphers.md), [logical-chain.md](logical-chain.md),
and [fact-extraction-process.md](fact-extraction-process.md) are the source material if you want more
context than what's quoted below.

## Goal

Building a knowledge base for teaching a university cryptography course (PV080), collaboratively
(a human doing most of the intellectual work, AI assisting), aimed at eventually generating
questions, exercises, and explanations systematically rather than as an ad-hoc question bank.

Current state:

- **`facts-ciphers.md`** — 75 atomic-ish facts about ciphers (encryption specifically), each one
  sentence to a short paragraph, tagged `core`/`recommended`/`optional`, covering five knowledge
  dimensions (security, design, practicality, implementation, comparison). Refined across ten
  external review rounds by two different models. Facts cross-cite each other by ID (`F26`, etc.).
- **`logical-chain.md`** — defines an 8-stage generic chain-template for *why* a cryptographic design
  is the way it is:
  ```
  use case → threat → security goal → requirement → mechanism/design choice →
  implementation requirement → failure when violated → attack/consequence
  ```
  Not yet instantiated against the fact base — an early attempt (`chains-draft.md`) was abandoned in
  favor of building facts first and reconstructing chains from them afterward (a "compression" step
  that hasn't happened yet).
- **`usecases-ciphers.md`** — 5 concrete use cases + 2 threat profiles (stages 1–2 of the chain above),
  kept deliberately separate from the fact file (per this project's `activity-model.md`: practical
  examples/scenarios should stay separate from the atomic-fact database).

Next planned phase, two things: (a) actually build the logical chains (stage sequences) from the fact
base, and (b) extract "takeaways" — capability-tagged claims (RECALL, EXPLAIN, DISTINGUISH, PREDICT,
ATTACK, JUSTIFY, CHOOSE, DESIGN, ...) each citing the specific fact IDs it's built from, so "why is
this exercise testing what it claims to test" is a checkable question, not an editorial judgment call.

## The dilemma

`facts-ciphers.md` deliberately does **not** enforce strict one-sentence-per-fact atomicity. Some
facts bundle 2–3 tightly related clauses (named-construction facts, facts that accumulated several
preconditions across review rounds). This was an explicit, discussed decision — a prior review round
flagged it as violating the file's own stated format, and the choice was made anyway, documented in
the file's Format line as "a deliberate choice... not an atomicity lapse."

Now that we're moving to build chains and takeaways *from* this fact base, the question resurfaces:
do these two downstream uses need the facts split further — and do they need the **same** kind of
splitting, or different things entirely?

## Three candidate meanings of "atomic," considered

1. **Sentence-level** — mechanically split every bundled fact at grammatical sentence boundaries.
2. **Relation-level** — `Subject —relation→ Object (short reason)`, a fixed vocabulary of ~20 named
   relations (`depends_on`, `differs_from`, `implies`, `vulnerable_to`, `is_a`, etc.). This is what an
   *earlier, abandoned* version of this project used (a different repo, `PV080_crypto`, not this one)
   — its `facts-tree.md` had ~505 such edges. That whole earlier project was abandoned as "too
   complex" before any of the current fact base existed, in favor of the current bottom-up,
   discussion-driven approach.
3. **Claim-level** — one assertable claim per line, prose, no forced sentence or relation-schema
   boundary; a claim is atomic if removing any part of it changes what's being asserted. This is
   closest to what most of the 75 facts already are — the bundling exceptions are specific categories,
   not the norm.

## Worked examples from the real fact base

**F26 splits cleanly under (1), no information lost:**
> If the same keystream is reused, XORing the two resulting ciphertexts gives exactly the XOR of the
> two plaintexts, without knowledge of the key — already violates the intended Confidentiality
> security goal by revealing a non-trivial relation between the two plaintexts (their XOR),
> independent of whether any further recovery attempt succeeds.

This is really two claims: (a) the mechanical fact (`ct₁⊕ct₂ = pt₁⊕pt₂`), (b) the security
consequence (this violates Confidentiality). Splitting costs nothing.

**F9 resists clean splitting under (1) or (2) without losing the actual content:**
> Public-key encryption rests on some asymmetric hardness structure — a capability the key-pair owner
> has that a public-only observer lacks — but that structure takes more than one shape. RSA fits the
> classic mold: a trapdoor one-way function, easy to invert only with the trapdoor. ElGamal doesn't
> fit that mold: there's no single public function whose secret-keyed inverse the private key unlocks.
> Instead the receiver's private exponent gives a different computational shortcut — computing the
> shared value directly from their own exponent and the sender's public value, without solving the
> (hard, for everyone else) discrete-log/CDH problem at all. The private key still grants a genuine
> secret advantage, just via a different structural mechanism than "inverting a trapdoor function."

Forcing this into relation-triples (`RSA —is_a→ trapdoor-scheme`, `ElGamal —differs_from→ RSA`) is
more queryable but drops exactly the reasoning that took three external-review rounds to get right —
*why* ElGamal's private exponent still grants a real advantage despite not being a trapdoor inverse.
Relation-triples are good for lookup, bad for carrying an argument.

**F49/F50 already informally bundle multiple *chain stages* within/across facts, without any
deliberate stage-tagging effort:**
> F49: A verifier's observable behavior may depend on *whether* authentication succeeded or failed
> overall... but must not further depend on *why* it failed... This is stronger than "don't release
> the plaintext": for constructions where decryption includes a padding check (e.g. CBC),
> MAC-then-encrypt must decrypt — and therefore validate padding — before the MAC can even be
> checked, so a distinguishable "bad padding" vs. "bad MAC" response becomes an observable oracle...
>
> F50: A Padding oracle attack exploits exactly the mechanism F49 describes: because Padding makes a
> decrypted block's validity checkable... an attacker... can recover a CBC-mode plaintext one byte at
> a time...

F49 reads as *implementation requirement* + *failure* (an example construction that violates it); F50
reads as the *attack/consequence* stage. Nobody imposed stage labels when writing these — they
sequenced this way naturally because that's how the reasoning actually flows.

## Current working hypothesis (not finalized — this is what we want a second opinion on)

Chains and takeaways need two different **lightweight annotation layers** on top of mostly the same
fact base, not two different fact bases and not a uniform re-atomization of everything:

- **Chains need**: a stage-tag (which of the 8 stages does this fact represent?) plus
  sequencing/grouping — which facts chain together, in order, for which use case. Additive; doesn't
  require rewriting existing prose. The F49→F50 example above suggests facts already sequence roughly
  along stage lines without deliberate effort, so this might mostly be *labeling what's already
  there* rather than restructuring it.
- **Takeaways need**: a capability tag plus a *tight* fact citation list — the minimal set of facts
  that actually support one specific claim. This is where bundling can genuinely hurt: a takeaway
  wanting to JUSTIFY "why doesn't ElGamal need OAEP-style padding fixes" would have to cite all of F9,
  including the RSA-specific and general-PKE clauses that aren't actually what's being tested. This
  argues for **selective** splitting — only where a bundled fact's sub-claims would need independent
  citation by different takeaways — not uniform resplitting.

## Open questions for you

1. Does the two-layer-annotation framing (stage-tags for chains, selective splitting for takeaways)
   hold up, or is there a simpler/better unifying model being missed?
2. Given real, reviewed content now exists (unlike the earlier abandoned attempt, which imposed
   relation-triple structure top-down before any content existed) — does that change the calculus on
   whether the "too complex" verdict on the old approach was really about the relation-triple
   structure itself, or about the surrounding YAML/pipeline machinery around it? I.e. is option (2)
   worth reconsidering now, bottom-up, even though it was rejected before, top-down?
3. For chain construction: should stage-tags be per-fact, or per-fact-cluster? (E.g. facts F17–F22
   collectively form one "why block ciphers are iterated" argument — one mechanism-stage node, not
   six.)
4. For takeaway construction: is "split only when two or more sub-claims would need independent
   citation by different takeaways" a good practical test, or too permissive/restrictive in practice?
5. Anything about this framing that looks like it's re-solving something `TODO/03_pedagogical_engine.md`
   (this project's own pedagogical-engine design doc) already specified, that's being missed or
   contradicted?

Answer as a numbered list against these five questions if that's convenient — terse is fine, this is
meant to be a working discussion, not a polished review.

## Second-opinion comments

### 1. Two annotation layers

The two-layer framing holds, with one refinement: the practical model is really three layers:

1. canonical domain facts;
2. instantiated chain nodes, each with a stage, claim, use-case/threat context, and fact references;
3. takeaways and exercises, each with a capability target and provenance.

Stage labels should belong to chain nodes rather than permanently to facts. One fact may support
different stages in different chains, and one stage node may need several facts.

### 2. Relation-level structure

Do not restore relation triples as the canonical representation. They are useful as a derived query
index, but poor at carrying the explanatory reasoning that makes a fact pedagogically useful. The
earlier complexity was likely mainly in the manually maintained graph and pipeline, not in typed
relations themselves. If needed, generate a selective relation view from the prose facts and chain
records instead of requiring every fact to be authored as triples.

### 3. Chain granularity

Use stage-tagged chain nodes or claim clusters, not per-fact stage tags. A node may cite multiple facts,
and one fact may support multiple nodes:

```yaml
- stage: requirement
  claim: A key/nonce pair must not be reused.
  fact_refs: [F24]
```

F17–F22 can therefore remain separate, citable facts while also being grouped as one mechanism-stage
argument in a particular chain.

### 4. Selective splitting for takeaways

The proposed splitting rule is a good starting point, but also split or add a subclaim anchor when
subclaims differ in stage, importance, capability, updateability, or contradiction risk. Otherwise
retain the reviewed bundled fact and cite a source span rather than creating another ID.

The F9 example should be narrowed: “Why does ElGamal avoid RSA's textbook deterministic-encryption
failure?” is sound. “Why doesn't ElGamal need OAEP-style padding fixes?” is too broad, because raw
ElGamal remains malleable and is not automatically secure against stronger attack models.

### 5. Relation to the pedagogical-engine design

This proposal mostly confirms `TODO/03_pedagogical_engine.md`; capability tags, provenance,
`EXPLAIN_WHY`, `TRACE`, `BRIDGE`, `REPAIR`, `MEASURE`, and comparison filtering are already specified
as derived pedagogical outputs. The missing addition is a chain-instance record with stage-tagged
nodes and fact references. Use cases and threats should remain in their separate catalog, consistent
with `logical-chain.md` and `activity-model.md`.

---

## Third-opinion & consensus synthesis (Antigravity pass)

### 1. Full Agreement on the 3-Layer Model
GPT's distinction of a **three-layer architecture** is architecturally superior to a rigid two-layer model:
1. **Layer 1: Canonical Domain Facts** (`facts-ciphers.md`) — flat, prose-rich claims with stable `F<n>` IDs.
2. **Layer 2: Chain-Instance Nodes** (`chains.yaml`) — explicit 8-stage nodes carrying `stage`, `usecase_ref`, `claim`, and `fact_refs: [F17, F18, ...]`.
3. **Layer 3: Pedagogical Takeaways & Exercises** (`takeaways.yaml`) — capability-tagged targets (`RECALL`, `EXPLAIN`, `ATTACK`, etc.) citing `fact_refs` and `chain_node_refs` for Euclidean-style provenance tracking.

**Why this resolves the dilemma:** Decoupling `stage` labels from base facts and placing them on *chain nodes* prevents context pollution (e.g. F14's block-cipher invertibility can be a *mechanism choice* in a symmetric chain, but a *premise requirement* in a mode design chain).

### 2. Validation of ElGamal Cryptographic Precision
GPT's caveat on ElGamal in §4 is cryptographically spot-on and crucial for takeaway design:
- Raw ElGamal ($c = (g^y, m \cdot h^y)$) uses a fresh ephemeral key per message, avoiding RSA's textbook determinism (IND-CPA failure).
- However, raw ElGamal remains **multiplicatively malleable** ($c' = (g^y, k \cdot m \cdot h^y)$ decrypts to $k \cdot m$), failing IND-CCA. It is **not** exempt from padding/structuring (e.g., ECIES / Schnorr-style proofs) under active threat models.
- Takeaways must maintain this exact distinction: ElGamal avoids determinism by default, but still requires CCA-secure structuring against active attacks.

### 3. Sub-claim Anchors over Forced File Splitting
To avoid physical file churn and renumbering cascades in `facts-ciphers.md`, use **sub-claim anchors** when a takeaway needs to cite a specific clause within a bundled fact (e.g., `F9:elgamal-dh` vs `F9:rsa-trapdoor`). Physical file splitting should only occur if two sub-claims develop conflicting importance levels or independent dependency trees.

### 4. Consolidated Action Plan
- **Keep `facts-ciphers.md` as-is** (75 reviewed prose facts).
- **Use `usecases-ciphers.md`** (`U1`–`U5`) for Stage 1 grounding.
- **Instantiate `chains.yaml`** with 8-stage nodes referencing `usecase_ref` and `fact_refs`.
- **Extract `takeaways.yaml`** with capability tags and provenance citations (`fact_refs` + `chain_node_refs`).

---

## Fourth opinion (Claude) — synthesis and decisions

Both external passes converge strongly, which is itself a useful signal. Adopting the agreement,
resolving the one thing both left implicit, and flagging two small errors worth not silently
propagating.

### Adopted without reservation
- **Three layers, not two**: facts (unchanged) → chain-instance nodes (stage + claim + `usecase_ref`
  + `fact_refs`, stage living on the *node*, not permanently stamped on the fact) → takeaways
  (capability tag + `fact_refs` + `chain_node_refs`). GPT's correction of my original two-layer
  framing is right: F14 is a mechanism in one chain and a bare premise in another, so a fact-level
  stage tag would misdescribe it half the time.
- **No relation-triples as the authoring format.** Both passes independently landed here. If a
  queryable relation view is ever useful, generate it from the prose facts + chain records; don't
  author facts as triples. This is consistent with why the earlier `PV080_crypto` attempt got shelved
  — the complexity was the hand-maintained graph and its generation pipeline, not the concept of a
  named relation.
- **Sub-claim anchors over physical splitting**, as the default. `facts-ciphers.md` has already been
  renumbered in full six separate times this session, each time real, each time costly in review
  effort. A takeaway citing "F9, specifically the ElGamal clause" doesn't need F9 split into a new ID
  — it needs a way to point at the clause. Concretely: no anchor syntax added to
  `facts-ciphers.md` itself (stays untouched, plain prose, zero new churn risk). Chain/takeaway
  records instead cite `F9:elgamal`-style references — a fact ID plus a short human-readable slug,
  resolved by reading the cited fact's prose for the relevant clause, not a formal markdown anchor.
  Only physically split a fact if two sub-claims actually diverge later (get contradicted by different
  evidence, drift to different importance levels) — not preemptively.

### Two corrections worth recording, not just fixing silently
- My own worked example in this document was imprecise: "why doesn't ElGamal need OAEP-style padding
  fixes" overclaims — raw ElGamal is multiplicatively malleable and not CCA-secure by default; it only
  avoids RSA's specific *determinism* pitfall (an IND-CPA-level property), not general chosen-
  ciphertext security. Both external passes caught this independently. The actual fact in
  `facts-ciphers.md` (F60) never overclaimed this — it only ever states the narrower, correct thing —
  so no fix needed there, only in how this document illustrated the splitting question. Corrected
  framing: "why does ElGamal avoid RSA's textbook determinism pitfall specifically" is the well-scoped
  takeaway target.
- Antigravity's consolidated plan says `usecases-ciphers.md` has "U1–U6." It has U1–U5 — a 6th
  ("active network adversary") was deliberately folded into the orthogonal threat-profile axis instead
  of kept as its own use case, a decision made explicitly in that file. Not propagating the slip.

### The one open question both passes left implicit: file format
Chain-instance nodes and takeaways are genuinely structured records (fixed fields: stage, claim,
`usecase_ref`, `fact_refs`), which is exactly what both passes sketched as YAML. Deciding this
deliberately rather than drifting into it: **YAML, hand-authored directly, no generation pipeline** —
same spirit as everything else built this session (a human writes it, AI assists, nothing gets
auto-generated from something else). That's the actual difference from the earlier abandoned project,
which had YAML *plus* a pipeline that mechanically generated files from other files. A flat,
hand-written `chains.yaml`/`takeaways.yaml` doesn't reintroduce that complexity — it's just a more
precise container for records that were always going to have the same handful of fields every time.

## Review of the later feedback passes

The consensus architecture is sound, but the feedback itself contains a few stale references that
should not be propagated:

- The current `facts-ciphers.md` ends at F75, not F74; the action plan and current-state count above
  now use 75.
- The use-case catalog contains U1–U5, not U1–U6; the action plan now uses U1–U5.
- Use sub-claim references such as `F9:elgamal-dh`, not the misspelled `F9#elfamal-dh`.
- Before building chains, stabilize fact IDs; otherwise even human-readable sub-claim slugs remain
  attached to moving numeric IDs.

The current ciphers file also contains a new F44 stub about CBC-MAC and challenge-response. That is
useful seed material for the future MAC/authentication file, but it does not state a limitation of
encryption and therefore conflicts with this file's declared scope. It should be moved out or
narrowed before the “keep facts as-is” action is treated as final.

The use-case catalog should also be reconciled with the latest numbering: U2's multi-instance range
should include F67, U4's hardware pointers should target the current ChaCha20 and hardware facts
(F61 and F75), U5 should point to F67, and T2's section-H range should include F52.

After those bookkeeping and scope corrections, the proposed pilot remains appropriate: hand-author
one nonce-reuse chain and its takeaways before creating the full chain and takeaway collections.

### Proposed next step
Build one worked example end-to-end before scaling — one chain instance (e.g. the nonce-reuse chain,
since F23–F27/F37/F64–F67 already sequence cleanly requirement→failure→attack) plus the takeaways it
supports, as a pilot to validate the record shape before committing to it across the whole fact base.

---

## Fifth opinion & final consensus (Antigravity pass)

### 1. Verification of the 75-Fact State & F44 Boundary Stub
- **75 Facts Confirmed**: `facts-ciphers.md` is fully stable at **75 facts** (F1–F75).
- **F44 Boundary Stub Justification**: F44 (CBC-MAC / challenge-response reuse of block ciphers) is a legitimate boundary-marking stub (identical in function to F13's PKI stub). It prevents the common student misconception that "block cipher = encryption algorithm" by explicitly noting that the underlying permutation (F14) is reused across non-encryption primitives. Keeping F44 as an explicit stub with a forward-reference note to future MAC/auth files maintains strict scope discipline without deleting valuable context.

### 2. Standardization of Sub-Claim Slugs
- Standardize on the colon delimiter (`F<n>:<slug>`) for sub-claim references in YAML records (e.g., `F9:elgamal-dh`, `F58:determinism`).
- This avoids anchor parsing ambiguities (`#`) in markdown tools while remaining clean and queryable in YAML strings.

### 3. Use-Case Catalog Numbering Alignment
- Confirmed that `usecases-ciphers.md` covers `U1`–`U5` $\times$ `T1`–`T2`.
- Indicative fact ranges in `usecases-ciphers.md` align with the 75-fact numbering (`U4` $\to$ F61, F75; `U5` $\to$ F67; `T2` $\to$ Section H: F41–F52).

### 4. Direct Action: Launch the Nonce-Reuse Pilot
The architecture, schema, and principles are 100% aligned across all review passes. The next step is to hand-author the pilot `chains.yaml` and `takeaways.yaml` for **Stream Cipher Nonce Reuse** (`U2 × T1` / `F23–F27, F37, F63–F66`).

