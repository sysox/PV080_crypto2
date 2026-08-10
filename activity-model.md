# PV080 Practical Activity Model

## Activity vocabulary

An activity describes what the student does with a practical example or task. A task may use one or several activities.

- `read` — inspect an explanation, definition, instructions, or documentation;
- `observe` — inspect an output, mapping, visualisation, failure, or protocol trace;
- `execute` — run an existing cell, program, protocol step, or experiment;
- `modify` — change an input, parameter, message, key, nonce, IV, or implementation;
- `implement` — write or complete code, a mapping, a protocol step, or a construction;
- `measure` — collect timing, sizes, frequencies, error rates, or other observations;
- `answer` — provide an explanation, prediction, calculation, or interpretation;
- `discuss` — reason with a partner, group, or class about an observation or design choice.

These are actions, not knowledge-graph fact types. The same cryptographic example can support multiple activities and can be reused in different tasks.

## Task metadata

Every practical task should be describable using the following fields:

| Field | Purpose |
| --- | --- |
| `id` | Stable identifier. |
| `title` | Short human-readable task name. |
| `purpose` | What the task is intended to show or develop. |
| `task` | Problem statement, goal, and requirements. |
| `workspace` | Notebook, VM, webpage, IDE, paper, discussion, or physical activity. |
| `resources` | Code, datasets, documentation, tools, and templates. |
| `dependencies` | Required software, hardware, accounts, or external services. |
| `activities` | One or more values from the activity vocabulary above. |
| `deliverables` | Answers, code, measurements, configuration, report, or design. |
| `outcomes` | Knowledge and skills intended to result. |
| `difficulty` | `basic`, `intermediate`, or `advanced`. |
| `time` | Estimated completion time. |
| `prerequisites` | Required knowledge or previous tasks. |
| `assessment` | Automatic check, manual review, peer review, discussion, or presentation. |
| `collaboration` | Individual, pair, small group, or whole class. |
| `importance` | `core`, `recommended`, or `optional`. |
| `variants` | Simplified, extended, or alternative versions. |
| `relationships` | Previous, next, alternative, extension, or related tasks. |

## Practical-example fields - TODO check later

The practical example itself should remain separate from the atom database. A task may refer to one or more atoms, facts, properties, designs, or attacks, but those links should be added only after the examples have been catalogued.

Useful example fields are:

```yaml
id: example_id
title: Human-readable title
context: Situation presented to students
inputs: Data, keys, parameters, or initial state
procedure: What is executed or changed
observations: Outputs students can inspect
questions: Questions students answer or discuss
variants: Alternative versions of the same example
resources: Notebook cells, library functions, files, or services
```

The fields above describe the example without deciding yet which definitions or facts it demonstrates.


