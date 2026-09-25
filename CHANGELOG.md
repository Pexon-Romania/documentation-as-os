# Changelog — documentation-as-os

> Append-only. One heading per release (newest first); work lands under **Unreleased** until it
> ships. Every `image/` or `scripts/` change carries an entry here (CI-enforced) — release notes
> are written FROM this file and always open with "Impact on existing instances."

## Unreleased

- **Codex runtime adapter (maintainer-run evidence, 2026-09-25):** operating the method from
  Codex exposed that the solo image could specify the portable hook contract but only install
  Claude Code wiring. The bootstrap now asks `Claude Code` / `Codex` / `both` without inferring;
  Codex gets repo-local `SessionStart`, `PostToolUse(Edit|Write)`, and graceful `Stop` handlers,
  `.agents/skills`, explicit `/hooks` trust, and one shared enforcement mode. The existing
  Claude paths and semantics remain intact; other harnesses remain evidence-counted runtime ports.
- **Post-launch audit fixes:** WALKTHROUGH's demo commands are now tagless (always the latest
  Release — no pin to go stale); README links the tour; MAINTAINERS carries the applied
  governance record and an honest census note (the CLI code-search instrument measured
  unreliable; the web UI per org is the fallback, registrations remain the record of truth).
- **`WALKTHROUGH.md`** — the full guided tour (the system · gates · Bench coexistence · knowledge
  channels · a run-it-yourself demo with a one-paste profile launcher), graduated from the
  adoption-call material as the onboarding front door; root lock updated.

## v2.2.2 — 2026-09-18 · platform coexistence guidance (issues #10–#11)

**Impact on existing instances:** none — guidance additions; Bench-based instances may adopt the
`@AGENTS.md`-first-line pattern at their next constitution touch (Helix already runs it).

- **Bench/FitKit-provisioned repos** (#10): BOOTSTRAP (poc + solo) and GETTING-STARTED now carry
  the coexistence pattern — AGENTS.md stays verbatim platform truth; the constitution takes
  CLAUDE.md keeping `@AGENTS.md` as line 1; §8 pre-seeds from the paved road; the platform's
  never-touch list folds into §9; Sonar policy pre-satisfied by the template.
- **The org's knowledge channels** (#11): GETTING-STARTED + the ENVIRONMENTS template point
  instances at the three live channels (Bench skills registry · Unified Docs MCP, read-only
  posture · the SSO docs portal) — point, don't restate; narrows the parked knowledge-product
  scope to method-level knowledge.

## v2.2.1 — 2026-09-18 · the field run's fixes (issues #3–#8)

**Impact on existing instances:** none breaking — template/wording improvements; pull them with
the next upgrade (`image/UPGRADE.md`) or ignore safely. All six findings came from the
first-day cold-adopter field run through the door.

- **`image/skeleton/adr.template.md` NEW** (#4) — the ADR shape scope-lock assumes
  (Amends/Supersedes header, append-only note); bootstrap STEP 2 installs it as
  `decisions/0000-adr-template.md`; SKELETON + scope-lock reference it.
- **Session notes have a home** (#5): constitution §7 names it — memory `## Session log`.
- **SKELETON rule 1 wins, said out loud** (#6): optional subsets named (support-pack,
  registers); bootstrap STEP 2 says omit what the stage doesn't need.
- **stop-gate block message neutral** (#7): no longer misdiagnoses deliberate cross-session
  commitments as stale docs.
- **doc-debt single home** (#8): the register is canonical; STATUS's section is a pointer that
  mirrors the count at write-out.
- **Release asset carries `START-HERE.txt`** (#3): the zip now tells a dev where to begin.

## v2.2.0 — 2026-09-16 · first versioned release (the org-repo extraction)

**Impact on existing instances:** none breaking — all five current instances are pre-versioned;
their move onto versioning is `UPGRADING.md` §pre-versioned (deliberate, guided, once).

- **Versioning machinery (new):** `image/VERSION` · generated `image/MANIFEST.json`
  (sha256/file) · the instance **stamp** (constitution footer) + **`OS-MANIFEST.lock`** written
  by every bootstrap · [`image/UPGRADE.md`](image/UPGRADE.md), the AI-run three-way-diff upgrade
  protocol · [`image/INSTANCE-CONTRACT.md`](image/INSTANCE-CONTRACT.md), the declared surface
  semver protects.
- **Three bootstrap profiles** (was two modes): `poc` (new — five minutes, no machinery) ·
  `solo` · `team`; profile graduation upgrades in place. Every profile now installs **the
  report-back door** (OS findings → this repo's issues; agent drafts, human files) and removes
  the installer after verification.
- **Validator template hardened** (ported from the live exemplar, ids knob-ified —
  `ID_PREFIXES`, knob 7): **ENV-STATE** warn (environment claims need environment + check +
  date; the truth-limit lesson) · **MANIFEST-SYNC** fail (stale machine index) · **SPEC-STATUS**
  warn (one status vocabulary). `OS-MANIFEST.lock` allowed at a team root.
- **Environment-state rule codified** in the constitution template (§3), the team protocol
  template (AGENTS §3), SELF-ENFORCEMENT (the honest truth-limit), and the team bootstrap's
  DOCS-STANDARD instruction: *code is never evidence for environment state; absence of a seed
  is not absence of data.*
- **`[OS]` classification** added to the LEARNINGS template (mechanical test: installed file or
  constitution-carried rule → OS-level); `/handover` and the stop-gate now sweep un-filed
  `[OS]` findings at session end.
- **Adoption tracking, zero-duty:** the bootstrap's last step offers a prefilled **`[adopted]`
  registration issue** (the label timeline = adoption-over-time, dated by GitHub); the footer
  stamp doubles as a **passive census key** (org code search — MAINTAINERS §census). No
  telemetry, no phone-home: registration is a human click, discovery is a steward sweep.
- **Exemplar learnings adopted** (audit vs the live instance, 2026-09-16): *corrections are
  corpus-wide* (CONVENTIONS template + constitution §5) · *reconcile, don't just read* (team
  AGENTS §1) · *no patching — investigate first* (constitution §3) · stop-gate warns when the
  doc-debt register is missing ("a checkpoint that cannot fail is not a checkpoint").
- **This repo itself:** the shell (README · METHOD · GETTING-STARTED · UPGRADING · CONTRIBUTING
  · MAINTAINERS · ADOPTERS · SECURITY — what runs where, nothing phones home) · issue templates
  (os-bug · improvement · suggestion · adopted) +
  PR template + CODEOWNERS · CI (`validate_repo.py` · `gen_manifest.py --check` ·
  `smoke_bootstrap.sh` · changelog guard · weekly cron) · the release workflow (tag →
  `image-….zip` asset).

## Pre-semver lineage

- **v2 — 2026-08-04:** the team tier, extracted from the production exemplar at team scale
  (shared org repo as source of truth · validator + CI + rulesets + selective code-owners ·
  delivery-line templates · governance runbook).
- **v1 — 2026-06-25:** the solo tier, dogfood-validated end-to-end (constitution · skeleton ·
  skills · graceful-enforcement hooks · the bootstrap).
