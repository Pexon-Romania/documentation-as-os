# documentation-as-os — the full walkthrough

> **Documentation stops being a record of the work and becomes the operating system the work
> runs on.** The `.md` files are the program; the AI agent is the runtime.
> This document: the whole system, the Bench/Spark Pro relationship, the knowledge channels,
> and the live demo — in walk-through order.

---

# PART 1 · THE SYSTEM

## 1.1 The problem it solves

Building with AI agents moved where a project's *state* can safely live:

- the agent **resets every session** and can change model mid-stream;
- the work **outruns one person's head** — priorities shift, requirements land mid-build;
- **code** shows *what*, never *why / what's next / what was agreed*;
- **a person's memory** doesn't survive a reset, a model swap, or a handover.

The only carrier that survives all of that — version-controlled, readable by humans *and*
agents, always current — is the documentation. So it gets promoted, literally:

| OS concept | Here | The file |
|---|---|---|
| **Boot sequence** | the constitution, read first every session | `CLAUDE.md` |
| **Process table** | live state: where we are · next · blocked | `STATUS.md` |
| **Persistent storage** | the durable *why*, survives any reset | `memory/` + `decisions/` |
| **Scheduler** | the delivery loop (admit → run → retire work) | the method itself |
| **Policy enforcement** | hooks + human gates (solo) · validator + CI + rulesets (team) | `.claude/hooks/` · CI |
| **syslog** | the learnings inbox — friction appended unprompted | `LEARNINGS.md` / issues |
| **The installer** | one prompt boots the image into any repo | `image/BOOTSTRAP.md` |

## 1.2 The big picture

```
            flaviusmoldovan-pexon/documentation-as-os  (the product repo — versioned Releases)
            ┌────────────────────────────────────────────────┐
            │  image/   ── the installable OS                │
            │  issues   ── THE DOOR (the only adopter duty) ◄──────────────┐
            └───────┬────────────────────────────────────────┘             │
                    │ download the Release asset (image-vX.Y.Z.zip)        │
                    ▼                                                      │
   YOUR repo ──► BOOTSTRAP (pick a profile, paste one prompt)              │
                    │                                                      │
                    ▼                                                      │
        ┌── THE INSTANCE (yours forever) ──────────────────┐               │
        │ constitution · live STATUS · memory · decisions  │  [OS] finding │
        │ skills · hooks · version stamp · upgrade lock    │ ──────────────┘
        └──────────────────────────────────────────────────┘   agent drafts,
                                                                human files
```

**Version-truth:** a **Release** is the consumable · `main` is unreleased · a PR is a proposal.
Every instance is **stamped** with the version it installed; every release opens with
*"Impact on existing instances."*

## 1.3 Three profiles — scaled to the stage

| You are… | Profile | What installs | Time |
|---|---|---|---|
| A POC / experiment (innovation) | **`poc`** | constitution-lite · STATUS · changelog · the door | **~5 min** |
| One builder + agent, real repo | **`solo`** | + full constitution · doc skeleton · 5 skills · 3 enforcement hooks | ~1 session |
| A team / commercial build | **`team`** | a shared docs repo as source of truth: validator · CI · rulesets · code-owners · delivery line | ~1 session + 1h governance sitting |

A funded POC **upgrades its profile in place** — it never re-adopts. The bootstrap's STEP 0
detects the situation by itself: *fresh repo → scaffold · existing code → build docs FROM the
code, incrementally · poc stamp found → upgrade in place · live solo/team stamp → STOP, use the
upgrade protocol.*

## 1.4 What a solo instance looks like

```
your-repo/
├── CLAUDE.md                  the constitution — read FIRST every session
│                                └ footer: version stamp + the report-back door
├── docs/
│   ├── product/ …             shareable (the ONLY bucket a user-facing AI may read)
│   ├── engineering/ …         internal (architecture · areas-map · deployment …)
│   ├── delivery/
│   │   ├── STATUS.md          live state — injected at every boot
│   │   ├── doc-debt.md        the graceful-enforcement ledger (canonical register)
│   │   ├── CHANGELOG.md       append-only, what shipped
│   │   └── decisions/         ADRs — the why (append-only; supersede, never rewrite)
│   └── OS-MANIFEST.lock       sha256 of what you installed from → upgrades diff against it
├── memory/                    the durable why across sessions
└── .claude/
    ├── skills/                /scope-lock · /workstream · /handover · /reconcile-docs · /gating
    ├── hooks/                 session-start · post-edit-docs · stop-gate
    └── os-mode                strict | relaxed  (auto-resets to strict every session)
```

