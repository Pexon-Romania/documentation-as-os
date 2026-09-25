#!/usr/bin/env bash
# documentation-as-os :: Stop hook — GRACEFUL "won't close with open doc-debt".
# Gates on a RELIABLE signal (open doc-debt), not a brittle git-staleness guess:
#   already blocked once       -> allow (never loop)
#   relaxed                    -> allow; remind of open debt
#   strict + open doc-debt     -> block ONCE: reconcile or relax
#   strict + no debt           -> allow + a light reminder to keep STATUS current
# (Detecting docs you forgot to even log as debt is the labeled frontier — a Stop+LLM-verify hook.)
# Validated in the dogfood run 2026-06-25 (fresh + existing repo).
set -uo pipefail
ROOT="${CLAUDE_PROJECT_DIR:-.}"
INPUT="$(cat 2>/dev/null || true)"
MODE="$(cat "$ROOT/.claude/os-mode" 2>/dev/null || echo strict)"
DEBT_FILE="$ROOT/docs/delivery/doc-debt.md"

# Count open doc-debt items robustly (grep -c prints "0" AND exits 1 on no match — don't double-count).
# A checkpoint that cannot fail is not a checkpoint: a MISSING register must be loud, never a
# silent all-clear (exemplar lesson, 2026-08-18 — a freshness check that no-opped on zero repos).
DEBT=0
if [ -f "$DEBT_FILE" ]; then
  DEBT="$(grep -cE '^- \[ \]' "$DEBT_FILE" 2>/dev/null || true)"
  DEBT="${DEBT:-0}"
else
  echo "stop-gate: doc-debt register missing at ${DEBT_FILE#$ROOT/} — the gate is running blind; recreate it (skeleton/doc-debt.template.md)." >&2
fi

# Never loop: if we already blocked this stop, let it through.
if printf '%s' "$INPUT" | grep -qE '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

if [ "$MODE" = "relaxed" ]; then
  if [ "$DEBT" -gt 0 ] 2>/dev/null; then
    echo "gating relaxed — ${DEBT} open doc-debt item(s); run /reconcile-docs when you square up." >&2
  fi
  exit 0
fi

# strict
if [ "$DEBT" -gt 0 ] 2>/dev/null; then
  echo "Hold on — ${DEBT} open doc-debt item(s). Reconcile (/reconcile-docs), defer ('/gating relax'), or confirm they're deliberate cross-session commitments before stopping (constitution: done = code+docs in sync · write-out before you stop)." >&2
  exit 2   # block once on a reliable signal; reconcile or relax, then stop cleanly
fi
echo "Before you stop: update STATUS (where we are / next) + any doc your changes touched (constitution: done = code+docs in sync · write-out before you stop); any [OS] findings not yet filed upstream? (report-back section)" >&2
exit 0
