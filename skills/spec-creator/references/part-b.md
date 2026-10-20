# Part B: for the build team

Part B is the build detail, written like a software architect's design pack. A builder who has never met the client can start slice 1 from this document without asking a question. If a question comes to mind while writing, the answer belongs in the spec, in a B13 row, or in A7 as a builder question.

The architecture figures lead. B1 and B2 come before any table. Keep prose above each figure to a sentence or two.

The list is fixed and is never renumbered. If a section does not apply, keep its heading and write `Not applicable.` with the reason. Tag claims as in [part-a.md](part-a.md). A Part B claim tagged Interpreted, Assumption or Open carries a Q link to A7, as in Part A. Use the vocabulary in [principles.md](principles.md): a **component** is a system-level thing, a **module** is a code-level thing.

Failure paths fail loud. Every failure row, in B2 and B4, says who sees the failure and how. A retry, fallback or degrade path exists only when a B13 row records it.

## Sections

**B1 Architecture map.** What is new, what exists, what is external. Layers run top to bottom: users, the client boundary (named), outside the boundary. Inside the boundary, group components by layer, for example interface, services, data and models. The Users layer lists roles and carries no chips. Every other component carries a kind chip, chosen from an open list such as UI, Service, DB, Index, Queue, LLM, API, Mail or Host, and one of `new`, `existing` or `external`. The lines between layers carry the channel or protocol. B1 and B3 list the same components.

**B2 System flow.** One item through the pipeline. Six stages or fewer per pipe. Split a longer flow into two pipes, each with its own caption. Stage kinds are trigger, model call, service call, person and store. A stage that can fail carries an `If it fails:` line saying who sees the failure and how. Each arrow is labelled with a contract name from B5.

**B3 Component register.** Two tables.

1. Components. One row per component in B1: kind (the same word as its chip in B1), status, responsibility, and notes (stack, constraint or a B13 decision ID).
2. Module map, for the components marked `new`. One row per module slice 1 or a Locked later slice needs: Module, Interface (what a caller must know, one line), Hides, Seam and adapters, Slice. Every module passes the deletion test. A seam row lists two adapters (a test fake counts) or says `none yet`. A Deferred decision gets no row.

**B4 Model call cards.** One card per model call in B2. Fields, in this order:

| Field | Holds |
|:--|:--|
| Purpose | What the call does, in one sentence |
| Model tier | Small, mid-size or large; hosted or local; structured output or not |
| Inputs | The input contract from B5, and any masking before the call |
| Output | The output contract from B5 |
| Grounding | Where the facts come from: retrieval, prompt context or none |
| Guardrails | Validation and refusal rules. A retry limit, and anything that follows the last retry, needs a B13 row. Default: fail loud, naming who sees it |
| Eval | How quality is measured, on what data, and the pass mark |
| Fallback | What a person does when the call fails |
| Budget | Latency target and token counts |

Name a tier. Name a vendor model only when the user decided it, and record that decision in B13. The schema lives in B5 and the card points to it.

**B5 Data contracts.** A register table first, one row per contract on a B2 arrow: Contract, Carries (a few words), Produced by, Read by. Then each contract gets a label paragraph with its name in backticks and one JSON block, with the type or allowed values as each value. A contract has the same name everywhere it appears. Write no `: caption` line after a JSON block.

**B6 Integrations.** One row per outside system: direction, protocol, auth method and configuration names. Write variable names only. A value never appears in the spec. If the context holds a key, token or connection string, do not copy it. Tell the user it is exposed and should be rotated.

**B7 Runtime and environments.** Environments and how they differ, hosting and why, where configuration and secrets come from, and how a change reaches production.

**B8 Security and privacy.** Data that must not leave and how it is masked, retention, who reads what, and provider terms that matter.

**B9 Non-functional targets.** Each measure has a target and a basis. A target nobody confirmed is an Assumption.

**B10 Tests and acceptance.** Each check says how it runs and what result passes. Every model call has an eval here, with its data and pass mark. Checks cross a module's interface, not its internals.

**B11 Build plan.** Slices that each work end to end. Slice 1 is the smallest slice that does. Each slice has a done-when that someone can observe, a Scaffold (the modules and directories it may create, named from the B3 module map), and the B10 checks that prove it. Nothing outside a slice's Scaffold is created in that slice, including empty folders and stubs.

**B12 Risks.** Risk, effect, response, owner.

**B13 Decision register.** One row per structural decision, one per applicable principle (`P1`, `P2`, and so on, see [principles.md](principles.md)), and D-compat. Columns:

| Column | Holds |
|:--|:--|
| ID | `D1`, `D2`, ... for decisions; `P1`, ... for principles; `D-compat` |
| Decision | What is decided, in the builder's words |
| Status | `Locked`, `Deferred`, `Experiment` or `Open` |
| Why or trigger | Locked: the reason. Deferred: the observable event that unlocks it. Experiment: the kill condition. Open: the owner |
| Door | `one-way` or `two-way` |

D-compat is always present. Default row: Backwards compatibility handling, Deferred, trigger "first consumer outside the repo, or first tagged release", two-way.

After hand-off, B13 is the only part of the spec that changes: the coding agent updates Status and Why or trigger when a trigger fires. Everything else stays as written.
