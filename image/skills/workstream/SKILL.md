---
name: workstream
description: Spin up a dedicated subfolder for a new workstream — its own space, tracker, and records (a "fork"). Use when a request is big enough to need its own home.
arguments: [name]
---

# workstream $name

Invoke as `/workstream` in Claude Code or `$workstream` in Codex.

Fork a workstream into its own space — the proven pattern (a dedicated subfolder per significant workstream keeps the main board clean).

1. Create `docs/workstreams/$name/` (or the project's convention).
2. Seed it:
   - `README.md` — what this workstream is, its scope, its status.
   - `TRACKER.md` — **open items only** (board = index); links to the records.
   - `decisions/` — its ADRs (the *why*).
3. Link it from the main `STATUS` index.
4. Run **`scope-lock`** inside it to frame the work.

Heavy detail (RCAs, analyses, build logs) lives in the workstream's own docs; the `TRACKER` stays a **scannable index that links to them** — never a record store.
