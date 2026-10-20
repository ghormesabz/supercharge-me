# Components

Digest of the Quarto pages for callouts, tables, figures, code and cross-references, read 2026-10-18:
<https://quarto.org/docs/authoring/callouts.html> · <https://quarto.org/docs/authoring/tables.html> · <https://quarto.org/docs/authoring/figures.html> · <https://quarto.org/docs/output-formats/html-code.html> · <https://quarto.org/docs/authoring/cross-references.html>

## Callouts

Types: `note`, `warning`, `important`, `tip`, `caution`.

```markdown
::: {.callout-tip title="Recommended next step"}
Content.
:::
```

- `collapse="true"` (collapsed) or `collapse="false"` (expanded) makes it collapsible. Needs the Bootstrap theme.
- `appearance="default|simple|minimal"`; document-wide `callout-appearance:`. The house format sets `default` and draws its own flat card.
- `icon=false` per callout; `callout-icon: false` document-wide. The house format sets it.
- Cross-reference ids: `#nte-`, `#tip-`, `#wrn-`, `#imp-`, `#cau-`.

## Tables

```markdown
| Default | Left | Right | Center |
|---------|:-----|------:|:------:|
| 12      | 12   |    12 |   12   |

: Caption {#tbl-id tbl-colwidths="[40,30,30]"}
```

- A header row is required. The separator row sets alignment.
- Relative widths follow dash counts in the separator when content is wider than the column. For exact widths use `tbl-colwidths`.
- A label must start with `tbl-` to be cross-referenced (`@tbl-id`). Caption sits below a Markdown table in the source; `tbl-cap-location` sets where it renders.
- Bootstrap classes go in the caption braces: `: Caption {.striped .hover}`.
- Cells cannot hold block content. Use a grid table (`+---+` borders, `=` header separator) when they must. Shortcodes do not work in grid tables.

## Figures

```markdown
![Caption](img.png){#fig-id fig-alt="Alt text" width=80% fig-align="left"}

See @fig-id.
```

- Ids start with `fig-`. `{.lightbox}` opens a figure in an overlay.
- Sub-figures: `::: {#fig-pair layout-ncol=2}` around labelled images, last paragraph is the main caption. Blank lines between images are required.
- Figure div: `::: {#fig-x}` around any content; the last paragraph is the caption.
- Custom layout: `layout="[[1,1],[1]]"`; a negative number adds a gap.

## Code

```yaml
code-copy: hover       # true | false | hover
code-fold: false       # true | show
code-line-numbers: true
code-overflow: scroll  # or wrap
syntax-highlighting: arrow   # adaptive; also github, a11y, atom-one, gruvbox ...
```

- Per block: ` ```{.python filename="app.py" code-line-numbers="true"} `.
- Show an executable example without running it: ` ```{{python}} `. Wrap docs that contain fenced examples in four backticks.
- `highlight-style` was the older option name. Current docs use `syntax-highlighting`.

## Cross-references

Labels are lowercase with a type prefix: `fig-`, `tbl-`, `lst-`, `eq-`, `sec-`, and the callout and theorem prefixes.

| Form | Renders |
|:--|:--|
| `@fig-x` | Figure 1 |
| `[Fig @fig-x]` | Fig 1 |
| `[-@fig-x]` | 1 |
| `[@fig-a; @fig-b]` | grouped |

`## Heading {#sec-id}` is referenced as `@sec-id`; numbers show only with `number-sections: true`.
