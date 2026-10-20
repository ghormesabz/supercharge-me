#!/usr/bin/env bash
# Mechanical done-checks for a spec folder.
#   check-spec.sh SPEC_DIR [--static]
# Prints PASS, FAIL, REVIEW or MANUAL per check and exits 1 on any FAIL.
# REVIEW and MANUAL lines need a person. --static skips the checks that need rendered HTML.
# Written for bash 3.2 (macOS default).
set -u

dir="${1:-}"
static=0
[ "${2:-}" = "--static" ] && static=1

if [ -z "$dir" ] || [ ! -f "$dir/spec.qmd" ]; then
  echo "usage: check-spec.sh SPEC_DIR [--static]   (SPEC_DIR must hold spec.qmd)" >&2
  exit 2
fi

spec="$dir/spec.qmd"
fails=0

pass()   { printf 'PASS    %s\n' "$1"; }
fail()   { printf 'FAIL    %s\n' "$1"; fails=$((fails + 1)); }
review() { printf 'REVIEW  %s\n' "$1"; }
manual() { printf 'MANUAL  %s\n' "$1"; }
indent() { sed 's/^/          /'; }
count()  { grep -o "$1" "$2" 2>/dev/null | wc -l | tr -d ' '; }

if grep -q -E '^spec-draft:[[:space:]]*true' "$spec"; then mode=draft; else mode=final; fi
echo "spec: $spec   mode: $mode"

# --- Outputs, Part B visibility, banner, size (need rendered HTML) ---------
if [ "$static" -eq 0 ]; then
  if [ "$mode" = draft ]; then need="design-review.html"; else need="design-sheet.html build-spec.html"; fi
  missing=""
  for f in $need; do [ -f "$dir/$f" ] || missing="$missing $f"; done
  if [ -n "$missing" ]; then
    fail "outputs missing:$missing (run render.sh)"
  else
    pass "outputs exist: $need"

    if [ "$mode" = draft ]; then
      n="$(count 'id="part-b"' "$dir/design-review.html")"
      if [ "$n" = 1 ]; then pass "Part B present once in design-review.html"; else fail "design-review.html shows Part B $n times, expected 1 (does this Quarto ignore when-meta?)"; fi
      b="$(count 'class="banner"' "$dir/design-review.html")"
      if [ "$b" -ge 1 ]; then pass "draft banner present in design-review.html"; else fail "draft banner missing from design-review.html"; fi
    else
      n="$(count 'id="part-b"' "$dir/design-sheet.html")"
      if [ "$n" = 0 ]; then pass "Part B absent from design-sheet.html"; else fail "design-sheet.html shows Part B $n times, expected 0 (does this Quarto ignore when-meta?)"; fi
      n="$(count 'id="part-b"' "$dir/build-spec.html")"
      if [ "$n" = 1 ]; then pass "Part B present once in build-spec.html"; else fail "build-spec.html shows Part B $n times, expected 1"; fi
      b1="$(count 'class="banner"' "$dir/design-sheet.html")"
      b2="$(count 'class="banner"' "$dir/build-spec.html")"
      if [ "$b1" = 0 ] && [ "$b2" = 0 ]; then pass "no draft banner in the final copies"; else fail "draft banner still present in a final copy (is spec-draft false?)"; fi
    fi

    for f in $need; do
      bytes="$(wc -c < "$dir/$f" | tr -d ' ')"
      if [ "$bytes" -le 3000000 ]; then pass "$f is $bytes bytes"; else fail "$f is $bytes bytes, over the 3,000,000 limit"; fi
    done
  fi
else
  echo "SKIP    outputs, Part B, banner and size (--static)"
fi

# --- Placeholders and comments ---------------------------------------------
hits="$(grep -n -E '\{\{|<!--' "$spec" || true)"
if [ -z "$hits" ]; then pass "no placeholders or HTML comments in spec.qmd"; else fail "placeholders or HTML comments in spec.qmd:"; printf '%s\n' "$hits" | indent; fi

# --- Writing rules ----------------------------------------------------------
em="$(grep -n $'\xe2\x80\x94' "$spec" || true)"
if [ -z "$em" ]; then pass "no em dashes"; else fail "em dashes:"; printf '%s\n' "$em" | indent; fi

hype="$(grep -n -i -E '(delve|leverag|utili[sz]|robust|streamlin|facilitat|empower|seamless|cutting-edge)' "$spec" || true)"
if [ -z "$hype" ]; then pass "no hype words"; else fail "hype words:"; printf '%s\n' "$hype" | indent; fi

filler="$(grep -n -i -w -E 'just|simply|actually|literally' "$spec" || true)"
if [ -z "$filler" ]; then pass "no filler adverbs"; else review "filler adverbs. Cut each unless it carries emphasis or contrast:"; printf '%s\n' "$filler" | indent; fi

