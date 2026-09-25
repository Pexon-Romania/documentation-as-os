# {{APP}} documentation — agent boot file (install as CLAUDE.md or AGENTS.md at the repo root)

> Thin by design: the working rules live in the documentation system — this file points there.

## 1 · Read first, every session
1. `AGENTS.md` — the working protocol. Follow it.
2. `README.md` — the documentation map; route to the line for your task.
3. The delivery board — where we are · what's next · what's blocked.

## 2 · The rules, in short (the protocol is authoritative)
- The code is the source of truth — verify against it before acting (five instrumentation rules).
- Docs are part of "done" — the validator FAILing means the change isn't done.
- Log docs learnings unprompted. The docs tree is locked — propose, don't improvise.

## 3 · One source of truth: this repo
The org repo is canonical. Edit in a clone: fresh branch → signed commit → PR (peer approval +
green `validate` check; system-layer paths also need the steward). Local copies elsewhere are
read-only mirrors. Git stays human-run.
