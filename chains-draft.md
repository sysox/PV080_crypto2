# Draft chains — for review

Small, single-branch instances of the [logical-chain.md](logical-chain.md) stages, pulled from our
discussion on ciphers. Each one is meant to be checked independently — mark it, edit it, cut a stage
that's wrong or missing. Nothing here is formalized into facts yet; that happens after you've verified
these.

Status key: `[ ]` not checked yet, `[x]` you've confirmed it, or just edit the line directly.

---

### Chain 1 — encoding vs. encryption
- [ ] use case: transform data into another representation
- [ ] threat: (none assumed — no adversary in scope)
- [ ] goal: none (no confidentiality claimed)
- [ ] requirement: transform must be public and invertible by anyone
- [ ] mechanism: encoding (e.g. Base64)
- [ ] failure/consequence: none — it was never supposed to hide anything; the failure is a *developer*
      mistaking it for encryption

### Chain 2 — confidentiality needs a secret
- [ ] use case: two parties exchange data over a channel others can observe
- [ ] threat: passive eavesdropper reads ciphertext
- [ ] goal: confidentiality
- [ ] requirement: the transform must NOT be invertible without extra information the adversary lacks
      (a key)
- [ ] failure if violated: transform is public/invertible → it's encoding, not encryption, goal fails
      by definition

### Chain 3 — symmetric bootstrap problem
- [ ] use case: two parties who've never met want confidentiality, no secure channel exists yet
- [ ] threat: same passive eavesdropper as chain 2
- [ ] requirement: symmetric encryption needs a shared key already in place on both ends
- [ ] failure: no pre-existing secure channel ⇒ no way to share that key ⇒ symmetric can't get started
      (circular dependency)
- [ ] consequence: motivates a different mechanism family (chain 4)

### Chain 4 — asymmetric breaks the bootstrap
- [ ] use case: same as chain 3 (no pre-shared secret)
- [ ] requirement: need an encryption key that can be made public without helping decrypt
- [ ] mechanism: trapdoor one-way function → key pair (pk, sk); Enc_pk, Dec_sk
- [ ] implementation requirement: sk never leaves its owner; pk authentically bound to the right owner
      (flagged, not expanded — this is where certificates/PKI hook in later)
- [ ] tradeoff/consequence: solves bootstrap, but computationally expensive, bounded message size

### Chain 5 — hybrid encryption resolves the tradeoff
- [ ] use case: chain 4's cost is too high for bulk data
- [ ] requirement: get asymmetric's no-pre-shared-secret benefit without paying its cost on every byte
- [ ] mechanism: use asymmetric once to exchange a fresh symmetric session key, then symmetric for the
      actual data
- [ ] this is a merge point, not a new branch — worth marking as such rather than a sibling of 3/4

### Chain 6 — stream cipher nonce reuse
- [ ] use case: symmetric confidentiality for a stream of data
- [ ] mechanism: stream cipher — key(+nonce) → keystream, XOR with plaintext
- [ ] requirement: keystream must never repeat under the same key
- [ ] implementation requirement: nonce must be unique per key, every time, including across restarts
- [ ] failure: nonce (or key) reused ⇒ same keystream twice
- [ ] attack: XOR the two ciphertexts ⇒ get XOR of the two plaintexts ⇒ crib-dragging/frequency
      analysis recovers both

### Chain 7 — ECB pattern leakage
- [ ] use case: symmetric confidentiality for multi-block data
- [ ] mechanism: block cipher used directly, one block at a time, no mode (ECB)
- [ ] requirement: (missing) — nothing randomizes/chains blocks
- [ ] failure: identical plaintext blocks ⇒ identical ciphertext blocks
- [ ] attack/consequence: attacker sees repeated ciphertext blocks ⇒ learns plaintext has repeated
      structure (the "ECB penguin") without recovering the key

### Chain 8 — confidentiality without integrity
- [ ] use case: same channel as chain 2, but adversary is now active, not just passive
- [ ] threat: adversary can modify ciphertext in transit
- [ ] goal (new, sibling to confidentiality): integrity/authenticity
- [ ] requirement: need a way to detect tampering, separate from confidentiality
- [ ] failure if only confidentiality is in place: e.g. CTR-mode ciphertext is malleable — flipping a
      ciphertext bit flips the corresponding plaintext bit predictably, with no error
- [ ] mechanism: MAC (symmetric) or signature (asymmetric), composed with encryption
      (Encrypt-then-MAC / AEAD)

---

## Things I'm unsure about — flag if wrong

- Chain 1: is "no goal, no threat" the right way to model encoding, or should it still get a threat
  entry so it's directly comparable to chain 2 in a table later?
- Chain 4's implementation requirement (key binding) is a stub — real content is a whole separate
  certificates/PKI sub-chain, not something to expand here.
- Chain 5 is marked as a merge point rather than its own branch — agree or should it be a normal chain?
- Chain 7 has an empty "requirement" stage (nothing was required, that's the bug) — is a chain allowed
  to have a deliberately empty/missing stage to make a pedagogical point, or should that be phrased
  differently?
