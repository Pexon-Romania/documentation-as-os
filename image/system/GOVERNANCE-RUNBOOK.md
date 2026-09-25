# The governance sitting — one hour, admin required once

> Run this ONCE when the shared docs repo is created (or when a team forms around an existing
> one). Everything here is settings, not content — after the sitting, day-to-day never needs
> admin again. **Verify every setting after applying it** (the commands include the checks —
> never assume a write took).

## 0 · Before you start
- The repo exists in your org, the system layer is seeded (validator, CI workflow, CODEOWNERS,
  the delivery-line templates), and the first CI run has gone green (the ruleset references the
  `validate` check by name — it must have run once).
- You hold temporary **admin** on the repo. Plan to hand it back: the steward's standing role is
  **`maintain`** — runs everything daily, cannot weaken the rules (that is a feature).

## 1 · Repo behavior
```bash
gh api -X PATCH repos/ORG/REPO -F allow_merge_commit=false -F allow_rebase_merge=false \
  -F delete_branch_on_merge=true -F has_wiki=false
# verify: response echoes the four values — read them, don't assume
```
Squash-only (one commit per PR) · auto-delete merged branches · no wiki (no second editable
surface to drift).

## 2 · The branch ruleset
```bash
gh api -X POST repos/ORG/REPO/rulesets --input ruleset.template.json
# verify: gh api repos/ORG/REPO/rules/branches/main --jq '[.[].type]'
```
What it encodes: PR-only main · one peer approval · code-owner review **on the system layer
only** (via CODEOWNERS — content never waits on one person) · required `validate` check · signed
commits · no force-push, no deletion. Bypass = repository **roles** `maintain` + `admin`
(audited) — the steward's lane, transferable with the role.

**Sequencing caution:** if you are migrating an existing history in, push the history FIRST,
enable `required_signatures` AFTER — old commits may predate your signing discipline; the rule
only affects new pushes.

## 3 · People
```bash
gh api -X PUT repos/ORG/REPO/collaborators/USER -f permission=push      # contributors: write
# steward: maintain (set by an org owner; ask for it explicitly when admin is reclaimed)
```
Ask your org owner for a **team** (e.g. `your-docs-maintainers`) and point CODEOWNERS at it —
succession becomes a membership change.

## 4 · Platform coexistence (org-managed repos)
- **Platform files** (compliance descriptors, org CI): they are not yours — never edit, and make
  any local tooling ignore them explicitly.
- **Org rulesets** layer with yours; same-type rules aggregate **strictest-wins**. Before adding
  a rule, check what already applies: `gh api repos/ORG/REPO/rules/branches/main` — and read it
  **unfiltered with ruleset attribution** (two same-type rules from different rulesets are easy
  to misread; a truncated listing once produced a false "no review required" finding).
- **Org policy bots** (code-scanning mandates etc.): a docs-only repo usually qualifies for the
  self-service exception — set it, record the rationale on the policy issue, close it. The
  register documents the decision either way.

## 5 · Record it
Governance is configuration; configuration is truth; truth gets documented. Every setting above
goes into the docs' own governance register (the 03-GitHub-equivalent page) **with its why** —
the sitting is itself a documentation event.
