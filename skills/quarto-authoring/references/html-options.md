# HTML options

Digest of <https://quarto.org/docs/output-formats/html-basics.html>, read 2026-10-18. Check against your installed Quarto.

## Contents

```yaml
toc: true              # default off
toc-depth: 2           # default 3
toc-expand: 2          # default 1; true expands all, false collapses all
toc-location: right    # default right (floating); also left, body, left-body, right-body
toc-title: Contents
```

- Add `.unnumbered .unlisted` to a heading to keep it out of the contents.
- `toc-location` has no effect under `theme: none` or `theme: pandoc`. The house format uses the Bootstrap theme, so it works.

## Numbering

```yaml
number-sections: true  # default off
number-depth: 3        # default all levels
```

`.unnumbered` on a heading excludes it.

## Anchors, scrolling, links

```yaml
anchor-sections: true          # default on; hover a heading for its link
smooth-scroll: false           # default off
link-external-icon: false
link-external-newwindow: true  # house default
link-external-filter: '^(?:http:|https:)\/\/www\.example\.com\/'
```

Per-link: `[text](https://example.com){.external target="_blank"}`.

## Self-contained output

```yaml
embed-resources: true  # one standalone file, data: URIs; house default
```

Without it, dependencies sit in `<name>_files/` beside the HTML. There is no `self-contained` option in current docs.

## Minimal mode

```yaml
minimal: true   # drops the Bootstrap theme, anchors, popups, tabsets, code copy, responsive figures
code-copy: true # re-enable single features
```

Not used by the house format. It trades components for a smaller file.

## Other options

| Option | Notes |
|:--|:--|
| `css` | Path or list of stylesheets. Loaded after the theme. |
| `include-in-header`, `include-before-body`, `include-after-body` | A file, or a `text:` block. |
| `html-math-method` | Default `mathjax`. |
| `citations-hover`, `footnotes-hover`, `crossrefs-hover` | Popups; `false` disables. |
| `comments` | `hypothesis`, `utterances` or `giscus`; `false` per page. |

Options that live on other pages: `lang`, `date-format`, `title-block-*`, `fig-*`, `tbl-*` (see `components.md`) and `code-*` (see `components.md`).
