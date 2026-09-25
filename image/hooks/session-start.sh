#!/usr/bin/env bash
# documentation-as-os :: SessionStart hook
# Boots the OS: injects the live state into context + resets graceful-enforcement to STRICT (auto-expire).
# stdout is injected into the agent's context — keep it SMALL (it runs every session).
# REFERENCE implementation — validate/tune in the bootstrap dogfood run.
set -uo pipefail
ROOT="${CLAUDE_PROJECT_DIR:-.}"
MODE_FILE="$ROOT/.claude/os-mode"

# Auto-expire: every session starts strict unless re-relaxed this session.
PREV="$(cat "$MODE_FILE" 2>/dev/null || echo strict)"
echo strict > "$MODE_FILE" 2>/dev/null || true

echo "=== documentation-as-os :: boot (constitution §1 — read this before starting) ==="
if [ "$PREV" = "relaxed" ]; then
  echo "(gating was RELAXED last session → reset to STRICT; run '/gating relax' to stay loose)"
fi

echo "--- STATUS (where we are / next / blocked) ---"
sed -n '1,40p' "$ROOT/docs/delivery/STATUS.md" 2>/dev/null || echo "(no STATUS yet — run the bootstrap)"

echo "--- open doc-debt (reconcile with /reconcile-docs) ---"
grep -E '^- \[ \]' "$ROOT/docs/delivery/doc-debt.md" 2>/dev/null | head -20 || echo "(none)"

echo "--- memory index ---"
sed -n '1,30p' "$ROOT/memory/MEMORY.md" 2>/dev/null || echo "(using the runtime's native memory)"

echo "=== end boot ==="
exit 0
