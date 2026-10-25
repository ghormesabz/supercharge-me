#!/usr/bin/env python3
"""Session handoff file for one workspace: write, read, clear, list, path, hook.

  handoff.py write [--nonce TOKEN]  Read handoff XML on stdin, validate, stamp, save.
  handoff.py read [--detail]        Print the saved handoff, or its detail sidecar.
  handoff.py clear                  Move the saved handoff into archive/.
  handoff.py list                   List the saved and archived handoffs.
  handoff.py path                   Print where this workspace's handoff lives.
  handoff.py hook                   SessionStart hook: tell the model a handoff is waiting.

Every command but hook takes --workspace ROOT, so a shell that has moved elsewhere still
hits the right slot.

The workspace is the enclosing git root, or the working folder outside a repo. Its handoff
lives in ~/.claude/supercharge-me/handoffs (SUPERCHARGE_HANDOFF_DIR moves it). Nothing is
deleted: a replaced, cleared or stale handoff moves to archive/, and the next write prunes
archive entries older than SUPERCHARGE_HANDOFF_KEEP_DAYS (30). The hook archives a handoff
older than SUPERCHARGE_HANDOFF_MAX_AGE_DAYS (14) instead of offering it.
"""
import sys

if sys.version_info < (3, 9):
    sys.exit("handoff: needs Python 3.9+")

import argparse
import glob
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import datetime

FORMAT_VERSION = "2"
SIDECAR = ".detail.md"
MAX_LINES, MAX_BYTES = 60, 4096
HASH_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
NONCE_RE = re.compile(r"^[A-Za-z0-9]{8,64}$")
RECENT = 3600  # a transcript older than this cannot be the one being written to
TAIL = 1 << 20  # the nonce is in the newest line, so only the end of a transcript is read

BASES = ("verified", "stated", "inferred")
STATES = ("new", "changed", "deleted", "read")
OWNERS = ("user", "agent")
# container element -> the one element it holds
CONTAINERS = {"status": "s", "decisions": "d", "files": "f", "open": "q", "next": "step", "skills": "skill"}
TEXT_ONLY = ("goal", "rejected", "detail")
# element -> attribute -> allowed values. Every attribute listed here is required.
ENUMS = {
    "s": {"basis": BASES},
    "d": {"basis": BASES},
    "f": {"state": STATES},
    "q": {"owner": OWNERS},
}


def warn(message):
    print(f"handoff: {message}", file=sys.stderr)


def env_number(name, default):
    try:
        value = float(os.environ[name])
    except (KeyError, ValueError):
        return default
    return value if value >= 0 else default


# --- where things live -----------------------------------------------------------------


def handoff_dir():
    return os.environ.get("SUPERCHARGE_HANDOFF_DIR") or os.path.expanduser(
        "~/.claude/supercharge-me/handoffs"
    )


def legacy_dir():
    # Where 1.0 kept handoffs when SUPERCHARGE_HANDOFF_DIR was not set.
    return os.path.join(os.path.realpath(tempfile.gettempdir()), "supercharge-me")


def archive_dir():
    return os.path.join(handoff_dir(), "archive")


def private_dir(path):
    os.makedirs(path, mode=0o700, exist_ok=True)
    try:
        os.chmod(path, 0o700)  # makedirs leaves an existing directory as it was
    except OSError:
        pass


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


def workspace_key(ws):
    return hashlib.sha1(ws.encode()).hexdigest()[:12]


def handoff_path(ws):
    return os.path.join(handoff_dir(), f"handoff-{workspace_key(ws)}.xml")


def sidecar_of(path):
    return path[: -len(".xml")] + SIDECAR


def live_paths(ws):
    """The saved handoffs for a workspace, preferred first. 1.0 files may still sit in temp."""
    name = f"handoff-{workspace_key(ws)}.xml"
    dirs = [handoff_dir()]
    if not os.environ.get("SUPERCHARGE_HANDOFF_DIR"):
        dirs.append(legacy_dir())
    return [p for p in (os.path.join(d, name) for d in dirs) if os.path.exists(p)]


def find_live(ws):
    paths = live_paths(ws)
    return paths[0] if paths else None


def archived(ws):
    pattern = os.path.join(glob.escape(archive_dir()), f"handoff-{workspace_key(ws)}-*.xml")
    return glob.glob(pattern)


