*Document 1 — What the system should achieve*

**Status:** the north-star vision doc; each requirement below is realized concretely elsewhere —
arity-1 definitions in [`definitions/precise-definitions.md`](definitions/precise-definitions.md),
the arity-2+ fact/why-chain layer in [`knowledge-graph/logic.md`](knowledge-graph/logic.md) +
[`knowledge-graph/facts-tree.md`](knowledge-graph/facts-tree.md), and the practical/demonstrable
layer in [`seminars/`](seminars/) (real exercises, not a hypothetical). See
[`02_knowledge_architecture.md`](02_knowledge_architecture.md) and
[`03_pedagogical_engine.md`](03_pedagogical_engine.md) for the current architecture and generation
design built on top of this vision.

# 1. Core objective

Create a clearly defined framework that gives AI a reliable structure
for generating teaching material, practical exercises, theory questions,
knowledge maps, learning paths, and assessment. The framework is
intended primarily for cryptography, where understanding requires
connecting definitions, design rationale, attacks, security properties,
implementation constraints, and practical trade-offs.

# 2. What the system should generate

1.  Exercises that make principles visible on concrete examples,
    including guiding questions that help students implement or reason
    about the mechanism.

2.  Questions for practising theory, understanding, distinctions between
    similar concepts, consequences of assumptions, and design choices.

3.  A knowledge view that shows dependencies, logical relations, design
    rationale, and the reasons why a primitive or property is needed.

4.  Learning trajectories adapted to what a student already knows, what
    they want to learn, their level, and the available time.

5.  Practical demonstrations and experiments that students can run,
    modify, measure, break, and repair.

6.  Assessment material derived systematically from the same knowledge
    source, rather than written as an unrelated question bank.

# 3. Desired structure of the knowledge

The source material should not be a conventional textbook. It should
contain small, explicit pieces of domain knowledge from which AI can
systematically derive teaching artefacts. The source should distinguish
the meaning of a concept from facts about it.

- Definitions should explain what a concept is. Non-defining properties
  should not be mixed into the definition merely because they are useful
  facts.

- Concepts may themselves depend on other concepts. For example, the
  definition of a block cipher depends on notions such as a block, key,
  function family, permutation/bijection, and fixed-size domain.

- The system should represent relationships such as classification,
  properties, dependencies, implications, requirements, and comparisons.

- Importance should be explicit so that AI can distinguish core
  takeaways from details.

- The canonical source should remain small; information that can be
  safely and systematically derived should not have to be duplicated
  manually.

# 4. Why a knowledge graph/view is needed

The knowledge view has two complementary purposes.

## 4.1 Learning order and navigation

- Show what a learner must understand before a target topic becomes
  meaningful.

- Allow a student to select what they do not yet know or what they want
  to learn.

- Allow a tutor to select a useful path under a time budget.

- Support multiple valid teaching trajectories rather than forcing one
  global chapter order.

## 4.2 Show the logic of cryptographic design

A central view should expose chains of reasoning such as:

> use case → threat → security goal → requirement → mechanism/design
> choice → implementation requirement → failure when violated →
> attack/consequence

This should make the “why” visible: why a construction has a particular
component, why a property is required, and what happens if the
requirement is violated.

# 5. Cryptography-specific knowledge dimensions

The framework should cover both security and practicality. Security
alone is insufficient for teaching real cryptographic design.

| **Dimension** | **Examples** |
|----|----|
| Security | threats, attacker capabilities, security goals, security notions, attacks, assumptions, failure modes |
| Design | requirements, mechanisms, composition, rationale, construction choices |
| Practicality | runtime, latency, throughput, memory, parallelism, bandwidth, state, ciphertext/signature overhead |
| Implementation | API usage, nonce/key management, validation, error handling, common misuse |
| Comparison | how closely related concepts/constructions differ and which distinction matters in practice |

# 6. Important pedagogical requirements

- Similar concepts that students commonly confuse should be explicitly
  comparable along concrete dimensions, not merely marked “different”.

- Teaching should support small-step scaffolding for weaker students and
  compressed paths for stronger students.

- A useful pattern is to start with a familiar or simpler mechanism and
  progressively add requirements and properties (for example
  encoding/Caesar → secrecy parameter → attacks → stronger
  constructions).

- Students should often predict an outcome before executing an
  experiment, then compare the prediction with the observed result.

- The same underlying knowledge should support explanation, prediction,
  application, debugging, attack, repair, design, and justification
  questions.

# 7. What should be demonstrable in cryptography

The system should collect not only what is true, but also what is
pedagogically demonstrable. Typical practical actions include:

- Use a primitive/function and inspect its input/output.

- Change one input while keeping others fixed and observe the output
  change.

- Compare two related constructions or concepts under the same inputs.

- Measure runtime, throughput, memory, output size, overhead, or scaling
  with parameters.

- Trace intermediate values of a construction.

- Intentionally violate a requirement and observe the failure.

- Run an attack and measure whether/how quickly it succeeds.

- Scale a toy attack with key size, hash size, password KDF cost, or
  other parameters.

- Modify ciphertext/tag/signature/AAD and observe verification or
  decryption behaviour.

- Run security-game-like experiments to make formal security notions
  concrete.

- Debug an insecure API use, repair it, and verify that the previous
  attack no longer works.

# 8. Intended AI workflow

> canonical domain knowledge → derive important takeaways → choose
> teaching path → generate explanation/examples/demos → generate
> practice → assess → update learner state

The key design goal is that the AI should act as a generator/compiler
over a trusted knowledge source, rather than using the language model
itself as the authoritative knowledge base.

# 9. Success criterion

A successful framework should let a small, well-structured cryptographic
knowledge source generate consistent definitions, dependency and
why-views, comparisons, learning paths, practical labs, scaffolded
exercises, theory questions, and exams — without maintaining each output
as a separate knowledge base.