# --- Builder terms in Part A -------------------------------------------------
terms="$(sed -n '/^# For domain review/,/^# For the build team/p' "$spec" | grep -n -i -w -E '(llm|api|sql|json|schema|vector|token|prompt|endpoint|pipeline|embedding|latency|p95|container)s?' || true)"
if [ -z "$terms" ]; then pass "no builder terms in Part A"; else review "builder terms in Part A. Replace each, or gloss it if the expert used it:"; printf '%s\n' "$terms" | indent; fi

# --- Secrets -----------------------------------------------------------------
rigid='(sk|pk)-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|xox[baprs]-[A-Za-z0-9-]{10,}|Bearer [A-Za-z0-9._~+/=-]{20,}|[A-Za-z][A-Za-z0-9+.-]*://[^[:space:]/:@]+:[^[:space:]/@]+@'
loose='(password|passwd|secret|api[_-]?key|token)[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9/+_-]{12,}'
s1="$(grep -n -E "$rigid" "$spec" || true)"
if [ -z "$s1" ]; then pass "no key, token or connection string values"; else fail "possible secret values (name the variable, never the value; tell the user to rotate it):"; printf '%s\n' "$s1" | cut -c1-80 | indent; fi
s2="$(grep -n -i -E "$loose" "$spec" || true)"
if [ -n "$s2" ]; then review "lines that look like name=value secrets:"; printf '%s\n' "$s2" | cut -c1-80 | indent; fi

# --- B13 decision register ---------------------------------------------------
reg="$(awk '/^## B13/ {on=1; next} on && /^#/ {exit} on && /^\|/ {print}' "$spec")"
if [ -z "$reg" ]; then
  fail "B13 decision register table not found"
else
  bad="$(printf '%s\n' "$reg" | awk -F'|' '
    function trim(s) { gsub(/^[ \t]+|[ \t]+$/, "", s); return s }
    NR == 1 { next }
    $0 ~ /^\|[ \t]*:?-+/ { next }
    {
      id = trim($2); st = trim($4); why = trim($5)
      if (st !~ /^(Locked|Deferred|Experiment|Open)$/) { printf("row %s: status \"%s\" is not Locked, Deferred, Experiment or Open\n", id, st); next }
      if (why == "" || why ~ /^\{\{/) {
        need = "a reason"
        if (st == "Deferred") need = "a trigger"
        if (st == "Experiment") need = "a kill condition"
        if (st == "Open") need = "an owner"
        printf("row %s: %s needs %s\n", id, st, need)
      }
    }')"
  if [ -n "$bad" ]; then fail "B13 register:"; printf '%s\n' "$bad" | indent; else pass "B13 statuses valid and every row has its reason, trigger, kill condition or owner"; fi
  if printf '%s\n' "$reg" | grep -q 'D-compat'; then pass "B13 holds the D-compat row"; else fail "B13 is missing the D-compat row"; fi
fi

# --- Hand-off files (final only) ----------------------------------------------
if [ "$mode" = final ]; then
  case "$dir" in
    */docs/spec/*)
      root="$(cd "$dir/../../.." 2>/dev/null && pwd)"
      if [ -f "$root/AGENTS.md" ]; then
        lines="$(wc -l < "$root/AGENTS.md" | tr -d ' ')"
        if [ "$lines" -le 60 ]; then pass "AGENTS.md is $lines lines"; else fail "AGENTS.md is $lines lines, over 60"; fi
        if grep -q '{{' "$root/AGENTS.md"; then fail "AGENTS.md still holds a placeholder"; else pass "AGENTS.md has no placeholders"; fi
      else
        fail "AGENTS.md not found at $root"
      fi
      if [ -f "$root/CLAUDE.md" ] && [ "$(tr -d '[:space:]' < "$root/CLAUDE.md")" = "@AGENTS.md" ]; then
        pass "CLAUDE.md is the one-line @AGENTS.md import"
      else
        fail "CLAUDE.md missing or not exactly @AGENTS.md"
      fi
      ;;
    *) manual "spec is not under docs/spec/SLUG, so AGENTS.md and CLAUDE.md were not checked" ;;
  esac
fi

# --- Checks that need a person -------------------------------------------------
manual "A3 and A4: every artefact in the .in and .out lanes is a row in A4 with the same words, and every A4 row is in a lane"
manual "Figures: run figure-shots.sh on the rendered HTML and look at every PNG"

echo "---"
if [ "$fails" -gt 0 ]; then
  echo "FAILED: $fails check(s)"
  exit 1
fi
echo "OK. Do the REVIEW and MANUAL lines yourself."
exit 0
