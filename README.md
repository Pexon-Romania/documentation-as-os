# documentation-as-os

> **Proprietary.** Copyright (c) 2026 Pexon Romania and Flavius Moldovan.
> All rights reserved. See [`LICENSE`](LICENSE).

**Documentation as the operating system of an AI-native project** — a versioned, clone-able
system that boots a repo from a constitution, runs the delivery loop, carries state across
sessions and models, and keeps itself current. The `.md` files are the program; the AI agent is
the runtime. Distilled from a production deployment and proven across five org instances
([`ADOPTERS.md`](ADOPTERS.md)). The idea in one read: [`METHOD.md`](METHOD.md).

> **Adopting? The latest [Release](../../releases) is all you need** — download the
> `image-…zip` asset, record the tag, and follow
> [`GETTING-STARTED.md`](GETTING-STARTED.md). Five minutes for a POC.
> Prefer the guided tour first? **[`WALKTHROUGH.md`](WALKTHROUGH.md)** — the whole system +
> a run-it-yourself demo.

## Get it (version-truth)

| State | Meaning |
|---|---|
| **A Release (`vX.Y.Z`)** | The consumable — versioned, checked, upgrade-tracked. **Start here.** |
| `main` | Unreleased work — correct but not yet a version you can quote |
| A PR | A proposal |

Never install from a copied folder or from `main`: a hand-passed image goes stale silently, and
"which version are you on?" must always be answerable. Every instance is **stamped** at install;
every release states its **impact on existing instances**; upgrades are a guided three-way diff
([`UPGRADING.md`](UPGRADING.md)).

## Pick your profile

| You are… | Profile | What installs | Time |
|---|---|---|---|
| A POC / experiment (innovation tier) | **`poc`** | constitution-lite + live STATUS + changelog + the report-back door | ~5 min |
| One builder + agent on a real repo | **`solo`** | + full constitution, doc skeleton, 5 skills, graceful-enforcement hooks | ~1 session |
| A team / commercial build | **`team`** | a shared docs repo that IS the source of truth: validator, CI, rulesets, code-owners, delivery line | ~1 session + 1h governance sitting |

A POC that grows up **upgrades its profile in place** — it never re-adopts. The prompts:
[`image/BOOTSTRAP.md`](image/BOOTSTRAP.md).

> **Runtime, honestly:** the *method* is runtime-agnostic ([`METHOD.md`](METHOD.md) §adopting);
> the solo image ships adapters for **Claude Code, Codex, or both**. The bootstrap asks instead
> of inferring. On Copilot/Cursor/another runtime, file a `runtime-port` issue — that label is
> how demand gets counted and prioritized.

## What semver protects

Instances customize what the bootstrap installs — by design. So versions protect the
**instance contract**: the file roles, hook semantics, skill names, validator knobs, and stamp
locations an instance's muscle memory depends on —
[`image/INSTANCE-CONTRACT.md`](image/INSTANCE-CONTRACT.md). Breaking it = MAJOR; new capability
= MINOR; fixes = PATCH. Everything else is internal and may move in a MINOR.

## Layout

- **[`image/`](image/)** — the product: the bootstrap (3 profiles), the upgrade protocol, the
  constitution + skeleton + skills + hooks (solo tier), the system layer — validator, CI,
  CODEOWNERS, ruleset, governance runbook (team tier), `VERSION` + `MANIFEST.json`.
- **[`METHOD.md`](METHOD.md)** — the compact why (leadership / first read).
- **[`GETTING-STARTED.md`](GETTING-STARTED.md) · [`UPGRADING.md`](UPGRADING.md)** — adopt · stay current.
- **[`scripts/`](scripts/)** — this repo's own gates: `validate_repo.py`, `gen_manifest.py`,
  `smoke_bootstrap.sh` (CI runs them on every change + weekly).
- **[`ADOPTERS.md`](ADOPTERS.md)** — the estate view (maintainer-kept; adopters owe only issues).

## Report back — issues are the only duty

Hit an OS bug, friction, or an idea worth codifying? File the matching
[issue template](../../issues/new/choose) — **os-bug · improvement · suggestion** — quoting the
image version + profile from your constitution's footer stamp. Your instance's constitution
carries this door as a standing instruction, so your agent drafts the report for you. A note in
your repo dies there; an issue reaches every instance. (Help with *your* instance is different —
see [`GETTING-STARTED.md`](GETTING-STARTED.md) §the-door.)

## Working on this repo (humans and AI)

Boot from [`CLAUDE.md`](CLAUDE.md) → [`AGENTS.md`](AGENTS.md) (Mode B) →
[`CONTRIBUTING.md`](CONTRIBUTING.md). The law of the house: **method changes are evidence-gated**
— extracted from a real instance, never designed by committee. Governance:
[`MAINTAINERS.md`](MAINTAINERS.md).

---

*documentation-as-os. Proprietary material owned and maintained by **Pexon Romania and
Flavius Moldovan** — derived from production AI-delivery experience, packaged to install anywhere, kept honest
against the artifacts; the artifact wins. This repo runs the system on itself.*
