---
name: scope-lock
description: Run the front of the delivery loop — turn a request into a signed, buildable scope. Use before building anything non-trivial, and again whenever the request changes mid-flight.
---

# /scope-lock

Turn the request into a **locked scope before any code**.

1. **Treat it as a hypothesis, not a spec.** Restate what you understand is being asked.
2. **Cross-check against reality** — read the relevant code + `STATUS` + memory. Surface contradictions, hidden work, and what is *not* possible right now.
3. **Confirm the open questions** with the human/business; capture their answers verbatim where it matters.
4. **Write the scope** as an ADR (template: `docs/delivery/decisions/0000-adr-template.md`, shipped by the bootstrap) to `docs/delivery/decisions/` or the workstream's folder: **In scope** · **Deferred** · **Out**, each with the *why*. One concern, scannable.
5. **Get explicit sign-off** ("locked?") before building. Nothing substantial is built before this.
6. **Update `STATUS`** with the locked scope + the next step.

Re-run me when the request changes mid-flight — **record the delta, don't absorb it silently:**
- **A change to already-locked scope = a NEW superseding ADR**, not an edit to the old one. Write the next zero-padded `000N-…`, give it an `Amends:` / `Supersedes:` header, and banner the old ADR ("partially amended by 000N") — never rewrite the old one (append-only history, §7).
- **Changing a persisted shape, a stored format, or a public contract? Decide and RECORD the backward-compat / migration strategy** (default-at-read vs migrate-on-write, etc.) — never silently rewrite a user's data (§2).
- **Unlocking a §8 locked decision happens *loudly*:** update §8 with a pointer to the superseding ADR — never silently.
