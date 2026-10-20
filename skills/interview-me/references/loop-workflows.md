# Loop workflows

Read this when grilling aims at **workflow specs** for recurring loops in the user's life or work (trigger: "loop me", or a request to design a workflow within a workspace). Apply the Rounds discipline from `SKILL.md` with the vocabulary and output target below.

Derived from `skills/in-progress/loop-me/SKILL.md` in mattpocock/skills (MIT). See NOTICE.

## Vocabulary

- A **loop** is a recurring pattern in the user's life: their career, their week, their morning, a single repeated activity. Picturing a life as loops within loops reveals how predictable its activities really are, which is what makes them worth **delegating**. Use the lens to find loops worth specifying, and propose ones the user hasn't noticed.
- A **workflow** is the spec of one loop, made real. You run a workflow on a loop: the loop is its running instantiation. Workflows live in `workflows/*.md` and are the source of truth.
- **Trigger**: what fires each run, an **event** (a new email, a new issue) or a **schedule** (every morning). Event-triggering is usually the more efficient.
- **Checkpoint**: a human-in-the-loop point where the user is asked to verify or decide. Some workflows have none and run autonomously; some use no AI at all.
- **Push right**: defer the checkpoint as far as it will go. Do maximal work before involving the human, so they are asked once, late, with everything prepared.
- **Brief**: what a checkpoint presents, a tight, decision-ready summary (what was produced, why, and a link down to the asset itself), never the raw output. The user reads a brief, not a draft. Speed of review is imperative.

Reach for this vocabulary only when a workflow calls for it, never as a checklist. A workflow needs no AI, no checkpoint and no schedule unless the grilling shows it does.

## Done

A workflow spec is done when an implementer agent could build it without asking a single question. Grill until then.

## Workspace

- `workflows/*.md`: one spec per workflow.
- `NOTES.md`: raw notes on the user's world, tools, channels and their own terminology. When it is empty or thin, interview them about their world before specifying anything. Sharpen fuzzy terms into canonical ones as they surface, and record them here.
