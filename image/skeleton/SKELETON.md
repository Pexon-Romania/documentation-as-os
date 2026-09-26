# The doc skeleton — what the OS scaffolds

> The minimum **living doc-set** the bootstrap creates in a fresh repo, or **builds from the code** in an existing one. Filed by audience (the buckets); each consumer reads only its bucket. Start minimal — the loop grows the rest (don't front-load).

---

## The tree

```
CLAUDE.md                       ← the constitution (from ../CONSTITUTION.template.md)
docs/
  product/        (shareable · a user-facing AI reads ONLY this)
    overview.md · how-it-works.md · areas-map.md · known-limitations.md · faq.md · releases.md · bugs.md
    support/      (the support-pack — onboarding lives here)
      runbook.md · escalation.md · faq.md · admin-how-to.md
  engineering/    (internal)
    architecture.md · data-model.md · deployment.md · dependencies.md · tech-debt.md
  delivery/       (internal)
    STATUS.md           ← live current-state (ALWAYS) — from ./STATUS.template.md
    CHANGELOG.md        ← append-only · what shipped
    decisions/          ← ADRs — the *why*
    doc-debt.md         ← open doc-debt register (from ./doc-debt.template.md)
memory/
  MEMORY.md          ← small project-scoped experience index (from ./MEMORY.template.md)
```

## Per-file role + how the bootstrap fills it

| File | Role | Fresh repo | Existing repo |
|---|---|---|---|
| `overview` | what it is & does | stub with prompts | written from README + code |
| `how-it-works` | the end-to-end journey | stub | written from the running flows |
| **`areas-map`** | components → where they live (**highest-leverage routing doc**) | stub | **built from the code's module map** |
| `known-limitations` | caveats (open items only) | empty register | mined from TODOs / issues / gaps |
| `architecture` | how it's built | stub | written from the code |
| `STATUS` | where we are · next · blocked · doc-debt | seeded "Phase 0" | seeded from current reality |
| `CHANGELOG` | shipped, append-only | empty | optionally seeded from git history |
| `decisions/` | ADRs (the why) | `0000-adr-template.md` (from `./adr.template.md`) | + seed the obvious past decisions |
| `memory/MEMORY.md` | outcomes, failed paths, corrections + pointers to canonical truth | empty hot index + entry contract | seed only verified, reusable experience — never copy docs |
| `support/*` | onboarding pack | stubs with `[FILL IN]` (owner · SLAs · contacts) | same |
| `doc-debt` | skipped updates to reconcile | empty | empty |

## Rules the skeleton obeys

- **Minimum for the stage — THIS RULE WINS over the tree above** — create only what the project needs now; the loop adds the rest. Optional subsets: the **support-pack** when a support audience exists; the **registers** (known-limitations · bugs · releases · faq) on their first real entry. A tiny project starts with overview · areas-map · the delivery trio · `memory/MEMORY.md`.
- **Routing:** a user-facing AI is pointed at `docs/product/` only — never engineering, delivery, or the constitution.
- **Registers carry open items only** — `known-limitations`, `bugs`, `doc-debt`: resolved items are removed.
- **`doc-debt.md`** is the graceful-enforcement ledger — skipped doc updates land here, the
  `SessionStart` hook surfaces them, and the `reconcile-docs` skill clears them.
- **Board = index, docs = records** — `STATUS` and registers stay scannable; heavy detail lives in the linked docs they point to.
- **Memory = experience + pointers, not duplicated truth** — current work stays in STATUS,
  decisions in ADRs, environment facts in the environment register, and repeatable methods in
  skills. Runtime-native memory may cache this context, but never replaces the Git-tracked file.
- **Never written anywhere here:** credentials, hostnames, PII, the internal way-of-working.

---

*Part of documentation-as-os (`image/skeleton/`). The bootstrap (`../BOOTSTRAP.md`) instantiates this. Proprietary material owned by **Pexon Romania and Flavius Moldovan**.*
