# Facts — ciphers

Atomic, flat facts about cipher-related terms, pulled from the cipher discussion and nine external
review passes. No forced chain/stage structure — see [logical-chain.md](logical-chain.md) for that
layer, which chains get reconstructed from these afterward once enough facts exist and repetition
across them becomes visible (that's the compression step we agreed on).

Every **bold term** below is already precisely defined in
[`definitions/pv080-definitions.md`](definitions/pv080-definitions.md) — this file adds no new
definitions, only relations between them. Terms in *italics* aren't defined anywhere yet; flagged at
the bottom. Section J gives named constructions (AES, RSA, ElGamal, ChaCha20, DES, RC4) their own
facts as concrete instances of the general concepts above — scoped to actual ciphers only; DH, DSA,
and ECDSA are key-agreement/signature primitives, not encryption, and are deliberately left for a
later file (see Flags).

Format: `id (importance) — statement`, importance from `activity-model.md`'s `core`/`recommended`/
`optional` scale. "Statement" is usually one atomic sentence, but a named-construction fact (section
J) or a fact that's accumulated several tightly-related preconditions across review rounds may bundle
2–3 clauses into one fact rather than fragment into several new IDs — a deliberate choice (see
`fact-extraction-process.md` §4), not an atomicity lapse.

---

## A. Foundations: encryption, decryption, and the need for a secret

- **F1** (core) — **Encryption algorithm** and **Decryption algorithm** are inverse operations for the
  intended recipient: `Dec(k, Enc(k, pt)) = pt` for symmetric schemes, or `Dec(sk, Enc(pk, pt)) = pt`
  for asymmetric schemes.
- **F2** (core) — **Confidentiality** requires that recovering the plaintext from the ciphertext,
  without the relevant decryption key (the secret key for symmetric schemes, the private key for
  asymmetric schemes — a public key is intentionally available to everyone), be computationally
  infeasible for an adversary (or genuinely impossible, for **Information-theoretic security**) — not
  merely publicly unknown or inconvenient.
- **F3** (core) — A plain **Encoding** fails F2 outright: it is a public, invertible mapping by
  design, which is exactly why encoding is not encryption. (Meeting F2 is necessary but not
  sufficient for a full security guarantee — e.g. semantic security needs more than this alone.)
- **F4** (core) — Assuming **Kerckhoffs's principle** (the algorithm itself is public), if there is no
  secret key, the intended recipient has no decryption advantage over an eavesdropper with the same
  **Ciphertext-only capability** — both can run the identical public algorithm on the same ciphertext.
- **F5** (core) — Even when a secret key exists, security requires the key be unpredictable (drawn
  uniformly from a sufficiently large **Keyspace**) and kept secret; a short or predictable **Key**
  permits **Exhaustive key search (brute-force attack)** regardless of how strong the algorithm is
  otherwise.

## B. Symmetric vs. asymmetric

- **F6** (core) — **Symmetric encryption** requires both parties to already share the same secret
  **Key** before secure communication can start.
- **F7** (core) — Establishing a shared **Key** between parties with no prior contact and no existing
  **Secure channel** is circular: transmitting the key securely already requires a secure channel.
- **F8** (core) — **Public-key encryption** breaks this circularity: the **Public key** can be sent
  over an insecure channel without helping an eavesdropper decrypt — though this benefit assumes the
  public key is authentically bound to its owner (F13); an unauthenticated public key can simply be
  substituted by an active adversary.
- **F9** (core) — Public-key encryption rests on some asymmetric hardness structure — a capability the
  key-pair owner has that a public-only observer lacks — but that structure takes more than one shape.
  RSA fits the classic mold: a **Trapdoor one-way function**, easy to invert only with the trapdoor.
  ElGamal (F59) doesn't fit that mold: there's no single public function whose secret-keyed inverse
  the private key unlocks. Instead the receiver's private exponent gives a different computational
  shortcut — computing the shared value directly from their own exponent and the sender's public
  value, without solving the (hard, for everyone else) discrete-log/CDH problem at all. The private
  key still grants a genuine secret advantage, just via a different structural mechanism than
  "inverting a trapdoor function." Not every public-key encryption
  scheme is a trapdoor one-way function in disguise; trapdoor functions are the standard foundation
  for RSA-style schemes specifically, not for public-key encryption in general.
- **F10** (recommended) — Symmetric encryption needs no trapdoor/algebraic structure — a sufficiently
  unpredictable **Keystream** generator or **Block cipher** can form its core — which is why symmetric
  primitives can be built from simpler, faster operations than public-key primitives. A bare block
  cipher alone does not constitute secure encryption of an arbitrary message, though: it also needs a
  correct **Mode of operation** and nonce/IV handling (F15, F36) — the primitive is necessary, not
  sufficient.
- **F11** (core) — For known public-key encryption constructions (e.g. RSA), public-key operations are
  computationally far more expensive than symmetric ones and typically bounded in message size — an
  empirical property of current constructions, not a mathematical necessity of the general
  definition — which motivates **Hybrid encryption**. (Elliptic-curve cryptography (ECC) is a family
  of underlying mathematical primitives used to *build* such schemes, e.g. key agreement or signature
  constructions — it is not itself an encryption scheme.)
- **F12** (core) — **Hybrid encryption** uses public-key encryption once, to transport a symmetric
  session key, then symmetric encryption for the actual data — combining public-key's
  no-pre-shared-secret benefit with symmetric's speed.
- **F13** (core) — A **Public key** must itself be authentically bound to its owner. If an active
  adversary can substitute a different public key without detection, they can perform a
  **Man-in-the-middle attack** — defeating confidentiality despite the encryption mechanism itself
  being secure. (Stub: full treatment belongs to a certificates/PKI chain, not expanded here.)

## C. Block cipher foundations

- **F14** (core) — A **Block cipher** is a keyed permutation on fixed-size blocks: for each key,
  encryption is a bijective — hence invertible — map from blocks to blocks of the same size. This
  invertibility is what makes decryption possible at all.
- **F15** (core) — Because a block cipher only defines a mapping for one block, using it on any
  longer message requires deciding how to handle multiple blocks — exactly the gap a **Mode of
  operation** fills (section G).
- **F16** (core) — Separately, most messages don't divide evenly into whole blocks: encrypting a
  message that isn't an exact multiple of the block size additionally requires **Padding**,
  **Ciphertext stealing**, or another explicit length-handling mechanism for the final partial block —
  a distinct problem from the multi-block handling in F15.

## D. Why block ciphers are iterated constructions

- **F17** (core) — A uniformly random permutation over n-bit blocks has no compact description in
  general (~`n·2ⁿ` bits), so a short **Key** cannot directly select one from the full space of
  permutations.
- **F18** (core) — A **Block cipher** must be efficiently computable from a short key while still
  being indistinguishable from a random permutation to anyone without the key — a direct tension with
  F17.
- **F19** (core) — That tension is resolved not by trying to *be* a random permutation, but by
  iterating a simple keyed **Round function** many times (each application a **Round**). Iteration
  alone isn't sufficient: the **Key schedule** and round function together must avoid exploitable
  regularity (e.g. too much self-similarity between rounds enables slide-style attacks) and must
  accumulate enough **Non-linearity** and **Diffusion** — though round keys need not all be fully
  independent of one another to achieve this.
- **F20** (recommended) — A single round, while normally designed to be invertible (necessary for the
  overall cipher to be invertible at all), typically doesn't yet provide adequate security alone —
  insufficient **Confusion** and **Diffusion** only accumulate once many rounds are composed.
- **F21** (recommended) — Too few rounds, or a round function with insufficient **Non-linearity**,
  leaves statistical structure intact, which differential/linear cryptanalysis can exploit (e.g.
  reduced-round AES is broken this way even though full AES is not).
- **F22** (recommended) — Block cipher designs generally lack a reduction to a hard problem the way
  many public-key schemes do (F9): many, but not all, public-key schemes are proven secure via a
  reduction to a stated hardness assumption, and even then the reduction doesn't make the scheme
  unconditionally secure — it only shifts trust onto the assumption and the reduction's own
  correctness. Block ciphers instead rely on an empirical claim: surviving public cryptanalysis over
  time.

## E. Stream ciphers and keystream reuse

- **F23** (core) — A **Stream cipher** combines plaintext with a **Keystream** (generated from the key
  and, typically, a **Nonce**) one unit at a time via **Exclusive OR (XOR)**; the keystream is
  generated to match the plaintext's length, and decryption applies the identical XOR operation with
  the same keystream, since XOR is its own inverse.
- **F24** (core) — For a **Synchronous stream cipher**, the keystream depends only on the key and
  nonce, so it must never repeat under the same key: reusing a (key, nonce) pair reproduces the same
  keystream for two different plaintexts.
- **F25** (core) — A secure stream cipher's **Keystream** must additionally be computationally
  indistinguishable from a truly random sequence to anyone without the key. F24's uniqueness
  requirement is necessary but not sufficient for this — a keystream generator can satisfy F24 (never
  repeating under the same key) while still being statistically distinguishable from random.
- **F26** (core) — If the same keystream is reused, XORing the two resulting ciphertexts gives exactly
  the XOR of the two plaintexts, without knowledge of the key — already violates the intended
  **Confidentiality** security goal by revealing a non-trivial relation between the two plaintexts
  (their XOR), independent of whether any further recovery attempt succeeds.
- **F27** (recommended) — The XOR-of-plaintexts from F26 can further allow an attacker to fully
  recover both plaintexts via **Crib-dragging** or **Frequency analysis**, given enough structure in
  the underlying data — full recovery isn't guaranteed, though F26 alone already broke confidentiality
  regardless of whether it succeeds.

## F. One-time pad — the ideal/limiting case

- **F28** (core) — **One-time pad** is the extreme case of a **Stream cipher**: the **Keystream**
  equals a truly random key, at least as long as the message, used exactly once.
- **F29** (core) — Used correctly, One-time pad achieves **Perfect secrecy** — the ciphertext is
  statistically independent of the plaintext, holding even against an adversary with unlimited
  computational power (**Information-theoretic security**).
- **F30** (core) — F29's perfect-secrecy guarantee covers plaintext *content* for a fixed, known
  length; the ciphertext is the same length as the plaintext, so OTP (and stream ciphers generally)
  does not hide message length unless a separate mechanism (e.g. padding to a fixed length) is added.
- **F31** (recommended) — OTP and unauthenticated stream ciphers generally provide confidentiality
  only. They inherit the same **Malleability** as other unauthenticated XOR-based constructions (F42):
  flipping a ciphertext bit flips the corresponding plaintext bit predictably, with no built-in
  integrity check.
- **F32** (core) — One-time pad's perfect secrecy relies on F24's requirement in its strictest form:
  the keystream (= the key itself) must never repeat. Reusing it collapses directly to the F26 attack
  — the classic "two-time pad" break.
- **F33** (recommended) — One-time pad's key must be truly random and as long as the entire message,
  which pushes the original key-distribution problem down to every bit of plaintext — this is why OTP
  is information-theoretically perfect but not practical at scale.
- **F34** (recommended) — Practical stream ciphers replace OTP's truly random keystream with one
  expanded from a short key via a **PRNG**/**CSPRNG**, trading perfect/information-theoretic secrecy
  for computational security in exchange for practical key distribution — the expanded keystream must
  still satisfy F25's pseudorandomness requirement; a PRNG/CSPRNG is exactly what's meant to provide
  that, and RC4 (F62) is the case where the generator falls short of it.

## G. Modes of operation and ECB

- **F35** (core) — A **Mode of operation** is a public procedure for using a **Block cipher** on
  messages longer than one block, typically introducing an IV, nonce, or counter so that repeated or
  related plaintext blocks don't produce identical or trivially related ciphertext.
- **F36** (core) — IV/nonce inputs are generally not secret — they can be sent in the clear — but
  whether a mode requires them to be merely unique or additionally unpredictable depends on the
  specific mode (e.g. CTR needs a non-repeating counter start; CBC needs an unpredictable IV).
- **F37** (core) — Violating a mode's IV/nonce requirement (F36) causes concrete failures analogous to
  stream-cipher keystream reuse: reusing a CTR nonce reproduces the same keystream, collapsing exactly
  to the F26/F27 attack; using a predictable IV in CBC can let an adversary distinguish encryptions of
  chosen plaintexts — a break of the mode, not of the underlying block cipher itself.
- **F38** (recommended) — In CBC and other modes where a block cipher's input is chained from the
  previous ciphertext (rather than a monotonically incrementing counter), encrypting enough data under
  one key risks a birthday-bound *coincidental* collision among block-cipher inputs: after roughly
  `2^(n/2)` blocks for an n-bit block size, two chained inputs are likely to coincide by chance even
  with perfectly managed IVs. Because a block cipher is a permutation (F14), equal outputs mean equal
  inputs, so an attacker who observes a ciphertext-block collision can deduce a relation between the
  two corresponding plaintext blocks from values they can already see. This is a real practical
  concern for small block sizes (DES's 64-bit blocks, F61, give a birthday bound around `2^32` blocks)
  and essentially irrelevant for AES's 128-bit blocks (`2^64`) — the mechanism behind the real-world
  Sweet32 attack. **CTR mode is not at risk this way**: its block-cipher input is the counter itself,
  so as long as the counter doesn't repeat (F64), F14's permutation property *deterministically*
  guarantees distinct inputs produce distinct outputs — no coincidental collision is possible at all.
  CTR's only collision risk is the separate, non-probabilistic one from actual counter/nonce reuse
  (F37).
- **F39** (core) — Electronic Codebook (ECB) applies a block cipher independently to each block with
  no chaining, randomization, or counter — it is itself a (degenerate) mode of operation, not the
  absence of one — so identical plaintext blocks always produce identical ciphertext blocks under a
  fixed key.
- **F40** (recommended) — Repeated ciphertext blocks under ECB reveal that the corresponding plaintext
  blocks are identical — leaking structure without recovering the key or the plaintext content itself.

## H. Confidentiality vs. integrity vs. replay

- **F41** (core) — **Confidentiality** and **Integrity** are independent security goals; achieving one
  does not imply the other.
- **F42** (core) — Some constructions are prone to **Malleability**: flipping a ciphertext bit (e.g.
  under CTR mode / stream ciphers) flips the corresponding plaintext bit predictably, with no built-in
  error signal.
- **F43** (core) — Confidentiality-only encryption needs an additional authentication mechanism to
  detect tampering — a **Message authentication code (MAC)** (symmetric) or a **Digital signature**
  (asymmetric). This in turn requires the MAC key or signing private key itself be authentic and kept
  secret — the same requirement as F5/F13, applied to a different primitive. (Integrated constructions
  like **AEAD**, F44, provide this within a single primitive rather than as a literally separate
  add-on.)
- **F44** (core) — **Authenticated encryption with associated data (AEAD)** packages confidentiality
  and integrity into a single, integrated construction (e.g. GCM) rather than requiring a
  hand-assembled combination of separate encryption and MAC algorithms — the standard modern default
  for symmetric authenticated encryption. Part of what an AEAD construction must define is failure
  behavior: on verification failure it must output a rejection symbol (⊥) with no partial plaintext or
  diagnostic detail, precisely to avoid the oracle problem in F48.
- **F45** (recommended) — When a dedicated AEAD construction (F44) isn't used, encryption and a MAC
  can instead be combined by hand (**Generic composition**) — **Encrypt-then-MAC**,
  **MAC-then-encrypt**, or **Encrypt-and-MAC** — but the three orderings are not equally safe.
- **F46** (core) — **Encrypt-and-MAC** computes the tag directly over the *plaintext*, sent alongside
  the ciphertext. A MAC is designed only for unforgeability, not confidentiality, so it may leak
  information about the plaintext through the tag itself — e.g. a deterministic MAC produces the same
  tag for the same plaintext, letting an adversary test for repeated messages via the tag even when
  the encryption half is independently randomized. This is a distinct failure from MAC-then-encrypt's
  (F48), not a variant of it.
- **F47** (core) — Generic composition (F45) requires the encryption key and the MAC key be
  independently derived or otherwise separated; reusing one key for both primitives can create
  cross-primitive attacks even when each primitive is secure in isolation.
- **F48** (core) — A verifier's observable behavior may depend on *whether* authentication succeeded
  or failed overall — a single, uniform failure signal is fine and necessary — but must not further
  depend on *why* it failed, and specifically not on an internal parsing/validation step (such as
  padding-validity) evaluated before authentication succeeds. This is stronger than "don't release the
  plaintext": for constructions where decryption includes a padding check (e.g. CBC),
  **MAC-then-encrypt** must decrypt — and therefore validate padding — before the MAC can even be
  checked, so a distinguishable "bad padding" vs. "bad MAC" response becomes an observable oracle (a
  **Padding oracle attack**), even though a single uniform "authentication failed" signal would have
  been safe. **Encrypt-then-MAC** avoids this structurally: a failed MAC check rejects uniformly
  before decryption, and any padding validation inside it, ever runs.
- **F49** (recommended) — A **Padding oracle attack** exploits exactly the mechanism F48 describes:
  because **Padding** (F16) makes a decrypted block's validity checkable (well-formed padding or not),
  an attacker who can distinguish "valid padding" from "invalid padding" after decryption — via a
  different error, timing, or connection behavior — can use many such oracle queries, without knowing
  the key, to recover a CBC-mode plaintext one byte at a time, by manipulating bytes of the preceding
  ciphertext block and observing which manipulated values yield valid padding.
- **F50** (core) — Given independently-keyed schemes (F47), no parsing-dependent observable behavior
  before authentication (F48), an
  unforgeable MAC, an encryption scheme that actually achieves its intended confidentiality
  **Security goal** (a stronger bar than F2's bare infeasible-recovery floor alone),
  IV/nonce/associated-data covered by the MAC computation, and no exploitable implementation side
  channels, **Encrypt-then-MAC** is the generically robust ordering among the three in F45: computing
  the MAC over the ciphertext lets integrity be checked without decrypting or trusting the encryption
  scheme's own robustness — a guarantee that depends on all of these stated assumptions, not one
  holding unconditionally regardless of the specific schemes combined.
- **F51** (recommended) — Encryption (with or without a MAC) does not by itself prevent an adversary
  from replaying, deleting, or reordering previously valid ciphertexts. Preventing this requires an
  explicit **Freshness** or sequence value that is itself covered by the authentication mechanism —
  not merely encrypted — and checked by the verifier; a MAC over content alone doesn't protect the
  message's position in a sequence.

## I. Comparisons

Terms close enough in meaning, or similar enough in surface shape, that students commonly conflate
them. Each entry names the dimension that actually distinguishes the pair (or trio), not just "they're
different." (MAC-vs-signature and keyed-hash-vs-MAC comparisons were removed from this section — see
Flags: they don't state a limitation of *encryption*, which is this file's actual boundary for
touching MAC/signature material at all, so they're scope creep here rather than genuinely missing.)

- **F52** (core) — **Encoding**, Caesar, and encryption: Caesar has a key (unlike encoding), but its
  keyspace (~25 non-identity shifts) is far too small to satisfy F5's unpredictability/infeasibility
  requirement — so Caesar is structurally encryption-shaped (has the F1 mechanics) but functionally
  encoding-grade (fails F2). The dimension that actually separates all three isn't "has a key or not"
  but keyspace size / infeasibility of exhaustive search. (Caesar named only as an illustrative
  example, same treatment as other named constructions below — not a `precise-definitions.md` entry.)
- **F53** (core) — **Block cipher** vs. **Stream cipher**: a block cipher operates on fixed-size
  blocks and needs a **Mode of operation** for anything longer (F15); a stream cipher operates on data
  of any length directly via a **Keystream** (F23), with no block-size constraint. Neither subsumes
  the other — block ciphers give stronger structural analysis tools (F17–F22), and while a block
  cipher *can* avoid padding overhead via F16's ciphertext-stealing alternative, it still has to
  explicitly choose and implement that mechanism; a stream cipher never faces the padding problem to
  begin with.
- **F54** (core) — **Nonce** vs. **Initialization vector (IV)**: a nonce's requirement is normally
  just uniqueness under a given key; an IV's requirement is mode-dependent — sometimes uniqueness
  suffices (CTR), sometimes unpredictability is required (CBC) (F36).
- **F55** (core) — **Generic composition** vs. **Hybrid encryption**: both are "combine two
  independently-designed primitives" patterns, easily conflated, but fixed and different: generic
  composition specifically combines encryption + MAC into authenticated encryption (F45); hybrid
  encryption specifically combines public-key + symmetric encryption to solve the bootstrap problem
  (F12). Same surface shape, different problem solved.
- **F56** (recommended) — **Parallelization** vs. **Error propagation**: both are properties of a
  **Mode of operation**, easily conflated as "how robust/fast is this mode," but distinct dimensions.
  CTR is parallelizable in both directions with no error propagation beyond the corrupted bit itself;
  CBC decryption is parallelizable *and* has 2-block error propagation per corrupted ciphertext block
  — the two properties vary independently, one doesn't imply or exclude the other.

## J. Concrete constructions

Named, real-world ciphers as instances of the general concepts above. Per doc 02 §4, these are
deliberately fact-subjects only, not `precise-definitions.md` entries — the general concept (block
cipher, stream cipher, public-key encryption) is what's defined; the named construction is just an
example of it.

- **F57** (core) — **AES** (Advanced Encryption Standard) is a concrete instance of a **Block cipher**
  (F14): a **Substitution-permutation network (SPN)** with 128-bit blocks and 128/192/256-bit keys,
  10/12/14 rounds depending on key size — the standard modern illustration of F17–F22's
  iterated-construction reasoning.
- **F58** (core) — **RSA** is a concrete instance of **Public-key encryption** (F8, F9): its hardness
  rests on the *RSA problem* (computing `e`-th roots modulo a composite `n`) — related to, but not
  proven equivalent to, the **Integer factorization problem** (factoring `n` breaks RSA; no proof
  shows breaking RSA requires factoring). Textbook (unpadded) RSA has two distinct weaknesses beyond
  F2's bare infeasible-recovery floor: it's deterministic (encrypting the same plaintext twice yields
  the same ciphertext, enabling equality tests — an IND-CPA-style failure), and separately it's
  multiplicatively homomorphic (`Enc(m₁)·Enc(m₂) ≡ Enc(m₁·m₂) mod n`, enabling ciphertext malleability
  and chosen-ciphertext attacks — an IND-CCA-style failure, not a consequence of the determinism issue).
  Practical RSA encryption requires randomized padding (e.g. RSA-OAEP) to close both gaps.
- **F59** (core) — **ElGamal** is a second, independent concrete instance of **Public-key encryption**
  (F8, F9): its confidentiality rests on the **Decisional Diffie-Hellman problem (DDH)** in a
  **Group** — a stronger assumption than the **Computational Diffie-Hellman problem (CDH)** alone,
  which only guarantees that computing the shared value is hard, not that ciphertexts built from it
  are indistinguishable. Encryption is inherently randomized (a fresh per-message ephemeral value), so
  it doesn't share RSA's (F58) textbook-determinism pitfall by default.
- **F60** (core) — **ChaCha20** is a concrete instance of a **Synchronous stream cipher** (F23): it
  generates its keystream from a key, nonce, and counter using only add-rotate-XOR operations, no
  S-boxes or lookup tables — fast in pure software without dedicated hardware support, unlike AES
  (F57), which benefits substantially from dedicated instructions (AES-NI) where available.
- **F61** (recommended) — **DES** (Data Encryption Standard) is a historical concrete instance of a
  **Block cipher** (F14) with a 56-bit key. The problem isn't that a DES key can be predictable — it
  can be perfectly uniformly random — it's that the total keyspace (`2^56` possibilities) is small
  enough for exhaustive search at modern computing power, violating F5's "sufficiently large keyspace"
  clause specifically, not its unpredictability clause. (DES's 64-bit block size is also small enough
  to be a birthday-bound concern in its own right, F38.) This is why DES is no longer considered
  secure and AES (F57) replaced it.
- **F62** (recommended) — **RC4** is a historical concrete instance of a **Synchronous stream cipher**
  (F23) whose keystream has statistically detectable biases in its early output bytes, violating F25's
  pseudorandomness requirement. This holds independent of nonce/key reuse — RC4 remains insecure even
  under perfect nonce/key hygiene, which is what makes it a violation of F25 specifically, not of F24.

## K. Implementation

`F24`, `F36`, `F47`, and `F48` each touch implementation already, but none of them is *about*
implementation as its own concern — they state a requirement and stop short of how it's actually met
in running code. This section closes that gap.

- **F63** (core) — Satisfying F24's uniqueness requirement in practice needs an explicit
  nonce-generation strategy: a monotonic counter (unique for as long as its state persists, doesn't
  wrap around — F64 — and stays unique across every instance sharing the key — F66) or a value
  independently and uniformly sampled at random from a sufficiently large space (unique with high
  probability, bounded by the **Birthday paradox**, F69) — which in turn depends on a real
  **CSPRNG** being available and correctly seeded, not just "call a random function." "Just don't
  reuse it" is a requirement, not an implementable instruction on its own.
- **F64** (core) — A counter-based nonce must never be allowed to wrap around and repeat a
  previously-used value within the lifetime of a key. A counter's finite bit-width imposes a hard,
  computable limit on how many messages can be safely encrypted under one key — a real operational
  limit, not just a theoretical one.
- **F65** (core) — A counter-based nonce that resets to zero on process restart, without persisting its
  last value across restarts, silently reuses nonces that were already used before the crash/restart —
  a common real-world instance of violating F24, not a hypothetical edge case.
- **F66** (core) — F65's restart problem generalizes spatially, not just temporally: when multiple
  instances sharing the same key run concurrently — replicas behind a load balancer, forked processes,
  or a cloned/restored VM or container snapshot — each independently maintaining a counter from the
  same starting state reproduces the exact same nonce sequence across instances, violating F24 just as
  surely as a single restarted process does. Coordinating nonce uniqueness across instances (e.g.
  partitioning the counter space, or folding a per-instance identifier into the nonce) is a distinct
  operational requirement from persisting state across one instance's own restarts.
- **F67** (core) — F47's independent-key requirement is typically achieved in practice via a **Key
  derivation function (KDF)**: deriving separate encryption and MAC keys from one shared secret using
  different context/info strings, rather than generating and distributing two unrelated keys.
- **F68** (core) — Verifying a MAC/tag (F48) must use a constant-time comparison; an early-exit
  byte-by-byte comparison can leak how many leading bytes matched via timing, which — given an
  actually exposed, measurable timing channel and enough attack attempts — can be exploited to forge a
  tag byte-by-byte. This is a real, demonstrated attack class, though it requires a genuine observable
  timing oracle and favorable conditions to exploit in practice, not just non-constant-time code in
  the abstract; F50's "no exploitable side channels" qualifier is not automatically satisfied just
  because the comparison logic is functionally correct.
- **F69** (recommended) — A random nonce, independently and uniformly sampled and long enough to make
  collisions negligible under the **Birthday paradox**, removes the need for persistent counter state
  across restarts (F65) or across instances (F66), at the cost of a longer nonce than a counter would
  need for the same collision risk — a concrete state-vs-nonce-length tradeoff implementers actually
  choose between.

## L. Practicality

Essentially absent before the review pass that added this section (`fact-extraction-process.md` §3
flags exactly this). F11 already states public-key operations are "far more expensive" than symmetric
ones, qualitatively — this section makes that, and the rest of the vision doc's §5 Practicality
dimension, into facts with an actual measurable dimension attached, matching `activity-model.md`'s
`measure` activity.

- **F70** (core) — Symmetric encryption/decryption throughput is typically orders of magnitude higher
  than public-key operations at a comparable security level — directly measurable (time N operations,
  compare) — though the exact ratio varies substantially by construction, implementation, and
  hardware, and by which operation is measured (e.g. RSA encryption/verification is much faster than
  RSA decryption/signing, because of how the public and private exponents are typically chosen).
- **F71** (core) — Ciphertext size scales differently by construction: symmetric ciphertext is roughly
  plaintext length plus a small fixed overhead (IV/nonce, and a tag if authenticated); RSA ciphertext
  is always exactly the modulus size regardless of (small) plaintext length, so encrypting a short
  message directly under RSA produces disproportionate ciphertext expansion.
- **F72** (recommended) — At the commonly-cited ~128-bit security level (a representative point, not a
  universal law — exact figures shift as hardness estimates are revised), symmetric keys need about
  128 bits, RSA moduli need about 3072 bits (roughly 24× larger), and ECC keys need about 256 bits
  (roughly 2× larger than the symmetric key, but over an order of magnitude smaller than the matching
  RSA modulus) — the concrete, measurable reason ECC-based constructions scale better than RSA as
  security requirements increase, beyond F11's qualitative ECC note.
- **F73** (recommended) — Whichever construction is used (stream cipher or a block-cipher mode like
  CTR), it's specifically choosing F63's *counter-based* nonce-generation strategy — not the
  construction itself — that requires persistent state (the current counter value) across the
  lifetime of a key. The asymmetry matters: the sender/nonce-allocator side always needs this
  persistence, to know the next unused value; the receiver only needs it too if the nonce is implicit
  (derived from its own synchronized counter rather than read off each message) — if the nonce is
  transmitted alongside the ciphertext, the receiver just reads it per message and carries no
  generating state of its own. This asymmetric persistence is exactly what F65's and F66's failure
  modes attack. Choosing F63's *random* nonce-generation strategy instead needs no persistent counter
  state on either side between messages — only per-message transmission of that message's nonce
  alongside the ciphertext, which F36 already establishes as safe since nonces aren't secret.
- **F74** (recommended) — Hardware support can change the practical ranking, not just the absolute
  speed: AES (F57) benefits substantially from dedicated instructions (AES-NI) where available;
  ChaCha20 (F60) is designed to be fast in pure software and can outperform AES on platforms without
  AES-NI (e.g. some mobile/embedded hardware). This is a real tradeoff, not an absolute one —
  well-optimized software AES can still be competitive in some cases, so "AES needs AES-NI to be fast"
  should be read as typical, not as a strict requirement.

---

## Flags

- **Resolved:** *crib-dragging*, *frequency analysis* (F27), *ciphertext stealing* (F16), and
  *Decisional Diffie-Hellman problem (DDH)* (F59) were flagged as undefined in earlier rounds — none
  existed anywhere in the definitions corpus, not even the full 306-entry `precise-definitions.md`.
  All four now have precise entries in both `precise-definitions.md` and `pv080-definitions.md`, and
  their usages above are bold (defined) rather than italic (undefined).
- ECB (F39), CBC/CTR (F36/F37/F54/F56), GCM (F44), and the section J named constructions (AES, RSA,
  ElGamal, ChaCha20, DES, RC4) have no `precise-definitions.md` entry by design — they're
  fact-subjects only, per doc 02 §4's named-artefact split. *AES-NI* and *add-rotate-XOR* (F60/F74)
  are still informal hardware/technique terms, left undefined — implementation trivia rather than
  cryptographic concepts, arguably out of scope for a conceptual definitions file (judgment call, flag
  if you disagree).
- DH, DSA, and ECDSA are deliberately not in section J — they're key-agreement/signature primitives,
  not encryption, so out of scope for a ciphers file. Natural seed for a future
  `facts-key-agreement.md`/`facts-signatures.md`, alongside F13's PKI stub.
- **MAC vs. digital signature** and **Keyed hash vs. MAC** comparisons were removed from section I
  (an external review caught this file's own stated boundary — "MAC/signature facts appear only where
  needed to state a limitation of encryption alone" — being violated by two comparisons that compared
  properties *within* the MAC/signature family instead). Both are genuinely useful comparisons, just
  not for this file; seed material for the same future MAC/signature file as the paragraph above,
  alongside DH/DSA/ECDSA.
- F22 sits in section D (block-cipher iteration) rather than B (symmetric vs. asymmetric) even though
  it's a public-key-vs-block-cipher security comparison — kept there deliberately, anchored to F9 and
  D's proof-vs-empirical theme, rather than moved.
- F56 (parallelization vs. error propagation) sits in section I (Comparisons) rather than G (Modes) or
  L (Practicality) — an external review suggested moving it; kept in I deliberately, since it's
  exactly the kind of commonly-conflated pair section I exists for, not primarily a modes fact or a
  measurable-benchmark fact.
- F13 and F43's key-authenticity/PKI concerns are deliberate stubs — the full certificates/PKI chain
  isn't expanded here.
- F72's numbers are representative of one commonly-cited security-level estimate, not a guaranteed or
  permanent equivalence — worth a caveat if ever used in an assessment context rather than a comparison
  illustration.
- Not yet checked against [`chains-draft.md`](chains-draft.md) for consistency — chains-draft predates
  all revisions of this file and still reflects the earliest, least precise phrasing. Reconcile once
  the compression/chain-reconstruction pass happens.
