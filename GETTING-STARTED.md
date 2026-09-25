# Getting started — adopt the OS in your repo

For teams and builders **installing** documentation-as-os. Changing the method itself →
[`CONTRIBUTING.md`](CONTRIBUTING.md). The why → [`METHOD.md`](METHOD.md).

## 0 · What you're getting

A system that makes your repo **boot from a constitution, keep a live current-state, remember
its decisions, and enforce "done = code + docs in sync" gracefully** — for humans and AI
sessions alike. It installs *into your repo* and becomes yours; this repo only ships the image
and receives your findings.

**Requirements:** Claude Code and/or Codex for the solo runtime layer (other runtimes: file a
`runtime-port` issue) · git · Python 3 for Codex hooks · for Claude hooks, bash on PATH
(macOS/Linux native; Windows = Git Bash).

## 1 · Pick your profile

| You are… | Profile | You get | Time |
|---|---|---|---|
| POC / experiment | **`poc`** | constitution-lite · live STATUS · changelog · the door | ~5 min |
| One builder + agent, real repo | **`solo`** | + full constitution · doc skeleton · 5 skills · graceful-enforcement hooks | ~1 session |
| Team / commercial build | **`team`** | a shared org docs repo as source of truth: validator · CI · rulesets · code-owners · delivery line | ~1 session + 1h sitting |

Growing later is an **in-place profile upgrade** (run the next profile's prompt from the
then-latest Release) — never a fresh adoption.

## 2 · Get a Release — not `main`, not a copied folder

On the [Releases page](../../releases), the latest release offers:

- **`image-….zip`** — the image alone: **this is all an adopter needs.**
- **Source code (zip / tar.gz)** — the whole repo, if you want the docs alongside.

**Record the tag you took** — the bootstrap writes it into your constitution's footer stamp,
and every report you ever file quotes it. Hand-passed copies are how stale forks re-hit
already-fixed problems; that's the whole reason Releases exist.

## 3 · Run the bootstrap — one prompt, your AI does the install

Unzip so `image/` sits at/beside your repo root. Open **Claude Code or Codex** in your repo, open
[`image/BOOTSTRAP.md`](image/BOOTSTRAP.md), and paste **your profile's prompt**. It will:

- detect fresh vs existing repo (existing → it builds the docs *from your code*, incrementally);
- **merge** into any constitution you already have — never clobber — and ask before anything
  irreversible;
- fill what it can infer and ask you the rest (locked decisions, forbidden ops);
- ask which runtime to wire — **Claude Code, Codex, or both** — before installing runtime files;
- **stamp the instance** (image version + profile in the constitution footer), write
  **`OS-MANIFEST.lock`** (future upgrades three-way diff against it), and install **the door**
  (the OS report-back standing instruction);
- verify, then **delete the installer folder** — your instance keeps everything it needs; a
  kept image copy becomes a silently-stale fork.

**On a Bench/FitKit-provisioned repo** (it arrives with a live boot layer, not a blank slate):
keep the template's `AGENTS.md` **verbatim** — it is platform truth (the skills-registry
protocol, DB discipline, CI fences) and forking it is the silent-fork trap. The constitution
takes `CLAUDE.md` and keeps `@AGENTS.md` as its **first line**, so the platform guide loads
every session; the platform's never-touch rules fold into your §9 forbidden ops, and the
paved-road stack pre-seeds §8 locked decisions. (The org's SonarQube scan policy is already
satisfied — the template ships the workflow.) The bootstrap prompt carries these steps.

**The organization's knowledge channels — point, don't restate:** use the approved live skills
registry for platform how-to material, the approved documentation connector for platform
reference, and the authenticated documentation portal for human readers. Mount external
documentation sources read-only from instance sessions. Your instance's dependency docs should
point at those sources, never copy them.

## 4 · What a healthy install looks like

Constitution boots with your rules + the footer stamp · STATUS reflects reality · (solo)
skills answer as `/scope-lock` in Claude and/or `$scope-lock` in Codex · the selected hooks are
live after restart (and Codex `/hooks` trust review) · the lock file exists · no unfilled
placeholders · the image folder is gone. The prompts end with an honest report of exactly this.

## 5 · Staying current

**Watch → Custom → Releases** on this repo. Every release opens with **"Impact on existing
instances."** Upgrading is deliberate and guided — place the new Release's `image/` beside your
repo and paste the prompt in [`image/UPGRADE.md`](image/UPGRADE.md): it diffs what upstream
changed against what you customized, hand-merges only where both moved, re-verifies, and
re-stamps. Details: [`UPGRADING.md`](UPGRADING.md).

## 6 · The door — reporting back (your only duty)

Your constitution carries the standing instruction, and your agent does the heavy lifting: when
the **OS itself** misbehaves — a hook misfires, a gate blocks wrongly, a template or rule
contradicts itself — the agent logs it as an `[OS]` finding and **drafts the prefilled issue**
(matching template, image version + profile from the stamp, the finding); you click and file:

- **[os-bug]** — something the OS ships is wrong or broke in your instance
- **[improvement]** — friction + the smallest durable fix
- **[suggestion]** — a pattern you proved (or disproved) worth codifying

A fourth template — **[adopted]** — is the optional one-click registration your bootstrap offers
at the end: it puts your instance on [`ADOPTERS.md`](ADOPTERS.md) and the adoption timeline;
skipping it changes nothing.

`/handover` and the stop-gate surface any un-filed findings, so reports don't rely on memory.
**Help with *your* instance** (filling your constitution, your project's docs) is yours and your
team's — this inbox is for the OS itself. Docs didn't answer something an adopter needed? That
itself is an **[improvement]** issue.

---

*documentation-as-os. Start small (`poc` is five minutes), grow in place. The artifact wins.*
