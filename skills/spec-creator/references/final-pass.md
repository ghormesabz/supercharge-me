# `--mode final`: after the review

`--mode final` folds the review back into the spec, in place. It edits `docs/spec/SLUG/spec.qmd`, not a copy, then renders the design sheet and the build spec and writes `AGENTS.md`.

## Preconditions

Refuse and say what is missing if any of these fail.

1. `docs/spec/SLUG/spec.qmd` exists and has `spec-draft: true`. If the repo holds several specs and the user did not name one, ask which.
2. The tag `spec-SLUG-draft` exists. Check with `git tag -l spec-SLUG-draft`.
3. There is review input: a non-empty diff against the tag, pasted notes, or both.

Review input is the reviewers' edits to the working tree since the tag, plus anything the user pastes: meeting notes, email answers, a marked-up copy, answers written into A7 and B13 of the design review.

## Steps

1. Read. Run `git diff --stat spec-SLUG-draft -- docs/spec/SLUG/`, then `git diff spec-SLUG-draft -- docs/spec/SLUG/spec.qmd` for the content. Read the pasted notes. For each change, note where, what the draft said, what it says now, and the source. Edit nothing yet.
2. Plan the change set. List every edit: what the review decided, which Assumption, Interpreted or Open claims it confirms, which A7 rows it answers, which B13 rows move, and what cascades into Part B (A3 and A4 against B2 and B5, rules against B4 guardrails and B10, scope against B1 and B3, a decision against the module map and the slice Scaffold). Keep edits already in the working tree. If a note and an edit disagree, ask.
3. Grill and restate. Hand what is still open to `supercharge-me:interview-me` under the rules in [grill-seed.md](grill-seed.md). Then restate the whole change set and wait for an explicit yes. Write nothing before it.
4. Apply the change set.
5. Flip tags. A reviewer-confirmed Assumption, Interpreted claim or Open item becomes Confirmed, with its source. Add a date only when the review input gives one. A rejected claim is rewritten. Add names only if the user supplies them.
6. Fill the Answer column in A7 from the review input. A row nobody answered stays empty, and its claim is tagged Open with an owner.
7. Update B13. A decision the review settled moves to Locked with its reason, or stays Deferred with its trigger. An Experiment keeps its kill condition. A row nobody answered stays Open with an owner. Nothing becomes Locked on silence.
8. Insert the change log (below) after the legend and before `# For domain review`.
9. Fill the sign-off Decision and Date only from what the user gives. Never invent a sign-off.
10. Set `spec-draft: false`. That removes the banner.
11. Re-render with `render.sh`, which now writes `design-sheet.html` and `build-spec.html` and removes `design-review.html`. Run `check-spec.sh`. The final copies must show no banner.
12. Write `AGENTS.md` and `CLAUDE.md` at `OUT`, following [handoff.md](handoff.md).
13. Report what changed. Ask whether to commit `docs/spec/SLUG/` and the two agent files, and commit only after a yes: `git add docs/spec/SLUG AGENTS.md CLAUDE.md && git commit -m "Apply review to SLUG scoping spec" -- docs/spec/SLUG AGENTS.md CLAUDE.md`. Do not tag. Then offer the optional hand-off files in [handoff.md](handoff.md).

## The change log

Part A changes go in the first table. Part B changes go in the second, inside the builder-only block, so the design sheet carries no build detail.

```markdown
# What the review changed {#changes}

| Where | Draft said | Now says | Source |
|:------|:-----------|:---------|:-------|
| {{A5, rule 2}} | {{Text in the draft}} | {{Text now}} | {{Person and date, or document}} |

::: {.content-visible when-meta="builder"}

| Where | Draft said | Now says | Source |
|:------|:-----------|:---------|:-------|
| {{B13, D2}} | {{Text in the draft}} | {{Text now}} | {{Person and date, or document}} |

:::
```

Drop a table that has no rows. If nothing changed in a part, write `No changes.` under its heading.
