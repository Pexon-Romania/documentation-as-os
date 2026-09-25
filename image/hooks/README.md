# Hooks — the enforcement layer

> These implement the design in [`../SELF-ENFORCEMENT.md`](../SELF-ENFORCEMENT.md) through
> harness-specific adapters. **Reference configs must be verified against current runtime docs
> and tested in the bootstrap dogfood run before they're relied on.** The heuristics below are
> honest about false positives.

---

## Claude Code adapter

| File | Hook / mechanism | Does |
|---|---|---|
| `settings.template.json` | the wiring + permission **`ask:`** rules | merge into `.claude/settings.json` |
| `session-start.sh` | `SessionStart` | inject STATUS + open doc-debt + memory index; **reset gating to `strict`** (auto-expire) |
| `post-edit-docs.sh` | `PostToolUse(Edit\|Write)` | docs-part-of-done nudge; in `relaxed` mode, log doc-debt |
| `stop-gate.sh` | `Stop` | **graceful** won't-close-on-stale-docs: `strict` → block *once*; `relaxed` → allow + remind; never loops |

## Codex adapter

[`codex/`](codex/) carries the equivalent repository-local adapter: `.codex/hooks.json` wiring
plus standard-library Python handlers for `SessionStart`, `PostToolUse(Edit|Write)`, and `Stop`.
Codex users review and trust the exact definitions with `/hooks`; changed definitions are
skipped until trusted again.

## The OS-mode file — `.claude/os-mode`

A one-word file: `strict` (default) or `relaxed`. The `/gating` (Claude) or `$gating` (Codex)
skill writes it; every installed adapter reads it and its SessionStart handler **resets it to
`strict` every session**. Keeping one shared path prevents a `both` installation from drifting.

## The human gates (no script — just rules)

Permission **`ask:`** rules in `settings.template.json` make Claude Code stop and ask before
irreversible operations. Codex uses its native sandbox/approval policy; hooks may inspect or
block operations, but must not be presented as a substitute for a real user approval. Tune the
selected runtime's permission layer to the project.

## Honest caveats (read before relying on these)

- **Heuristics, not proofs.** Post-edit path detection is best-effort. The Stop gate uses the
  explicit doc-debt register, blocks **once**, and is easily overridden (`/gating relax` or
  `$gating relax`). Tune it in the dogfood run.
- **Verify syntax.** The exact `settings.json` hook schema + matcher/`ask:` patterns are confirmed against the live Claude Code docs at install — don't assume this template is byte-correct.
- **Make scripts executable:** `chmod +x .claude/hooks/*.sh`.
- **Shell-profile gotcha:** hooks run via `sh -c`; an unconditional `echo` in your shell profile can corrupt a hook's output — guard profile output with `if [[ $- == *i* ]]`.
- **Windows:** the hooks are bash scripts — they need a bash on PATH (Git Bash works). Validated on macOS/Linux; on a bash-less Windows setup the OS still runs, minus the hook layer (the protocol + validator carry the line, as the team tier's exemplar does by choice).
- **Token cost:** `session-start.sh` injects every session — keep it a *small* pointer (it reads only the head of STATUS/memory), not whole files.

---

*Part of documentation-as-os (`image/hooks/`). Proprietary material owned by **Pexon Romania and Flavius Moldovan**. Reference implementations — validated in the dogfood run; the artifact wins.*
