---
name: spec-creator
description: Grill a build idea into a scoping spec that fixes the expensive structural decisions and defers the rest, render a design review, design sheet and build spec, and write AGENTS.md for the coding agent.
argument-hint: "[context paths or pasted text] [--mode draft|final|check] [--design NAME|PATH] [--principles PATH] [--out DIR] [--slug SLUG] [--help]"
disable-model-invocation: true
---

# Spec creator

Turns a fuzzy build idea into a spec the coding agent can start from without over-building. Every structural decision is **Locked** with a reason, **Deferred** with a trigger, or an **Experiment** with a kill condition. Slice 1 carries a scaffold budget: the agent creates what the slice names and nothing else.

Everything lands under `OUT/docs/spec/SLUG/`, where `OUT` is the repo root:

| File | When | Holds |
|:--|:--|:--|
| `spec.qmd` | always | The single source of truth. The coding agent reads this |
| `design-review.html` | draft | Part A and Part B with a draft banner. A working document: answer A7 and the register inline, solo or in an interview |
| `design-sheet.html` | final | Part A only, for people who do not build |
| `build-spec.html` | final | Part A and Part B, for builders |
| `OUT/AGENTS.md`, `OUT/CLAUDE.md` | final | Rules-only brief for the coding agent. `CLAUDE.md` is the one line `@AGENTS.md` |
| `figures.css`, `tokens.css`, `render.sh`, `_extensions/house/` | always | Layout, design overrides, render command, house format |

The figures carry the spec. They show what comes in, what goes out and what happens between, so a reader can check the process without reading the text. HTML is for people. The agent reads `spec.qmd` and `AGENTS.md`.

In this file, `assets/` and `references/` are in `${CLAUDE_SKILL_DIR}`, and scripts are in `${CLAUDE_PLUGIN_ROOT}/scripts/`. The reference files write the folder holding that `scripts/` as `PLUGIN`, so `PLUGIN/scripts/preflight.sh` is `${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh`. Run commands from `OUT`.

## Flags

`/supercharge-me:spec-creator [context] [--mode draft|final|check] [--design VALUE] [--principles PATH] [--out DIR] [--slug SLUG] [--help]`

| Flag | Meaning |
|:--|:--|
| `--mode draft` | Default. Grill, write, render the design review |
| `--mode final` | Fold the review back in, render the design sheet and build spec, write `AGENTS.md`. See [references/final-pass.md](references/final-pass.md) |
| `--mode check` | Run the checks on an existing spec. Writes nothing |
| `--design VALUE` | A path to a design file or folder, or the name of a design skill. See [references/design.md](references/design.md) |
| `--principles PATH` | Replace the shipped [references/principles.md](references/principles.md) |
| `--out DIR` | Repo root. Default: the current directory |
| `--slug SLUG` | Kebab-case name, matching `^[a-z0-9]+(-[a-z0-9]+)*$`. Default: derived from the title and agreed at the restate |
| `--help` | Print this table and stop |

The user types flags in chat, so read them as an LLM would, not as a parser:

1. Echo one line before acting: `Parsed: mode=draft, out=., design=neutral, principles=shipped, slug=to be agreed`. It is not a gate.
2. Map plain English to the flag: "do the final pass" is `--mode final`, "just check it" is `--mode check`.
3. Ask when the mode is unclear, because the mode decides what gets written. For any other flag, state the assumption and go on.
4. Ask about an unknown flag. A typo in chat is likelier than a flag that does not exist. Quote a `--design` path that has spaces.

## Context

Context is what the user pastes or names by path: files and folders. A folder means its text files, up to 200 KB each and 2 MB in total; list what you read and what you skipped. Skip a binary inside a folder and say so. A binary file the user names directly (DOCX, PDF, XLSX, PPTX) stops the run: name it and ask for text or markdown. Never convert files yourself. Read nothing else. Greenfield is the target; reading an existing codebase is out of scope.

## Draft flow

