# Use cases — ciphers

Stage-1 ("use case") and stage-2 ("threat") instances from
[logical-chain.md](logical-chain.md), for the cipher domain. Kept deliberately separate from
[facts-ciphers.md](facts-ciphers.md) — per [activity-model.md](activity-model.md): "the practical
example itself should remain separate from the atom database." Use cases are scenarios, not facts;
they don't get an F-id, and this file adds no new facts.

Five use cases, each broad enough to motivate a real cluster of facts rather than one narrow scenario.
Two threat profiles, kept **orthogonal** to the use cases rather than folded into them — a use case is
"who wants what, under which constraints"; a threat is "what an adversary can do," and the same threat
can apply across several different use cases (e.g. an active adversary threatens both U1 and U5, for
different reasons). Any use case can in principle combine with either threat profile; not every
combination is equally interesting pedagogically (noted per use case below).

Fact-ID mapping here is indicative, not exhaustive — precise citations belong to whatever takeaway or
task chain actually gets built from a use case, not to this catalog. Section letters (referring to
[facts-ciphers.md](facts-ciphers.md)) are given as pointers to *where to look*, not a claim that every
fact in that section applies.

---

## Use cases

- **U1 — First contact over an untrusted network, no pre-shared key.**
  Two parties who have never communicated before, with no secure channel and no way to exchange a
  secret in advance, want to communicate confidentially. This is the scenario that makes the
  symmetric/asymmetric split (section B) non-optional rather than a design preference — F7's bootstrap
  circularity is *this* use case's actual obstacle, and F8–F12 are the resolution.

- **U2 — Repeated communication between parties who already share a key.**
  Two parties who *do* already have a shared secret (from U1's resolution, an offline exchange, or
  whatever) exchange many messages over time, under the same key. This is where nonce/IV management
  actually starts to matter (sections E, F, G, K) — U1 only needs to establish the key once; U2 is
  where reuse/wraparound/multi-instance failures (F24, F37, F64–F66) become live risks, because now
  there's a *stream* of messages under one key rather than a single exchange.

- **U3 — Data at rest under a long-lived key, no live network protocol.**
  A file, a disk volume, or a database field is encrypted under a key that may live far longer than
  any single session, and decrypted much later, possibly by a different process entirely. No
  real-time negotiation exists to fall back on. Relevant to mode-of-operation choice (section G) and
  the birthday-bound data-volume limit under one key (F38) — "how much can I encrypt under this key
  before it's a problem" is a genuinely different question here than in U2's session-oriented framing.

- **U4 — Constrained device or bandwidth-limited deployment.**
  An embedded/IoT device, a mobile platform, or a link with real bandwidth limits needs confidentiality
  but can't spend what a general-purpose server can on compute, memory, or ciphertext overhead. This is
  the use case section L (Practicality) exists for — throughput, key size, ciphertext expansion, and
  the AES-NI-vs-ChaCha20 hardware-dependence fact (F60, F74) only matter *because* of a use case like
  this one; on an unconstrained server none of it is a real decision.

- **U5 — Horizontally-scaled service where multiple instances share one key.**
  Replicas behind a load balancer, forked worker processes, or cloned/restored container snapshots all
  hold the same key and may independently need to encrypt. This is the use case F66 was silently
  assuming without ever stating it — the whole point of that fact (nonce uniqueness *across instances*,
  not just across time) only exists because of this specific deployment shape.

## Threat profiles

- **T1 — Passive eavesdropper.** Observes ciphertext, nothing else. The minimum threat needed to
  motivate confidentiality (F2) at all; relevant to every use case above, since "someone might just be
  reading this" is always in scope.
- **T2 — Active network adversary.** Can inject, alter, replay, reorder, or truncate messages, not just
  read them. This is what makes section H (confidentiality-vs-integrity, MAC, AEAD, replay/freshness,
  F41–F51) necessary rather than optional — under T1 alone, confidentiality-only encryption is
  sufficient; T2 is the threat that breaks that sufficiency.

Interesting combinations: U1×T1 and U1×T2 are both worth building exercises around (T2 adds F13's MITM
concern on top of U1's bootstrap problem). U2/U3/U5×T1 are the natural home for most of sections E–G
and K. Any use case ×T2 pulls in section H regardless of which use case it is — T2's consequences don't
really depend on which use case introduced the channel.

---

## Open items

- Not yet cross-checked against [chains-draft.md](chains-draft.md)'s early per-chain "use case" lines
  — those were written before this catalog existed and may not align cleanly with U1–U5.
- No use case here is specific to public-key-only scenarios beyond U1 (e.g. long-term public-key
  storage/rotation) — may need a U6 once the future certificates/PKI file (flagged in
  facts-ciphers.md's Flags section) exists, if it turns out to need its own use case rather than
  reusing U1.
