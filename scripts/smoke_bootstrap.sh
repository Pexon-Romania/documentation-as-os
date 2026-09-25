#!/usr/bin/env bash
# smoke_bootstrap.sh — CI smoke test of the install path (the mechanical half of BOOTSTRAP.md).
# An agent-run bootstrap can't be CI'd; this proves what CAN be: the image is complete, the
# templates instantiate, placeholders are enumerable, stamp/lock/door land, and a fresh team
# instance passes its own validator (including the ENV-STATE / MANIFEST-SYNC / SPEC-STATUS
# checks firing on cue). The agent-run half is re-earned at every MINOR/MAJOR release
# (CONTRIBUTING — the release checklist).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
IMG="$ROOT/image"
W="$(mktemp -d)"
trap 'rm -rf "$W"' EXIT
fail() { echo "SMOKE FAIL: $*" >&2; exit 1; }

# ── Part 0 · the image is complete ──────────────────────────────────────────────
for f in VERSION MANIFEST.json BOOTSTRAP.md UPGRADE.md INSTANCE-CONTRACT.md \
         CONSTITUTION.template.md SELF-ENFORCEMENT.md \
         skeleton/SKELETON.md skeleton/STATUS.template.md skeleton/doc-debt.template.md \
         hooks/settings.template.json hooks/session-start.sh hooks/post-edit-docs.sh hooks/stop-gate.sh \
         system/validate_docs.template.py system/validate-docs.template.yml \
         system/CODEOWNERS.template system/ruleset.template.json system/GOVERNANCE-RUNBOOK.md; do
  [ -f "$IMG/$f" ] || fail "image incomplete: image/$f missing"
done
for s in scope-lock workstream handover reconcile-docs gating; do
  [ -f "$IMG/skills/$s/SKILL.md" ] || fail "image incomplete: skill '$s' missing"
done
for t in AGENTS BOOT README-ROUTER CONVENTIONS LEARNINGS WORK_TRACKER CHANGELOG ENVIRONMENTS; do
  [ -f "$IMG/templates/$t.template.md" ] || fail "image incomplete: templates/$t.template.md missing"
done
grep -q '"files"' "$IMG/MANIFEST.json" || fail "image/MANIFEST.json has no files map"
DOOR="https://github.com/flaviusmoldovan-pexon/documentation-as-os"
grep -q "$DOOR" "$IMG/BOOTSTRAP.md" || fail "BOOTSTRAP.md carries no upstream door"
echo "smoke 0/3: image complete"

# ── Part 1 · solo-profile mechanical install (what STEP 1-6 produce, scripted) ──
S="$W/solo"; mkdir -p "$S/docs/delivery" "$S/.claude/hooks"
sed -E 's/\{\{[^}]*\}\}/X/g' "$IMG/CONSTITUTION.template.md" > "$S/CLAUDE.md"
VER="$(tr -d '[:space:]' < "$IMG/VERSION")"
{ printf '\n## OS report-back (standing)\nOS-level findings: draft the upstream issue at %s/issues/new (os-bug | improvement | suggestion), include the image version + profile from the footer stamp; un-filed drafts live under "## OS findings (to file upstream)" in STATUS.\n' "$DOOR"
  printf '\n<!-- documentation-as-os · image %s · profile: solo · installed %s · upstream: %s -->\n' "$VER" "$(date +%F)" "$DOOR"; } >> "$S/CLAUDE.md"
sed -E 's/\{\{[^}]*\}\}/X/g' "$IMG/skeleton/STATUS.template.md" > "$S/docs/delivery/STATUS.md"
sed -E 's/\{\{[^}]*\}\}/X/g' "$IMG/skeleton/doc-debt.template.md" > "$S/docs/delivery/doc-debt.md"
for s in scope-lock workstream handover reconcile-docs gating; do
  mkdir -p "$S/.claude/skills/$s"; cp "$IMG/skills/$s/SKILL.md" "$S/.claude/skills/$s/"
