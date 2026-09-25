# Skills — the OS's codified processes

> The delivery loop and graceful-enforcement controls as runtime-portable **skills**. The
> bootstrap installs each at `.claude/skills/<name>/SKILL.md` for Claude Code and/or
> `.agents/skills/<name>/SKILL.md` for Codex. Invoke `/name` in Claude Code or `$name` in Codex.
> Keep them **terse** — skills load into context, so lean is correct.

| Skill | What it does |
|---|---|
| **`scope-lock`** | Front of the loop — turn a request into a signed, buildable scope before any code |
| **`workstream <name>`** | Fork a new workstream into its own subfolder (its own space · tracker · records) |
| **`handover`** | Build the handover doc-set **fresh from the code** — layered, grounded |
| **`reconcile-docs`** | Pay down doc-debt (the graceful-enforcement catch-up) |
| **`gating <relax\|strict\|status>`** | Control enforcement mode — relax for the unpredictable; it logs debt + auto-expires |

The loop's *build-while-current* isn't a skill — it's how you work (constitution §5; the hooks
enforce it). The boot read-in and human gates aren't skills either — they're hooks plus the
selected harness's native permission layer (`../hooks/`).

---

*Part of documentation-as-os (`image/skills/`). Proprietary material owned by **Pexon Romania and Flavius Moldovan**.*
