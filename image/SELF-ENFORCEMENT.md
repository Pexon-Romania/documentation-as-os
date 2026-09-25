# Self-enforcement — how the OS keeps itself current

> The honest model of what the system enforces *on its own*, what it *gates to a human*, what stays best-effort — and crucially, **how it bends without breaking.** Grounded in Claude Code's real mechanisms, validated in the dogfood runs (deep evidence lives with the steward, available to reviewers on request). This is the spec the actual `hooks/` configs implement.

---

## The point

On the source project, a real share of "keeping the docs true" is the **operator prompting it** (do the loop, update STATUS, don't skip the gate). This layer moves as much of that as possible from operator-discipline into **harness-enforced mechanism** — *without* becoming a rigid system you'd switch off.

## Graceful enforcement — hold the line · yield to judgment · reconcile the debt ⭐

A rigid enforcer gets switched off the first time it blocks something urgent. An **adaptive** one earns its keep. So every gate works in three beats:

1. **Holds the line by default.** Gates block; the session won't close on stale docs; the read-in always runs. **Strict is the resting state.**
2. **Yields to you, in the moment, with one word.** Real projects bring unpredictable, urgent, exploratory moments. Tell the OS *"relax the gating"* (a prompt, or `/gating relax`) and it **downgrades block → guide** — it lets you move, it doesn't fight you.
3. **Never forgets — reconciles the debt.** A relaxed gate doesn't vanish: the skipped update is logged as **doc-debt**, surfaced next session, and the OS *helps you pay it down* (`/reconcile-docs`). A necessary mess never silently becomes permanent drift.

> It's **documentation debt, handled like tech debt** — taken on *deliberately*, *tracked and paid back*, never hidden. The adaptivity is not a weakening of enforcement; it is **what keeps the enforcement switched on** through a real project.

**Anti-permanent-relax guardrail (the honest failure mode):** `relaxed` is **loud** (the doc-debt shows every session) and it **auto-expires** (resets to `strict` next session unless re-set). You can't relax once and drift forever — staying loose is a *choice*, made with the debt in view.

**Mechanism (grounded):** an OS-mode the hooks read (`strict` default / `relaxed`), toggled by a prompt or skill; relaxed → hooks **warn + log** instead of block; the `SessionStart` hook **surfaces the doc-debt**; a `/reconcile-docs` skill clears it.

## The layers

Every **HARD** gate below is *default-hard · operator-overridable (one word) · debt-tracked* — that's Graceful enforcement, applied.

| Goal | Mechanism (Claude Code) | Default strength | v1? |
|---|---|---|---|
| **Never start cold** — read-in STATUS + memory + any open doc-debt | `SessionStart` hook → inject a *small* pointer | HARD (auto) | ✅ |
| **Standing rules + locked decisions** | `CLAUDE.md` (+ `.claude/rules/` path-scoped) | SOFT (agent follows) | ✅ |
| **Human gate** — stop & ask before irreversible ops (commit/push, schema, delete, prod) | permission **`ask:` rules** | HARD (stops & asks *you*) | ✅ |
| **Docs-part-of-done nudge** — code changed, was its doc touched? | `PostToolUse(Edit\|Write)` hook → warn / `additionalContext` | MEDIUM (warns) | ✅ |
| **Won't close with open doc-debt** *(reliable form of "don't close on stale docs")* | `Stop` hook → blocks once on open doc-debt; relaxed → remind; never loops (`stop_hook_active` guard) · **validated 2026-06-25** | HARD-by-default | ✅ |
| **Loop stages** — intake · scope-lock · build · handover · spin-up-workstream | **skills** (`/command`) | codified | ✅ |
| **Adaptivity** — relax/strict toggle · doc-debt register · reconcile | `/gating relax` · `/gating strict` · `/reconcile-docs` skills + hooks reading the mode | — | ✅ |

## The honest line

- **AUTO — harness-enforced:** the read-in, the doc-debt surfacing, the post-edit nudge. Run whether or not anyone remembers.
- **HUMAN-IN-THE-LOOP — codified, enforced, *and* overridable:** the gates stop and require *you*; and you can relax them with a word. You are always in control — the OS makes the control point un-skippable *and* un-rigid.
- **SOFT — best-effort:** the `CLAUDE.md` rules (reinforced by the read-in + nudges).
- **What no layer catches — the known truth-limit:** the validator checks *structure and consistency*, **not truth**. A confidently-worded false claim about environment state passes every check and gets its `last_verified` re-stamped on each sweep, which reads as corroboration (it happened live: a false "ships empty" claim stood ~2 months across 9 files). The constitution's env-state rule + the validator's ENV-STATE warn narrow that gap; **only a human looking at the environment closes it.**
- **FRONTIER — measured, not claimed:** the *autonomous* clone-and-self-boot end-to-end, and **tuning the gate friction** (how strict before it annoys) — learned from the dogfood run, not guessed.

## Why ask-rules, not a "prompt-the-user" hook

In interactive Claude Code a hook **cannot pop its own prompt to the user** — it can only block (exit 2 / `deny`) or inject text. So the clean human-gate is the built-in permission **`ask:`** rule: the OS pauses and asks *you* to approve. A `PreToolUse` exit-2 hook is the *hard-deny* alternative for things that should never run unprompted.

## What ships in `hooks/` (then tested in the dogfood run)

- `SessionStart` — read-in (STATUS head + memory index) **+ surface open doc-debt**.
- `PostToolUse(Edit|Write)` — docs-part-of-done nudge.
- `Stop` — won't-close-on-stale-docs, **graceful** (override-with-a-word, logs debt, `stop_hook_active` guard).
- permission **`ask:` rules** — the human gates.
- the **OS-mode** read + `/gating relax` · `/gating strict` · `/reconcile-docs` skills + the **doc-debt register**.

All authored, then **tested** (clean repo + existing repo) before this layer is "done." Exact `settings.json` syntax confirmed against the live docs at wiring.

---

*Part of documentation-as-os (`image/`). Proprietary material owned by **Pexon Romania and Flavius Moldovan**. Grounded in the Claude Code facts in `_evidence/`; the artifact wins.*
