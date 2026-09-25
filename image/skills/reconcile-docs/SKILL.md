---
name: reconcile-docs
description: Pay down doc-debt — the doc updates skipped while gating was relaxed. Use when the session-start surfaces debt, or anytime to square up.
---

# /reconcile-docs

Square up the **doc-debt** logged while the gating was relaxed.

1. Read `docs/delivery/doc-debt.md` (the register). Each entry = a code change whose doc wasn't updated.
2. For each: read the change, **update its doc** in the right bucket, re-ground, stamp `Last verified: <date>`.
3. **Remove the entry** once reconciled — registers carry open items only.
4. Update `STATUS` (the open-doc-debt section).

If the debt is large, `/scope-lock` the reconciliation itself so it's a tracked piece of work, not an open-ended cleanup.
