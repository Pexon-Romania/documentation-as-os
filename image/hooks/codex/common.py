#!/usr/bin/env python3
"""Shared helpers for the documentation-as-os Codex hook adapter."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def read_event() -> dict[str, Any]:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, OSError):
        return {}


def repo_root(event: dict[str, Any]) -> Path:
    candidates = [event.get("cwd"), os.environ.get("CODEX_PROJECT_DIR"), os.getcwd()]
    for value in candidates:
        if not value:
            continue
        start = Path(str(value)).expanduser().resolve()
        for candidate in (start, *start.parents):
            if (candidate / "docs" / "delivery").is_dir():
                return candidate
    try:
        value = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=os.getcwd(),
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if value:
            return Path(value).resolve()
    except (OSError, subprocess.CalledProcessError):
        pass
    return Path(os.getcwd()).resolve()


def mode_file(root: Path) -> Path:
    # Shared deliberately with Claude Code so a "both" install has one enforcement mode.
    return root / ".claude" / "os-mode"


def read_mode(root: Path) -> str:
    try:
        value = mode_file(root).read_text(encoding="utf-8").strip()
    except OSError:
        return "strict"
    return value if value in {"strict", "relaxed"} else "strict"


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False))
