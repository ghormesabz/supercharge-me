# Principles

Shipped defaults for the structure contract. The grill walks the ones that apply to the build, recommends the default for each, and records every acceptance, override and exemption as a B13 row. `--principles PATH` swaps this file; the rest of the skill keeps working if the replacement uses the same shape: a Rule, a Consequence and a Default per principle.

## Vocabulary

Use these terms exactly in B3, B11 and B13. Condensed from `skills/engineering/codebase-design/SKILL.md` in mattpocock/skills (MIT). See NOTICE.

- **Module**: anything with an interface and an implementation. A function, a class, a package, a vertical slice.
- **Interface**: everything a caller must know to use the module correctly: the types, and also invariants, ordering, error modes, required configuration and performance. Not just the signature.
- **Depth**: leverage at the interface, meaning the behaviour a caller or test can exercise per unit of interface they must learn. **Deep**: much behaviour behind a small interface. **Shallow**: an interface nearly as complex as its implementation.
- **Seam**: a place where behaviour can change without editing in that place. The location where a module's interface lives.
- **Adapter**: a concrete thing that satisfies an interface at a seam. It names a role, not what is inside.
- **Deletion test**: imagine deleting the module. If complexity vanishes, it was a pass-through. If it reappears across N callers, it earned its place.
- **Two-adapter rule**: one adapter is a hypothetical seam; two adapters (a real one and a test fake count) is a real one.

Two levels, kept apart: a **component** is a system-level thing in B1 and B3's first table (a database, a queue, a UI, an outside service). A **module** is a code-level thing in B3's module map.

## The principles

Each has a **Rule**, a **Consequence** for the project in plain words, and a **Default**.

**P1 Core first, thin adapters.**
Rule: all behaviour lives in one core with a typed interface. CLI, HTTP and app are adapters with no logic of their own.
Consequence: when the thing grows from a command line into an app, nothing is rewritten and the two cannot drift apart.
Default: adopt for anything with a user interface. Not applicable to a one-off script or a pure library; record which.

**P2 Deep modules.**
Rule: small interface, much hidden behaviour. A module that only forwards calls fails the deletion test and is deleted.
Consequence: fewer files, fewer places to look, and an agent finds the right one quickly.
Default: adopt.

**P3 Lock the one-way doors only.**
Rule: decide now what is expensive to reverse (data model, public interface, module boundaries, authentication). Defer the rest with a trigger.
Consequence: the first structure is small, and the unknowns stay visible instead of being guessed.
Default: adopt.

**P4 Walking skeleton.**
Rule: slice 1 is the thinnest path that works end to end. Structure appears when a slice needs it.
Consequence: you see the thing run early, and nothing is built for a slice that has not started.
Default: adopt.

**P5 No abstraction before the second use.**
Rule: introduce a seam only where two adapters exist, or a test needs the second.
Consequence: no speculative layers, and every abstraction can point to the variation that pays for it.
Default: adopt.

**P6 Contracts at boundaries.**
Rule: every boundary has a named schema (a B5 contract) before code is written on either side.
Consequence: pieces can be built and tested separately and still fit.
Default: adopt wherever two modules or systems meet.

**P7 Test at the interface.**
Rule: a slice's done-when is observable behaviour, checked across the module's interface and not past it.
Consequence: internals can change without breaking tests, and "done" is never an opinion.
Default: adopt.

**P8 One obvious place for each thing.**
Rule: names an agent can search for; no indirection that needs a map to follow.
Consequence: the next person, or agent, finds the code without a tour.
Default: adopt.

**P9 Scaffold budget.**
Rule: each slice lists the modules and directories it may create (B11). Nothing else is created, including empty folders and stubs for Deferred decisions.
Consequence: the repo never grows ahead of the work, so an early structural guess cannot harden into the shape of the project.
Default: adopt.

**P10 Pure core, effects at the edges.**
Rule: decisions and calculations are functions of their inputs. Reading, writing and calling out happen at the edges.
Consequence: the core is easy to test and replay.
Default: opt-in. Fits some stacks and some problems better than others; recommend it when the build is mostly transformation of data.

**P11 Fail loud.**
Rule: during development, errors surface where they happen. No swallowed exceptions, silent fallbacks, hidden retries or backwards-compatibility shims unless a B13 row says so. Compatibility is a Deferred decision with the trigger "first consumer outside the repo, or first tagged release".
Consequence: failures show up while they are cheap, and the design gets fixed instead of papered over.
Default: adopt, always. Failure rows in B2 and B4 name who sees the failure and how.

## Shape

Name the project's shape in the grill: script, library, tool (command line), or app (user interface plus services). It decides which principles apply:

| Shape | Notes |
|:--|:--|
| Script | P1, P5, P10 usually not applicable. Keep P4, P7, P11 |
| Library | P1 not applicable (the library is the core). P2, P6, P7 carry the most weight |
| Tool | P1 applies: the command line is one adapter. Design the core interface first so an app adapter can follow |
| App | All apply. P1 and P6 matter most |

## Register entries

Each principle that applies gets one B13 row: `P1`, `P2` and so on, Status `Locked` (adopted or exempted, with the reason), `Deferred` or `Experiment`. D-compat is always present. The register is the only part of the spec that changes after hand-off.
