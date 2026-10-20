# Design

`--design` changes the look and nothing else: colour roles, font families and a logo. The layout lives in the house format and `figures.css`, which read 16 tokens. Branding means writing a `tokens.css` that overrides some of them. The token table, contrast rule, font rule and logo rule are in `supercharge-me:quarto-authoring`, [references/tokens.md](../../quarto-authoring/references/tokens.md). Read it before this step.

## Find the source

Take the first rule that applies.

1. `--design VALUE` where VALUE is an existing path. It can be a design-system folder, a CSS file with variables, a `brand.yml` or `_brand.yml`, a tokens file, or a markdown brief. If VALUE is also the name of an installed skill, the path wins.
2. `--design VALUE` where VALUE matches an installed design skill. Call it and read its colours, type and rules.
3. No `--design`, but the spec folder already holds `tokens.css` with overrides. Reuse it. `--mode final` does this by default.
4. Nothing else applies. Write the neutral `tokens.css` from `assets/tokens.css`: no overrides, the house defaults apply.

If VALUE is neither a path nor an installed skill, stop and say so. Do not guess a brand.

## Derive the tokens

Read the source for colours, type families, corner style and logo. Convert colours to six-digit hex. Map them to the token names and keep the names. If the source has no value for a token, keep the default and list the token in the report. Do not invent a palette.

From a `_brand.yml`: `color.palette` and its roles give `--ink` (foreground), `--paper` (background) and `--accent` (primary); `typography` gives `--font-body`, `--font-head` and `--font-mono`; `logo` gives the file to reference. The brand file stays where it is. Only `tokens.css` is written.

## Check contrast

Test the pairs in `tokens.md` against 4.5:1 before writing the file, and list every token you changed in the report. Test `--accent` on `--paper` first.

## Write the files

Write `tokens.css` in the spec folder with the header and rules in `tokens.md`. When you kept the neutral set, copy `assets/tokens.css` and use `the house defaults` as SOURCE.

A logo is referenced from the front matter or a header file by relative path, and only a file the user names. Never fetch an asset tree, logo, image or font file from the design source on your own. Never edit `figures.css` to match a brand. Never hard-code a colour in the `.qmd`.
