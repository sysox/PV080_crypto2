# PV080 Cryptography — Precise Definitions

**Status:** consolidated draft; requires expert review before publication as normative material.

**Purpose:** This document is the definition layer from which atomic knowledge-graph facts and pedagogical materials can be produced. It intentionally separates precise statements from analogies, simplifications, and examples.

**Convention:** entries here state only what a term *means*. Relations between terms (differs-from, implies, enables, equivalent-to, is-a-special-case-of, historical/comparative claims, worked examples) do not belong inline — `equivalent-to` covers both a term turning out to characterize the same thing as another named entry (e.g. Invertibility ⟺ Injective mapping) and a term's condition being restatable as a property that isn't itself a separately-defined entry (e.g. Surjective ⟺ `f(X) = Y`) — through this document's last several passes they were tracked separately in [`../archive/knowledge-graph/facts/precise-definitions-facts.md`](../archive/knowledge-graph/facts/precise-definitions-facts.md), now archived along with the rest of the consumed source material. Whether that split continues to be actively maintained going forward, or the fact layer is rebuilt fresh when the term→relation phase of work starts, is an open question, not a resolved one; see `knowledge-graph/logic.md` §1 for the definition/fact (arity) test this convention rests on. Every time a definition is widened for generality, the narrowed original case is not just dropped — it becomes a `typical_case` fact (`knowledge-graph/logic.md` §2a).

**Precision:** Each definition should be as precise as possible — ideally stated mathematically — while remaining clear and concise. Exempt: descriptive attack/technique entries (Slide attack, Related-key attack, MITM, Downgrade attack, etc.) describe a method rather than a property, and formalizing them doesn't add clarity — they still need to be unambiguous prose, just not mathematical. Also exempt: genuinely qualitative design concepts (e.g. Confusion) where one measurable indicator (e.g. Non-linearity's formula) is a proxy correlated with the concept, not a canonical restatement of it — force the formula onto the indicator's own entry, not onto the qualitative concept it merely supports.

**Composition:** When a term's meaning is exactly the combination of already-defined sibling terms, define it by composing them (`Bijection` — an injective and surjective mapping) rather than restating their content in new words.

**Scope discipline:** Do not add a new entry, or a fact pointing at a new entry, unless the term is actually referenced or load-bearing elsewhere in this document. An unreferenced term invented to formalize a passing detail (e.g. a standalone `Algebraic degree` entry with nothing pointing to it) is an orphan and should be merged into whichever entry actually needed it instead.

**Consistency:** Entries in the same structural family (e.g. all `*-resistance` notions, all attack entries) should receive the same level of formalization and explanatory shape as their siblings — a difference in treatment needs a stated reason, not just more editorial attention on one entry.

**Textual + formal:** Where a mathematical formalization is possible, give both — a short prose clause naming what the thing is, plus the formula — not one instead of the other. A bare formula with no sentence saying what it represents is as unhelpful as a sentence that could have been a formula but isn't.

**Notation:** One convention throughout, no exceptions. Lowercase letters (`pt, ct, k, x, y, n, r`) denote elements; the matching uppercase letter (`P, C, K, X, Y`) denotes the set that element belongs to. `pt`/`ct` (not single-letter `m`/`c`) match the `pk`/`sk` pattern and keep plaintext/ciphertext distinct from a hash function's generic `m` input, which is not drawn from `P`. For a mapping, use `X` for the domain and `Y` for the codomain — not `A, B`, which are reserved for protocol parties (Alice, Bob) in Part G. In probability statements, a capital letter may also denote the random variable ranging over the correspondingly-named space (e.g. `Pr[X = x]` for `x ∈ X`) — context inside `Pr[...]` disambiguates this from the space itself. For a generic abstract group, `Group` itself is stated with a generic operation `∘` and identity `e` for full generality; every concrete group entry below it (`Order`, `Generator`, `Subgroup`, `Discrete logarithm problem`, etc.) switches to multiplicative notation — juxtaposition/exponentiation for `∘`, `1` for the identity — since that's how this course's groups (`Z*_p`-style) are actually written. Exception: elliptic-curve groups use additive/point notation instead (`+`, point `O`), never multiplicative.

**Quantifiers:** State conditions in explicit symbolic form rather than paraphrased prose — e.g. `a₁ ≠ a₂ ⟹ E(a₁) ≠ E(a₂)` rather than "distinct inputs have distinct outputs."

**Symbol glossary:** Reuse this fixed set of symbols across every entry rather than inventing new ones per entry.

| Set | Element | Meaning |
|---|---|---|
| `X, Y` | `x, y` | generic domain, codomain |
| `P` | `pt` | plaintext space |
| `C` | `ct` | ciphertext space |
| `K` | `k` | keyspace |
| — | `pk`, `sk` | public key, private (secret) key |
| — | `n` | nonce |
| — | `r` | randomness used by a probabilistic algorithm |
| — | `σ` | a signature |
| — | `t` | a MAC/authentication tag |
| — | `A` | a probabilistic polynomial-time (efficient) adversary |
| — | `Enc`, `Dec` | encryption algorithm, decryption algorithm |
| — | `S`, `V` | signing algorithm, verification algorithm |
| — | `H` | a hash function |

**Scope flag:** Where a term is generic and not specific to cryptography (e.g. black-box testing, white-box testing), note this explicitly so readers don't read it as a crypto-native concept.

**Synonyms:** When multiple terms are used for the same concept, name the entry `Term (alias)` — the term outside the parentheses is canonical and is what other entries should use when they reference the concept; the parenthetical is noted once, not necessarily reused elsewhere. Reserve `Term / Term` (no parentheses) for the rare case where usage in the literature is genuinely split with no preferred term. A third, distinct use of the same `Term (X)` shape: when an entry defines a canonical algorithm or object that has its own shorthand symbol reused in formulas elsewhere in this document (`Encryption algorithm (Enc)`, `Signing algorithm (S)`, `Hash function (H)`), the parenthetical is that symbol, not an alias — the symbol is also listed in the Symbol glossary below, and is never itself a name someone would write in place of the term.

