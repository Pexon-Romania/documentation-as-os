# AGENTS.md — the working protocol for documentation-as-os

> The non-negotiables for anyone — human or AI session — touching this system. **Two audiences,
> two modes.** (Adapted from the pattern this method itself fathered in its code-repo
> instances: the protocol travels, lessons flow home.)

## 1 · Which mode are you in?

- **Mode A — ADOPTING the OS** (installing/upgrading it in YOUR repo): §2.
- **Mode B — CHANGING the method** (a PR to this repo): §3.

## 2 · Mode A — in your instance

1. **Install from a Release, never a copy** — record the tag; it lands in your constitution's
   footer stamp. Walk-through: [`GETTING-STARTED.md`](GETTING-STARTED.md).
2. **Run the profile prompt exactly** ([`image/BOOTSTRAP.md`](image/BOOTSTRAP.md)) — it stamps
   the instance, writes `OS-MANIFEST.lock`, installs the report-back door, and removes the
   installer. All four matter later.
3. **Don't patch OS internals in your instance** (hooks, skills, validator machinery, template
   mechanics). Editing your copy makes it a fork **you** now maintain — and silent forks re-hit
   already-fixed problems. Need an internal change? That's an issue (or PR) here.
   *Customizing what the bootstrap told you to customize — your constitution's rules, knobs,
   ask-lists, content — is normal and yours.*
4. **Send `[OS]` findings home — a standing instruction your constitution carries.** The test
   is mechanical: *is the problem in a file the bootstrap installed, or a rule the constitution
   carries?* → your agent drafts the prefilled issue (os-bug · improvement · suggestion; image
   version + profile from the stamp); you click and file. `/handover` and the stop-gate surface
   any un-filed findings.
5. **Watch Releases; upgrade deliberately** — release notes open with "Impact on existing
   instances"; the upgrade is a guided three-way diff ([`image/UPGRADE.md`](image/UPGRADE.md)),
   never a re-copy.

## 3 · Mode B — changing the method

1. **Read in:** `CHANGELOG.md` (top) → the open issues (they ARE the board) →
   [`CONTRIBUTING.md`](CONTRIBUTING.md).
2. **Evidence-gated:** the change cites a real instance's experience — an issue from the field,
   or a maintainer-run instance. A gate nobody hit yet doesn't ship.
3. **Check the contract first:** [`image/INSTANCE-CONTRACT.md`](image/INSTANCE-CONTRACT.md)
   decides whether your change is PATCH, MINOR, or a MAJOR conversation.
4. **Done =** the change + a `CHANGELOG.md` entry + `image/MANIFEST.json` regenerated + all
   three gates green locally (`validate_repo.py` · `gen_manifest.py --check` ·
   `smoke_bootstrap.sh`). CI enforces this; a red check means not done.
5. **Prompts stay version-free** (CI-checked): BOOTSTRAP/UPGRADE say "latest Release; record
   the tag" — a pinned version in a prompt re-freezes the world.
6. **Releases per [`CONTRIBUTING.md`](CONTRIBUTING.md)** — the live agent-run bootstrap on a
   scratch repo is the non-CI-able gate; the checklist holds that line.

## 4 · Critical rules — both modes

- **The instance is the ground truth for instance claims; the image is the ground truth for
  method claims.** Code is never evidence for environment state.
- **Never present an idea as shipped** — `main` is unreleased; a Release is the consumable.
- **No secrets, credentials, absolute local paths, or instance-internal content** in this repo,
  its issues, or its templates.
- **Git on this repo is human-run** — sessions prepare branches/edits; commit/push/PR/merge are
  the human's, signed per the ruleset, no AI trailers.

## 5 · Sources of truth

| Concern | Lives at |
|---|---|
| The method + the image (this product) | **this repo** — Releases are the consumable |
| A project's docs, state, decisions | **that project's instance** — never here |
| Field findings, improvement ideas | **this repo's issues** (the only report-back duty) |
| Deep evidence / program record | the steward (available to reviewers on request) |

---

*documentation-as-os working protocol. Steward: [`MAINTAINERS.md`](MAINTAINERS.md). The
artifact wins.*