done
cp "$IMG"/hooks/*.sh "$S/.claude/hooks/"; chmod +x "$S/.claude/hooks/"*.sh
echo strict > "$S/.claude/os-mode"
cp "$IMG/MANIFEST.json" "$S/docs/OS-MANIFEST.lock"
grep -q '{{' "$S/CLAUDE.md" && fail "solo: unfilled placeholder survived in CLAUDE.md"
grep -q "profile: solo" "$S/CLAUDE.md" || fail "solo: stamp missing"
grep -q "$DOOR/issues" "$S/CLAUDE.md" || fail "solo: door missing"
grep -q '"files"' "$S/docs/OS-MANIFEST.lock" || fail "solo: lock missing/empty"
[ -x "$S/.claude/hooks/stop-gate.sh" ] || fail "solo: hooks not executable"
# the stop-gate must run against the fresh instance and allow a clean stop (no debt)
( cd "$S" && CLAUDE_PROJECT_DIR="$S" bash .claude/hooks/stop-gate.sh </dev/null >/dev/null 2>&1 ) || fail "solo: stop-gate errored on a clean instance"
echo "smoke 1/3: solo instantiation OK (stamp + lock + door + hooks live)"

# ── Part 2 · team-profile synthetic instance passes its own validator ──────────
T="$W/team"; mkdir -p "$T"/{scripts,app-documentation,dependencies,support,leaders,delivery/specs,delivery/incidents,.github/workflows}
# knobs: strip the template header (first '# ═' block), set the id prefix
sed '/^# ═/,/^# ═/d' "$IMG/system/validate_docs.template.py" | sed 's/^ID_PREFIXES = ()/ID_PREFIXES = ("PL",)/' > "$T/scripts/validate_docs.py"
echo "name: validate" > "$T/.github/workflows/validate-docs.yml"
echo "# boot" > "$T/CLAUDE.md"
cp "$IMG/MANIFEST.json" "$T/OS-MANIFEST.lock"   # root lock must be structure-lock legal
fm() { printf -- "---\napp: synth\naudience: [engineers]\nscope: %s\nstatus: live-prod\ncovers: %s\nkeywords: [x]\nsources: [%s]\nrelated: [%s]\nlast_verified: %s\n---\n\n" "$1" "$2" "$3" "$4" "$(date +%F)"; }
{ fm shareable "map" "" "AGENTS.md, DOCS-STANDARD.md, DOCS-SYSTEM.md, delivery/CHANGELOG.md, delivery/WORK_TRACKER.md, delivery/specs/TEST_SPEC.md, dependencies/ENVIRONMENTS.md, app-documentation/01-CORE.md"; echo "# Map"; } > "$T/README.md"
{ fm internal "protocol" "" "README.md"; echo "# Protocol"; } > "$T/AGENTS.md"
{ fm internal "standard" "" "README.md"; echo "# Standard"; } > "$T/DOCS-STANDARD.md"
{ fm shareable "system" "" "README.md"; echo "# System"; } > "$T/DOCS-SYSTEM.md"
{ fm shareable "core doc" "app/core.py" "../README.md"; printf "# Core\n\nThe rules table ships empty.\n\npad\npad\n\nzero rows in dev (admin panel, %s) — evidenced.\n" "$(date +%F)"; } > "$T/app-documentation/01-CORE.md"
{ fm internal "changelog" "" "../README.md"; printf "# Changelog\n### %s\n## On dev — awaiting promotion\n- **PL-2 — pending**\n## Shipped to prod\n- **PL-1 — shipped**\n" "$(date +%F)"; } > "$T/delivery/CHANGELOG.md"
{ fm internal "board" "" "../README.md"; printf "# Board\n| PL-1 | building | — |\n"; } > "$T/delivery/WORK_TRACKER.md"
{ printf -- "---\napp: synth\naudience: [engineers]\nscope: internal\nstatus: dev-only\ncovers: spec\nkeywords: [x]\nsources: []\nrelated: [../../README.md]\nlast_verified: %s\n---\n\n# Spec PL-1\n" "$(date +%F)"; } > "$T/delivery/specs/TEST_SPEC.md"
{ fm internal "envs" "" "../README.md"; echo "# Envs"; } > "$T/dependencies/ENVIRONMENTS.md"
OUT="$(python3 "$T/scripts/validate_docs.py" --write-manifest 2>&1)" || fail "team: validator FAILed on a fresh instance:
$OUT"
echo "$OUT" | grep -q "ENV-STATE:"        || fail "team: ENV-STATE warn did not fire"
echo "$OUT" | grep -q "BOARD↔CHANGELOG:"  || fail "team: BOARD↔CHANGELOG warn did not fire"
echo "$OUT" | grep -q "SPEC-STATUS:"      || fail "team: SPEC-STATUS warn did not fire"
echo "$OUT" | grep -q "OS-MANIFEST.lock"  && fail "team: root OS-MANIFEST.lock was flagged — structure lock must allow it"
python3 "$T/scripts/validate_docs.py" >/dev/null 2>&1 || fail "team: MANIFEST-SYNC failed on a fresh manifest"
sed -i.bak 's/covers: core doc/covers: core doc CHANGED/' "$T/app-documentation/01-CORE.md" && rm -f "$T/app-documentation/01-CORE.md.bak"
python3 "$T/scripts/validate_docs.py" >/dev/null 2>&1 && fail "team: stale manifest was NOT caught (MANIFEST-SYNC)"
echo "smoke 2/3: team instantiation OK (validator PASS; ENV-STATE/BOARD/SPEC fire; SYNC catches staleness)"

echo "smoke 3/3: PASS"
