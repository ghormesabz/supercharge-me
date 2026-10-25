---
name: handoff
description: Saves the state of this session as a compact XML handoff so a fresh session in the same folder can pick it up. A SessionStart hook offers it when one is opened there. Use only when the user says "hand this over", "save my progress", "I'm out of context", or invokes /supercharge-me:handoff. Skip for summaries meant to be read by people.
disable-model-invocation: true
---

# Handoff

Saves where we are, so the next session starts warm. Writes one XML file for this workspace (the git root, or this folder outside a repo) to `~/.claude/supercharge-me/handoffs`. Never edits anything in the workspace.

In this file, the script is `${CLAUDE_SKILL_DIR}/scripts/handoff.py`. Run it as `python3 ${CLAUDE_SKILL_DIR}/scripts/handoff.py CMD` from inside the workspace. If the shell has moved elsewhere, add `--workspace ROOT`.

## Write

1. **Gather.** Use the conversation. If git exists, run `git status --short` and `git diff --stat` to confirm which files changed. You may run `ls` or `stat` on a path you list under `files` to confirm it is there or gone, but never read file contents. Anything you did not check gets `basis="stated"` or `"inferred"`.
2. **Compose** the XML below. Under 60 lines. Facts, not narrative. Escape `&`, `<` and `>` in text. Never write a secret, token or credential into it. Also:
   - Paths inside the workspace are relative. Paths outside it start with `~/`. Write full identifiers (UUIDs, skill IDs, hashes) and never truncate them. Redact only secrets and credentials.
   - Name another session only by the name or ID the harness gave you. Never infer what another session is working on or owns.
   - When a decision reverses an earlier stated plan or leaves work undone, say so in `leaves`.
   - An open question states what the session already shows for or against.
   - Any delete, overwrite or `rm -r` gets an `f` entry with `state="deleted"` and a `recover` attribute.
   - Revisit material longer than about 10 lines, such as a proposed edit list, goes in `detail`. Wrap it in `<![CDATA[` … `]]>` so it needs no escaping.
   - The goal's first clause names the work area, because the hook shows the goal to the next session for routing.
3. **Save** by piping it in: `python3 ${CLAUDE_SKILL_DIR}/scripts/handoff.py write --nonce TOKEN <<'XML'` … `XML`. Replace TOKEN with 8 letters and digits you invent for this save, written out literally. Invent a new one every time, and never reuse an earlier token or copy one from an example: a token found in two transcripts identifies neither, and a branched or forked session starts with a copy of its parent's transcript. Never use `$(…)` or a variable: the script finds this session's transcript by looking for the token as typed in the command, and an expanded one never appears there. The script may wait a few seconds for the transcript to catch up. It checks the schema, stamps `version`, `created`, `workspace`, `branch`, `head`, `session` and `transcript` on the root itself, so leave those off, and archives any earlier handoff for this folder. On an error it lists every problem: fix and resend. A warning on stderr, about size or a missing transcript, does not mean the save failed.
4. **Confirm.** Tell the user the path the script printed and that a new session opened in this folder will offer to pick it up. If it printed `replaced:`, say which handoff was replaced and where it was archived.

## Format

```xml
<handoff>   <!-- the script stamps: version created workspace branch head session transcript -->
  <goal>Work area first, then what this session was for. One or two sentences.</goal>
  <status>
    <s basis="verified|stated|inferred">One fact per element.</s>
  </status>
  <decisions>
    <d why="reason" basis="stated|inferred" leaves="what it leaves undone (optional)">What was decided</d>
  </decisions>
  <files>
    <f path="src/x.py" state="new|changed|deleted|read" recover="PATH|transcript|none">One-line note</f>
  </files>
  <open>
    <q owner="user|agent">Question, plus what the session already shows for or against</q>
  </open>
  <next>
    <step>First thing to do</step>
  </next>
  <rejected>Option tried or ruled out, and why. Repeatable.</rejected>
  <skills>
    <skill name="plugin:skill">When the next session should load it</skill>
  </skills>
  <detail>Long revisit material. The script moves it to a sidecar file.</detail>
</handoff>
```

`basis` says how you know. **verified**: a tool result in this session shows it. **stated**: the user said it. **inferred**: you reasoned it. Every `s` and `d` needs one, and nothing is `verified` unless a tool result shows it. `recover` is required on a deleted file: a backup path, `transcript` (the full text sits in a tool result in this session's transcript), or `none`.

`decisions` and `rejected` are the parts a fresh session cannot recover from the files, so they matter most. Omit an element that has nothing in it.

## Pick up

A `SessionStart` hook (`hooks/hooks.json`) tells the model when a handoff exists for the workspace it was opened in: the goal, its age, the session that wrote it, and whether git HEAD has moved. It never loads the body. A handoff older than 14 days is archived instead of offered; if the hook says so, mention it to the user once.

After the user says yes:

1. `python3 ${CLAUDE_SKILL_DIR}/scripts/handoff.py read --workspace ROOT`. Summarise goal, status and next in three lines. Keep the basis labels, so say which status lines are only inferred. If `head` differs from the current git HEAD, say so.
2. `python3 ${CLAUDE_SKILL_DIR}/scripts/handoff.py clear --workspace ROOT`. This moves the file to `archive/`, kept 30 days, so the next session is not asked again.

`read --detail` prints the long revisit material when you need it. If the user asks to restore a file marked `recover="transcript"`, search the `transcript` file named on the root for its content, and do not ask the user for it. Claude Code deletes transcripts after 30 days by default (`cleanupPeriodDays`), so an old handoff's file may be gone: if it is, say so.

To set one aside without picking it up: `clear`. To see what is saved and archived for this folder: `list`.