**Homonyms:** When the same term name is used for two genuinely *different* concepts in different contexts — a naming collision, not a synonym — put the disambiguating context in the term name itself (e.g. `RNG forward secrecy`), not in the alias bracket. The `Term (alias)` bracket stays reserved for synonyms of the same concept; mixing a disambiguator into it (e.g. `Forward secrecy (RNG state, backtracking resistance)`, cramming context and alias together) conflates two different jobs into one bracket. Default to qualifying only the less-commonly-referenced sense and leaving the more central one bare, unless both are used about equally.

**Section placement:** A term belongs in the most specific Part where it is used. It belongs in Part A (general concepts) only if it is used across two or more of the other Parts.

## Part A — General concepts

### A0. The field

**Cryptography** — The discipline of constructing and analyzing techniques for protecting information and computation against adversaries.

**Steganography** — The practice of concealing the existence of data within other data.

**Cryptanalysis** — The discipline of analyzing cryptographic techniques to find and exploit their weaknesses.

**Cryptology** — Cryptography together with cryptanalysis.

**Trusted** — A component relied upon to meet expectations, independent of whether that reliance is justified.

**Trustworthy** — A component that reliably meets expectations, and so merits the confidence placed in it.

**Penetration testing (pen testing)** — Authorized testing of a system's security by attempting to demonstrate exploits against it.

**Black-box testing** — Generic testing methodology carried out without access to design documents or source code.

**White-box testing** — Generic testing methodology carried out with access to design documents or source code.

**Side-channel attack** — An attack that infers secret information from measurable physical characteristics of a device's execution (timing, power draw, electromagnetic emission, cache behavior, etc.) of operations that process that secret, rather than from a weakness in the algorithm's mathematical definition.

**Timing attack** — A side-channel attack that infers secret information from variations in how long an operation takes to execute.

**Fault injection attack** — A physical/implementation attack that deliberately induces hardware or software errors during a cryptographic computation, then exploits the faulty output to recover secret material.

**Security goal** — A property that a system's design is intended to guarantee.

**Attack** — An attempt by an adversary to violate a system's stated security goal.

**Threat model** — A statement of the capabilities and limitations assumed of an adversary, defining what a system is designed to resist.

**Asset** — A resource that a security policy protects.

**Principal** — An agent whose identity and privileges are relevant to a security policy.

**Security policy** — A specification of what actions and access a system permits and forbids.

**Transposition** — A classical encryption technique that permutes the positions of symbols in a message.

**Substitution** — A classical encryption technique that replaces each symbol with another according to a fixed rule.

**Frequency analysis** — A cryptanalytic technique against substitution-style ciphers that infers plaintext or key material from the statistical distribution of symbols in ciphertext, exploiting the non-uniform symbol frequencies of the underlying plaintext language.

**Crib-dragging** — A cryptanalytic technique against ciphertexts produced under a reused keystream: a guessed plaintext fragment (a "crib") is XORed against the combined ciphertext at successive offsets, and offsets producing plausible text incrementally reveal the keystream and both underlying plaintexts.

### A1. Data and structure

**Alphabet** — A finite set of symbols.

**Symbol** — An element of an alphabet.

**Finite sequence / string** — An ordered finite list of symbols.

**Concatenation** — Joining two strings, written `x ∥ y`.

**Block** — A string of a fixed length processed as one unit.

**Block size** — The fixed length of a block.

**Padding** — A reversible and unambiguous extension of data to meet a required length or format.

**Byte** — An 8-bit string.

**Message** — Data treated as one logical unit.

**Plaintext** — A message before encryption, `pt ∈ P`, where `P` is the plaintext space.

**Ciphertext** — The output of encryption, `ct ∈ C`, where `C` is the ciphertext space.

### A2. Mappings

**Mapping / function** — A rule `f: X → Y` assigning exactly one output to every input in `X`.

**Injective mapping (one-to-one mapping)** — A mapping `f: X → Y` such that `a₁ ≠ a₂ ⟹ f(a₁) ≠ f(a₂)`. 

**Invertibility** — The property that a mapping `f: X → Y` has an inverse mapping.

**Surjective mapping** — A mapping `f: X → Y` such that for every `y ∈ Y` there exists `x ∈ X` with `f(x) = y`.

**Bijection** — An injective and surjective mapping.

**Permutation** — A bijection from a set onto itself.

**Image** — The set of outputs produced by a mapping, `f(X) = \{f(x) : x ∈ X\}`.

**Inverse mapping** — For an injective mapping `f: X → Y`, the mapping `f⁻¹: f(X) → X` such that `f⁻¹(f(x)) = x` for all `x ∈ X`.

**One-way function** — A function that is efficiently computable but computationally infeasible to invert on a specified input distribution without additional information. A formal security definition must specify the security parameter, input distribution, adversary, and success probability.

**Trapdoor one-way function (trapdoor function)** — A one-way function that becomes efficiently invertible when secret trapdoor information is provided.

**Lookup table** — A concrete representation of a mapping as an explicit table of input-output pairs.

**Encoding** — A fixed, public, injective mapping between representations.

**Decoding** — The inverse of an encoding mapping, defined on the image of the encoding.

**Encryption (enciphering)** — Informal name for the transformation carried out by an `Encryption algorithm` (below); see that entry for the formal definition.

**Decryption (deciphering)** — The transformation of ciphertext into plaintext (or a failure indicator), parameterized by a key.

**Deterministic encryption mapping** — For a fixed key and fixed public parameters, a deterministic algorithm may induce a mapping `E_k: P → C`.

**Encryption algorithm (Enc)** — A public algorithm `Enc` that produces ciphertext from key material and a plaintext, using whatever additional inputs the scheme specifies.

**Probabilistic encryption algorithm** — An encryption algorithm using internal randomness `r`: `ct ← Enc(k₁, pt; r)`.

**Nonce-based encryption algorithm** — An encryption algorithm deterministic given an externally-supplied nonce: `ct ← Enc(k₁, pt, n)`.