# --- reading git without git -----------------------------------------------------------


def git_dir_of(root):
    """The git directory of a checkout, following a worktree or submodule .git file."""
    dot_git = os.path.join(root, ".git")
    if os.path.isdir(dot_git):
        return dot_git
    with open(dot_git, encoding="utf-8") as f:
        line = f.readline().strip()
    if not line.startswith("gitdir:"):
        return None
    return os.path.normpath(os.path.join(root, line[len("gitdir:"):].strip()))


def common_dir_of(git_dir):
    # A linked worktree keeps HEAD in its own directory and its refs in the main one.
    try:
        with open(os.path.join(git_dir, "commondir"), encoding="utf-8") as f:
            return os.path.normpath(os.path.join(git_dir, f.read().strip()))
    except OSError:
        return git_dir


def read_ref(git_dir, common, ref):
    """Commit hash for a ref name: the loose file first, then packed-refs."""
    if not ref.startswith("refs/") or ".." in ref.split("/"):
        return None
    for d in (git_dir, common):
        try:
            with open(os.path.join(d, ref), encoding="utf-8") as f:
                value = f.read().strip()
        except OSError:
            continue
        if HASH_RE.match(value):
            return value
    try:
        with open(os.path.join(common, "packed-refs"), encoding="utf-8") as f:
            for line in f:
                sha, _, name = line.strip().partition(" ")
                if name == ref and HASH_RE.match(sha):
                    return sha
    except OSError:
        pass
    return None


def resolve_head(root):
    """(branch, full hash) read straight from .git, or None if it cannot be read.

    The hash is empty on an unborn branch. Branch is empty on a detached HEAD."""
    try:
        git_dir = git_dir_of(root)
        if not git_dir:
            return None
        common = common_dir_of(git_dir)
        with open(os.path.join(git_dir, "HEAD"), encoding="utf-8") as f:
            head = f.read().strip()
    except OSError:
        return None
    if HASH_RE.match(head):
        return "", head
    if not head.startswith("ref:"):
        return None
    ref = head[len("ref:"):].strip()
    if ref == "refs/heads/.invalid":  # the reftable backend; its refs are not plain files
        return None
    branch = ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ""
    return branch, read_ref(git_dir, common, ref) or ""


def usable_git():
    path = shutil.which("git")
    if not path:
        return False
    if path == "/usr/bin/git" and shutil.which("xcode-select"):
        # The macOS stub opens an install dialog until the Command Line Tools exist.
        return subprocess.run(["xcode-select", "-p"], capture_output=True).returncode == 0
    return True


def git(cwd, *args):
    try:
        out = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=5
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def branch_and_head(ws):
    """Branch and short hash for the stamp. The git binary is a fallback, not the way in."""
    if not os.path.exists(os.path.join(ws, ".git")):
        return "", ""
    found = resolve_head(ws)
    if found:
        return found[0], found[1][:7]
    if not usable_git():
        return "", ""
    return git(ws, "branch", "--show-current"), git(ws, "rev-parse", "--short", "HEAD")


# --- the writing session ---------------------------------------------------------------


def config_dir():
    return os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")


def mentions(path, needle):
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - TAIL))
            return needle in f.read()
    except OSError:
        return False


def transcripts_with(needle):
    pattern = os.path.join(glob.escape(config_dir()), "projects", "*", "*.jsonl")
    now = time.time()
    return [
        p for p in glob.glob(pattern)
        if now - os.path.getmtime(p) <= RECENT and mentions(p, needle)
    ]


def find_transcript(nonce):
    """The one recent transcript that contains nonce, else None with a warning.

    Claude Code writes the transcript a few seconds behind the tool call, so the nonce
    may not be on disk yet. Wait for it, but stop at once if it shows up twice."""
    if not NONCE_RE.match(nonce):
        warn("--nonce must be 8 or more letters and digits, so session and transcript are not recorded.")
        return None
    deadline = time.time() + env_number("SUPERCHARGE_HANDOFF_WAIT", 10)
    while True:
        hits = transcripts_with(nonce.encode())
        if hits or time.time() >= deadline:
            break
        time.sleep(0.25)
    if len(hits) == 1:
        return hits[0]
    if hits:
        warn(f"the nonce is in {len(hits)} transcripts, so session and transcript are not recorded.")
    else:
        warn("no recent transcript holds the nonce, so session and transcript are not recorded.")
    return None


