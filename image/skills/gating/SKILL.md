---
name: gating
description: Control graceful enforcement — relax the hard gates for unpredictable/urgent moments, return to strict, or check status. Relaxing logs doc-debt and auto-expires.
arguments: [mode]
---

# /gating $mode

Control the OS's enforcement mode. `$mode` = `relax` | `strict` | `status`.

- **`relax`** — set mode to `relaxed`. The hard gates (won't-close-on-stale-docs, etc.) **downgrade to warn + log doc-debt** instead of block — for unpredictable, urgent, or exploratory moments. It is **loud** (open debt shown every session) and **auto-expires to `strict` next session** unless re-set.
- **`strict`** — set mode to `strict` (the default). Gates enforce.
- **`status`** — report the current mode + the open doc-debt count.

**Mechanism:** write `$mode` to the OS-mode file (`.claude/os-mode`); the hooks (`../hooks/`) read it. Relaxing **never disables the OS** — it degrades *block → guide* and keeps the receipts (the doc-debt register + `/reconcile-docs`).