**Decryption algorithm (Dec)** — An algorithm `Dec` that recovers plaintext from a ciphertext, or returns `⊥` for an invalid ciphertext or decryption failure.

**Probabilistic decryption algorithm** — A decryption algorithm matching a probabilistic encryption algorithm: `Dec(k₂, ct) ∈ P ∪ {⊥}`.

**Nonce-based decryption algorithm** — A decryption algorithm matching a nonce-based encryption algorithm: `Dec(k₂, ct, n) ∈ P ∪ {⊥}`.

### A3. Keys and parameters

**Key** — The output of a scheme's `KeyGen` algorithm, supplied as a parameter to its other algorithms.

**Symmetric key (secret key)** — Secret key material shared by the parties using a symmetric scheme.

**Key length** — The bitlength of a key.

**Master key** — A long-term key used to derive or protect other (typically shorter-lived) keys.

**Round key** — A key derived by a key schedule and used within a single round of an iterated construction.

**Public key** — The publicly distributable half of an asymmetric key pair.

**Private key** — The secret half of an asymmetric key pair, kept by its owner.

**Key pair** — Mathematically related public and private keys generated together.

**Keyspace** — The set of valid keys or key-generation outputs for a scheme.

**Session key** — A symmetric key generated for use during a single communication session or transaction.

**Security parameter (`λ`)** — A value controlling key sizes, input sizes, and the intended computational difficulty of a scheme.

**KeyGen** — The randomized key-generation algorithm of a scheme, on input a security parameter: `k ← KeyGen(λ)` (symmetric) or `(pk, sk) ← KeyGen(λ)` (asymmetric).

**Nonce** — A public input associated with an instance of a cryptographic scheme or protocol; the specific property required of it (e.g. uniqueness, unpredictability) depends on the construction.

**Initialization vector (IV)** — A public per-message input to a mode of operation; the specific property required of it (e.g. unpredictability, uniqueness) depends on the mode.

**Counter** — A value identifying a block position within a single encryption operation.

**Key derivation function (KDF)** — A function deriving one or more cryptographic keys from a source of keying material, typically also taking a salt or context string: `k ← KDF(km, salt, info)`.

**Key stretching** — A key derivation function deliberately designed to be slow.

**Password-based key derivation function (PBKDF)** — A key derivation function specifically intended to turn a low-entropy password into a cryptographic key.

### A4. Encryption schemes and security

**Encryption scheme** — A triple of polynomial-time algorithms `Π = (KeyGen, Enc, Dec)`.

**Negligible function** — A function `ε: ℕ → [0,1]` such that for every polynomial `p`, there exists `n₀` such that `ε(n) < 1/p(n)` for all `n > n₀`.

**Correctness** — For a key output by `KeyGen`, and matching public parameters between an operation `Op₁` and its counterpart `Op₂`, the counterpart succeeds as intended: `Pr[Op₂(Op₁(x)) = expected result] = 1` in an error-free scheme, or `≥ 1 − ε(λ)` for some negligible function `ε` in a scheme allowing error.

**Valid ciphertext** — A ciphertext valid relative to a specified key and public parameters if it can be produced by `Enc` for some plaintext and allowed randomness.

**Invalid ciphertext** — A ciphertext that is not a valid ciphertext relative to a specified key and public parameters.

**Symmetric encryption** — Encryption and decryption using shared secret key material.

**Public-key encryption** — Encryption using `pk`; decryption using `sk`.

**Kerckhoffs’s principle** — A cryptosystem's security should depend only on the secrecy of the key.

**Security through obscurity (security by obscurity)** — Relying on the secrecy of a system's design or implementation.

**Information-theoretic security** — Security that holds even against an adversary with unlimited computational power, resting on the information available to the adversary.

**Perfect secrecy** — The property that the plaintext and ciphertext random variables are statistically independent: for every `pt` and `ct` with `Pr[C = ct] > 0`, `Pr[P = pt | C = ct] = Pr[P = pt]`.

**One-time pad** — A symmetric encryption scheme XORing plaintext with a truly random key at least as long as the message, the key never reused.

**Adversary** — Generally: the source or threat agent behind a potential attack. In a cryptographic security experiment: a probabilistic polynomial-time algorithm (or algorithm family) attempting to break a stated security notion of a scheme, with capabilities and access defined by the experiment.

**Computational security** — The property that a scheme satisfies a specified computational security notion when every probabilistic polynomial-time adversary has negligible advantage in the corresponding security experiment.

**Security experiment / game** — A formal procedure defining the challenger, adversary inputs and oracle access, challenge generation, winning condition, and probability space.

**Oracle access** — In a security experiment, the adversary's ability to submit chosen inputs to a specified algorithm and receive its output, without learning the underlying key.

**Adversarial advantage** — The difference between an adversary's success probability and the baseline success probability defined by a security experiment.

**Security notion** — A security experiment paired with an advantage threshold (typically: negligible) a scheme must satisfy.

**Existential unforgeability under chosen-message attack (EUF-CMA)** — The security notion under which no efficient adversary, given a signing/tagging oracle for chosen messages, can produce a valid signature/tag on any message not previously submitted to the oracle, except with negligible probability.

**Reduction** — A polynomial-time transformation from breaking a scheme's claimed security notion to solving or breaking some other problem or primitive.

**Provable security** — The approach of establishing confidence in a scheme's security via an explicit reduction to a stated hardness assumption, rather than by informal argument or the absence of known attacks.

**Random oracle model** — An idealized security-proof setting in which a hash function is modeled as a perfectly random function, answering each new query freshly and consistently.

**Standard model** — A security-proof setting using only the stated computational assumptions, with no idealized primitives.

**Semantic security** — The requirement that a ciphertext reveal no partial information about the plaintext to an efficient adversary beyond its length.

**Indistinguishability under chosen-plaintext attack (IND-CPA)** — The security notion under which no efficient adversary, given chosen-plaintext capability, can distinguish which of two adversarially chosen equal-length plaintexts was encrypted, with advantage better than negligible over random guessing.

