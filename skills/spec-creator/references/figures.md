# Figures

Four figures are always drawn: A2 context map, A3 process flow, B1 architecture map, B2 system flow. They are Pandoc fenced divs styled by `assets/figures.css`, so the user edits them as text and re-renders. The house format's tokens colour them.

Open `assets/example/spec.qmd` first. It uses every class below.

## Frame

Each figure sits in `::: {.fig}` and ends with `::: {.cap}` holding one sentence, for example `Figure A2. ...`. In every figure, the first paragraph of a column, lane, layer, stage or zone is its label. Leave a blank line between a label paragraph and a list.

Width: A2 and A3 take `.fig .column-page`. B1 and B2 take `.fig .column-screen-inset`, because six stages need the room. Narrow windows scroll the figure sideways inside its frame.

Keep stage names and step names on one line. In a six-stage pipe, a name of about 14 characters fits, and a longer one may wrap. If the render shows a name that wraps, shorten it. A hyphenated identifier such as EXC-01 can break at the hyphen. Write it as `[EXC-01]{.nw}` to keep it whole.

## A2 context map: `.ctx`

Inside `.ctx`, in order: `.col` (comes in), `.hand` (arrow label), `.core` (the thing), `.hand`, `.col` (goes out). A `.fence` div under `.ctx` lists what is outside this build. Each bullet starts with a kind chip: `[person]{.k}`, `[system]{.k}` or `[data]{.k}`. The `.core` holds the name, one or two sentences, and the human check that stays.

## A3 process flow: `.lanes`

One `.lane` per row. Kinds: `.steps` (an ordered list), `.in`, `.person`, `.tool`, `.check`, `.out`. Keep all six unless a lane is empty for every step.

- Every lane has one list item per step, so the columns line up. A step where nothing happens is `- [-]{.none}`. It renders as a striped placeholder.
- A line break inside an item is a backslash at the end of the line.
- 3 to 7 steps. More than that, and the flow needs splitting.
- Artefact names in `.in` and `.out` match the A4 table word for word. Every name in a lane is a row in A4, and every row in A4 appears in a lane.

## B1 architecture map: `.arch`

Inside `.arch`, top to bottom: `.layer`, `.bus`, `.zone`. A `.zone` is a dashed boundary with its name as the first paragraph, and holds its own `.layer` and `.bus` children. A `.bus` carries the channel or protocol between two layers.

A node is a list item: `- [Kind]{.k} **Name** [new]{.new}`, then `\` and a line break, then one line on what it does. The chip is one of `[new]{.new}`, `[existing]{.existing}` or `[external]{.external}`. Keep to four nodes a layer. Add the three-chip `.legend` under the figure.

## B2 system flow: `.pipe`

Inside `.pipe`, alternate `.stage` and `.hand`. A stage kind is one of `.trigger`, `.model`, `.api`, `.store`, `.human`. Its first paragraph is the kind label, then the stage name, then one short sentence of about 12 words or fewer. A `.hand` holds the contract name in backticks and renders as an arrow. A contract name of up to 10 characters fits above its arrow, whatever the number of stages. The arrow label is a fixed 5.5rem wide and breaks mid-word past that. `check-spec.sh` fails on a longer name, so pick contract names of 10 characters or fewer in B5 and use them everywhere. Add `.dashed` to a `.hand` for an optional or asynchronous hop. A stage that can fail holds `::: {.alt}` with `If it fails:` and who sees it.

Six stages or fewer per pipe. Split a longer flow into two pipes, each in its own `.fig`, captioned `Figure B2a.` and `Figure B2b.`. Draw a stage that is sometimes skipped with a `.dashed` hand into it, and say in the caption when it is skipped.

## Model call card: `.card`

In B4. The first paragraph is `[LLM]{.k} Call name`. A definition list follows, one term and `: definition` pair per field in [part-b.md](part-b.md), with a blank line between pairs.

## Limits

Flexbox cannot draw arbitrary graph edges. B1 is layered and B2 is linear. If the system is a true graph, draw the main path in B2, put the other paths in a second pipe, and say so in the caption.

The kit uses `:has()` and `color-mix()`, which need an evergreen browser.

## Pandoc and Quarto rules

- Pipe-table column widths follow the dash counts in the separator row. For exact widths, add a caption line: `: Caption {tbl-colwidths="[18,56,26]"}`.
- Use `.note` for notes. The house format styles Quarto callouts, but the spec uses `.note` and `.banner` so the kit does not depend on them.
- Do not write HTML comments. Quarto copies them into the output.
- A line that starts with `:` straight after a code block renders as a stray paragraph, or becomes the caption of the next table. Label a code block with a paragraph above it.
- Do not use shortcodes, mermaid or graphviz blocks, or `draft: true`. Quarto has its own draft feature. This kit's flag is `spec-draft`.

## Look at the figures

Headless Chrome ignores scroll position, so every screenshot shows the top of the page. `figure-shots.sh` shifts each figure to the top of a scratch copy and takes one screenshot per figure:

```bash
bash PLUGIN/scripts/figure-shots.sh OUT/docs/spec/SLUG/build-spec.html
```

On draft, point it at `design-review.html`. It prints the folder holding `fig1.png`, `fig2.png` and so on, in page order: A2, A3, B1, then each B2 pipe. It exits 1 with a message when no browser is installed; then say so in the report.

View each image. Check that the right edges line up, no text is clipped, no label breaks mid-word or at a hyphen, and every arrow has a label. Fix and re-render until clean. Delete the folder when done.
