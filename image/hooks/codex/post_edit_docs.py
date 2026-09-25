#!/usr/bin/env python3
"""Codex PostToolUse(Edit|Write): nudge docs-part-of-done and log relaxed debt."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from common import emit, read_event, read_mode, repo_root


def edited_paths(event: dict) -> list[str]:
    tool_input = event.get("tool_input") if isinstance(event.get("tool_input"), dict) else {}
    found: list[str] = []
    for value in (event.get("file_path"), tool_input.get("file_path")):
        if isinstance(value, str) and value.strip():
            found.append(value.strip())
    command = tool_input.get("command")
    if isinstance(command, str):
        found.extend(
            match.strip()
            for match in re.findall(r"^\*\*\* (?:Add|Update|Delete) File:\s*(.+)$", command, re.MULTILINE)
        )
    return list(dict.fromkeys(path.replace("\n", " ").replace("\r", " ") for path in found))


def is_code(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return bool(path) and "/docs/" not in f"/{normalized}" and not normalized.endswith((".md", ".mdx"))


event = read_event()
root = repo_root(event)
paths = [path for path in edited_paths(event) if is_code(path)]
if not paths:
    raise SystemExit(0)

mode = read_mode(root)
messages: list[str] = []
for path in paths:
    message = f"docs-part-of-done: '{path}' changed - update its doc in the same change."
    if mode == "relaxed":
        debt_file = root / "docs" / "delivery" / "doc-debt.md"
        try:
            with debt_file.open("a", encoding="utf-8") as handle:
                handle.write(f"- [ ] {path} - doc not yet updated ({date.today().isoformat()})\n")
            message += " [gating relaxed -> logged as doc-debt; use $reconcile-docs later]"
        except OSError:
            message += " [gating relaxed, but the doc-debt register could not be written]"
    messages.append(message)

emit(
    {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "\n".join(messages),
        }
    }
)