**Pseudorandom function (PRF)** — A keyed function whose input-output behavior is computationally indistinguishable from that of a function chosen uniformly at random from all functions of the same domain/range, to any efficient adversary without the key.

**Pseudorandom permutation (PRP)** — A keyed permutation computationally indistinguishable from a uniformly random permutation of the same domain, to any efficient adversary without the key.

**Unicity distance** — The amount of ciphertext needed, on average, for a computationally unbounded attacker to uniquely determine the key (or plaintext) from ciphertext alone, given redundancy in the plaintext language.

**Secret sharing** — Splitting a secret into multiple shares distributed among parties, such that only specified authorized subsets of shares can reconstruct the secret, while unauthorized subsets reveal nothing about it.

**Key wrapping** — Encrypting one key using another key, for secure storage or transport of the wrapped key.

### A5. Operations, goals, and capabilities

**Bitwise operations** — Operations performed at the level of individual bits.

**Exclusive OR (XOR)** — The bitwise operation returning 1 if its two input bits differ and 0 if they match.

**Word operations** — Operations performed on fixed-size machine words.

**Confidentiality** — Preventing an unauthorized party from learning protected information beyond permitted leakage.

**Integrity** — The property of data, software, or hardware remaining unaltered except by authorized parties.

**Authorization (authorized access)** — The property of computing resources being accessible only by authorized entities.

**Availability** — The property of information, services, and computing resources remaining accessible for authorized use.

**Authentication** — Assurance that a principal, data, or software is genuine relative to expectations arising from appearances or context.

**Entity authentication** — Assurance that the identity of a principal involved in a transaction is as asserted.

**Data origin authentication (data authentication)** — Assurance that the source of data or software is as asserted.

**Accountability** — The ability to identify principals responsible for past actions.

**Non-repudiation of origin** — Strong evidence of unique origination, making it hard for a party to have produced data and later successfully deny having done so.

**Exhaustive key search (brute-force attack)** — Systematically enumerating candidate secret keys or key-generation choices and testing consistency with available observations.

**Ciphertext-only capability** — Access only to ciphertexts produced under the target key.

**Known-plaintext capability** — Access to plaintext–ciphertext pairs produced under the target key.

**Chosen-plaintext capability (CPA)** — Ability to request encryption of chosen plaintexts.

**Chosen-ciphertext capability (CCA)** — Ability to request decryption of chosen ciphertexts, subject to the restrictions of the experiment.

**Passive adversary** — An adversary that observes and records information without altering it.

**Active adversary** — An adversary that injects, alters, or originates messages.

## Part B — Symmetric constructions

**Block cipher** — A keyed permutation on fixed-length blocks: each key selects a bijective map from blocks to blocks of the same size. `E: K × X → X`, `E(k, ·): X → X` bijective for every `k ∈ K`.

**Key schedule** — A public algorithm deriving round keys from a main key.

**Round** — One application of an internal transformation in an iterated construction.

**Round function** — The specific transformation applied at each round of an iterated construction.

**Permutation box (P-box)** — A fixed component in a block cipher round that permutes bit positions.

**Feistel network** — A block cipher design paradigm that splits each block into two halves and applies a sequence of rounds, each updating one half using a round function of the other half and a round key, then swapping.

**Substitution-permutation network (SPN)** — A block cipher design paradigm alternating layers of substitution (nonlinear, local, via S-boxes) and permutation (linear, block-wide diffusion) over several rounds.

**S-box (substitution box)** — A small, fixed, nonlinear lookup table used as a round component in a block cipher, mapping a short input to a short output.

**Differential cryptanalysis** — A chosen-plaintext cryptanalytic technique studying how differences in plaintext pairs propagate to differences in the resulting ciphertext pairs, seeking input differences that lead to output differences with unexpectedly high probability.

**Linear cryptanalysis** — A known-plaintext cryptanalytic technique seeking linear approximations (over `GF(2)`) relating plaintext, ciphertext, and key bits that hold with probability noticeably different from one half.

**Slide attack** — A cryptanalytic technique exploiting self-similarity between rounds of an iterated cipher, by aligning ("sliding") two encryptions under the same key by one round.

**Meet-in-the-middle attack** — An attack on multiple sequential encryption that computes and stores all possible intermediate values from one direction, then searches for a match against values computed from the other direction.

**Related-key attack** — An attack exploiting a known or chosen mathematical relationship between two or more keys, rather than requiring the keys themselves to be known.

**Correlation attack** — An attack on stream ciphers exploiting a statistical bias between the keystream and an individual generator component's output.

**Linear feedback shift register (LFSR)** — A shift register whose next-state feedback value is a linear function of selected current-state values.

**Nonlinear feedback shift register (NLFSR)** — A shift register whose feedback function is nonlinear.

**Filter generator** — A keystream generator producing output by applying a nonlinear filtering function to the values at selected fixed positions of a single shift register.

**Combining generator** — A keystream generator producing output by combining the outputs of multiple shift registers through a nonlinear function.

**Clock control (irregular clocking)** — A stream-cipher design technique in which one shift register's own state determines when another register is stepped, rather than stepping every register in lockstep on every clock cycle.

**Keystream period** — The length of a stream cipher's keystream before it repeats.

**Mode of operation** — A public procedure describing how a block cipher processes messages longer than one block and how IVs, nonces, or counters enter the computation.

**Ciphertext stealing** — A technique for handling a final plaintext block shorter than the block size without padding: ciphertext bits are rearranged between the last two blocks so the total ciphertext length exactly matches the plaintext length.

**Stream cipher** — A symmetric encryption construction that combines plaintext with a keystream, one unit at a time, where the keystream is generated from key material.

**Synchronous stream cipher** — A stream cipher whose keystream depends only on the key and public parameters, not on the plaintext or ciphertext.

**Self-synchronizing stream cipher (asynchronous stream cipher)** — A stream cipher whose keystream generation depends in part on a fixed number of previously produced ciphertext digits.

**Keystream** — A sequence of pseudorandom or truly random bits, bytes, or blocks generated from key material and public parameters.

