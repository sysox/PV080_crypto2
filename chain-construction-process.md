# Chain-construction process

Companion to [fact-extraction-process.md](fact-extraction-process.md), for the next layer: building
[chains.yaml](chains.yaml) and [takeaways.yaml](takeaways.yaml) from `facts-ciphers.md`'s facts and
`usecases-ciphers.md`'s use cases/threats. Same purpose — a checklist to run *before* calling a chain
or takeaway done, built from what two review rounds (across 4 chains, 14 takeaways) actually caught,
so the next batch of chains gets checked against these up front instead of finding the same categories
again one at a time.

## 1. Branching that hides an implicit condition or alternative

**The pattern:** a node's claim mentions two or more options ("a persistent counter, or a randomly
sampled value"; "either a dedicated AEAD construction, or by hand"), but only *one* of them actually
gets modeled forward into `leads_to`. The other option silently becomes a dead end that looks, to a
reader, like it just wasn't considered — or worse, like the chain is claiming something about it that
it never actually modeled.

- Caught in `nonce-reuse`: `impl_requirement` allowed counter-based *or* random-nonce strategies, but
  all three downstream failure nodes were counter-specific. Fixed by rewording the node's claim to
  explicitly scope it to the counter branch and note (without modeling) that random nonces have a
  different failure profile elsewhere (F69/F70).
- Caught in `composition-integrity`: one `mechanism` node cited both AEAD and manual composition, but
  only manual composition's failures were traced forward — AEAD was mentioned, then silently abandoned.
  Fixed by splitting into `mechanism_aead` (its own terminal, safe node) and `mechanism_manual` (leads
  into the three-ordering branch).

**Check for every node whose claim contains "or," "either/or," "alternatively," or names more than one
option**: is every named option actually modeled as its own branch (even a one-node terminal branch
for a safe option), or is the scoping to *one* option stated explicitly? Don't let a claim gesture at
an alternative without either modeling it or disclaiming it.

## 2. Context (use case / threat) that shifts mid-chain, stated only in prose

**The pattern:** a chain declares one `usecase_ref`/`threat_ref` at the top, but a specific node's
actual context differs — and that difference only shows up as a clause in the node's `claim` text, not
in the schema. The schema has fields for exactly this (`usecase_ref`/`threat_ref` overrides at the
node level); using prose instead means nothing downstream (a takeaway, a query, another AI reading the
file) can actually detect the shift without parsing free text.

- Caught in `nonce-reuse`: `failure_multi_instance`'s claim said "this is where U5 becomes relevant
  rather than U2" — true, but only in prose. Fixed with a node-level `usecase_ref: U5` override.
