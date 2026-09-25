# documentation-as-os — repo constitution (boot file)

> This repository is the **home of the method** — the versioned image adopters install, and the
> docs around it. It is **not an instance**: no project's docs ever live here. Read this first,
> every session; it overrides default behavior.

## 1 · Route yourself

- **Adopting the OS into another repo?** You're in the wrong working directory — the work
  happens in *that* repo. Take the latest Release and follow
  [`GETTING-STARTED.md`](GETTING-STARTED.md). This repo only receives your **issues**.
- **Changing the method itself?** [`AGENTS.md`](AGENTS.md) Mode B +
  [`CONTRIBUTING.md`](CONTRIBUTING.md). Read `CHANGELOG.md` (top) and the open issues first —
  **the issue list is this repo's board**; there is no STATUS file here by design.

## 2 · The laws of this repo — never violate

1. **Instances never live here.** Any PR adding a project's docs, examples of "our project on
   the OS", or adopter content is declined — instances live in their own repos; this repo ships
   the image and receives issues.
2. **Evidence-gated change:** a method change — especially one adding or tightening a gate —
   cites at least one real instance's experience (an issue, or a maintainer-run instance).
   Extracted, not designed.
3. **The normative surface is atomic:** anything an adopter's instance depends on
   ([`image/INSTANCE-CONTRACT.md`](image/INSTANCE-CONTRACT.md), the bootstrap, the templates,
   GETTING-STARTED, UPGRADING, METHOD) changes only here, in one PR — never split across homes.
4. **Touching the stable surface is a MAJOR conversation first** — check the contract before
   renaming any file role, hook semantic, skill, knob, or stamp location.
5. **Every `image/` or `scripts/` change carries a `CHANGELOG.md` entry AND a regenerated
   `image/MANIFEST.json`** (`python3 scripts/gen_manifest.py`). CI fails without both.
6. **Done = gates green:** `python3 scripts/validate_repo.py` + `python3 scripts/gen_manifest.py
   --check` + `bash scripts/smoke_bootstrap.sh` — a FAIL means the change is not done.
7. **The root is locked** (validate_repo TREE check). New root files or folders need the
   steward's approval FIRST — propose in an issue.
8. **No secrets, no absolute local paths, no personal or instance-internal content.** Evidence
   claims stay at the level of [`METHOD.md`](METHOD.md) §proven; deep evidence lives with the
   steward and is available to reviewers on request.
9. **Git is human-run on this org repo:** sessions author branches and content; the human runs
   commit / push / PR / merge (signed, per the ruleset). Short clean messages. **No AI
   co-author trailers, ever.**
10. **Releases follow the checklist** in [`CONTRIBUTING.md`](CONTRIBUTING.md) — including the
    live agent-run bootstrap before any MINOR/MAJOR tag. Never tag red.

## 3 · Write-out before you stop

Update the CHANGELOG for anything shipped, reply/label the issues you triaged (`ADOPTED` names
where it got codified; `REJECTED` says why), and leave the next step in the PR or issue thread —
this repo's state lives in git + issues, nowhere else.

---

*documentation-as-os — the repo runs the system on itself (product-repo tier: constitution +
changelog + issues-as-board + CI gates). Steward: see [`MAINTAINERS.md`](MAINTAINERS.md).*