**Determinism** — The property that identical algorithm inputs always produce identical output.

**Malleability** — The ability to transform a valid output of a keyed algorithm into another valid output, without knowing the key.

**Parallelization** — The ability to process multiple blocks or positions independently and concurrently.

**Error propagation** — The extent to which corruption in an input affects the corresponding output.

**Authentication tag** — The output value attached to data to allow verification of its authenticity.

**Keyed hash** — A hash function that takes a secret key as an additional input.

**Message authentication code (MAC)** — An authentication tag computed as a function of a message and a secret key, sent alongside the message so any party holding that key can verify it: `t ← MAC(k, m)`, verified by recomputing `MAC(k, m)` and comparing to the received `t`.

**Tag truncation** — Using only a prefix of a MAC or AEAD algorithm's full-length output as the tag.

**Authenticated encryption (AE)** — Encryption combined with data authentication.

**Generic composition** — Building authenticated encryption by combining a separate encryption algorithm and a separate MAC algorithm.

**Associated data (AD)** — Data, possibly empty, covered by an integrity/authenticity guarantee but not encrypted.

**Authenticated encryption with associated data (AEAD)** — Authenticated encryption that additionally covers associated data.

**Nonce-misuse resistance** — The property that an AEAD scheme's security degrades gracefully under nonce reuse: even if a nonce repeats, ciphertexts leak nothing beyond whether the same `(nonce, associated data, plaintext)` triple was encrypted before.

**Encrypt-then-MAC** — Generic composition ordering: encrypt the plaintext, then compute the MAC over the resulting ciphertext.

**MAC-then-encrypt** — Generic composition ordering: compute the MAC over the plaintext, append it, then encrypt both together.

**Encrypt-and-MAC** — Generic composition ordering: compute the MAC over the plaintext and the encryption of the plaintext independently, sending both.

**Message expansion** — The increase in output length beyond input length.

## Part C — Asymmetric primitives

**Public-key cryptography (asymmetric cryptography)** — The branch of cryptography using key pairs: a public key and a mathematically related private key.

**Hard problem** — A computational problem believed infeasible at cryptographic parameter sizes.

**Integer factorization problem** — Given a composite integer `n`, finding its prime factors.

**Discrete logarithm problem (DLP)** — Given a cyclic group, a generator `g`, and an element `h = gˣ`, finding `x` modulo `ord(g)`: the unique `x ∈ {0, 1, ..., ord(g)−1}` such that `gˣ = h`.

**Computational Diffie-Hellman problem (CDH)** — Given a cyclic group, a generator `g`, and elements `gᵃ` and `gᵇ`, computing `gᵃᵇ`.

**Decisional Diffie-Hellman problem (DDH)** — Given a cyclic group, a generator `g`, and elements `gᵃ`, `gᵇ`, and `gᶜ`, deciding whether `c ≡ ab (mod ord(g))`: distinguishing the distribution of `(gᵃ, gᵇ, gᵃᵇ)` from `(gᵃ, gᵇ, gᶜ)` for uniformly random `a, b, c`.

**Group** — A set with a binary operation combining any two elements into another element of the set, satisfying closure, associativity, an identity element, and inverses: `(G, ∘)` with `∘: G × G → G` such that `∀a,b,c ∈ G: (a∘b)∘c = a∘(b∘c)`; `∃e ∈ G: ∀a ∈ G, e∘a = a∘e = a`; `∀a ∈ G, ∃a⁻¹ ∈ G: a∘a⁻¹ = a⁻¹∘a = e`.

**Generator** — An element of a group whose powers produce every element of the group (or, of a subgroup, every element of that subgroup): `g ∈ G` such that `{gᵏ : k ∈ ℤ} = G`.

**Subgroup** — A subset of a group that is itself a group under the same operation: `H ⊆ G`, `H ≠ ∅`, such that `∀a,b ∈ H: a∘b⁻¹ ∈ H`.

**Order (of a group)** — The number of elements in a group: `|G|`.

**Order (of an element)** — For `b ∈ G`, the smallest positive integer `j` such that `bʲ = 1`: `ord(b) = min\{j ∈ ℕ⁺ : bʲ = 1\}`.

**Probable prime** — An integer that has passed one or more probabilistic primality tests.

**Provable prime** — An integer proven prime with mathematical certainty via a primality-proving algorithm.

**PH-safe prime (Pohlig-Hellman-safe prime)** — A prime `p` such that `p − 1` has a "large" prime factor `q`, resisting the Pohlig-Hellman algorithm for computing discrete logarithms: `p = Rq + 1` for some large prime `q` and integer `R`.

**Safe prime** — A prime `p = 2q + 1` where `q` is also prime.

**DSA prime** — A prime `p = Rq + 1` with a large prime factor `q` of `p − 1`, where `q` is chosen large enough to be PH-safe but not much larger.

**Secure prime** — A prime `p = 2Rq + 1` where `q` is prime and `R` is either prime or has only prime factors larger than `q`.

**Strong prime (RSA context)** — A prime `p` (one of the two RSA modulus factors `p, q` in `n = pq`) traditionally chosen so that `p − 1` and `p + 1` each have a large prime factor.

**Security strength** — An estimate of a scheme's resistance to the best known attacks, expressed in bits, as distinct from raw key bitlength.

**Integer factorization cryptography (IFC)** — Public-key systems whose hardness rests on the difficulty of factoring a large composite modulus.

**Finite field cryptography (FFC)** — Public-key systems whose hardness rests on the discrete logarithm problem in a finite field.

**Elliptic curve cryptography (ECC)** — Public-key systems implementing encryption, signatures, and key agreement using operations over points on an elliptic curve.

**Post-quantum cryptography** — Cryptography designed to remain secure against adversaries with access to a large-scale quantum computer.

**Key encapsulation mechanism (KEM)** — A public-key primitive with a `(KeyGen, Encapsulate, Decapsulate)` interface: `(ek, ss) ← Encapsulate(pk)` produces a fresh symmetric key `ss` together with its encapsulation `ek` under a recipient's public key; `ss ← Decapsulate(sk, ek)` recovers `ss` using the private key.

