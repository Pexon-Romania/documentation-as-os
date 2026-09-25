# Codex hook adapter

This adapter implements the same stable enforcement contract as the Claude Code hooks:
`SessionStart` read-in, `PostToolUse(Edit|Write)` documentation nudging, and a graceful `Stop`
gate. It uses Codex's repository-local hook layer.

Install `hooks.template.json` as `.codex/hooks.json`, copy `common.py`, `session_start.py`,
`post_edit_docs.py`, and `stop_gate.py` into `.codex/hooks/`, then review and trust the exact
definitions with Codex's `/hooks` command. Changed hooks must be reviewed again. Project hooks
only load in a trusted project.

Both runtime adapters deliberately share `.claude/os-mode`. That path is part of the established
instance contract, and one shared value prevents a Claude+Codex installation from enforcing two
different modes.

The command template resolves scripts from the git root and is validated on macOS/Linux. On
Windows, set each handler's `commandWindows` during bootstrap and verify it in a real Codex
session before relying on it.

The Python programs use only the standard library. `SessionStart` writes small model context;
`PostToolUse` returns structured `additionalContext`; `Stop` exits `2` to continue once when
strict mode has open debt and honors `stop_hook_active` to avoid loops.

---

*Part of documentation-as-os (`image/hooks/codex/`). Proprietary material owned by Pexon
Romania and Flavius Moldovan. Reference implementation; the artifact wins.*
