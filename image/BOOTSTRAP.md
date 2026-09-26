# BOOTSTRAP — the prompts that boot the OS into a repo

> Three install profiles, scaled to your stage (the thesis's "scale to your stage", made
> executable): **P — poc** (five minutes: constitution-lite + live state + the door; no
> machinery) · **A — solo** (one operator + agent: constitution · skeleton · skills · hooks) ·
> **B — team** (a shared org docs repository that becomes the project's source of truth:
> validator + CI + governance + the delivery line). A POC that grows up **runs the next
> profile's prompt — it upgrades in place, it never re-adopts.**
> *The magic is the engineered image each prompt instantiates — not the sentence.*

## How to use

1. **Get the latest Release** of `Pexon-Romania/documentation-as-os` (the `image-…zip` asset is the
   image alone; the source archive works too). **Record the tag you took.** Never install from
   a copied folder or `main` — version-truth lives in Releases.
2. Place the `image/` folder at/beside the target repo root.
3. Open **Claude Code or Codex** in the repo and paste the profile prompt below. The prompt
   asks which runtime to wire (`Claude Code`, `Codex`, or `both`) before it writes runtime files;
   answer its remaining questions (placeholders; anything irreversible).
4. It installs, verifies, **stamps the instance** (version + profile in the constitution
   footer, `MANIFEST.lock` for future upgrades, the upstream report-back door), then removes
   the installer folder.

Upgrading an existing instance later → [`UPGRADE.md`](UPGRADE.md). The surface upgrades
protect → [`INSTANCE-CONTRACT.md`](INSTANCE-CONTRACT.md).

## Profile P — poc *(innovation tier: five minutes, no machinery)*

```
You are bootstrapping the "documentation-as-os" POC PROFILE into THIS repository. The system
image is in ./image/ (or the path I give you). Work carefully, ASK before anything
irreversible, VERIFY — don't assume.

STEP 0 · Runtime. ASK me: "Which agent runtime should this instance support: Claude Code,
  Codex, or both?" Do not infer the answer. POC has no hooks, but the answer selects the boot
  file: Claude Code -> CLAUDE.md; Codex -> AGENTS.md; both -> AGENTS.md is canonical and
  CLAUDE.md imports it with @AGENTS.md as line 1. Never create two divergent constitutions.

STEP 1 · Constitution-lite. At the runtime-selected boot location, if ./CLAUDE.md or AGENTS.md
  already exists, MERGE — ask me
  first, never clobber (platform-provisioned repo with CLAUDE.md = an @AGENTS.md import: the
  constitution takes CLAUDE.md, keep @AGENTS.md as its first line, never edit AGENTS.md). Otherwise create the selected boot file as a SHORT constitution from
  image/CONSTITUTION.template.md keeping only: §1 boot (read this file + STATUS every
  session), §2 critical rules, §5 done = code + docs in sync (manual — no hooks in this
  profile), §7 write-out before you stop. Because POC has no project-memory file, remove the
  memory read/search/write clauses from §1 and §7 instead of leaving a broken pointer. Fill
  every {{PLACEHOLDER}} you keep; ask for what you can't infer. Do not invent. DELETE the
  template's instructional header comment.

STEP 2 · Live state. Create docs/delivery/STATUS.md from image/skeleton/STATUS.template.md
  and docs/delivery/CHANGELOG.md (append-only, empty). That's the whole poc doc-set.

STEP 3 · Stamp + lock + door. (a) Append to the constitution footer:
  "<!-- documentation-as-os · image <version from image/VERSION> · profile: poc ·
  installed <today> · upstream: https://github.com/Pexon-Romania/documentation-as-os -->".
  (b) Copy image/MANIFEST.json to docs/OS-MANIFEST.lock (future upgrades diff against it).
  (c) Add this standing section to the constitution:
  "## OS report-back (standing) — when the OS itself misbehaves (a rule contradicts itself,
  a template is wrong, friction in the method): DRAFT the upstream issue immediately —
  prefill https://github.com/Pexon-Romania/documentation-as-os/issues/new with the matching
  template (os-bug | improvement | suggestion), the image version + profile from the footer
  stamp, and the finding — and hand me the link to file. If I don't file it now, record the
  draft under '## OS findings (to file upstream)' in STATUS so it survives the session."

STEP 4 · Verify, then remove the installer. Check: constitution boots, STATUS + CHANGELOG
  exist, no unfilled {{PLACEHOLDER}} remains, the stamp/lock/door are in place. Then DELETE
  the image folder you installed from (ask me first if it sits inside this repo's tree) —
  the instance keeps the stamp, lock, and door; a kept image copy becomes a silently-stale
  fork.

STEP 5 · Register (optional, zero-duty) + report. Offer me the prefilled adoption-
  registration link — https://github.com/Pexon-Romania/documentation-as-os/issues/new with the
  "Adopted" template, instance name + profile + image version filled — one click puts this
  instance on the estate view; skipping changes nothing. Then report honestly: what you
  installed, every placeholder you filled vs left for me, what you could not verify.
  Graduating later: run the SOLO profile prompt from the then-latest Release — it detects
  this tier and upgrades in place.
```