**Encapsulation** — In a KEM, the algorithm producing a fresh symmetric key and its encapsulation under a public key: `(ek, ss) ← Encapsulate(pk)`.

**Decapsulation** — In a KEM, the algorithm recovering the symmetric key from an encapsulation using the private key: `ss ← Decapsulate(sk, ek)`.

**Key agreement** — Key establishment in which parties derive shared secret material over a public channel without transmitting that secret directly.

**Hybrid encryption** — Combining public-key and symmetric-key encryption: a symmetric session key encrypts the payload message, and a public-key algorithm encrypts the session key for the recipient: `ct ← Enc_sym(k, pt)`, `c_k ← Enc_pk(pk, k)`; send `(c_k, ct)`.

**Digital signature (σ)** — A public-key mechanism in which a private key produces a message-bound signature and the corresponding public key verifies it, providing data origin authentication and data integrity, and — assuming the private key remains exclusively controlled by its owner — supporting non-repudiation of origin: `σ ← S(sk, m)`, `V(pk, m, σ) ∈ {VALID, INVALID}`.

**Signing algorithm (S)** — The algorithm that, parameterized by a signer's signing private key, produces a signature tag for a message: `σ ← S(sk, m)`.

**Verification algorithm (V)** — The algorithm that, parameterized by a signer's verification public key, checks whether a purported signature tag is valid for a given message, returning VALID or INVALID: `V(pk, m, σ) ∈ {VALID, INVALID}`.

**Digital signature with appendix** — The default signature style: verification requires the message itself alongside the signature tag: `m ∥ σ` is transmitted; `V(pk, m, σ)` takes `m` as an explicit input.

**Digital signature with message recovery** — A signature style in which the tag itself encodes the message, so verification recovers the original message from the tag.

**Detached signature** — A signature tag transmitted or stored separately from the message it covers: `m` and `σ` transmitted/stored as separate objects.

**Attached signature** — A signature tag bundled together with the message it covers into a single object: `m ∥ σ` transmitted as one unit.

**Sign-then-encrypt** — Signing ordering: apply the signature first, then encrypt the message and its signature together: `σ ← S(sk, m)`, then `ct ← Enc(k, m ∥ σ)`.

**Encrypt-then-sign** — Signing ordering: encrypt the message first, then sign the resulting ciphertext: `ct ← Enc(k, m)`, then `σ ← S(sk, ct)`.

## Part D — Hash functions

**Hash function (H)** — A public, unkeyed function mapping arbitrary-length inputs to fixed-length outputs: `H: \{0,1\}^* → \{0,1\}^n`.

**Cryptographic hash function** — An efficiently computable hash function designed to be preimage-, second-preimage-, and collision-resistant.

**Digest (hash value, message digest, fingerprint)** — The fixed-length output `H(m)` of a hash function.

**Compression function** — An internal fixed-size-to-fixed-size function iterated to process arbitrary-length input: `f: \{0,1\}^n × \{0,1\}^b → \{0,1\}^n`, taking a chaining value and a message block to a new chaining value.

**Merkle-Damgård construction** — A hash-function design that iterates a compression function over successive padded input blocks, chaining each block's output into the next, with the final chaining value as the digest.

**Sponge construction** — A hash-function design that absorbs input blocks into an internal state via a fixed permutation (the absorb phase), then produces output blocks by repeatedly extracting from and re-permuting that state (the squeeze phase).

**Preimage resistance** — For a hash function `H`, no efficient adversary given `y = H(m)` for `m` drawn from a specified distribution can output `m'` with `H(m') = y`, except with negligible probability: for every efficient `A`, `Pr[m' ← A(y) : H(m') = y] ≤ ε(λ)` for some negligible function `ε`.

**Second-preimage resistance** — For a hash function `H`, no efficient adversary given `m₁` (drawn from a specified distribution) can output `m₂ ≠ m₁` with `H(m₂) = H(m₁)`, except with negligible probability: for every efficient `A`, `Pr[m₂ ← A(m₁) : m₂ ≠ m₁ ∧ H(m₂) = H(m₁)] ≤ ε(λ)` for some negligible function `ε`.

**Collision resistance** — For a hash function `H`, no efficient adversary can output a pair `m₁ ≠ m₂` with `H(m₁) = H(m₂)`, except with negligible probability: for every efficient `A`, `Pr[(m₁,m₂) ← A() : m₁ ≠ m₂ ∧ H(m₁) = H(m₂)] ≤ ε(λ)` for some negligible function `ε`.

**Avalanche effect** — A small input change causes a large, unpredictable output change on average: for a hash function `H: {0,1}^* → {0,1}^n` and any input `x ∈ {0,1}^ℓ` with bit position `i ∈ {1,...,ℓ}`, `HD(H(x), H(x ⊕ 2ⁱ)) ≈ n/2`.

**One-way hash function** — A hash function providing preimage resistance.

**Collision-resistant hash function** — A hash function providing collision resistance.

**Birthday paradox** — The fact that, for a set of size `m`, a randomly sampled collection needs only about `√m` elements before a collision (two equal elements) becomes likely.

**Birthday attack** — A generic collision-finding attack applying the birthday paradox: for a hash function with `n`-bit output, a collision is expected after computing roughly `2ⁿ/²` hash values.

**Length-extension attack** — An attack on Merkle-Damgård-style hash functions exploiting their iterated internal structure: given `H(m)` (and the length of `m`, but not `m` itself), an attacker can compute `H(m ∥ pad ∥ m′)` for a chosen suffix `m′`, without knowing `m`.

**Salt** — A public value combined with an input before hashing or key derivation.

## Part E — Randomness

**Randomness** — Unpredictability and uniformity, according to the relevant model. Loosely used to mean unpredictability or absence of exploitable pattern. 

**Entropy** — A measure of uncertainty available from a source, expressed in bits: `H(X) = -Σₓ p(x) log₂ p(x)` for a random variable `X` with distribution `p`.

