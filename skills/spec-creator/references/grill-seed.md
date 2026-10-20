# Grill seed

The grill settles everything the spec needs before any file is written. `supercharge-me:interview-me` runs the rounds in Rounds Mode. This file gives it the tree. The rules below override the hook where they differ.

## Rules

- Ask in plain chat text. Do not use a form tool.
- Put a recommended answer on every question, and word the question so "yes" accepts it.
- Seed each recommendation from the injected context and say where it came from. If the context is silent, recommend the most common choice and label it a guess.
- Facts come from the injected context and nowhere else. Search it before you ask, and do not send a sub-agent to find a fact. If the context states a fact, do not ask about it. If it only implies a fact, or answers part of it, ask the user to confirm and cite the part it answers. If it says nothing, the fact is an Open question with an owner. Decisions always go to the user.
- A yes to a guess makes it an Assumption. Only a fact the user states, or a source supplies, is Confirmed.
- The Feeds column is for you. Never say a section code such as A1 or B3 to the user.
- Do not save the grill to disk. The spec holds what was settled.
- There is no round cap. The grill ends when the frontier is empty or the user says "enough".
- Anything left unsettled becomes an Open question in A7 or a row in B13, with an owner: SME, builder or client.
- Write nothing until the user answers "yes" to the restate. "Sounds good" and "whatever you think" are not yes. Ask what they would change. The restate holds everything the spec will say, risks included, so that one yes is the only gate. A reply of "sounds good" to a round is not a gate to chase, because the restate asks again.
- One proposition per question. A question with two parts cannot be accepted with one "yes". Split it, and ask the second in the same round as a separate numbered question.
- Where the context prescribes a schema, a list, a name set or a decision, the spec may extend or change it only in view. Each such addition goes to the user as its own question and appears in the restate under Departures from context.
- **Principles round.** When Systems and data and Constraints are settled, put the relevant principles from [principles.md](principles.md) (or the `--principles` file) to the user in one round. Each carries its default as the recommendation and a one-line consequence for this build. Skip the ones that cannot apply and say which. An override or a skipped principle becomes a B13 row.
- **Decisions are three-way.** For every structural decision, the recommendation names its status: Locked (why), Deferred (what event unlocks it), or Experiment (what kills it). A one-way door is Locked only when an answer is needed to start slice 1. Everything else defers.
- **Backwards compatibility defaults to deferred.** Unless the user says a consumer exists today, record D-compat as Deferred with the trigger "first consumer outside the repo, or first tagged release". Error handling defaults to fail loud.
- On `--mode final`, grill only what is still open after the review input is applied.

## Read the context first

Before round one, pull out the named people and roles, systems, documents, volumes, dates and quoted rules. Each becomes a recommended answer or a Confirmed fact with its source. A fact the context states goes straight into the restate.

If nothing was injected, say so and ask for it. If the user wants to go on without context, the grill is the only source, and no claim is Confirmed until the user states it.

## Tags

Every fact and every recommendation ends up with one of four tags. The restate shows them.

| Tag | Meaning |
|:--|:--|
| Confirmed | The user stated it, or a person or document in the context says it. Name the source |
| Interpreted | Our reading of what the context says |
| Assumption | Our guess |
| Open | Nobody has answered. It has an owner |

## The tree

Start at the top. A branch opens when the branches in its Needs column are settled. Branches with the same Needs can share a round.

| Branch | Needs | Settles | Feeds | Seed question |
|:--|:--|:--|:--|:--|
| Problem and users | None | Who has the problem, what changes for them, why now | A1 | Who uses this day to day, and what do they stop doing by hand? |
| Inputs | Problem and users | Every artefact that comes in, its format, who supplies it | A2, A3, A4 | What arrives, from whom, in what shape? |
| Process and checkpoints | Inputs | The steps, who does each, where a person decides | A3 | Which steps does a person keep, and what do they see when they decide? |
| Outputs | Process and checkpoints | Every artefact that leaves, its format, who receives it | A2, A3, A4 | What leaves, to whom, and what do they do with it? |
| Domain rules | Process and checkpoints | Rules the thing must follow, and the source of each | A5 | Which rules must it never break, and where are they written? |
| Out of scope | Outputs | What is not being built | A6 | What would someone reasonably expect that we are leaving out? |
| Systems and data | Inputs, Outputs | Systems touched, what exists, what is new, where data lives, the stack | B1, B3 | Which systems does it read or write, which already exist, and what is it built in? |
| Model design | Process and checkpoints, Domain rules, Systems and data | Which steps use a model, what goes in and out, grounding, failure | B2, B4, B5 | Which steps need a model, what does each read, and what happens when it is wrong? |
| Integrations | Systems and data | Protocol, auth method, configuration names | B6 | How does each system let us in, and who holds the credentials? |
| Constraints | Systems and data | Hosting, data residency, budget, speed, privacy | B7, B8, B9 | Which limits are fixed before we design anything? |
| Shape and principles | Systems and data, Constraints | Project shape (script, library, tool, app), which principles apply, each structural decision's status, the modules slice 1 needs | B3, B11, B13 | Which of these are one-way doors for this build, and which can wait for a trigger? |
| Risks | Model design, Integrations, Constraints, Shape and principles | What could go wrong, the response, the owner | B12 | What would make this fail in the first month? |
| Acceptance | Outputs, Risks, Shape and principles | How we know it works, the smallest slice that proves it, and what slice 1 may create | B10, B11 | What result lets the SME say it works, and what is the least we must build to show it? |

Not every build uses a model. If the grill shows there is no model call, B4 says `Not applicable.` and gives the reason.

## The restate

When the frontier is empty, write the restate and wait for an explicit yes.

```text
Title, slug, author: {{Title}} / {{slug}} / {{person or team, else Builder team}}
Problem and users:   {{one line}}
People and sources:  {{each named person, role and document, and what it supplied}}
Flow:                {{each step in one line, marking where a person decides}}
Comes in, goes out:  {{artefacts}}
Rules:               {{each rule with its source}}
Systems and stack:   {{new, existing, external; language and runtime, or Open}}
Model use:           {{which steps, or none}}
Volumes and dates:   {{counts, frequencies and deadlines, each with its source}}
Constraints:         {{the binding limits}}
Principles:          {{adopted, overridden, not applicable, each with its reason}}
Decisions:           {{Locked with reason; Deferred with trigger; Experiment with kill condition}}
Slice 1 scaffold:    {{the modules and directories slice 1 may create}}
Out of scope:        {{items}}
Risks:               {{each risk, the response and the owner}}
Acceptance:          {{the first slice and its done-when}}
Open questions:      {{each with an owner}}
Departures from context: {{each place the spec adds to or changes what the context prescribes, or none}}
Design source:       {{path, skill, spec folder or neutral}}
First read it differently: {{where the first inference diverged, or no divergence}}
Mode:                {{draft or final}}
```