## Profile A — solo *(the original flow, dogfood-validated 2026-06-25)*

```
You are bootstrapping the "documentation-as-os" SOLO PROFILE into THIS repository. The system
image is in ./image/ (or the path I give you). Work carefully, ASK before anything
irreversible, and VERIFY — don't assume.

STEP 0 · Detect mode.
  - No / sparse code  -> FRESH (scaffold).
  - Existing codebase -> EXISTING (analyze + migrate).
  - A poc-profile constitution already installed -> UPGRADE (extend in place; keep its
    stamp history).
  - A solo/team stamp already present -> STOP: this instance is live — re-running the
    bootstrap duplicates stamps and re-asks settled questions. Version moves use
    image/UPGRADE.md; a broken install is repaired by hand against the lock.
  State which mode and why before proceeding.

  Then ASK me exactly: "Which agent runtime should I wire: Claude Code, Codex, or both?"
  Do not infer from the harness running this bootstrap. Record the answer for STEPS 1, 3, 4,
  7, and 8.

STEP 1 · Constitution.
  Select the boot shape from my runtime answer: Claude Code -> CLAUDE.md; Codex -> AGENTS.md;
  both -> AGENTS.md is the canonical constitution and CLAUDE.md keeps @AGENTS.md as line 1.
  Never create two divergent constitutions. If the selected ./CLAUDE.md or AGENTS.md ALREADY
  EXISTS: do NOT overwrite — MERGE the OS rules in (or
  append a clearly-marked "documentation-as-os" section) and ASK me first (real existing
  repos usually have one). Otherwise copy image/CONSTITUTION.template.md to the selected
  canonical boot file (and create the import-only CLAUDE.md for `both`).
  Fill every {{PLACEHOLDER}}: infer what you safely can from the repo (name, stack,
  source-of-truth, environments); ASK me for what you can't (locked decisions, domain rules,
  forbidden ops). Set `{{MEMORY_LOCATION}}` to `memory/MEMORY.md`. Do not invent. DELETE the
  template's instructional header comment — installer text never ships in a live constitution.
  PLATFORM-PROVISIONED REPO (e.g. Bench/FitKit: CLAUDE.md is an @AGENTS.md import and AGENTS.md
  is the platform's repository guide): the constitution TAKES CLAUDE.md and keeps @AGENTS.md as
  its FIRST line (the import loads the platform guide every session — never fork or edit
  AGENTS.md, it is platform truth); seed §8 locked decisions from the paved-road stack (decided
  by the platform, pointer not restatement) and fold the platform's never-touch rules into §9
  (CI workflow jobs/triggers/refs · platform config keys · compliance descriptors · migration history).
  If my runtime answer includes Codex but that platform AGENTS.md must remain verbatim, STOP and
  surface the conflict: do not claim a full Codex install until the platform owner provides an
  approved Codex instruction path or permits the OS constitution to be included.

STEP 2 · Skeleton.
  Scaffold the doc tree per image/skeleton/SKELETON.md (docs/product, docs/engineering,
  docs/delivery, the support-pack, a memory seed) — SKELETON rule 1 WINS: omit the files
  this stage doesn't need (the support-pack and empty registers are optional subsets).
  Create docs/delivery/STATUS.md from STATUS.template.md, docs/delivery/doc-debt.md from
  skeleton/doc-debt.template.md, and docs/delivery/decisions/0000-adr-template.md from
  skeleton/adr.template.md. Create memory/MEMORY.md from skeleton/MEMORY.template.md and keep
  its hot index within the first 30 lines (the SessionStart adapters inject only that head).
  Runtime-native memory may supplement this file, never replace it: the Git-tracked file is the
  portable project memory across runtimes. FRESH = empty index + guided stubs; EXISTING = seed
  only verified outcomes and pointers in STEP 5 — never copy raw histories or documents.

STEP 3 · Skills.
  Install the five skills (scope-lock, workstream, handover, reconcile-docs, gating) for the
  selected runtime(s): Claude Code -> .claude/skills/<name>/SKILL.md; Codex ->
  .agents/skills/<name>/SKILL.md; both -> both locations. Claude invokes them as `/name`;
  Codex invokes them as `$name`.

STEP 4 · Hooks (enforcement). ASK before writing settings.
  - Always create .claude/os-mode containing `strict`. It is the stable shared state even for a
    Codex-only install; `both` must never have two enforcement-mode files.
  - If the answer includes Claude Code: MERGE image/hooks/settings.template.json into
    .claude/settings.json (or settings.local.json if the repo uses that) WITHOUT clobbering;
    copy image/hooks/*.sh -> .claude/hooks/ and chmod +x them; verify current Claude hook and
    permission syntax; tune `ask:` rules to this repo's irreversible operations.
  - If the answer includes Codex: copy image/hooks/codex/{common.py,session_start.py,
    post_edit_docs.py,stop_gate.py} -> .codex/hooks/ and copy
    image/hooks/codex/hooks.template.json -> .codex/hooks.json WITHOUT clobbering an existing
    hook config (merge matching event groups). Verify against the current official Codex hook
    docs. Tell me Codex will skip project hooks until I review and trust them with `/hooks`;
    do not claim they are live before that review. On Windows, add and test `commandWindows`
    for every handler before relying on it.

STEP 5 · EXISTING mode only — build the docs FROM the code.
  Read the actual code. Write the product + engineering bucket docs grounded in it (overview,
  how-it-works, architecture, areas-map, data-model, deployment, known-limitations). Mark
  [VERIFIED]/[INFERRED]; stamp Last verified. Do NOT migrate everything at once — start with
  architecture + areas-map + STATUS, then migrate incrementally over sessions until the OS
  docs are the live source. Log not-yet-migrated areas as doc-debt.

STEP 6 · Stamp + lock + door.
  (a) Append to the constitution footer: "<!-- documentation-as-os · image <version from
  image/VERSION> · profile: solo · installed <today> · upstream:
  https://github.com/Pexon-Romania/documentation-as-os -->".
  (b) Copy image/MANIFEST.json to docs/OS-MANIFEST.lock (upgrades diff against it).
  (c) Add this standing section to the constitution:
  "## OS report-back (standing) — when the OS itself misbehaves (a hook misfires, a gate
  blocks wrongly, a template/skill contradicts itself): the test is 'is the problem in a
  file the bootstrap installed, or a rule this constitution carries?' If yes it's OS-level:
  record it as an '[OS]' line under '## OS findings (to file upstream)' in STATUS, DRAFT the
  upstream issue (prefill https://github.com/Pexon-Romania/documentation-as-os/issues/new with the
  matching template — os-bug | improvement | suggestion — plus the image version + profile
  from the footer stamp and the finding), and hand the human the link. /handover and the
  stop-gate surface un-filed [OS] findings."

STEP 7 · Start the loop.
  NOTE: restart every selected harness so it loads the skills + hooks. For Claude Code, verify
  `/scope-lock`; for Codex, review/trust the hook definitions with `/hooks` and verify
  `$scope-lock`. In THIS session, run the scope-lock steps manually. Run the selected runtime's
  scope-lock skill on the first real task. Update STATUS (where we are / next).

STEP 8 · Verify, then remove the installer.
  Check: one canonical constitution + skeleton + memory/MEMORY.md + the selected runtime
  skills/hooks in place,
  os-mode = strict, no unresolved installer placeholders in instantiated content (the fields in
  `decisions/0000-adr-template.md` are intentionally left for future ADRs), stamp/lock/door present.
  Exercise each selected
  adapter: SessionStart injects STATUS, doc-debt, and the memory hot index; a synthetic code edit
  produces a nudge; relaxed mode logs debt; strict Stop blocks once and honors stop_hook_active.
  Then DELETE the image folder you installed from
  (ask me first if it sits inside this repo's tree) — a kept image copy becomes a
  silently-stale fork; upgrades come from the next Release via image/UPGRADE.md.

STEP 9 · Register (optional, zero-duty) + report — honestly.
  Offer me the prefilled adoption-registration link (the "Adopted" issue template at the
  upstream repo: instance name + profile + image version) — one click, estate view; skipping
  changes nothing. Then tell me: what you installed; every placeholder you filled vs. left
  for me; runtime choice; permissions/ask rules set; hook trust state; what you could NOT verify
  (hook syntax or firing?); and what remains
  (migration backlog, validation). Label what's working vs. what's assumed-until-tested.
```