# --- validating and stamping -----------------------------------------------------------


def label(el):
    hint = el.get("path") or " ".join((el.text or "").split())[:40]
    return f'<{el.tag}> "{hint}"' if hint else f"<{el.tag}>"


def check_item(el):
    errors = []
    for attr, allowed in ENUMS.get(el.tag, {}).items():
        value = el.get(attr)
        options = "|".join(allowed)
        if value is None:
            errors.append(f'{label(el)} needs {attr}="{options}"')
        elif value not in allowed:
            errors.append(f'{label(el)} has {attr}="{value}"; use {options}')
    if el.tag == "f" and el.get("state") == "deleted" and not (el.get("recover") or "").strip():
        errors.append(f'{label(el)} is deleted, so it needs recover="PATH|transcript|none"')
    if len(el):
        errors.append(f"{label(el)} holds text only, not child elements")
    return errors


def check_container(box):
    errors = []
    item_tag = CONTAINERS[box.tag]
    if (box.text or "").strip():
        errors.append(f"<{box.tag}> holds <{item_tag}> elements, not bare text")
    for item in box:
        if item.tag == item_tag:
            errors += check_item(item)
        else:
            errors.append(f"<{item.tag}> is not allowed in <{box.tag}>; use <{item_tag}>")
    return errors


def validate(root):
    """Every problem with the tree, each naming the element at fault."""
    errors = []
    if not (root.findtext("goal") or "").strip():
        errors.append("<goal> is required")
    if len(root.findall("detail")) > 1:
        errors.append("only one <detail> is allowed")
    known = ", ".join(list(CONTAINERS) + list(TEXT_ONLY))
    for child in root:
        if child.tag in CONTAINERS:
            errors += check_container(child)
        elif child.tag in TEXT_ONLY:
            if len(child):
                errors.append(f"<{child.tag}> holds text only, not child elements")
        else:
            errors.append(f"<{child.tag}> is not allowed in <handoff>; use {known}")
    return errors


def parse_handoff(raw):
    if "<!DOCTYPE" in raw:
        sys.exit("handoff: remove the <!DOCTYPE ...> declaration and resend.")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        sys.exit(f"handoff: not well-formed XML ({e}). Escape & < > in text and resend.")
    if root.tag != "handoff":
        sys.exit(f"handoff: root element must be <handoff>, got <{root.tag}>.")
    problems = validate(root)
    if problems:
        sys.exit("handoff: fix these and resend:\n" + "\n".join(f"  - {p}" for p in problems))
    return root


def stamp(root, ws, nonce):
    # The script owns the metadata, so the model cannot get it wrong.
    root.attrib.clear()
    root.set("version", FORMAT_VERSION)
    root.set("created", datetime.now().astimezone().isoformat(timespec="minutes"))
    root.set("workspace", ws)
    branch, head = branch_and_head(ws)
    if branch:
        root.set("branch", branch)
    if head:
        root.set("head", head)
    if not nonce:
        warn("no --nonce given, so session and transcript are not recorded.")
        return
    transcript = find_transcript(nonce)
    if transcript:
        root.set("session", os.path.splitext(os.path.basename(transcript))[0])
        root.set("transcript", os.path.abspath(transcript))


def warn_if_unrecoverable(root):
    if root.get("transcript"):
        return
    for f in root.iter("f"):
        if f.get("recover") == "transcript":
            warn(f'{label(f)} says recover="transcript" but no transcript was recorded.')


def take_detail(root, ws):
    """Remove <detail> text from the tree, leaving a pointer. Returns the text, or None."""
    detail = root.find("detail")
    if detail is None:
        return None
    root.remove(detail)
    text = detail.text or ""
    if not text.strip():
        return None
    ref = f"handoff-{workspace_key(ws)}{SIDECAR}"
    ET.SubElement(root, "detail", ref=ref, lines=str(len(text.splitlines())))
    return text


def warn_if_large(text):
    lines, size = len(text.splitlines()), len(text.encode("utf-8"))
    if lines > MAX_LINES or size > MAX_BYTES:
        warn(
            f"saved, but {lines} lines and {size} bytes is over the budget of "
            f"{MAX_LINES} lines and {MAX_BYTES} bytes. Cut status, and move long material to <detail>."
        )


