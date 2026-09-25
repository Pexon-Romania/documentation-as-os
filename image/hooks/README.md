# Hooks — the enforcement layer

> These implement the design in [`../SELF-ENFORCEMENT.md`](../SELF-ENFORCEMENT.md) on Claude Code's real mechanisms. **Reference configs — verified against the live docs and TESTED in the bootstrap dogfood run before they're relied on** (the v1 "done" gate). The heuristics below are honest about false positives.

---

## What ships here

| File | Hook / mechanism | Does |
|---|---|---|
| `settings.template.json` | the wiring + permission **`ask:`** rules | merge into `.claude/settings.json` |
| `session-start.sh` | `SessionStart` | inject STATUS + open doc-debt + memory index; **reset gating to `strict`** (auto-expire) |
| `post-edit-docs.sh` | `PostToolUse(Edit\|Write)` | docs-part-of-done nudge; in `relaxed` mode, log doc-debt |
| `stop-gate.sh` | `Stop` | **graceful** won't-close-on-stale-docs: `strict` → block *once*; `relaxed` → allow + remind; never loops |

## The OS-mode file — `.claude/os-mode`

A one-word file: `strict` (default) or `relaxed`. The `/gating` skill writes it; the hooks read it; `session-start.sh` **resets it to `strict` every session** (so a relax never silently persists). This is graceful enforcement's switch.

## The human gates (no script — just rules)

Permission **`ask:`** rules in `settings.template.json` make Claude Code *stop and ask you* before irreversible ops (`git push`/`commit`, `git reset --hard`, `rm -rf`, SQL `DROP`/`DELETE`/`TRUNCATE`). In interactive mode this is the right mechanism — a hook can't pop its own prompt. Tune the list to your project.

## Honest caveats (read before relying on these)

- **Heuristics, not proofs.** `stop-gate.sh` infers "stale" from *"code changed but STATUS didn't this session"* — it will sometimes false-positive. That's why it blocks **once** and is easily overridden (`/gating relax`). Tune it in the dogfood run.
- **Verify syntax.** The exact `settings.json` hook schema + matcher/`ask:` patterns are confirmed against the live Claude Code docs at install — don't assume this template is byte-correct.
- **Make scripts executable:** `chmod +x .claude/hooks/*.sh`.
- **Shell-profile gotcha:** hooks run via `sh -c`; an unconditional `echo` in your shell profile can corrupt a hook's output — guard profile output with `if [[ $- == *i* ]]`.
- **Windows:** the hooks are bash scripts — they need a bash on PATH (Git Bash works). Validated on macOS/Linux; on a bash-less Windows setup the OS still runs, minus the hook layer (the protocol + validator carry the line, as the team tier's exemplar does by choice).
- **Token cost:** `session-start.sh` injects every session — keep it a *small* pointer (it reads only the head of STATUS/memory), not whole files.

---

*Part of documentation-as-os (`image/hooks/`). Proprietary material owned by **Pexon Romania and Flavius Moldovan**. Reference implementations — validated in the dogfood run; the artifact wins.*
