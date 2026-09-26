# {{PROJECT_NAME}} — project memory

> A small, project-scoped index of experience that should improve the next session. This is
> **not another source of truth**: current work lives in STATUS, decisions in ADRs, environment
> facts in the environment register, shipped history in CHANGELOG, and reusable methods in
> skills. Memory records useful outcomes and points to those canonical homes.
>
> Last reviewed: {{DATE}}

## Hot index — injected at session start

Keep this section within the first 30 lines and under eight entries. Link; do not copy.

<!-- Format:
- [VERIFIED | INFERRED | NEEDS-CHECK] <topic> — <canonical path#section or episode ID> — reviewed <YYYY-MM-DD>
-->

- none yet

## Open conflicts

Conflicting claims are not active truth. Record both sources and the scope difference; resolve
with evidence or a human decision. Never silently use “newer wins” for different environments,
versions, or scopes.

- none

## Retrieval and write contract

Before a related task, search by area, command, error signature, and tag; load only relevant entries.

A memory claim is a lead to verify, never a fact to repeat without checking its canonical source.

Write an episode only when it can change future behavior: a consequential outcome, a failed path
worth avoiding, a correction, or a candidate reusable method. Reference raw documents and tool
output by path or ID; do not copy them. Never store transcripts, hidden reasoning, intermediate
drafts, credentials, hostnames, personal data, or large command output here.

If a durable fact or decision has no canonical record, update the correct document or ADR first;
then add only a pointer here.

## Skill candidates

Promotion is deliberate, never automatic. List a method here only after multiple successful uses
with linked episode evidence. Promote it to a versioned skill when its trigger, preconditions,
steps, failure modes, and success criteria are unambiguous and the required tools are dependable.

- none

## Session log — newest first

```text
### MEM-YYYYMMDD-N — <task/outcome in one line>
- Scope/tags: <area; searchable terms>
- Outcome: success | partial | failure
- Evidence: <commands, files, issue/ADR IDs, or environment check + date>
- What to reuse: <the useful result, or “none”>
- Avoid next time: <failed path + why, or “none”>
- Canonical updates: <STATUS/ADR/docs/skill paths, or “none”>
- Confidence: VERIFIED | INFERRED | NEEDS-CHECK
- Lifecycle: active | summarized in MEM-… | superseded by MEM-…
- Review on: <YYYY-MM-DD | never, with reason>
```

<!-- No entries yet. -->

## Reconciliation and forgetting

Review memory during handover and when related doc-debt is reconciled:

1. Re-check active entries against their canonical sources; scope apparent contradictions before
   resolving them.
2. Replace duplicates with one summary entry and point the originals to it.
3. Remove routine episodes from this active file after their review date once they no longer
   change behavior; Git retains the history. Never expire locked decisions — preserve them in ADRs.
4. Update or retire skill candidates when the code, environment, or required tools change. A stale
   procedure is worse than no procedure.
