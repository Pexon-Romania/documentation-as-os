---
app: {{APP}}
audience: [engineers, ops]
scope: internal
status: live-prod
covers: The docs-system learning log — issues, friction, and proposals any agent or dev appends WITHOUT being asked; the steward reviews and adopts/rejects.
keywords: [learnings, improvements, proposals, friction, self-improvement, inbox]
sources: []
related: [README.md, CONVENTIONS.md]
last_verified: {{TODAY}}
---

# Learnings — the system's own inbox

Append-only log of learnings **about this documentation system**. **Any agent or dev appends here
without asking** — it is a standing instruction in the protocol. The steward reviews **monthly, by
CLASS not by entry** (three entries from one root = the system pointing at a structural fix);
adopted items get codified (a rule, a validator check, a retired mechanism) and the entry is
flipped. Structure additions the locked tree forbids are *proposed* here first.

**Not for:** product bugs (→ the board) or factual drift you can fix on the spot (fix it — the
code wins — and re-stamp).

**The `[OS]` tag — findings that belong upstream.** The test is mechanical, not judgment: *is
the problem in a file the bootstrap installed, or a rule the constitution/protocol carries?*
If yes, it is OS-level — prefix the entry `[OS]`, and the agent DRAFTS the upstream issue in
the same beat (prefill `https://github.com/flaviusmoldovan-pexon/documentation-as-os/issues/new` with the
matching template — os-bug | improvement | suggestion — plus the image version + profile from
the boot-file footer stamp and the finding); the human clicks and files. `/handover` and the
stop-gate surface `[OS]` entries not yet filed. Local-instance learnings stay untagged and are
triaged here as usual.

## Entry format
```
### YYYY-MM-DD · <who: session/agent/dev> · <type: DOCS-BUG | GAP | FRICTION | PROPOSAL>
**Finding:** what you hit, concretely — with the discovery command where relevant.
**Suggestion:** the smallest durable fix.
**Status:** OPEN   ← steward flips to ADOPTED (say where codified) or REJECTED (say why)
```

---

## Log (newest first)
