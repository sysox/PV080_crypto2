# The logical chain of cryptographic design

Source: [`TODO/01_framework_vision_requirements.md`](TODO/01_framework_vision_requirements.md) §4.2.
This file defines the eight stage-types themselves — what each one *means* as a category — so that
later fact files can instantiate the chain for real topics without re-litigating what "threat" or
"requirement" means each time. It does not yet contain any cryptographic facts.

Domain instantiations of stages 1–2 (use case, threat) live separately from the fact layer — see
[usecases-ciphers.md](usecases-ciphers.md) for the cipher domain's use cases and threat profiles,
kept apart from [facts-ciphers.md](facts-ciphers.md) per `activity-model.md`'s own separation of
practical examples from the atom database.

> use case → threat → security goal → requirement → mechanism/design choice →
> implementation requirement → failure when violated → attack/consequence

## The eight stages

1. **Use case** — A real situation in which cryptography is applied: who wants what, with whom,
   under which constraints. Answers *"what is being protected, for whom, in what setting?"*
   Example: two parties exchange messages over a network neither of them controls.

2. **Threat** — A capability an adversary is assumed to have in that use case (part of the threat
   model). Answers *"what can go wrong, and who can make it go wrong?"*
   Example: an eavesdropper who can read every message on the wire.

3. **Security goal** — A property the design is intended to guarantee against that threat. Answers
   *"what must stay true despite the threat?"* (Matches the existing definition in
   [`definitions/pv080-definitions.md`](definitions/pv080-definitions.md): "a property that a
   system's design is intended to guarantee.")
   Example: confidentiality — the eavesdropper learns nothing about the plaintext.

4. **Requirement** — A necessary condition, usually on inputs, keys, or randomness, that must hold
   for the security goal to actually be achieved. Answers *"what must be true of the mechanism's
   inputs/behaviour for the goal to hold?"*
   Example: a given (key, nonce) pair must never be used to encrypt two different messages.

5. **Mechanism / design choice** — The concrete construction chosen to meet the requirement.
   Answers *"what construction implements this?"*
   Example: CTR mode with a per-message nonce.

6. **Implementation requirement** — A constraint on how the mechanism must be *used* in practice
   (state management, API contract) so that stage 4's requirement actually holds at runtime.
   Answers *"what must the implementer or caller do, or avoid, to not violate the requirement?"*
   Example: the nonce counter must survive restarts and be coordinated across processes so it is
   never reused.

7. **Failure when violated** — What breaking the requirement looks like concretely, at the level of
   data or computation — not yet the adversary's exploit, just the broken state. Answers *"what
   actually goes wrong, mechanically, when the requirement is violated?"*
   Example: two ciphertexts under the same keystream XOR to the XOR of their plaintexts.

8. **Attack / consequence** — What an adversary can now do with the failure, and how bad it is.
   Answers *"what can be recovered or broken, and what's the impact?"*
   Example: crib-dragging or frequency analysis on the XOR of the two plaintexts recovers both.

## Notes on using the chain

- Not every topic needs all eight stages populated explicitly every time. A topic can start mid-chain
  (e.g. a lecture may hand you the requirement directly, without re-deriving the threat model each
  time it's reused elsewhere).
- One use case can branch: the same "network eavesdropper" threat can motivate confidentiality *and*
  integrity goals, each with its own requirement/mechanism/failure/attack sub-chain.
- Stage 6 (implementation requirement) is where most real-world misuse bugs live — it's the stage
  most worth having explicit, separate facts for, since it's the one a working construction can still
  violate.
- Importance marking on chain instances (next step) should reuse `core` / `recommended` / `optional`
  from [`activity-model.md`](activity-model.md)'s `importance` field, rather than a new vocabulary.

## Open question before instantiating facts

Which stage-elements are worth being independent, reusable facts (citable from multiple chains) versus
inline prose within one chain's write-up? Tentative default: threats, security goals, and requirements
are reusable across many chains (e.g. "chosen-plaintext attacker" is the same threat for many
mechanisms) and should be written once and referenced; mechanism → failure → attack is usually
specific enough to one chain that it's fine to write inline. Revisit once 2–3 real chains exist and we
can see whether reuse actually happens.
