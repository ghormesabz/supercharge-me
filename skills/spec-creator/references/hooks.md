# Hooks and preflight

This skill calls other skills and checks the tools they need before it reads the context or asks a question. A missing hook stops the run. Do not write a substitute.

## The hooks

| Hook | What it does here | Needed |
|:--|:--|:--|
| `supercharge-me:quarto-authoring` | Installs the house format, Quarto mechanics, render errors | Always |
| `supercharge-me:interview-me` | The grill, in Rounds Mode, before the first draft | Always. On `--mode final`, only when answers are still open |
| The skill named in `--design` | Tokens and fonts for the document | Only when `--design` names a skill |

Both bundled skills ship in this plugin. If either is missing from the skill list in your context, the plugin is incomplete: stop, name it, and ask the user to reinstall `supercharge-me`.

## Preflight

1. Run `bash PLUGIN/scripts/preflight.sh --full`. It prints only problems and exits 1 when a required tool is missing. Required: Quarto 1.7 or later, git. Optional notes: `uv` (Python projects), Chrome or Chromium (figure check).
2. If a required tool is missing, stop. Relay the message and ask the user to install it and run the skill again.
3. If `--design` is absent, skip this step. Otherwise read its value (see [design.md](design.md)). If it names a skill, check that one is in the skill list too.

## Calling a hook

Call the Skill tool with the hook's name.

**`supercharge-me:quarto-authoring`.** Use it for how Quarto works and to install the house format. Its frontmatter, conventions and branding sections apply to documents in general. Where this skill's template and `figures.css` disagree with it, this skill wins.

**`supercharge-me:interview-me`.** Hand it the question tree in [grill-seed.md](grill-seed.md) and the injected context. The rules in `grill-seed.md` override the hook where they differ. The grill needs a live user to answer. If nobody is there, stop and say so. Never answer for the user.

**Design skill.** Called in the design step. See [design.md](design.md).