## Profile B — team *(the shared-repo era; production-proven 2026-07/08)*

Prereq: an empty(ish) repo in your org for the docs (a platform descriptor file is fine — never
touch it), and this `image/` available locally. Open your agent in a clone of that repo and paste:

```
You are installing the documentation-as-os TEAM PROFILE: this repository becomes the project's
documentation source of truth. The system image is in <path-to>/image/ (system/ + templates/).
Work carefully, ASK before anything irreversible, and VERIFY everything — two independent
instruments for any does-X-exist conclusion; never conclude absence from truncated output.

STEP 0 · Context. ASK me first: "Which agent runtime will operate this docs repo: Claude Code,
  Codex, or both?" Do not infer it. The team profile uses validator/CI governance rather than
  solo lifecycle hooks, but runtime choice controls which boot path you verify. Then ask me:
  the app repos this documents · the audience lines (default: leaders /
  support / app-documentation / dependencies / delivery — the shape that fits a user-facing
  product; LINES ARE AUDIENCES, NOT TOPICS: one line per reader type who arrives with different
  questions, so a platform or program home picks different lines — the metro rules stay, the map
  fits the project) · the item-ID prefix · who the steward is. Confirm what already exists in
  this repo before creating anything.

STEP 1 · Seed the tree. Create the audience-line folders (+ delivery/incidents, delivery/specs).
  Install from image/templates/: README-ROUTER → README.md · AGENTS.template → AGENTS.md ·
  BOOT.template → CLAUDE.md · CONVENTIONS + WORK_TRACKER + CHANGELOG + LEARNINGS → delivery/ ·
  ENVIRONMENTS → dependencies/. Fill every {{PLACEHOLDER}}. Write DOCS-STANDARD.md — the locked
  tree IS what you just created; additions go through the LEARNINGS proposal channel. Include the
  environment-state rule (AGENTS §3 / the validator's ENV-STATE warn): claims about what an
  environment CONTAINS need environment + check + date named, else [NEEDS-CHECK].

STEP 2 · System layer. scripts/validate_docs.py from image/system/validate_docs.template.py —
  set its seven knobs to the STEP-1 tree (keep "OS-MANIFEST.lock" in ALLOWED_ROOT_FILES) and
  delete the template header. Install .github/workflows/validate-docs.yml and .github/CODEOWNERS
  (point at the real team; if no org team exists yet, the steward's handle, with a comment that
  it swaps). Run the validator and fix until PASS with 0 fails.

STEP 3 · Stamp + lock + door. (a) Append to CLAUDE.md's footer:
  "<!-- documentation-as-os · image <version from image/VERSION> · profile: team ·
  installed <today> · upstream: https://github.com/Pexon-Romania/documentation-as-os -->". (b) Copy image/MANIFEST.json to
  ./OS-MANIFEST.lock at the repo root. (c) The LEARNINGS template already carries the [OS]
  classification header — that is the door; agents draft upstream issues from [OS] entries
  (prefill https://github.com/Pexon-Romania/documentation-as-os/issues/new with template + image
  version + profile) and the human files them.

STEP 4 · The first PR — which is also the working model forever: fresh branch → THE HUMAN runs
  the signed commit, push, PR → merge when the validate check is green. From now on the org repo
  is canonical; every local copy is a clone or read-only mirror; git stays human-run.

STEP 5 · Governance sitting. Walk the human through image/system/GOVERNANCE-RUNBOOK.md — repo
  behavior, the branch ruleset (image/system/ruleset.template.json), roles (steward = maintain,
  contributors = write). VERIFY each setting after applying it; record every setting + its why in
  the docs' own governance page. The sitting is a documentation event.

STEP 6 · First content. Existing app → build the reference docs FROM THE CODE, one audience line
  at a time, logging deferred areas as doc-debt; populate the board with the real open work.
  Then log your first LEARNINGS entry about this install — something always comes up, and the
  inbox working from day one is the point. Offer the human the prefilled adoption-registration
  link (the "Adopted" issue template at the upstream repo — optional, zero-duty). Finally:
  Report the runtime choice and verify its boot file is active. Then DELETE the local image
  folder you installed from (never vendor it into the docs repo) —
  upgrades come from the next Release via image/UPGRADE.md.
```

## What it produces

A repo that **boots from a constitution, owns its docs, enforces gracefully, runs the loop —
and knows its own version**: the stamp + `OS-MANIFEST.lock` make every future upgrade a
three-way diff instead of guesswork, and the door makes OS-level findings travel upstream as
issues without relying on anyone's memory.

## Honesty / validation

**This bootstrap *is* the validation.** The mechanical half (templates complete, placeholders
enumerable, a fresh instance passes its validator) is CI-tested on every change to this repo
(`scripts/smoke_bootstrap.sh`); the agent-run half (a live session executing a profile prompt on
a scratch repo) is re-earned at every MINOR/MAJOR release — the release checklist holds that
line, because an agent run can't be CI'd.

---

*Part of documentation-as-os (`image/`). Proprietary material owned by **Pexon Romania and Flavius Moldovan**, Senior AI Technical
Lead. The boot loader to the engineered image; the artifact wins.*
