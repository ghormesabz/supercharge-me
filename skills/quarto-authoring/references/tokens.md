# Tokens

A design system changes **colour roles, font families and a logo**. It never changes spacing, layout, radius rules or component styling. Sixteen CSS custom properties carry the whole design. The house format defines their defaults; a `tokens.css` beside the document overrides them.

```yaml
css: tokens.css      # in the document frontmatter, after format: house-html
```

## The tokens

| Token | Role | Default (light) |
|:--|:--|:--|
| `--ink` | Body text and strong lines | `#1a1a1a` |
| `--ink-soft` | Secondary text, labels, captions | `#585858` |
| `--paper` | Page background | `#ffffff` |
| `--paper-alt` | Panels, table header band, code | `#f5f5f2` |
| `--line` | Hairlines and quiet borders | `#d9d9d3` |
| `--accent` | Links, status dot, `new` chips, model-call stages | `#1d4ed8` |
| `--on-accent` | Text on an accent fill: `--paper` or `--ink` | `#ffffff` |
| `--ok` | Confirmed tag | `#1a7f37` |
| `--warn` | Assumption tag, amber dot, draft banner | `#8a5a00` |
| `--bad` | Open tag, red dot | `#b42318` |
| `--font-body`, `--font-head`, `--font-mono` | Font stacks, each ending in a generic family | system sans, system sans, system mono |
| `--radius` | Corner radius | `2px` |
| `--toc-w`, `--page` | Contents width, maximum content width | leave alone |

The house format has a light palette only. It follows no OS dark setting, so the page stays on `--paper` whatever the viewer's system uses.

## Contrast

Test each pair against 4.5:1 before writing the file.

| Pair | Where it shows |
|:--|:--|
| `--accent` on `--paper` | Links |
| `--on-accent` on `--accent` | Chips, model-call stages |
| `--paper` on `--ok`, and on `--bad` | Confirmed and Open tags |
| `--warn` on `--warn` mixed 10% over `--paper` | Assumption tag, draft banner |
| `--ink-soft` on `--paper`, and on `--paper-alt` | Labels, captions |

Bright brand colours fail most often. Test `--accent` on `--paper` first. If it fails, use the brand's darker shade, or darken until it passes, then set `--on-accent` to whichever of `--ink` and `--paper` passes. Do the same for `--ok`, `--warn` and `--bad`. Report every token you changed.

```python
def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

def mix(a, b, pct):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * pct + y * (1 - pct)):02x}" for x, y in zip(ca, cb))
```

For the warn pair: `ratio(warn, mix(warn, paper, 0.10))`.

## Fonts

The default is the system stack: nothing is fetched. A web font goes in as a link in the frontmatter, never in the CSS:

```yaml
include-in-header:
  - text: |
      <link data-external="1" rel="stylesheet" href="https://example.com/fonts.css">
```

Keep `data-external="1"`. Without it, `embed-resources: true` fetches the stylesheet at render time and bakes the font files into every copy (about 600 KB for one family at three weights). With it, the render stays offline and the viewer's browser fetches the font. Name the family first in `--font-body` and keep a system stack after it. Never use `@import` or embed a font file. A font with no public link: keep the system stack and say so.

## Logo

Reference a logo by relative path in the frontmatter or header; `embed-resources` inlines it. Copy only the file the user names. Never fetch assets from a design source on your own.

## Writing the file

First line: `/* Derived from SOURCE on YYYY-MM-DD. Swap values, keep names. */` (`date +%F`). Then only the tokens that differ from the defaults. A token the source has no value for keeps its default and goes in the report. Do not invent a palette.
