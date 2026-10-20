---
name: interview-me
description: Converges you and the model on what is actually wanted before anything is built. Use for any build, feature, idea, plan or design ask, especially when the model's first reading of the prompt could differ from the user's intent, or the ask omits who it is for, why now, what success is, or the binding constraint. Also on "interview me", "grill me", "stress-test this". Skip for unambiguous mechanical edits, pure information questions, and non-interactive runs.
---

# Interview me

User and model hold the same picture of the ask before anything exists. Done means the user has confirmed a written restate with an explicit yes.

People ask for "a dashboard" because that is what one asks for, and say "faster" with no number to hit. The cheapest moment to find that gap is before a plan, spec or code exists. Once building starts, the user rationalises the wrong thing into a good-enough thing and the misfit locks in.

## Mode

- **Sequential** (default): one linear ask. One question at a time, each with your guess attached.
- **Rounds**: a plan, decision or design with branching, interdependent sub-decisions. Use it on "grill me" language, or when sequential would take too many round trips. Work the design tree and ask a whole frontier per round.

Both modes attach a guess to every question, treat facts as your job and decisions as the user's, and stop only at shared understanding. When another skill hands you a question tree and rules (spec-creator does), run Rounds on that tree. Its rules win where they differ.

A live user must be present. In CI, `/loop` or any scheduled run, name the underspecification as a blocker and stop.

## Step 1: First inference

Before any question, write what you would assume and build if you had to start now, with an honest confidence number:

```
FIRST INFERENCE: You want a way to answer "how are we doing?" in standup; "dashboard" was the convention that came to mind.
CONFIDENCE: ~30% - missing: who it is for, what "metrics" means here, what success looks like
```

Below ~70%, say what is missing. The number is honest when you can predict the user's reaction to your next three questions. Keep the first inference: the restate compares against it.

## Sequential steps

**Ask.** One focused question, with the guess and the reasoning behind it:

```
Q: <one question>
GUESS: <your answer, and why>
```

Wait for the reaction before the next question. A wrong guess draws a correction faster than an open question draws an answer. Guess in a direction you expect to be corrected at least once, so agreement stays honest.

**Listen for want versus should-want.** Answers that sound like best practice ("scalable", "clean architecture", "the standard way", "I should probably") are the dangerous ones. Probe each with: *"If you didn't have to justify this to anyone, what would you actually want?"*

**Restate** when confidence is high (5 to 8 lines, the user's own words where possible):

```
Here is what I now think you want:

- Outcome:      <one line>
- User:         <who benefits>
- Why now:      <what changed>
- Success:      <how we know it worked>
- Constraint:   <the binding limit>
- Out of scope: <what we are not doing>
- First read it differently: <where your first inference diverged from the above, or "no divergence">

Yes / no / refine?
```

"Out of scope" and "First read it differently" are both required. Silent disagreement about non-goals and unexamined divergence are the two main ways a yes turns hollow.

**Confirm.** The gate is an explicit "yes". Each of these is something else:

| Reply | Meaning | Next move |
|---|---|---|
| "Whatever you think is best" | Delegation. They lack 95% confidence too | Re-ask with two concrete options as a choice |
| "Sounds good" / "Sure, let's go" | Ambiguous, often a polite exit | Ask: "Anything you'd refine?" |
| Silence, then "okay, start" | They gave up, not converged | Stop and ask what you missed |

A correction is folded in, then you restate again. Loop until the explicit yes.

## Rounds mode

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, docs), find it yourself before asking, then ask the rest of the frontier. The _decisions_ are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch visited, nothing left silently assumed. Write the restate in the shape above, over the whole settled tree, and wait for the explicit yes. Act on nothing before it.

Grilling aimed at workflow specs for recurring loops ("loop me")? Read [references/loop-workflows.md](references/loop-workflows.md).

## Stop

You are done when you can predict the user's reaction to the next three questions you would ask. If you cannot after several rounds, that is information about the ask. Say: "I've asked N questions and still can't predict your reactions. Something foundational is missing. Want to step back and reframe?"

## Output

A confirmed statement of intent: the sequential restate, or the settled tree and its restate. Specs, plans and tasks consume it downstream.

Offer to save it to `docs/intent/[topic].md` for multi-session work or a handoff, and save only after the explicit yes. If the ask is a build, offer the user `/supercharge-me:spec-creator` with the restate as context; it is user-invoked, so the user runs it.

## Common rationalisations

| Thought | Reality |
|---|---|
| "The ask is clear enough" | If you cannot write the desired outcome in one sentence, it is not. Run Step 1 |
| "Questions waste their time" | Four to six targeted questions cost little. Building the wrong thing costs the user everything |
| "I'll figure it out as I build" | Switching costs after code exists run about 10x. Discovery during build is rework |
| "I'll give them options to pick from" | Options suit someone who knows what they want. Asking narrows; listing widens |
| "Attaching my guess leads them" | Leading is the point. The risk is sycophancy; stay visibly willing to be wrong |
| "We've talked enough, I get it" | Predict their reaction to the next three questions. If you cannot, you do not |
| "They said yes, we're done" | A yes after a vague restate is hollow. Restate concretely and re-confirm |

## Red flags

- Sequential mode: three or more questions in one message. That is batching, not interviewing.
- A question without your guess or recommendation attached.
- "Whatever you think" accepted as a terminal answer.
- A spec, plan or task list produced before the explicit yes.
- "Scalable", "clean" or "modern" accepted as an answer without the *actually want* probe.
- Three rounds without your confidence visibly rising: reframe instead of asking more.
- A confidence number below ~70% with no stated gap.
- The intent doc saved before the yes.
- A restate missing "Out of scope" or "First read it differently".
