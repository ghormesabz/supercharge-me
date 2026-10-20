---
name: quarto-authoring
description: Use when producing an HTML deliverable from Markdown or a .qmd, such as a report, briefing note, memo, spec or one-pager that must look designed rather than default. Also when another skill needs a rendered HTML page. Skip for slides, spreadsheets, PDFs, and quick answers that stay in chat.
---

# Quarto authoring

One `.qmd` becomes one self-contained HTML file in the **house** format: a single reading column, one accent, flat surfaces, system fonts, light only. The frontmatter stays at five lines because the design lives in an installed Quarto format extension.

## Prerequisites

- Quarto 1.7 or later (`quarto --version`). No TeX, no network at render time: fonts are the system stack and `embed-resources` inlines everything.
- No Quarto? Write the `.qmd`, install the format, and hand back `quarto render FILE.qmd` as the one command to run.

## Workflow

1. **Install the format** beside the document: `bash ${CLAUDE_SKILL_DIR}/scripts/install-house.sh DIR`. It writes `DIR/_extensions/house/` and refuses to replace a different copy.
2. **Start from the template** in [assets/template.qmd](assets/template.qmd).
3. **Author the body** to the conventions below.
4. **Render**: `quarto render DIR/FILE.qmd`. Output is `DIR/FILE.html`.
5. **Check**: the render exits 0, the HTML exists, and `grep -c '{{' DIR/FILE.qmd` prints 0.

Done is the HTML on disk and the three checks passing. Report the output path.

## Frontmatter

```yaml
---
title: "Document title"
subtitle: "Context line"
author: "Author"
date: last-modified
format: house-html
---
```

Switches, all optional: `toc: true` for documents past two pages (the contents sit in the right margin), `number-sections: true` for formal reports, `date: "24 June 2026"` for a fixed date.

Set the design in `format: house-html` and nowhere else. Keep colour, font and layout out of the `.qmd`.

## Authoring conventions

- Australian English (organise, analyse, programme), sentence-case headings. Change `lang` in frontmatter for another locale.
- Lead with the decision or finding, in active voice. Cut hype words (*revolutionary, game-changing, seamless*).
- No emoji.
- **Cards are callouts.** Always give one a title. `.callout-note` and `.callout-tip` get the accent dot, `.callout-warning` and `.callout-caution` the amber dot, `.callout-important` the red dot. The format renders all of them as the same flat card.
- **Tables are plain Markdown** with a header row. Right-align numeric columns with `--:`. Relative widths follow the dash counts in the separator row.
- Reach for a figure or table before a paragraph of numbers.

## Branding

A design system changes colour roles, font families and a logo, and nothing else. Write the overrides to a `tokens.css` beside the document and add `css: tokens.css` to the frontmatter. The token names, defaults and contrast rules are in [references/tokens.md](references/tokens.md). Another skill can derive that file from a brand source.

## When rendering fails

- `Unknown format house-html`: step 1 was skipped, or the `.qmd` is not under the folder holding `_extensions/`.
- A fenced div shows as literal `:::`: a blank line is missing before it, or the opening line has attributes outside braces.
- `{{` in the output: a template placeholder was left unfilled.
- Anything else: read the Quarto error in full, then the matching digest below.

## References

| Read it when |  |
|:--|:--|
| Setting TOC, numbering, anchors, links, embedding | [references/html-options.md](references/html-options.md) |
| Changing the theme or SCSS | [references/themes-and-scss.md](references/themes-and-scss.md) |
| Placing figures, tables or notes in wider or margin columns | [references/layout.md](references/layout.md) |
| Callouts, tables, figures, code blocks, cross-references | [references/components.md](references/components.md) |
| Editing or extending the format extension | [references/extensions.md](references/extensions.md) |
| Branding: tokens, contrast, fonts, logo | [references/tokens.md](references/tokens.md) |

The digests paraphrase quarto.org and link each source page. Check them against your installed Quarto.
