#!/usr/bin/env bash
# documentation-as-os :: PostToolUse(Edit|Write) hook — docs-part-of-done nudge.
# If a likely-CODE file changed, remind to update its doc in the same change (constitution: done = code+docs in sync).
# In relaxed mode, also log it as doc-debt. Non-blocking.
# REFERENCE implementation + HEURISTIC (false positives possible) — validate/tune in the dogfood run.
set -uo pipefail
ROOT="${CLAUDE_PROJECT_DIR:-.}"
INPUT="$(cat 2>/dev/null || true)"
MODE="$(cat "$ROOT/.claude/os-mode" 2>/dev/null || echo strict)"

# Pull the edited file path out of the hook input (best-effort; tune to the real schema).
FILE="$(printf '%s' "$INPUT" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 | sed -E 's/.*"([^"]+)"$/\1/')"

# Only nudge for likely code — skip docs and markdown.
case "$FILE" in
  ""|*/docs/*|*.md|*.mdx) exit 0 ;;
esac

MSG="docs-part-of-done: '$FILE' changed — update its doc in the same change (constitution: done = code+docs in sync)."
if [ "$MODE" = "relaxed" ]; then
  echo "- [ ] $FILE — doc not yet updated ($(date +%F))" >> "$ROOT/docs/delivery/doc-debt.md" 2>/dev/null || true
  MSG="$MSG  [gating relaxed → logged as doc-debt; run /reconcile-docs later]"
fi

# Surface as a non-blocking reminder (stdout). The structured-JSON additionalContext form is the alternative — verify at wiring.
echo "$MSG"
exit 0
