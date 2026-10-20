<h1 align="center">supercharge-me</h1>

<p align="center">
  <em>A plugin to help cross the context gap between domain SMEs, builders, and agents</em>
</p>

---

You hand the agent a folder of domain notes and a one-line ask. It starts scaffolding straight away: a database layer, an auth module, a plugin system, a config loader. None of it came from you. It came from the agent's guess about what a project like yours usually needs.

Then you are stuck. Every later session reads that scaffold as fact and builds on it. The rules got baked in before anyone agreed to them, and you spend the project working around them.

supercharge-me closes that gap. WIP toolkit with the purpose of accelerating builds especially when interfacing between domain/builders. 

## Before / after

You ask for "a dashboard for the intake team".

**Without it**, the agent picks a framework, invents the metrics, adds user accounts and charts, and writes thirty files. A week later you find out the team wanted one number in standup.

**With it**, `interview-me` writes down its first guess and how sure it is, then asks one question at a time, each with its guess attached. Who reads it? What decision does it change? What does good look like, as a number? It ends with a restate, including what is out of scope and where its first reading was wrong, and waits for your explicit yes. `spec-creator` turns that into a spec where user accounts are **Deferred** until a named trigger fires, so slice 1 builds the one number and nothing else.

## The skills

### interview-me

The model calls it on its own when a build, plan or design ask could mean more than one thing. **Sequential** mode asks one question at a time. **Rounds** mode works a whole tree of linked decisions, asking every question it can answer now in one round. Both attach a recommended answer to each question, look up facts themselves instead of asking you, and stop only at a restate you confirm. "Sounds good" does not count as yes.

### spec-creator

You run it: `/supercharge-me:spec-creator`. It grills you with `interview-me`, then writes `spec.qmd` and renders it.

- **Draft** gives a `design-review.html` for reviewers to answer, solo or in a meeting.
- **Final** folds the review back in and writes a `design-sheet.html` for people who do not build, a `build-spec.html` for people who do, and `AGENTS.md` plus `CLAUDE.md` at the repo root for the coding agent.

Every structural decision in the register is **Locked** with a reason, **Deferred** with a trigger, or an **Experiment** with a kill condition. Slice 1 gets a scaffold budget. Errors fail loud until the register says otherwise. After hand-off only the register changes; `AGENTS.md` never does.

### quarto-authoring

The model calls it when you need an HTML deliverable: a report, memo, briefing note or one-pager. It installs the `house-html` Quarto format: one reading column, one accent, flat surfaces, light only. Frontmatter is five lines because the design lives in the format. A `tokens.css` swaps in your brand's colours, fonts and logo, and nothing else.

### handoff

Say "hand this over" or "I'm out of context", or run `/supercharge-me:handoff`. It saves the goal, decisions, files, open questions, next steps and rejected options as one XML file. The next session you open in the same workspace is told one is waiting, and reads it only after you say yes.

## How it works

```
idea ─► interview-me ─► spec-creator draft ─► review ─► spec-creator final ─► AGENTS.md ─► build slice 1
          (restate,        (spec.qmd,                     (design sheet,
           explicit yes)    design review)                 build spec)

handoff: any time a session runs long; the next session picks it up
```

Each step stops before writing anything until you say yes, and nothing is committed without your yes. The register is the one place decisions live, so the agent asks before it guesses a structural decision.

## Install

In Claude Code, as two separate prompts:

```
/plugin marketplace add ghormesabz/supercharge-me
```
```
/plugin install supercharge-me@supercharge-me
```

From a local clone: `claude plugin marketplace add ./supercharge-me`, then the same install. To try it for one session without installing: `claude --plugin-dir ./supercharge-me`.

### Requirements

Built for Claude Code on macOS with bash.

| Tool | Needed for |
|:--|:--|
| Quarto 1.7 or later | `spec-creator`, `quarto-authoring` |
| Python 3.9 or later | `handoff` and its session-start hook |
| `uv` (optional) | Initialising a Python project at the commit step |
| Chrome or Chromium (optional) | Figure screenshots in the spec check |

## Commands

| Command | What it does |
|:--|:--|
| `/supercharge-me:spec-creator` | Grill, then write and render the spec. Defaults to a draft |
| `/supercharge-me:spec-creator --mode final` | Fold the review back in, render the final copies, write `AGENTS.md` |
| `/supercharge-me:spec-creator --mode check` | Run the checks on an existing spec. Writes nothing |
| `/supercharge-me:handoff` | Save this session for the next one |

`interview-me` and `quarto-authoring` have no command; the model calls them when they fit. Ask for them by name if it does not.

`spec-creator` flags:

```
/supercharge-me:spec-creator [context] [--mode draft|final|check] [--design NAME|PATH]
                             [--principles PATH] [--out DIR] [--slug SLUG] [--help]
```

Flags are read from chat, so plain English works: "do the final pass" is `--mode final`. Output lands in `OUT/docs/spec/SLUG/`. `--design` changes colours, fonts and a logo only. `--principles` swaps the shipped defaults in `skills/spec-creator/references/principles.md`.

## Check it works

```
bash scripts/preflight.sh --full      # required and optional tools
bash scripts/render-example.sh        # renders the worked example spec in a scratch folder
bash scripts/check-spec.sh SPEC_DIR   # mechanical done-checks on a spec folder
bash scripts/figure-shots.sh HTML     # one PNG per figure, to look at
```

## FAQ

**Does it work with other agents?**
No. It is built and tested for Claude Code on macOS. The skills are plain Markdown, so they may work elsewhere, but nothing outside Claude Code is supported.

**Do I need Quarto for everything?**
No. `interview-me` and `handoff` need no Quarto. Only the HTML skills do.

**Why does it ask so many questions?**
Four to six questions cost minutes. A wrong scaffold costs the project. It stops once it can predict how you would answer its next three questions.

**Where does the handoff go?**
One file per workspace in the system temp folder: `$TMPDIR/supercharge-me/`. The workspace is the enclosing git root, or the folder itself outside a repo. macOS clears temp files that go unused for about three days, so set `SUPERCHARGE_HANDOFF_DIR` to keep them longer. The skill never writes secrets into it, and the file is deleted once picked up.

**Why does `AGENTS.md` never change?**
It holds rules only. The project's decisions live in the spec's register, and its commands live in the toolchain. A brief that never changes cannot drift out of date.

## Add a skill

Drop `skills/<name>/SKILL.md` in this folder. Set `disable-model-invocation: true` for skills only you should run. Bump `version` in `.claude-plugin/plugin.json`.

## Licence

MIT. Portions derive from Matt Pocock's skills (also MIT); see [NOTICE](NOTICE).
