---
app: {{APP}}
audience: [engineers, ops]
scope: internal
status: live-prod
covers: The canonical dev-vs-prod register — feature flags, dev-only / not-yet-promoted items, and the rule that docs default to prod truth.
keywords: [environments, dev vs prod, feature flags, dev-only, register, env truth]
sources: []
related: [CONVENTIONS.md, WORK_TRACKER.md]
last_verified: {{TODAY}}
---

# Environments — what is true where

> The docs describe **production** unless a doc's `status:` says otherwise. This page is the one
> answer to *"is X live, dev-only, or flagged off?"* — kept current at every promotion (beat 2).

## Prod baseline
- {{REPO}} `main` @ **{{DATE}}** (**#PR**) · migrations applied through **—** (the per-migration
  ledger lives next to the migrations in the code repo — link it, don't restate it).

## On the integration branch and NOT in prod
- *live list = the board's DEV-stage rows; name only standing items here (flagged-off features,
  dev-only subsystems).* 

## Feature flags
| Flag | Default | Dev | Prod | What it gates |
|---|---|---|---|---|

## Platform knowledge channels (point, don't restate)
- Platform **how-to** → the organization's approved live skills registry; fetch the official
  version and never embed a copy.
- Platform **reference** → the organization's approved documentation connector; treat it as
  read-only from project sessions.
- **Humans** → the platform docs portal (SSO). This register stays about THIS app's env truth;
  platform knowledge lives in those channels.
