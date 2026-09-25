#!/usr/bin/env python3
"""Codex Stop: continue once when strict mode has open documentation debt."""

from __future__ import annotations

import sys

from common import emit, read_event, read_mode, repo_root


event = read_event()
root = repo_root(event)
mode = read_mode(root)
debt_file = root / "docs" / "delivery" / "doc-debt.md"

missing = not debt_file.is_file()
try:
    debt = sum(1 for line in debt_file.read_text(encoding="utf-8").splitlines() if line.startswith("- [ ]"))
except OSError:
    debt = 0

if event.get("stop_hook_active") is True:
    emit({})
    raise SystemExit(0)

if missing:
    emit(
        {
            "systemMessage": (
                "stop-gate: docs/delivery/doc-debt.md is missing; the gate is running blind. "
                "Recreate it from the documentation-as-os skeleton."
            )
        }
    )
    raise SystemExit(0)

if mode == "relaxed":
    payload = {}
    if debt:
        payload["systemMessage"] = f"Gating relaxed: {debt} open doc-debt item(s); use $reconcile-docs later."
    emit(payload)
    raise SystemExit(0)

if debt:
    print(
        f"Hold on - {debt} open doc-debt item(s). Reconcile with $reconcile-docs, "
        "defer with $gating relax, or confirm they are deliberate cross-session commitments.",
        file=sys.stderr,
    )
    raise SystemExit(2)

emit(
    {
        "systemMessage": (
            "Before you stop: update STATUS and every document touched by the change; "
            "surface any unfiled [OS] findings."
        )
    }
)
