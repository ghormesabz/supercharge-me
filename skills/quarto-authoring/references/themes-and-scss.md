# Themes and SCSS

Digest of <https://quarto.org/docs/output-formats/html-themes.html> and <https://quarto.org/docs/authoring/brand.html>, read 2026-10-18.

## `theme` values

```yaml
theme: default   # Bootstrap 5
theme: cosmo     # one of 25 Bootswatch themes
theme: pandoc    # Pandoc default HTML
theme: none      # no theme CSS added
```

Under `theme: none` the standard HTML components break: callouts are unstyled, `toc-location` has no effect, collapsible callouts and tabsets need Bootstrap. The house format therefore builds on the Bootstrap theme.

## Custom SCSS

A theme file has two sections:

```scss
/*-- scss:defaults --*/
$font-size-base: 1.0625rem !default;   // Sass variables, before Bootstrap compiles

/*-- scss:rules --*/
h2 { margin-top: 2.4rem; }             // plain CSS, after Bootstrap
```

Layer a file over a base: `theme: [cosmo, custom.scss]`. A lone `custom.scss` inherits the default Bootstrap theme. The house format sets `theme: house.scss` in its extension.

Sass variables worth knowing: `$body-bg`, `$body-color`, `$link-color`, `$font-family-sans-serif`, `$font-family-monospace`, `$font-size-base`, `$line-height-base`, `$headings-*`, `$h1-font-size` to `$h6-font-size`, `$border-radius`, `$enable-shadows`, `$toc-color`, `$callout-border-width`, plus Bootstrap's own.

Page-width Sass: `$grid-sidebar-width`, `$grid-body-width`, `$grid-margin-width`, `$grid-column-gutter-width`.

## Light and dark

```yaml
theme:
  light: [cosmo, theme.scss]
  dark: [cosmo, theme-dark.scss]
respect-user-color-scheme: true   # follow the OS; Quarto 1.7+, needs JavaScript
```

That is for a theme outside the house format. The house format is light only and compiles one theme. It republishes colours as CSS custom properties. See `tokens.md`.

## `_brand.yml`

Quarto 1.6+ reads `_brand.yml` next to the document or project, and a document can point elsewhere with `brand: path/to/_brand.yml` or turn it off with `brand: false`.

- **Controls**: `color` (named `palette` plus roles `foreground`, `background`, `primary`), `typography` (fonts and their use for base, headings, links, monospace), `logo` (`small`, `medium`, `large`, with light and dark variants), `defaults: bootstrap`.
- **HTML**: `primary` sets link, navbar and progress-bar colours. Bootstrap-based formats map the remaining semantic colours to Bootstrap colours of the same name.
- **Fonts**: examples use `source: google`. Other sources are in the brand reference.
- **Logo**: a path relative to `_brand.yml`, or a URL, with optional `alt`.
- **Not documented**: how `_brand.yml` behaves under `theme: none`. Test before relying on it.

To keep one design channel, the house format reads `tokens.css`. If a `_brand.yml` sits next to the document, Quarto still applies it to Bootstrap variables, and `tokens.css` loads later and wins for everything the house stylesheet draws. Set `brand: false` in the document when you want only the tokens.
