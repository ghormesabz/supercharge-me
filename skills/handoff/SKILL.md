---
name: handoff
description: Saves the state of this session as a compact XML handoff in the temp folder so a fresh session in the same folder can pick it up. A SessionStart hook offers it when one is opened there. Use only when the user says "hand this over", "save my progress", "I'm out of context", or invokes /mahan-skills:handoff. Skip for summaries meant to be read by people.
disable-model-invocation: true
---

# Handoff

Saves where we are, so the next session starts warm. Writes one XML file for this folder. Never edits anything in the workspace.

In this file, the script is `${CLAUDE_SKILL_DIR}/scripts/handoff.py`. Run it from the workspace root, always as `python3 ${CLAUDE_SKILL_DIR}/scripts/handoff.py CMD`.

## Write

1. **Gather.** Use the conversation. If git exists, run `git status --short` and `git diff --stat` to confirm which files changed. Read nothing else.
2. **Compose** the XML below. Under 60 lines. Facts, not narrative. Paths relative to the workspace. Escape `&`, `<` and `>` in text. Never write a secret, token or credential into it.
3. **Save** by piping it in: `python3 ${CLAUDE_SKILL_DIR}/scripts/handoff.py write <<'XML'` … `XML`. The script checks it is well-formed XML, stamps `version`, `created`, `workspace`, `branch` and `head` on the root itself, so leave those off, and replaces any earlier handoff for this folder. On an error it prints the reason: fix and resend.
4. **Confirm.** Tell the user the path the script printed and that a new session opened in this folder will offer to pick it up.

## Format

```xml
<handoff>
  <goal>One or two sentences.</goal>
  <status>Done so far, in a few lines.</status>
  <decisions>
    <d why="reason">What was decided</d>
  </decisions>
  <files>
    <f path="src/x.py" state="new|changed|read">One-line note</f>
  </files>
  <open>
    <q owner="user|agent">Unresolved question</q>
  </open>
  <next>
    <step>First thing to do</step>
  </next>
  <rejected>Option tried or ruled out, and why.</rejected>
</handoff>
```

`decisions` and `rejected` are the parts a fresh session cannot recover from the files, so they matter most. Omit an element that has nothing in it.

## Pick up

A `SessionStart` hook (`hooks/hooks.json`) tells the model when a handoff exists for the folder it was opened in. It never loads the file. After the user says yes: `python3 ${CLAUDE_SKILL_DIR}/scripts/handoff.py read`, summarise goal, status and next in three lines, then `python3 ${CLAUDE_SKILL_DIR}/scripts/handoff.py clear` so the next session is not asked again. If `head` differs from the current git HEAD, say so.

To delete one without picking it up: `clear`.