**Entropy source** — A physical or system process that supplies raw, at least partially unpredictable data.

**Estimated entropy** — A statistical estimate of the true entropy per unit of data from a source, as opposed to its nominal or assumed entropy.

**RNG** — A mechanism intended to produce random numbers or bits.

**TRNG (true random number generator, truly random number generator)** — An RNG deriving output from a physical entropy source.

**PRNG (pseudorandom number generator)** — A deterministic algorithm expanding a seed into a longer sequence that mimics true randomness.

**CSPRNG (cryptographically secure PRNG)** — A PRNG whose output is computationally indistinguishable from suitable uniform randomness and remains unpredictable under the specified compromise model.

**Seed** — The initial input determining a deterministic algorithm's output.

**Internal state** — The memory of an iterative process used to compute and update future output.

**State update function** — The rule determining how an internal state changes with each step.

**Unpredictability** — The RNG quality property that no adversary can guess the next output better than its true conditional distribution allows, given all previous outputs: `Pr[A(x₁, ..., xᵢ) = xᵢ₊₁] ≤ 2^{-H_∞(Xᵢ₊₁ | x₁,...,xᵢ)} + ε(λ)` for some negligible function `ε`, where `H_∞` is conditional min-entropy.

**Uniformity** — The RNG quality property that every possible output value is equally likely: `Pr[X = x] = 1/|X|` for all `x ∈ X`.

**Bias** — Deviation of a random source's output distribution from uniform: `δ = maxₓ |Pr[X = x] − 1/|X||`.

**Whitening** — Post-processing applied to raw entropy source output to remove bias before use.

**Entropy pool** — A generator's collection of accumulated, mixed entropy samples from one or more sources.

**Reseeding** — Refreshing a PRNG's internal state with fresh entropy.

**State compromise attack** — An attack that recovers an iterative process's internal state and uses it to predict future outputs.

**RNG forward secrecy (backtracking resistance)** — The property that compromise of a PRNG's current internal state does not allow reconstruction of *past* outputs.

**RNG backward secrecy (prediction resistance)** — The property that after the internal state is reseeded with sufficient fresh entropy, a prior compromise of that state does not allow prediction of subsequent outputs.

## Part F — Cross-cutting design properties

**Computational indistinguishability** — No efficient adversary, given a sample from one of two distributions `D₀`, `D₁`, can determine which with more than negligible advantage: for every efficient `A`, `|Pr[A(x)=1 : x←D₀] − Pr[A(x)=1 : x←D₁]| ≤ ε(λ)` for some negligible function `ε`.

**Construction property** — A structural or statistical property of a construction's behavior, evaluated directly rather than through an adversarial security experiment.

**Diffusion** — The design property that each input symbol influences many output symbols: for `F: \{0,1\}^n → \{0,1\}^m`, `Fⱼ` depends on bit `i` if `∃x: Fⱼ(x) ≠ Fⱼ(x ⊕ 2ⁱ)`; diffusion holds when `|\{j : Fⱼ \text{ depends on } i\}|` is large for every `i`.

**Confusion** — The design property that the relationship between key material and output is complex, making it difficult to infer the key from observed outputs.

**Strict avalanche criterion (SAC)** — Flipping any input bit changes each output bit with probability exactly one half, under the specified experiment: `Pr[Fⱼ(x) ≠ Fⱼ(x ⊕ 2ⁱ)] = 1/2` for all `i, j`.

**Non-linearity** — A quantitative measure of how far a function is from the nearest affine approximation: for `F: \{0,1\}ⁿ → \{0,1\}`, `NL(F) = min_{a∈\{0,1\}ⁿ, b∈\{0,1\}} |\{x : F(x) ≠ a·x ⊕ b\}|` (Hamming distance to the nearest affine function `a·x ⊕ b`); for vector-valued `F: \{0,1\}ⁿ → \{0,1\}ᵐ`, `NL(F) = min_{c∈\{0,1\}ᵐ\setminus\{0\}} NL(c·F)`, the minimum over all nonzero linear combinations of output coordinates.

## Part G — Authentication protocols and key establishment

**Protocol** — A defined sequence of message exchanges and local computations between parties (principals), designed to achieve a specific goal.

**Secure channel** — A communication channel providing confidentiality and integrity for the data sent over it.

**Freshness** — The property that a value or message is newly generated for the current protocol run, not reused from an earlier one.

**Cryptographic protocol** — A protocol that involves cryptographic techniques.

**Authentication protocol** — A cryptographic protocol that provides entity authentication, authenticated key establishment, or both.

**Claimant (prover)** — The party (entity or device) being authenticated in an authentication protocol.

**Verifier** — The party given assurances of another's identity in an authentication protocol.

**Challenge-response** — A protocol pattern in which a verifier sends a fresh challenge and a claimant proves knowledge of a secret by returning a response computed as a function of the challenge and the secret, without revealing the secret itself.

**Unilateral authentication** — Authentication in which one party proves its identity to another, without the reverse.

**Mutual authentication** — Authentication in which each party proves its identity to the other.

**Key establishment (key exchange)** — A means by which two end-parties arrange a shared secret for securing subsequent communications.

**Key transport** — Key establishment in which one party unilaterally chooses the key and transfers it to the other.

**Authenticated key establishment** — Key establishment integrated with entity authentication in a single protocol.

**Key management** — Establishing shared keys, securing them in transit and storage, and (for public keys) establishing and maintaining trust in their integrity and authenticity.

**Ephemeral key** — A short-term secret, established for one session.

**Crypto-strength key (strong secret)** — A key chosen uniformly at random from a sufficiently large keyspace, such that no strategy beats exhaustive search: `H(K) = log₂|K|` (full entropy), with `H(K) ≥ λ`.

**Weak secret** — A secret drawn from a distribution predictable enough that guessing strategies beat exhaustive search of the nominal keyspace: min-entropy `H_∞(secret) = -log₂ max_x Pr[secret = x]` is small relative to `log₂|K|`.

