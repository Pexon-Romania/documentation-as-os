# Security posture — what runs where, what leaves your machine

The short version: **everything runs locally in your repo, nothing phones home, and the only
data that ever leaves an instance is what a human deliberately submits as a GitHub issue.**

## What the install puts on your machine

- **Markdown files** (constitution, docs skeleton, templates) — inert content.
- **Three shell hooks** (`.claude/hooks/*.sh`) — short, readable scripts *you* install and can
  audit in two minutes: they read your repo's own STATUS/doc-debt files and print reminders.
  They make **no network calls**, touch nothing outside `$CLAUDE_PROJECT_DIR`, and are executed
  by your own Claude Code session under your user. (Windows note: they require a bash on PATH.)
- **Five skills** (markdown instruction files) and **permission `ask:` rules** — the ask-rules
  *add* human confirmation gates before irreversible operations; they never grant anything.
- The **poc profile installs none of the above** — three markdown files only.

## What never happens

- **No telemetry, no phone-home, no beacons.** Adoption registration is a prefilled GitHub
  issue a **human** reviews and clicks; skipping it changes nothing. The steward's census is a
  passive code search over repos the searcher can already access.
- **No credentials anywhere.** The image ships none, the templates forbid committing them, and
  the skeleton rules ban credentials/hostnames/PII in shareable docs.
- **No write access needed.** Adopters never get write to this repo; org-repo git stays
  human-run.

## The scope fence (team tier)

Per-file `scope:` frontmatter is the machine-readable boundary an AI-serving tool must respect
(`shareable` vs `internal`); the validator enforces it. Point any docs-serving tool at
`shareable` only — that boundary is the reason a docs set is safe to expose to an assistant.

## Reporting a security concern

File an **os-bug** issue describing the class of problem (this is an org-internal repo). If it
shouldn't be visible even org-internally, contact the steward directly (MAINTAINERS.md).

---

*documentation-as-os. Verify, don't trust: the hooks are ~40 lines each — read them.*
