#!/usr/bin/env python3
"""Codex SessionStart: inject live state and reset graceful enforcement to strict."""

from __future__ import annotations

from common import mode_file, read_event, read_mode, repo_root


def excerpt(path, limit: int, missing: str) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()[:limit]
    except OSError:
        return [missing]


event = read_event()
root = repo_root(event)
previous = read_mode(root)
target = mode_file(root)
source = event.get("source")
if source != "compact":
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("strict\n", encoding="utf-8")
    except OSError:
        pass

lines = ["=== documentation-as-os :: boot (read before starting) ==="]
if source == "compact":
    lines.append(f"(context rehydrated after compaction; gating remains {previous.upper()})")
elif previous == "relaxed":
    lines.append("(gating was RELAXED last session -> reset to STRICT; use $gating relax to stay loose)")
lines.append("--- STATUS (where we are / next / blocked) ---")
lines.extend(excerpt(root / "docs" / "delivery" / "STATUS.md", 40, "(no STATUS yet - run the bootstrap)"))
lines.append("--- open doc-debt (reconcile with $reconcile-docs) ---")
debt = excerpt(root / "docs" / "delivery" / "doc-debt.md", 10000, "")
open_items = [line for line in debt if line.startswith("- [ ]")][:20]
lines.extend(open_items or ["(none)"])
lines.append("--- memory index ---")
lines.extend(excerpt(root / "memory" / "MEMORY.md", 30, "(using the runtime's native memory)"))
lines.append("=== end boot ===")

# SessionStart accepts plain stdout as additional developer context.
print("\n".join(lines))