# --- files -----------------------------------------------------------------------------


def write_atomic(path, text):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(text.encode("utf-8"))
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def emit(path):
    with open(path, "rb") as f:
        sys.stdout.buffer.write(f.read())
    sys.stdout.buffer.flush()


def preview(text, limit):
    text = " ".join((text or "").split())
    return text[:limit] + ("…" if len(text) > limit else "")


def short(session):
    return session[:8] if session else "unknown"


def age(seconds):
    if seconds < 3600:
        return f"{max(1, int(seconds // 60))} min"
    if seconds < 86400:
        return f"{int(seconds // 3600)} h"
    return f"{int(seconds // 86400)} d"


def read_meta(path):
    """Root attributes plus the goal of a saved handoff; empty if it cannot be read.

    Version 1 files read the same way."""
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        if "<!DOCTYPE" in raw:
            return {}
        root = ET.fromstring(raw)
    except (OSError, ValueError, ET.ParseError):
        return {}
    return {**root.attrib, "goal": root.findtext("goal") or ""}


def created_at(meta, path):
    try:
        return datetime.fromisoformat(meta["created"]).astimezone().timestamp()
    except (KeyError, ValueError):
        return os.path.getmtime(path)


def move(src, dest):
    shutil.move(src, dest)
    os.utime(dest, None)  # retention counts from the day it was archived


def archive(path):
    """Move a handoff, and its detail sidecar, into archive/. Returns the new path."""
    meta = read_meta(path)
    key = os.path.basename(path)[len("handoff-"):-len(".xml")]
    created = meta.get("created") or time.strftime(
        "%Y-%m-%dT%H%M", time.localtime(os.path.getmtime(path))
    )
    private_dir(archive_dir())
    base = os.path.join(archive_dir(), f"handoff-{key}-{re.sub(r'[^0-9A-Za-z+-]', '', created)}")
    dest, n = base + ".xml", 1
    while os.path.exists(dest):
        n += 1
        dest = f"{base}-{n}.xml"
    if os.path.exists(sidecar_of(path)):
        move(sidecar_of(path), sidecar_of(dest))
    move(path, dest)
    return dest


def archive_replaced(ws):
    for old in live_paths(ws):
        meta, seconds = read_meta(old), time.time() - os.path.getmtime(old)
        dest = archive(old)
        print(
            f"replaced: {preview(meta.get('goal'), 80)} "
            f"({age(seconds)}, session {short(meta.get('session'))}) archived at {dest}"
        )


def prune_archive():
    cutoff = time.time() - env_number("SUPERCHARGE_HANDOFF_KEEP_DAYS", 30) * 86400
    for path in glob.glob(os.path.join(glob.escape(archive_dir()), "handoff-*")):
        try:
            if os.path.getmtime(path) < cutoff:
                os.remove(path)
        except OSError:
            pass


# --- commands --------------------------------------------------------------------------


def resolve(args):
    return workspace(args.workspace or os.getcwd())


def cmd_write(args):
    ws = resolve(args)
    root = parse_handoff(sys.stdin.read())
    stamp(root, ws, args.nonce)
    warn_if_unrecoverable(root)
    detail = take_detail(root, ws)
    ET.indent(root)
    text = ET.tostring(root, encoding="unicode") + "\n"

    path = handoff_path(ws)
    private_dir(handoff_dir())
    archive_replaced(ws)
    prune_archive()
    if detail is not None:
        write_atomic(sidecar_of(path), detail)
    write_atomic(path, text)
    warn_if_large(text)
    print(f"{path} ({os.path.getsize(path)} bytes)")


def cmd_read(args):
    ws = resolve(args)
    path = find_live(ws)
    if not path:
        sys.exit(f"handoff: nothing saved for {ws}.")
    if args.detail:
        if not os.path.exists(sidecar_of(path)):
            sys.exit("handoff: this handoff has no detail.")
        path = sidecar_of(path)
    emit(path)


def cmd_clear(args):
    path = find_live(resolve(args))
    if path:
        print(f"archived {archive(path)}")
    else:
        print("nothing to clear")