## 1.5 A session's life — where the gates sit

```
SESSION START ──► SessionStart hook injects: STATUS head · open doc-debt · memory index
                  (and resets a lingering "relaxed" back to STRICT — relax never persists)
      │
   THE LOOP    request = a HYPOTHESIS → /scope-lock → ADR before code → build
      │        └ edit a code file → PostToolUse hook: "update its doc in the SAME change"
      │        └ urgent moment?  /gating relax → gates warn instead of block,
      │                          every skipped doc update is LOGGED as doc-debt
      ▼
SESSION END ──► Stop hook:  open doc-debt + strict  →  BLOCKS ONCE (reconcile or relax)
                            clean                   →  reminder (+ any un-filed [OS] findings?)
                            (never loops; a missing register is loud, never silent)
```

**Graceful enforcement — the design law:** every hard gate *holds the line by default*, *yields
to one word*, and *never forgets* (the skip becomes tracked doc-debt, repaid via
`/reconcile-docs`). Rigid enforcers get switched off; this one is built to stay on.

## 1.6 All the gates, one table

| Gate | Mechanism | Strength |
|---|---|---|
| Never start cold | `SessionStart` hook → boot injection | auto, every session |
| Docs-part-of-done nudge | `PostToolUse(Edit\|Write)` hook | warns (logs debt when relaxed) |
| Won't close on stale docs | `Stop` hook — blocks **once** on open debt | hard, overridable by a word |
| Human gate on irreversible ops | permission `ask:` rules (git push, deletes, DDL…) | stops and asks YOU |
| Loop stages | the 5 skills (`/scope-lock` …) | codified process |
| Relax/repay | `/gating relax` → debt ledger → `/reconcile-docs` | adaptivity with receipts |
| **Team tier adds:** docs contract | `validate_docs.py` — frontmatter · links · scope fences · locked tree · board↔changelog · env-state claims · manifest sync… **FAIL = not done** | CI-required check |
| Team governance | branch ruleset (PR-only · review · signed) + selective CODEOWNERS | server-side |
| The product repo itself | 6 CI checks incl. a **bootstrap smoke test** + weekly bitrot cron | gates the method's own changes |

**The honest limit, stated in the product:** the machinery checks *structure and consistency,
not truth* — which is why the constitution carries *"code is never evidence for environment
state"* and the validator warns on unevidenced environment claims. Only a human at the
environment closes that gap.

## 1.7 Versioning & upgrades — why instances don't fork

Instances customize what the bootstrap installs (by design), so upgrades are never "re-copy":

```
new image MANIFEST.json ─┐
your OS-MANIFEST.lock ───┼─► per file, a 3-way verdict:
your installed files ────┘     unchanged upstream        → skip
                               upstream moved, you didn't → MECHANICAL update
                               both moved                 → guided HAND-MERGE
                               content-bearing (constitution/STATUS) → review deltas, never overwrite
                               new file                   → new capability
```

SemVer protects a **declared instance contract** (file roles · hook semantics · skill names ·
stamp/lock locations). The upgrade is itself an engineered prompt (`image/UPGRADE.md`) — same
philosophy as the install.

## 1.8 The door — feedback that doesn't rely on memory

The only adopter duty is **issues**: `os-bug` · `improvement` · `suggestion` (+ optional
one-click `adopted` registration). And the duty is **agent-borne**: the constitution carries a
standing rule with a mechanical test — *"is the problem in a file the bootstrap installed, or a
rule the constitution carries?"* — the agent records `[OS]` findings, **drafts the prefilled
issue** (version + profile from the stamp), and the human clicks. `/handover` and the stop-gate
sweep un-filed findings at session end. Triage: every adopted finding is codified (a rule, a
template, a check) and the issue closes **naming where** — method changes are *evidence-gated:
extracted from real instances, never designed by committee*. Adoption is measured by the
`adopted` label timeline + a stamp census — real events, never slideware.

## 1.9 Two repos, three rings

| Home | Audience | Holds |
|---|---|---|
| **`flaviusmoldovan-pexon/documentation-as-os`** | every adopter | the image · METHOD · GETTING-STARTED · UPGRADING · the door · Releases |
| **`…-hub`** (proprietary, stewarded) | steward + selected contributors | full thesis · evidence register (§A–§H) · decision record (OD-01…14) · rollout |
| the steward's lane | steward | raw program records |

One law binds them: **anything an adopter needs lives in the product repo** — the hub is
rationale and evidence, one-way-referenced, never load-bearing for an install.

## 1.10 Receipts — the launch week (all verifiable on this repo)