**Time-variant parameter (TVP)** — A value included in a protocol message to provide uniqueness or freshness, or to cryptographically bind messages within a protocol run.

**Forward secrecy** — The property that disclosure of long-term secret keys does not compromise the secrecy of session keys established in earlier protocol runs.

**Known-key security** — The property that compromise of a session key does not put at risk future key management.

**Liveness** — The property, provided by entity authentication, that an identified far-end party is actually active and participating in the protocol at the present instant.

**Key confirmation** — Explicit evidence, from received data demonstrating knowledge of a session or data key, that another party possesses the correct key.

**Implicit key authentication** — A key establishment property whereby the set of parties who could possess a given key is narrowed to one specifically identified party, without confirming that party actually possesses it.

**Explicit key authentication** — Implicit key authentication combined with key confirmation.

**Replay attack** — Reusing a previously captured protocol message, verbatim, at a later time.

**Reflection attack** — Replaying a captured protocol message, verbatim, back to the party that originated it.

**Forgery** — Producing a valid authentication tag without the key or private information needed to do so legitimately.

**Distinguishing attack** — An attack that succeeds at telling two distributions, or a scheme's output from random, apart with non-negligible advantage.

**Algebraic attack** — A cryptanalytic technique that expresses a cipher's or generator's behavior as a system of equations and solves that system to recover key or state material.

**Weak-key attack** — An attack exploiting specific key values for which a cipher behaves atypically, rather than a general weakness holding for all keys.

**Invalid-curve attack** — An attack on elliptic-curve protocols that supplies a point not actually on the intended curve, exploiting insufficient point validation to leak information about the private key.

**Man-in-the-middle attack (MITM, middle-person attack)** — An attack in which an adversary interposes itself between two parties, independently completing the protocol with each while each believes it is communicating directly with the other.

**Dictionary attack** — A guessing attack using a heuristically prioritized candidate list.

**Forward search attack** — An attack exploiting deterministic public-key encryption with a small or predictable message space: an attacker precomputes the encryption of every candidate value, then compares any later-observed ciphertext against the precomputed table.

**Confounder** — A sufficiently long random value inserted into protocol data specifically to remove recognizable structure that would otherwise serve as verifiable text.

**Small-subgroup (confinement) attack** — An attack on unauthenticated Diffie-Hellman-style key agreement in which an active attacker manipulates exchanged public values so the resulting shared key is forced into a small, easily-searched subgroup.

**Single sign-on (SSO)** — Generic identity-architecture concept, not crypto-specific: an architecture letting a user authenticate once and then access multiple services or resources without re-authenticating separately to each.

**Identity provider (IdP)** — Generic identity-architecture concept, not crypto-specific: a trusted third party in a federated identity system that authenticates users and issues authentication tokens that service providers rely on.

**Federated identity system** — Generic identity-architecture concept, not crypto-specific: a single sign-on architecture supporting authentication across distinct administrative domains, via identity providers trusted by multiple, independently-operated service providers.

**Downgrade attack** — An attack that forces a protocol negotiation to select an older or weaker algorithm, parameter set, or protocol version than the parties would otherwise use.

**Padding oracle attack** — An attack that exploits a system's distinguishable responses to different padding-validity outcomes during decryption.

**Offline guessing attack** — A dictionary-style attack requiring no per-guess interaction with a legitimate verifier.

**Online guessing attack** — A dictionary-style attack requiring per-guess interaction with a legitimate server.

**Verifiable text** — Protocol data an attacker can use to test whether a candidate secret is correct, without further interaction.

**Partition attack** — An attack using a data field in a protocol message (partitioning text) that leaks enough information to split a candidate-secret dictionary into "still possible" and "eliminated" sets.

**Zero-knowledge proof** — An entity-authentication or proof method by which a claimant convinces a verifier that it knows a secret (or that a statement is true) without revealing anything about the secret beyond that fact.

**Password-authenticated key exchange (PAKE)** — A key establishment protocol that uses a (possibly weak, password-derived) shared secret for mutual authentication of the established key, designed to resist offline guessing attacks.

## Part H — Public-key certificates and PKI

**Public-key certificate** — A data structure binding a public key to a named Subject via a digital signature.

**Certification Authority (CA)** — A trusted third party that issues public-key certificates, vouching for the association between a named Subject and a public key.

**Relying party** — Any party that relies on a certificate, placing trust in its associated trust anchor.

**Trust anchor** — A CA (or its public key) trusted directly, not via a certificate signed by another CA.

**Root certificate** — A self-signed certificate at the top of a certificate hierarchy, serving as a trust anchor.

**Self-signed certificate** — A certificate whose signature is produced by the private key corresponding to its own embedded public key, rather than by a separate issuing CA.

**Intermediate CA** — A CA whose own public key is itself certified by another CA.

**Certificate chain (chain of trust)** — A sequence of certificates, from a target certificate through zero or more intermediate CAs, whose topmost certificate is validated against a trust anchor.

**Certificate validation** — The process of checking that a certificate is fit for reliance.

**Trust store** — A device's or application's local collection of trust anchors it accepts.

**PKI (public-key infrastructure)** — The technologies and processes for issuing, distributing, validating, and revoking public-key certificates.

**Distinguished Name (DN)** — A set of `<attribute, value>` pairs that together identify a named entity within its issuing namespace.

**Registration Authority (RA)** — An entity a CA may delegate to for facilitating and vetting certificate requests, without itself issuing certificates.

**Certificate revocation** — Terminating a certificate's validity before its expiration date.

**Certificate Revocation List (CRL)** — A CA-signed, dated list of serial numbers of revoked certificates.

**Trust model** — The system — design, procedures, and rules, as instantiated by software — by which applications recognize public-key certificates as valid and determine the allowed uses of their public keys.

**Trust on first use (TOFU)** — A liberal certificate/key trust approach: accept and remember a presented key or certificate the first time it is seen, without independent verification.

**Check on first use (COFU)** — A conservative certificate/key trust approach: independently verify a presented key or certificate before trusting it.