def cmd_list(args):
    ws = resolve(args)
    rows = []
    for path in live_paths(ws) + archived(ws):
        meta = read_meta(path)
        # created has minute resolution, so two saves in one minute fall back to file time
        rows.append(((created_at(meta, path), os.path.getmtime(path)), path, meta))
    if not rows:
        print(f"no handoffs for {ws}")
    for _, path, meta in sorted(rows, key=lambda row: row[0], reverse=True):
        fields = [path, meta.get("created", "unknown"), short(meta.get("session")), preview(meta.get("goal"), 80)]
        print("\t".join(fields))


def cmd_path(args):
    ws = resolve(args)
    print(find_live(ws) or handoff_path(ws))


# --- the SessionStart hook -------------------------------------------------------------


def say(message):
    json.dump(
        {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": message}},
        sys.stdout,
    )


def head_drift(ws, stamped):
    found = resolve_head(ws)
    if not stamped or not found or not found[1]:
        return "head unknown"
    if found[1].startswith(stamped):
        return f"HEAD has not moved since the handoff ({stamped})"
    return f"HEAD moved: the handoff was at {stamped}, it is now {found[1][:7]}"


def archived_lately(ws, within=86400):
    return sum(1 for p in archived(ws) if time.time() - os.path.getmtime(p) <= within)


def offer(ws, meta, seconds):
    me = shlex.quote(os.path.abspath(__file__))
    flag = f"--workspace {shlex.quote(ws)}"
    facts = (
        f"Written {age(seconds)} ago by session {short(meta.get('session'))}; "
        f"{head_drift(ws, meta.get('head'))}."
    )
    lately = archived_lately(ws)
    if lately:
        facts += f" Archived for this folder in the last 24 h: {lately}."
    return "\n".join([
        "A session handoff for this folder is waiting.",
        f"Goal: {preview(meta.get('goal'), 160) or 'unknown'}",
        facts,
        "In your first reply, tell the user it exists and ask whether to pick it up, then carry on "
        "with whatever they asked. If their request is clearly unrelated to the goal, mention the "
        "handoff in one line and carry on. Do not read it until they say yes.",
        f"On yes: run `python3 {me} read {flag}`, give the goal, status and next steps in three "
        f"lines, keeping the basis labels (say which status lines are only inferred), note head "
        f"drift, then run `python3 {me} clear {flag}`, which archives it so the next session is "
        f"not asked again. `read --detail {flag}` prints the long revisit material if you need it.",
        "On no: leave it alone.",
    ])


def offer_handoff():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    if not isinstance(event, dict) or event.get("source") == "compact":
        return
    ws = workspace(event.get("cwd") or os.getcwd())
    path = find_live(ws)
    if not path:
        return
    meta = read_meta(path)
    if event.get("session_id") and event.get("session_id") == meta.get("session"):
        return  # this session wrote it, so it already has the context
    seconds = time.time() - os.path.getmtime(path)
    if seconds > env_number("SUPERCHARGE_HANDOFF_MAX_AGE_DAYS", 14) * 86400:
        dest = archive(path)
        say(
            f"A session handoff for this folder was {age(seconds)} old, so it was archived at {dest} "
            f"instead of offered. Its goal was: {preview(meta.get('goal'), 160) or 'unknown'}. "
            f"Tell the user once, in one line, then carry on."
        )
        return
    say(offer(ws, meta, seconds))


def cmd_hook(args):
    try:
        offer_handoff()
    except Exception as e:  # a hook must never break session start
        warn(f"hook skipped: {e}")


def main(argv=None):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--workspace", metavar="ROOT", help="workspace folder (default: the current folder)")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True, metavar="CMD")
    commands.add_parser("write", parents=[common]).add_argument(
        "--nonce", metavar="TOKEN", help="8 or more letters and digits you typed literally in this command"
    )
    commands.add_parser("read", parents=[common]).add_argument(
        "--detail", action="store_true", help="print the detail sidecar instead"
    )
    for name in ("clear", "list", "path"):
        commands.add_parser(name, parents=[common])
    commands.add_parser("hook")

    args = parser.parse_args(argv)
    {
        "write": cmd_write,
        "read": cmd_read,
        "clear": cmd_clear,
        "list": cmd_list,
        "path": cmd_path,
        "hook": cmd_hook,
    }[args.command](args)


if __name__ == "__main__":
    main()
