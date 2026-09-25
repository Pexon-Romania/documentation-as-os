---
app: {{APP}}
audience: [engineers, ops]
scope: internal
status: live-prod
covers: How work is tracked — item scheme, the stage model, the two-beat rule, and the claims rules.
keywords: [conventions, stages, work tracking, changelog, two-beat, verifiable claims]
sources: []
related: [WORK_TRACKER.md, CHANGELOG.md, ../dependencies/ENVIRONMENTS.md]
last_verified: {{TODAY}}
---

# Delivery conventions

## Identifiers
- **Item ID:** `{{PREFIX}}-##` — sequential, never reused (gaps are documented, not recycled).
- **Type:** BUG · FIX · IMPROVEMENT · TECH-DEBT · FEATURE · OPS · **Priority:** P0–P3.

## Stage model — the ONLY status vocabulary
`DISCOVERED → SCOPED → BUILT → DEV-PR → DEV-LIVE → VALIDATED → PROD-PR → PROD → VERIFIED`
(+ `DEFERRED`). Specs, board rows, and changelog sections all use these words; **when surfaces
disagree, the board is the truth and the other surface is the bug.**

## The two-beat rule ⭐
- **Beat 1 — merge to the integration branch:** a board row + an "On dev — awaiting promotion"
  changelog line. *Nothing else* — reference docs keep describing production.
- **Beat 2 — production promotion:** the changelog entry moves to "Shipped", the environment
  register updates, and you run the reverse lookup over the promoted code range
  (`validate_docs.py --which-docs <changed paths>`) — registers are the floor, the touched
  reference docs are the ceiling. **A promotion is a documentation event.**

## Claims must be verifiable
- **Acceptance criteria name the environment they are checked in** — never a machine the
  validation won't run on.
- **Completeness claims record the discovery command, not the count** — "all N endpoints" hides
  the N+1th; the search that produced the list IS the claim.
- **Corrections are corpus-wide.** Before committing a correction to any claim, grep the corpus
  for the claim's phrasing (and its obvious paraphrases) and fix **every occurrence in the same
  change** — a correction that fixes one file and leaves the echoes standing gives the reader a
  coin flip. And name the error honestly: a doc that was always wrong is corrected as *"this doc
  was wrong"*, never *"this is no longer true"* — mis-framing a documentation error as a change
  in the world buries whatever the error was hiding.

## The SOP
1. New work → board row with ID + stage. 2. Advance the stage as it moves. 3. Confirm
DEV-LIVE/PROD with a human (merges + rebuilds aren't directly observable). 4. At PROD → beat 2
(above), then run the validator. 5. Changelog entries stay scannable — deep detail goes to a
linked record (spec / incident RCA).
