<!-- documentation-as-os · the constitution (boot file). Save as CLAUDE.md (Claude Code) or AGENTS.md at the repo root.
     Fill every placeholder; delete any rule that genuinely doesn't apply. Keep it SHORT and CURRENT — it's the constitution, not a wiki.
     The hooks in image/hooks/ enforce §1/§5/§7; the skills in image/skills/ run §4 and the graceful-enforcement controls.
     DELETE THIS WHOLE COMMENT at install — installer instructions never ship in a live constitution. -->

# {{PROJECT_NAME}} — Agent Constitution

> {{ONE_LINE_WHAT_THIS_IS}}.
> **Read this FIRST, every session. It overrides default behavior.**

## 1 · Boot — read in, every session
Before ANY work, read — in order:
1. **This file** — the rules + locked decisions.
2. **`{{STATUS_DOC}}`** (e.g. `docs/delivery/STATUS.md`) — where we are · what's next · what's blocked · **open doc-debt**.
3. **The doc for the area you're touching** (in `{{DOCS_LOCATION}}`).
4. **Project memory** (`{{MEMORY_LOCATION}}`) — durable decisions + learnings.

Don't start work until you know the current state and the task. *(The `SessionStart` hook surfaces 2–4 automatically; if it didn't fire, read them yourself.)*

**Reconcile, don't just read:** if `{{STATUS_DOC}}` carries a forward-looking line ("do X next session", "restart to activate"), check whether it already happened and fix it on the spot — a `Last verified` date doesn't make a future-tense claim true.

## 2 · Critical rules — never violate
- **The code is the source of truth.** Verify against it; a doc that disagrees is the bug — fix the doc.
- **Production-grade by default.** No shortcuts, band-aids, "temporary" code, or mock data on production paths. If the proper fix is the same effort, do the proper fix.
- **Ask before anything irreversible or architectural** — schema, public API, data deletion, {{PROMPT/MODEL changes if you ship AI features}}, deploys. *(The human gates — permission `ask:` rules — stop and ask you here; you decide.)*
- **{{DOMAIN_INTEGRITY_RULES}}** — your domain's data-integrity rules *(delete if N/A)*.

## 3 · Verify before you act
- Read the actual source — never diagnose from memory, a summary, or what a doc claims.
- Trace the full path (caller → callee → data); confirm each link before you state it.
- A sub-agent's or a memory's claim is a **lead to verify**, not a fact to repeat. Say what you verified and how sure you are. Not sure → read more → ask.
- **No patching — investigate first.** On a break: understand *why* + the full blast radius *before* writing a fix.
- **Code is never evidence for environment state.** What an environment *contains* — rows, configured rules, counts — can't be read from the repo: state it only with the environment + the check + the date named (*"six active rules in dev and prod (admin panel, 2026-09-09)"*), else tag it `[NEEDS-CHECK]`. Absence of a seed is not absence of data.

## 4 · How we build — the loop
- Treat a non-trivial request as a **hypothesis, not a spec.** Cross-check it against the plan and the real code *before* building.
- **Lock scope before code** — what's in / what's deferred, in writing, signed off. *(run the
  `scope-lock` skill: `/scope-lock` in Claude Code, `$scope-lock` in Codex)*
- **Re-run the loop** when priorities or requirements move; record the change, don't absorb it silently.
- A workstream that needs its own space gets its own subfolder. *(`/workstream`)*

## 5 · "Done" = code + docs + AI-context in sync — *gracefully enforced*
A change isn't complete until the **code** works, the **docs** reflect it, and the **AI-context** (this file, memory, the docs you read) reflects it.
- When you change a documented surface, **update its doc in the SAME change** — you have the context now.
- Stamp `Last verified: <date>` on docs you touch; tag uncertain claims `[VERIFIED]` / `[INFERRED]` / `[NEEDS-CHECK]`.
- **Corrections are corpus-wide:** before fixing a wrong claim, grep for its phrasing and fix every echo in the same change; name a doc error *"this doc was wrong"*, never *"this is no longer true."*
- **The OS holds you to this** (it won't close the session on stale docs). When reality demands
  speed, say **"relax the gating"** (run the `gating relax` skill) — it yields, **logs the skip
  as doc-debt**, and helps you reconcile later (`reconcile-docs`). Relaxing is loud and expires;
  it never becomes silent drift.

## 6 · Source of truth & deploy
- One **source of truth** for the code (`{{SOURCE_OF_TRUTH}}`); everything else is a copy it feeds.
- Environments: {{ENVIRONMENTS}}. **Prove a change in test before production. Never edit production directly.**
- Fresh branch per change; stage only the change's files (verify the count); **a human runs git** (commit / push / PR).
- Commit messages: **one short imperative line — no AI co-author trailers, ever.**

## 7 · Write-out before you stop
Update `{{STATUS_DOC}}` (where we are + next step), append a session note **to memory (`## Session log`)**, record any decision in memory (**append-only — never lose the *why***), and clear or log any doc-debt — **a forward-looking commitment ("do X next session") is logged as a `- [ ]` doc-debt item *when you write it*, so the gates track it, not your memory.** **If it mattered this session, it's written before the session ends.** *(The `Stop` hook checks this — gracefully.)*

## 8 · Locked decisions (do not silently change)
> To change one, it's deliberate — never silent: record it in a **superseding ADR** and update
> this list with a pointer to it (the `scope-lock` skill handles the ritual).

{{LOCKED_DECISIONS — the architecture/tooling choices that are final, so they aren't relitigated. e.g. "Frontend: <framework>. Backend: <framework>. DB: <db>. Auth: <method>."}}

## 9 · Forbidden operations
{{FORBIDDEN_OPS — destructive/irreversible actions no one does without explicit sign-off: force-push to a shared branch; DROP/TRUNCATE/DELETE-without-WHERE; commit a secret; deploy to prod without a validated test pass.}}

<!-- Portable: §1–§7 (the rules); the project-specifics are the values you filled. This file is the boot sequence of documentation-as-os. -->
