# Part A: for domain review

Part A is the copy a domain expert reads, and the whole of the design sheet. They know the work and not the build. Write it in their words, take terms from the context, and keep it short enough to read in one sitting. An expert should be able to mark every line right, wrong or unsure without asking what a word means.

## Claim tags

Tag every claim that carries weight, in the Status column or beside the claim.

| Tag | Use when | Needs |
|:--|:--|:--|
| Confirmed | An expert said it or a document states it | A source you can point to in the context. A5 shows it in the Source column. Elsewhere, name it in the cell when the claim could be disputed |
| Interpreted | It is our reading of what we were told | A Q link to A7 |
| Assumption | It is our guess | A Q link to A7 |
| Open | Nobody has answered yet | An owner, in A7 |

A Q link is `[Q1](#q1){.qref}`. Names go in a source only when the user supplied them. Never invent a name, a date or a quote.

## Sections

The list is fixed and is never renumbered. If a section does not apply, keep its heading and write `Not applicable.` with the reason.

**Banner, view note and legend.** Leave them as the template has them. Fill in who reviews the draft.

**A1 Summary and sign-off.** Two to four sentences: what this is, who uses it, what changes for them. Then the key facts table, which starts with who it is for, scale, what it does, what it does not do and target. The table can grow. Add a row for any other fact the expert must check. A row nobody has answered carries `[Open]{.tag .open}` and a Q link to its A7 row, which names the owner. Then the sign-off sheet with one row per reviewer role. Leave Name, Decision and Date empty.

In the front matter, the author is the person or team the user names at the restate, else `Builder team`. The date is today's, from `date +%F`.

**A2 Context map.** Who and what surround the thing. The left column holds what comes in, each tagged `[person]`, `[system]` or `[data]`. The centre holds the thing, with one line on the human check that stays. The right column holds what goes out. The band below lists what is outside this build.

**A3 Process flow.** One item, start to finish, in 3 to 7 steps. Lanes: Steps, Artefacts in, Person, Tool, Checkpoint, Artefacts out. Every lane has one list item per step, and `[-]{.none}` where nothing happens. Put a Q link on any checkpoint that is an assumption.

**A4 Inputs and outputs.** One row per artefact in A3. In or out is `In`, `Internal` or `Out`. Names match A3 word for word, in both directions.

**A5 Domain rules.** One row per rule, in plain words, with its source. A rule with no source is Interpreted or Assumption.

**A6 Out of scope.** What someone would reasonably expect and is not being built. One line each, with a reason where it helps.

**A7 Review questions.** One row for every Interpreted and Assumption claim, and for every Open item, wherever it sits in the spec. That includes Part B claims and every Open row in B13: the row names the B13 ID, for example `(B13 D5)` in Why it matters. `check-spec.sh` fails on a tag with no Q link and on an Open B13 row that A7 does not name. Phrase it as what we assumed, so a reviewer can answer yes or give a correction. Who is `SME`, `builder`, `client`, or a named role such as `Client IT`. Why it matters says what the answer changes. Leave Answer empty in a draft. Number questions from Q1 and give each an anchor: `[Q1]{#q1}`. Rows for the builder or client show in both copies, so word them in plain terms too.

## No builder terms in Part A

`check-spec.sh` prints every hit from this command as a `REVIEW` line:

```bash
sed -n '/^# For domain review/,/^# For the build team/p' spec.qmd \
  | grep -n -i -w -E '(llm|api|sql|json|schema|vector|token|prompt|endpoint|pipeline|embedding|latency|p95|container)s?'
```

Read every hit. Replace it with the expert's own term or a plain description. A term the expert uses in their own documents may stay, with a short gloss on first use. The check passes when it prints nothing, or when every hit is a term the expert used and is glossed on first use. List those hits in the report.
