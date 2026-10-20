# Format extensions

Digest of <https://quarto.org/docs/extensions/formats.html>, read 2026-10-18.

The house format is a Quarto format extension. A document selects it with `format: house-html`: the directory name plus the base format.

## Layout

```
_extensions/
  house/
    _extension.yml
    house.scss
```

Only `_extensions/` is required; Quarto ignores anything outside it on install. Quarto finds `_extensions/` in the document folder or a parent project folder.

## `_extension.yml`

```yaml
title: House HTML
author: Mahan
version: 0.1.0
quarto-required: ">=1.7.0"
contributes:
  formats:
    html:
      theme: house.scss
      embed-resources: true
```

- Options under `html:` are ordinary HTML format options. `theme` paths are relative to the extension folder.
- Options shared across base formats go under `common:`; filters and shortcodes bundle with `filters:` and `shortcodes:`.
- A document overrides any contributed option in its own frontmatter.

## Selecting and testing

```yaml
format: house-html            # or:
format:
  house-html:
    toc: true
```

Render at render time with `quarto render doc.qmd --to house-html`.

## Install paths

- The bundled `scripts/install-house.sh DIR` copies the extension. This is the route this plugin uses; Workflow step 1 in `SKILL.md` has the full command.
- `quarto add <org>/<ext>` installs from GitHub into a project. `quarto use template` installs with a starter `template.qmd`.
- Copying `_extensions/` by hand is not covered by the docs page. It works because the folder is self-contained; confirm with a test render.

## Editing the house format

1. Edit `house.scss`. Defaults go in the `scss:defaults` section, rules in `scss:rules`.
2. Express every colour, font and radius in the rules through the CSS custom properties in `:root`, so `tokens.css` can override them.
3. Install the edited copy into a scratch folder and render `assets/template.qmd`. Look at the result in a browser.
