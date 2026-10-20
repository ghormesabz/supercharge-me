#!/usr/bin/env python3
"""Session handoff file for one folder: path, write, read, clear, hook.

  handoff.py path            Print where this folder's handoff lives.
  handoff.py write           Read handoff XML on stdin, validate, stamp, save.
  handoff.py read            Print the saved handoff. Exit 1 if there is none.
  handoff.py clear           Delete the saved handoff.
  handoff.py hook            SessionStart hook: tell the model a handoff is waiting.

The file name comes from the real path of the workspace: the enclosing git root, or
the working folder outside a repo. A session opened anywhere in the same workspace
finds it and a session opened elsewhere does not. Set
SUPERCHARGE_HANDOFF_DIR to move it off the system temp folder.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import datetime


def handoff_dir():
    return os.environ.get("SUPERCHARGE_HANDOFF_DIR") or os.path.join(
        os.path.realpath(tempfile.gettempdir()), "supercharge-me"
    )


def workspace(cwd):
    # Walk up for .git rather than running git, so the hook never touches the
    # macOS /usr/bin/git stub.
    here = d = os.path.realpath(cwd)
    while not os.path.exists(os.path.join(d, ".git")):
        parent = os.path.dirname(d)
        if parent == d:
            return here
        d = parent
    return d


def handoff_path(cwd):
    key = hashlib.sha1(workspace(cwd).encode()).hexdigest()[:12]
    return os.path.join(handoff_dir(), f"handoff-{key}.xml")


def git(cwd, *args):
    try:
        out = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=5
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def cmd_write(cwd):
    raw = sys.stdin.read()
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        sys.exit(f"handoff: not well-formed XML ({e}). Escape & < > in text and resend.")
    if root.tag != "handoff":
        sys.exit(f"handoff: root element must be <handoff>, got <{root.tag}>.")

    # The script owns the metadata, so the model cannot get it wrong.
    root.attrib.clear()
    root.set("version", "1")
    root.set("created", datetime.now().strftime("%Y-%m-%dT%H:%M"))
    root.set("workspace", workspace(cwd))
    branch, head = git(cwd, "branch", "--show-current"), git(cwd, "rev-parse", "--short", "HEAD")
    if branch:
        root.set("branch", branch)
    if head:
        root.set("head", head)
    ET.indent(root)

    path = handoff_path(cwd)
    os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(ET.tostring(root, encoding="unicode") + "\n")
    os.replace(tmp, path)
    print(f"{path} ({os.path.getsize(path)} bytes)")


def cmd_read(cwd):
    path = handoff_path(cwd)
    if not os.path.exists(path):
        sys.exit(f"handoff: nothing saved for {workspace(cwd)}.")
    with open(path, encoding="utf-8") as f:
        sys.stdout.write(f.read())


def cmd_clear(cwd):
    path = handoff_path(cwd)
    if os.path.exists(path):
        os.remove(path)
        print(f"deleted {path}")
    else:
        print("nothing to delete")


def age(seconds):
    if seconds < 3600:
        return f"{max(1, int(seconds // 60))} min"
    if seconds < 86400:
        return f"{int(seconds // 3600)} h"
    return f"{int(seconds // 86400)} d"


def cmd_hook(cwd):
    try:
        cwd = json.load(sys.stdin).get("cwd") or cwd
    except (ValueError, AttributeError):
        pass
    path = handoff_path(cwd)
    if not os.path.exists(path):
        return
    st = os.stat(path)
    me = os.path.abspath(__file__)
    message = (
        f"A session handoff for this folder is waiting (written {age(time.time() - st.st_mtime)} ago, "
        f"{st.st_size} bytes). In your first reply, tell the user it exists and ask whether to pick it up, "
        f"then carry on with whatever they asked. Do not read it until they say yes. "
        f"On yes: run `python3 {me} read`, give the goal, status and next steps in three lines, "
        f"note if `head` differs from the current git HEAD, then run `python3 {me} clear`. "
        f"On no: leave it alone."
    )
    json.dump(
        {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": message}},
        sys.stdout,
    )


COMMANDS = {
    "path": lambda cwd: print(handoff_path(cwd)),
    "write": cmd_write,
    "read": cmd_read,
    "clear": cmd_clear,
    "hook": cmd_hook,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        sys.exit(__doc__)
    COMMANDS[sys.argv[1]](os.getcwd())
