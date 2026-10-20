# mahan-skills

Skills for converging with the model before building. A grill settles intent, a house HTML format makes Quarto output look designed, and a spec creator fixes the expensive structural decisions and defers the rest, so the coding agent's first scaffold is small and correct.

Version 0.2.0. MIT.

| Skill | Invoked by | Does |
|:--|:--|:--|
| `interview-me` | the model, on build, idea, plan or design asks where its first reading could differ from yours | Sequential or rounds grill that ends in a restate you confirm with an explicit yes |
| `quarto-authoring` | the model, when an HTML deliverable is needed | The `house-html` Quarto format: one reading column, one accent, flat surfaces, light and dark. Frontmatter is five lines |
| `spec-creator` | you: `/mahan-skills:spec-creator` | Grill, then `spec.qmd` with a decision register, then HTML for reviewers and builders, then `AGENTS.md` for the agent |
| `handoff` | the model, on "hand this over" or "I'm out of context"; or you: `/mahan-skills:handoff` | Saves goal, decisions, files, open questions and next steps as XML in the temp folder. A new session in the same folder is offered it at start |

## spec-creator

```
/mahan-skills:spec-creator [context] [--mode draft|final|check] [--design NAME|PATH]
                           [--principles PATH] [--out DIR] [--slug SLUG] [--help]
```

Flags are read from chat, so plain English works ("do the final pass"). Output lands in `OUT/docs/spec/SLUG/`:

- **draft**: `spec.qmd` and `design-review.html`, a working document to answer solo or in an interview.
- **final**: `design-sheet.html` for non-builders, `build-spec.html` for builders, plus `AGENTS.md` and `CLAUDE.md` (`@AGENTS.md`) at the repo root.

Every structural decision is Locked with a reason, Deferred with a trigger, or an Experiment with a kill condition. Slice 1 gets a scaffold budget. Errors fail loud until the register says otherwise. After hand-off only the register changes; `AGENTS.md` never does.

Design systems change colours, fonts and a logo only (`--design`). Principles are shipped defaults in `skills/spec-creator/references/principles.md`; `--principles` swaps them.

## handoff

Writes one XML file per folder to the system temp folder (`$TMPDIR/mahan-skills/handoff-<hash of the folder's real path>.xml`, or `$MAHAN_HANDOFF_DIR`). `scripts/handoff.py write` rejects XML that is not well-formed and stamps `created`, `workspace`, `branch` and `head` itself. A `SessionStart` hook (`startup` and `clear`) tells the model a handoff is waiting for the folder; it reads the file only after you say yes, then deletes it.

## Install

```
claude plugin marketplace add ./mahan-skills      # or <owner>/mahan-skills from GitHub
claude plugin install mahan-skills@mahan
```

To try it for one session: `claude --plugin-dir ./mahan-skills`.

## Requirements

Quarto 1.7 or later, git, Python 3.9 or later. Optional: `uv` (initialises a Python project at the commit step), Chrome or Chromium (figure screenshots). A `SessionStart` hook warns when a required tool is missing; `bash scripts/preflight.sh --full` checks everything.

## Check it works

```
bash scripts/render-example.sh        # renders the worked example in a scratch folder
bash scripts/check-spec.sh SPEC_DIR   # mechanical done-checks on a spec folder
bash scripts/figure-shots.sh HTML     # one PNG per figure
```

## Add a skill

Drop `skills/<name>/SKILL.md` in this folder. Set `disable-model-invocation: true` for skills only you should run. Bump `version` in `.claude-plugin/plugin.json`.

## Licence

MIT. Portions derive from Matt Pocock's skills (also MIT); see `NOTICE`.