- Caught in `rsa-determinism`: the equality-testing branch only needs passive observation (T1, the
  chain default), but the malleability branch needs an active capability (submit a transformed
  ciphertext for processing) — a different threat entirely. Fixed with a node-level `threat_ref: T2`
  override, which also required adding `threat_ref` as a documented override field (it existed for
  `usecase_ref` already but hadn't been needed for `threat_ref` until this case).

**Check for every node's claim text**: does it name a use case or threat capability that differs from
the chain's declared default? If so, that's a missing structural override, not just descriptive prose.

## 3. Unstated assumptions a node silently relies on

Same failure mode as `fact-extraction-process.md` §3's "implicit premises," one layer up — a chain
node can silently assume a fact's precondition without citing it.

- Caught in `nonce-reuse`: the `requirement` node cited only F24 (uniqueness), but a downstream fact
  (F63/RC4) needs F25 (pseudorandomness) too — the chain implicitly assumed a properly pseudorandom
  generator without ever stating it. Fixed by citing F25 alongside F24 and adding an explicit
  assumption clause: *this chain isolates the uniqueness failure mode; a weak generator is a different
  chain, not this one.*

**Check**: for every node that eventually gets cited by a downstream fact or takeaway, does the chain
actually state every precondition that fact depends on, or does it silently borrow one from outside the
chain's own citations?

## 4. Citation/provenance precision

Two distinct sub-issues, both about `fact_refs`/`chain_node_refs` not doing useful work:

- **Redundant citation.** A takeaway cited a fact directly (`fact_refs: [F67]`) that was already
  supplied through a `chain_node_refs` entry pointing at the node that cites it. Adds no provenance,
  just clutter — and risks drifting out of sync with the node's own citations over time. **Check**:
  before adding a direct `fact_refs` entry to a takeaway, confirm it isn't already reachable through
  a cited chain node.
- **Stale pointers after renumbering.** `usecases-ciphers.md` was written before `facts-ciphers.md`'s
  F44 insertion shifted every later fact ID by one. Four spots were caught by review; a full sweep
  found the file's *other* fact-ID mentions were still correct, but only checking would confirm that,
  not assuming it. **Check after any `facts-ciphers.md` renumbering**: grep every other file
  (`usecases-ciphers.md`, `chains.yaml`, `takeaways.yaml`, this file) for `F\d+` and re-verify each one
  resolves to the fact it's supposed to — don't assume a partial fix (the four flagged spots) means the
  rest of the file is clean.

## 5. Takeaway prompt precision — claim strength and grounding

Three variants of the same root issue: a takeaway's plain-English `claim`/`prompt_sketch` drifting
looser or stronger than what the cited facts actually support, or than what's needed for the exercise
to be well-defined.

- **Overstated claim strength.** A takeaway framed MAC-then-encrypt and Encrypt-and-MAC as flatly
  "unsafe" — the underlying fact (F51) only claims Encrypt-then-MAC is generically robust *under
  stated assumptions*, not that the other two are broken in all circumstances. Fixed by reframing to
  "not generically robust under the same minimal assumptions" and asking what specific risk each
  introduces, rather than asserting they're simply wrong.
- **Missing concrete grounding.** A PREDICT-capability prompt about ECB-encrypting an image didn't
  specify header handling, block alignment, or padding — real ambiguities that would make the exercise
  ungradable as written, not just under-specified prose.
- **Missing scope boundary.** A DEBUG-capability prompt didn't say whether the expected fix was
  confidentiality-only or full authenticated encryption, risking the student (or a grader) reasonably
  bringing in a different chain's content (MAC/AEAD) when the exercise was actually scoped narrower.

**Check every `prompt_sketch`**: does its claim strength match exactly what the cited facts assert (not
stronger, not vaguer)? Does it specify enough concrete detail that two different people would produce
the same expected answer? Is its scope boundary explicit if a plausible reader could reach for content
from a different chain?

## 6. What's *not* yet been an issue, worth watching for anyway

Categories from `fact-extraction-process.md` that generalize to this layer but haven't shown up yet in
only 4 chains / 14 takeaways — worth checking proactively on the next batch rather than waiting to
rediscover them:

- **An entire capability or stage type systematically absent.** `fact-extraction-process.md` §3 found
  Practicality entirely missing from an early facts pass. The chain/takeaway equivalent: after the next
  batch, check capability coverage (currently ATTACK×3, JUSTIFY×2, PREDICT×2, DEBUG×2, DISTINGUISH×2,
  DESIGN×1, CHOOSE×1, APPLY×1 — RECALL, TRACE, EXPLAIN, and IMPLEMENT have zero takeaways so far) and
  stage coverage (every chain so far ends at `attack` — none has modeled a `use_case`/`threat` node
  explicitly, since those live in `usecases-ciphers.md` by design, but also none has needed more than
  one `security_goal` node per chain; worth checking whether that's a real pattern or just small-sample
  coincidence once more chains exist).
- **Scope drift back into a boundary already fixed once**, the same pattern `fact-extraction-process.md`
  §3 caught for MAC/signature facts creeping into `facts-ciphers.md`'s comparisons section. Watch for
  a future chain quietly pulling in DH/DSA/ECDSA/certificate content that was deliberately deferred to
  a future file.
