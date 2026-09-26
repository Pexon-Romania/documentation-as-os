---
name: handover
description: Produce or refresh the handover doc-set — built fresh FROM the code, layered and grounded. Use to hand the project (or a part) to a new maintainer or the support team.
---

# handover

Invoke as `/handover` in Claude Code or `$handover` in Codex.

Build the handover set **from the code**, not from stale notes.

1. **Read the actual code** for the area in scope.
2. Write/refresh the **product** + **engineering** bucket docs — overview, how-it-works, architecture, areas-map, data-model, deployment, known-limitations — **layered** (plain first, then deep), one concern per file.
3. **Ground every load-bearing claim** in the source; mark `[VERIFIED]` / `[INFERRED]`; stamp `Last verified: <date>`.
4. Keep the **support-pack** current (`docs/product/support/`: runbook · escalation · FAQ · admin-how-to) — this is the **support-team onboarding surface**. Mark org-specifics `[FILL IN]` (owner · SLAs · contacts); never invent them.
5. **No credentials, hostnames, or PII** in the shareable bucket.
6. **Sweep the OS findings:** any `[OS]`-tagged entries (LEARNINGS, or STATUS "OS findings")
   not yet filed upstream? List them now with their prefilled issue links (per the
   constitution's OS report-back section) — a missed report may survive a session, never a
   handover.
7. **Reconcile project memory:** verify the hot-index pointers for the handed-over area, surface
   unresolved conflicts, summarize duplicate episodes, and retire stale routine entries. Decisions
   remain in ADRs; never turn memory into a second source of truth.

A user-facing AI tool reads the **product** bucket only — never engineering, delivery, or the constitution.
