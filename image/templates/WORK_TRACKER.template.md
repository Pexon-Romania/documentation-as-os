---
app: {{APP}}
audience: [engineers, ops]
scope: internal
status: live-prod
covers: The live delivery board — open work only, one row per item, staged; the single source of current state.
keywords: [board, tracker, current state, open work, stages]
sources: []
related: [CHANGELOG.md, CONVENTIONS.md]
last_verified: {{TODAY}}
---

# Work board

> **Updated {{TODAY}}.** Prod baselines: {{REPO}} **#—** (migrations through **—**).
> **Active:** — · **Deferred:** —

## Active

| ID | What & why | Type | Priority | Stage | Next |
|---|---|---|---|---|---|
| {{PREFIX}}-01 | … | FIX | P2 | DISCOVERED | … |

## Backlog

| ID | What | Type | Priority | Notes |
|---|---|---|---|---|

*Rows leave this board when they reach PROD — the changelog is where they live forever. The board
carries OPEN work only; if it's done, it's history, not status.*