Live 4 days · **3 releases**, all gate-green · a **cold agent** given nothing but the repo
adopted it, built a real project (13→20 tests), and survived a mid-flight requirement change
with a superseding ADR — audited 13/13 against its tree · its **6 findings were fixed and
released the same day** (issues #3–#8 → v2.2.1) · **5 org instances** on ADOPTERS, one already
through the fleet's first version upgrade · validation before launch: ~60 scripted assertions
across every mode, gate, and route.

---

# PART 2 · PLATFORM-MANAGED REPOS × docs-as-os

## 2.1 What a provisioned repo actually ships (~52 files, four layers)

```
organization/<stack>/
│  LAYER 1 · platform contract (NEVER touch)
├── platform.yml                    compliance descriptor and environment declarations
├── .github/workflows/ci.yml        the reusable Spark Pro pipeline (test → deploy per branch)
├── .github/workflows/operations.yml  the MTP jobs (prod promotion)
├── .github/workflows/sonarqube.yml   org scan policy — pre-satisfied on day 0
│  LAYER 2 · platform-committed wiring (KEEP — load-bearing)
├── wrangler.jsonc                  real Hyperdrive IDs (both envs) · Secrets Store bindings
│  LAYER 3 · template code + THE BOOT LAYER
├── CLAUDE.md                       = one line: @AGENTS.md  (an import)
├── AGENTS.md                       the platform's repository guide: the skills-registry
│                                   protocol · DB discipline (schema-per-branch, Drizzle,
│                                   SET LOCAL search_path) · secrets rules · CI fences
├── worker/  web/  scripts/         the paved-road app (DAL core, db-schema sync, Biome, Vite)
│  LAYER 4 · demo content (replaced via new migrations — history never edited)
└── migrations/0000_*.sql · example handlers/components
```

**Key insight: a Bench repo is not a blank adopter — it arrives with a live boot layer.**

## 2.2 The coexistence pattern (shipped in v2.2.2)

```
CLAUDE.md  (yours — the constitution)        AGENTS.md  (the platform's — NEVER edited)
┌───────────────────────────────┐            ┌────────────────────────────────────┐
│ @AGENTS.md   ◄── line 1 ──────┼───imports──│ skills registry: fetch the LIVE    │
│ §1 boot · §2 rules · the loop │            │ skill, official-only, announce use │
│ §8 locked decisions ◄─────────┼─pre-seeded─│ paved-road stack (Hono·Drizzle·…)  │
│ §9 forbidden ops  ◄───────────┼─folds in───│ never-touch: CI jobs · bench.yml · │
│ version stamp · the door      │            │ platform config · migration history│
└───────────────────────────────┘            └────────────────────────────────────┘
                     ONE boot · TWO jurisdictions
        platform law = HOW the infra works · constitution = HOW the work runs
```

- The platform's guide loads **every session** via the import — zero drift, nothing restated.
- The paved-road stack arrives **pre-locked** (§8 points at it instead of re-deciding).
- The platform's red lines become constitution law (§9), guarded by the same human gates.
- Upgrades can't collide **by construction**: the OS's manifest walks only OS files; the
  platform's 52 files aren't in it.

**Validated pattern** — born with the OS on a managed stack · merged the platform template with
exactly this pattern (`@AGENTS.md` is literally line 1 of its constitution) · took the fleet's
first version upgrade · walking skeleton merged and **Dev live** through the platform's own CI.

---

# PART 3 · THE KNOWLEDGE CHANNELS (and the deliberate seam)

## 3.1 Three live channels — the OS points, never duplicates

```
   platform HOW-TO ──►  approved live skills registry
                        validated, versioned skills · fetch live, never embed

platform REFERENCE ──►  approved documentation connector
                        permission-gated · instances mount it READ-ONLY

            HUMANS ──►  authenticated documentation portal

   project MEMORY  ──►  the instance's own docs-as-os        ← what THIS system owns
   method PATTERNS ──►  the `knowledge-candidate` label      ← parked until it earns a home
```

The boundary in one line: **docs-as-os owns per-project memory; platform knowledge stays where
the platform already serves it.** Bench instances get the skills channel automatically (it
rides `AGENTS.md`); the MCP mount is a deliberate, token-gated step.

---

# PART 4 · THE LIVE DEMO — copy-paste, side by side

> Layout: this doc on one half · a fresh terminal + VS Code on the other.
> Every block below is paste-ready. **Watch-for** notes say what to point at.

## Demo A — fresh project, `poc` profile (the five-minute tier)

> One terminal + ONE VS Code window (opened on the demo ROOT, so you see the image and the
> project side by side the whole time).

**A1 · Stage on the Desktop, pull the product from the Release, open the window (terminal):**
```bash
mkdir -p ~/Desktop/docs-os-demo && cd ~/Desktop/docs-os-demo
gh release download -R flaviusmoldovan-pexon/documentation-as-os -p 'image-*.zip'
unzip -q image-*.zip && rm image-*.zip
code -n .
```
**You see (VS Code):** two things in the tree — `image/` and `START-HERE.txt`.
**Do, in the tree:** click `START-HERE.txt` (one sentence: open BOOTSTRAP, pick a profile) →
click `image/BOOTSTRAP.md`, point at **STEP 0** for twenty seconds: *fresh → scaffold ·
existing code → docs built FROM the code · poc stamp → upgrade in place · live install → STOP.*
Mode selection is the prompt's job; the three profiles are three blocks in this one file.

**A2 · The empty project is born — watch the tree, not the terminal:**
```bash
mkdir my-poc && cd my-poc && git init
printf '# roster-poc
3-day POC: print a fair random standup order from a names file.
' > README.md
```
**You see (same VS Code tree):** `my-poc/` appears next to `image/`, holding one README.
**This is any dev's day zero** — an idea and an empty folder. One command installs the OS.

**A3 · THE LAUNCHER — extracts the profile prompt from the version-true file and starts the
session with it** (same terminal, already inside `my-poc`):
```bash
PROMPT="$(awk '/^## Profile P/{f=1} f&&/^```/{c++; next} c==1{print} c==2{exit}' ../image/BOOTSTRAP.md)"
claude --permission-mode acceptEdits "The image is at ../image. $PROMPT"
```
- Terminal-side profile choice: swap `Profile P` → `Profile A` (solo) / `Profile B` (team).
- `acceptEdits` lets file writes flow; shell commands still stop and ask.

**A4 · Answer 2–3 short questions, then watch the tree:**
- project one-liner → *"3-day POC: fair random standup order from a names file"*; anything else
  it can't infer → shortest honest answer (it never invents).
**You see, in order, inside `my-poc/`:** `CLAUDE.md` → `docs/delivery/STATUS.md` +
`CHANGELOG.md` → `docs/OS-MANIFEST.lock` → then it **asks permission to delete `../image/`** —
approve, and **watch `image/` vanish from the tree**.
**What just happened:** that pause is the **human gate** — irreversible operations always stop
and ask. And the installer never stays: the project keeps a version stamp and a lock, never a
stale copy that silently forks.

**A5 · The receipts (terminal):**
```bash
tail -6 CLAUDE.md
cat docs/delivery/STATUS.md
python3 -c "import json;print(json.load(open('docs/OS-MANIFEST.lock'))['version'])"
```
**You see:** the **footer stamp** (image version · profile · date · upstream) · the
**report-back door** section · the lock printing the image version you just installed.
**Five minutes in:** the repo boots from a constitution, carries its own state, knows its
version, and knows how to report back. `solo` adds the five skills and three enforcement hooks;
`team` adds the validator, CI, and governance — same file, different block in the same launcher.

## Demo B — the loop with receipts (browser, 3 minutes)

1. **Issues → filter `label:improvement`, all states** — on launch morning, a cold adopter
   built a real project against this repo; its six findings are these issues; all six were
   fixed, merged through the full gate stack, and released as **v2.2.1 the same day**.
2. **Release v2.2.1** — the notes open with *Impact on existing instances*.
3. **The open issues** — the inbox is real, not theater; small diagnosed ones make good
   first PRs.
4. **ADOPTERS.md** — the current proprietary adoption record.
5. **The deployment evidence archive** — proof from a live development environment.
6. **The approved skills registry** — the live knowledge channel.

## Demo C — optional deep-dive: an EXISTING repo

Point the same launcher (with `Profile A`) at a repo that already has code — STEP 0 flips to
EXISTING mode and the agent writes `overview`/`areas-map`/`architecture` **from the code**,
migrating incrementally. On a Bench/FitKit repo, the same run applies the coexistence pattern
(Part 2). A pre-built example is the fastest way to see the end state.

---

## Where everything lives (leave this on screen at the end)

| Want to… | Go to |
|---|---|
| Adopt (5 min → full) | `flaviusmoldovan-pexon/documentation-as-os` → GETTING-STARTED |
| Understand the method | METHOD.md (5 min) · the hub's thesis (deep) |
| Report / suggest / register | the repo's issues — the only duty |
| Stay current | Watch → Releases; upgrades are guided 3-way diffs |
| Platform knowledge | skills registry (live) · unified-docs MCP (read-only) · the portal |
