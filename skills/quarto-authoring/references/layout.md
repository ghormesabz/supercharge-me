# Layout

Digest of <https://quarto.org/docs/output-formats/page-layout.html> and <https://quarto.org/docs/authoring/article-layout.html>, read 2026-10-18.

## `page-layout`

```yaml
page-layout: article   # house default: reading-width body, margins, sidebars
page-layout: full      # article grid, expands into empty sidebar and margin
page-layout: custom    # plain container; bring your own Bootstrap grid classes
```

## `grid`

```yaml
grid:
  sidebar-width: 220px   # px only
  body-width: 720px      # px only; about 70 characters at 17px
  margin-width: 260px    # px only
  gutter-width: 2rem     # px, em or rem
```

Widening `margin-width` widens the whole page. To keep the total, cut `body-width` by the same amount.

## Column classes

Apply to a fenced div, or as a class on a figure or table (`::: {.column-page}`).

| Column | Classes |
|:--|:--|
| Body | `.column-body`, `.column-body-outset`, `.column-body-outset-left`, `.column-body-outset-right` |
| Page inset | `.column-page-inset`, `-left`, `-right` |
| Page | `.column-page`, `.column-page-left`, `.column-page-right` |
| Screen inset | `.column-screen-inset`, `.column-screen-inset-shaded`, `-left`, `-right` |
| Screen | `.column-screen`, `.column-screen-left`, `.column-screen-right` |
| Margin | `.column-margin` |

Wide figures (context maps, architecture maps, pipelines) take `.column-page`.

`[text]{.aside}` puts a note in the margin without a footnote number.

## Captions and references

| Option | Values | Default |
|:--|:--|:--|
| `fig-cap-location` | `top`, `bottom`, `margin` | `bottom` |
| `tbl-cap-location` | `top`, `bottom`, `margin` | `top` |
| `reference-location` | `document`, `section`, `block`, `margin` | `document` |
| `citation-location` | `document`, `margin` | `document` |
