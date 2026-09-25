# Maintainers

documentation-as-os is proprietary material owned by Pexon Romania and Flavius Moldovan.
Its steward is:

- **Flavius Moldovan** (`@flaviusmoldovan-pexon`) — steward of the image and the contract.

Changes to the machinery (`image/`, `scripts/`, `.github/`, the root protocol files) route
through the steward via [`.github/CODEOWNERS`](.github/CODEOWNERS); everything else needs one
peer review per the ruleset. Method changes ratify **evidence-first** (CONTRIBUTING §flow) —
the steward's pen signs codifications, not opinions.

**Succession:** when a maintainer team exists, the CODEOWNERS handle swaps for
`@flaviusmoldovan-pexon` — one line; ownership follows the role, not the person.
Area maintainers are added here as the contributor base grows (the ladder: contributor →
area maintainer → co-steward).

## Governance settings (the applied record)

The repo runs the image's own governance
([`image/system/GOVERNANCE-RUNBOOK.md`](image/system/GOVERNANCE-RUNBOOK.md) +
[`image/system/ruleset.template.json`](image/system/ruleset.template.json)): squash-only ·
delete-branch-on-merge · no wiki · PR-only main with one approval · code-owner review on the
system layer · required `validate` check · signed commits · no force-push or deletion.

**The applied record (each verified by API read-back on the date shown):**
- 2026-09-18 · repo behavior: squash-only merges · delete-branch-on-merge · no wiki.
- 2026-09-18 · ruleset `docs-main-protection` on `main`: PR-only · 1 approving review ·
  code-owner review · required `validate` check · signed commits · non-fast-forward · no
  deletion (bypass: maintain/admin roles, audited). Layered on the org's rules
  (`repository_visibility` + required `credentials-scan`).
- 2026-09-18 · the six labels created · description + topics set.
- 2026-09-18 · SonarQube policy: docs-repo exception (`sonarqube_exception=true`), rationale on
  the closed policy issue — both repos.
- 2026-09-22 · the hub hardened for group write: CODEOWNERS → steward + ruleset
  `hub-main-protection` (PR-only · review · code-owner · signed · non-fast-forward · no
  deletion; no required check — the hub has no CI).
- 2026-09-22 · collaborator model verified: humans = `push` (propose-only under the rulesets);
  the `admin` accounts are the org's standard platform/service set (identical across org repos).

## The adoption census (steward ritual, monthly with the triage cadence)

Two instruments, cross-checked:

1. **The `adopted` label timeline** — self-registrations
   ([issues labeled `adopted`](../../issues?q=label%3Aadopted)); each becomes an ADOPTERS row,
   then closes. Adoption-over-time = the label's open-date sequence, no tooling needed.
2. **The stamp census — indicative only.** Every bootstrap writes a distinctive footer stamp,
   so instances are in principle discoverable via code search — but the CLI rides GitHub's
   legacy engine and is measurably unreliable (2026-09-22: identical queries returned 1 result,
   then 0, thirty seconds apart; `--filename` unsupported; multi-`--owner` queries break).
   Use the GitHub web UI with the query `"documentation-as-os"` and the relevant owner filter,
   treat any result as a floor,
   exclude this repo and the hub (they carry the key natively) — and rely on instrument 1
   (registrations) as the record of truth.

## Support boundary

This repo supports **the method**: os-bug / improvement / suggestion issues, triaged weekly.
Help operating *your instance* belongs to your team — the docs route:
[`GETTING-STARTED.md`](GETTING-STARTED.md) → your instance's own constitution and skills.

---

*documentation-as-os.*