1. **Parse.** Echo the parsed flags. `--help` prints the table and stops.
2. **Preflight.** Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/preflight.sh --full`. A non-zero exit stops the run: relay its message. Then load the hooks per [references/hooks.md](references/hooks.md). A missing hook stops the run.
3. **Context.** Read what the user supplied. If it holds a secret, follow the Rules before you ask anything.
4. **Grill.** Call `supercharge-me:interview-me` in Rounds Mode with the tree in [references/grill-seed.md](references/grill-seed.md). It ends with a restate. Wait for an explicit yes before writing anything.
5. **Design.** Follow [references/design.md](references/design.md). Write `tokens.css`.
6. **Write.** `mkdir -p OUT/docs/spec/SLUG`. Follow `supercharge-me:quarto-authoring` Workflow step 1 to install the house format into that folder. Copy `assets/spec-template.qmd` to `spec.qmd`, and `assets/figures.css` and `assets/render.sh` beside it. Fill every placeholder. Part A: [references/part-a.md](references/part-a.md). Part B: [references/part-b.md](references/part-b.md). Figures: [references/figures.md](references/figures.md). The section lists are fixed and never renumbered.
7. **Render and check.** `bash OUT/docs/spec/SLUG/render.sh`, then `bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-spec.sh OUT/docs/spec/SLUG` and the manual checks below. Fix and re-render until the script exits 0.
8. **Report.** List the files and sizes; the number of claims at each tag; the Open questions with owners; the register counts (Locked, Deferred, Experiment, Open); the design source and any tokens left at the default; anything skipped, such as the figure check without a browser. If the design names a web font, say that the viewer's browser fetches it.
9. **Commit, tag, init: only on a yes.** If `OUT` is not a git repo and the grilled stack is Python, offer `uv init --bare --vcs git` in `OUT` (never plain `uv init`, which adds `main.py` and `README.md`). For any other stack, ask which init to run. Check `git tag -l spec-SLUG-draft`. Ask in plain text: commit `docs/spec/SLUG/` and tag it `spec-SLUG-draft`? If the tag exists, say the question moves it. Do nothing until the user says yes. Then run `git add docs/spec/SLUG && git commit -m "Add SLUG scoping spec for review" -- docs/spec/SLUG` and `git tag spec-SLUG-draft` (`git tag -f` only when the yes covered the move). `--mode final` compares against that tag.

## Final flow

Follow [references/final-pass.md](references/final-pass.md), then [references/handoff.md](references/handoff.md).

## Check flow

Run `check-spec.sh` on the spec folder and report each line. Writes nothing.

## Rules

- Never invent a name, quote, date, number, decision or sign-off. A claim with no source is an Assumption or an Open question.
- Never write a secret into the spec. Variable names only. If the context holds a key, token, password or connection string, say so in your first message, before any question: name the variable, never repeat the value, and tell the user it is exposed and to rotate it, even if they call it a test value.
- Never commit or tag without an explicit yes. Write only inside `OUT/docs/spec/SLUG/`, plus `OUT/AGENTS.md` and `OUT/CLAUDE.md` at `--mode final`, any hand-off file the user ticked, and scratch files in a `mktemp -d` folder that you delete after. Ask before replacing a file that existed before this run.
- Send the context and the spec to no outside service.
- Ask grill questions in plain chat text, each with a recommended answer.
- Fail loud. A spec that hides a failure path behind a quiet fallback has made a structural decision without recording it. Failure rows say who sees the failure and how.

## Writing

- Short, plain sentences. Active voice. Say who does what.
- Australian English. `lang: en-AU` is in the template. Change it only if the design source asks for another locale.
- Define each acronym on first use in Part A, and again on first use in Part B. These need no definition: SME, IT, ID and URL everywhere, and API, REST, JSON, SQL, HTTPS, UI and LLM in Part B.
- No em dashes. No hype words (delve, leverage, utilise, robust, streamline, facilitate, empower, seamless, cutting-edge). No filler adverbs (just, simply, actually, literally), throat-clearing openers, recap at the end of a section, or closing flourish.
- Part A uses the expert's words. Part B names things as the code will.
- A number needs a source or a tag.

## Done-checks

`check-spec.sh` runs the mechanical checks and prints `PASS`, `FAIL`, `REVIEW` or `MANUAL` per line; it exits 1 on any `FAIL`. Do the `REVIEW` and `MANUAL` lines yourself and report each.

| Line | Check |
|:--|:--|
| Outputs | The HTML for the mode exists. `design-review.html` on draft; `design-sheet.html` and `build-spec.html` on final |
| Placeholders | `spec.qmd` holds no `{{` and no `<!--` |
| Part B | Absent from `design-sheet.html`, present once in the others. If both show Part B, the installed Quarto ignores `when-meta`: stop and tell the user |
| Banner | Present in `design-review.html`, absent in the final copies |
| A3 and A4 (`MANUAL`) | Every artefact in the `.in` and `.out` lanes is a row in A4 with the same words, and every A4 row is in a lane |
| Builder terms (`REVIEW`) | No builder terms in Part A. Each hit is replaced, or is a term the expert used and is glossed on first use. List those hits in the report |
| Figures (`MANUAL`) | Run `bash ${CLAUDE_PLUGIN_ROOT}/scripts/figure-shots.sh` per [references/figures.md](references/figures.md) and look at every PNG. Without a browser, say so |
| Size | Each HTML is 3,000,000 bytes or less |
| Writing | No em dashes or hype words. Filler adverbs print as `REVIEW`: cut each hit unless it carries emphasis or contrast |
| Secrets | No key, token, password or connection string value |
| Register | B13 holds only valid statuses. Every Deferred row names a trigger, every Experiment a kill condition |
| Hand-off (final) | `AGENTS.md` exists at `OUT`, 60 lines or fewer, and `CLAUDE.md` is `@AGENTS.md` |

## References

| File | Read it when |
|:--|:--|
| [references/hooks.md](references/hooks.md) | Running the preflight and calling the other skills |
| [references/grill-seed.md](references/grill-seed.md) | Running the grill and writing the restate |
| [references/principles.md](references/principles.md) | Walking principles in the grill and writing the register |
| [references/design.md](references/design.md) | Handling `--design`, deriving tokens, checking contrast |
| [references/part-a.md](references/part-a.md) | Writing A1 to A7 and tagging claims |
| [references/part-b.md](references/part-b.md) | Writing B1 to B13 and the model call cards |
| [references/figures.md](references/figures.md) | Drawing the four figures, Pandoc rules, checking the render |
| [references/final-pass.md](references/final-pass.md) | Running `--mode final` |
| [references/handoff.md](references/handoff.md) | Writing `AGENTS.md` and the optional hand-off files |
| `assets/example/spec.qmd` | Before drawing the first figure. A worked spec with invented data. `bash ${CLAUDE_PLUGIN_ROOT}/scripts/render-example.sh` renders it. Never copy its names or data into a real spec |
