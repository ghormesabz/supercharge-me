# Hand-off

At `--mode final`, the spec already sits in the repo it seeds, at `docs/spec/SLUG/`. Hand-off writes the brief the coding agent reads, then offers two optional files.

## `AGENTS.md` and `CLAUDE.md` (always, at `OUT`)

1. Copy `assets/AGENTS.template.md` to `OUT/AGENTS.md`. Replace `{{SPEC_PATH}}` with `docs/spec/SLUG` and change nothing else. The file is rules only, so it does not change as the project does: no directory tree, no module list, no status, no versions, no commands. The register holds the project's decisions and the toolchain holds its commands.
2. Write `OUT/CLAUDE.md` as one line: `@AGENTS.md`.
3. If either file already exists, show the user what would change and ask before replacing it.

`check-spec.sh` confirms `AGENTS.md` has no `{{`, is 60 lines or fewer, and that `CLAUDE.md` is the one-line import.

To add a project-specific rule, put it in B13 or the slice Scaffold, never in `AGENTS.md`.

## Optional files

Offer these as a numbered list in plain text. The user ticks the numbers they want. Do only what is ticked. Never create a README, a commit or a GitHub repo, and add no scaffolding beyond what is ticked.

1. `.gitignore` and `.env.example` at `OUT`.

`.gitignore` lists `.env`, `.venv/` and `__pycache__/`. If the file exists, append only the lines it lacks.

`.env.example` has one line per variable name in B6, each with an empty value, for example `CASE_SYSTEM_API_KEY=`. Never write a real value.

Repo initialisation is not a hand-off step. It happens at the draft's commit-and-tag step, with `uv init --bare --vcs git` for a Python stack.
