# INSTANCE-CONTRACT — the surface semver protects

> Every instance of documentation-as-os depends on the names and behaviors below. **A release
> that breaks any of them is a MAJOR version.** A release that adds capability without breaking
> them is a MINOR. Wording, layout, and internals may move in a MINOR — if your instance only
> touches this surface, upgrades are mechanical. (Upgrading: `UPGRADE.md` · versions: `VERSION`
> + the repo's Releases page — release notes always open with "Impact on existing instances.")

## 1 · The stable surface

### File roles (what the OS promises exists, by role)
| Role | Default name | Tier |
|---|---|---|
| Constitution (boot file, read first every session) | `CLAUDE.md` (or `AGENTS.md`) at repo root | all |
| Live current-state | `docs/delivery/STATUS.md` | all |
| Doc-debt register (graceful-enforcement ledger) | `docs/delivery/doc-debt.md` | solo · team |
| Append-only shipped record | `docs/delivery/CHANGELOG.md` | all |
| Decisions (the *why*, append-only) | `docs/delivery/decisions/` + memory | solo · team |
| Router map (≤3 hops entrance) | `README.md` | team |
| Working protocol | `AGENTS.md` | team |
| Delivery line | `delivery/` — `CONVENTIONS` · `WORK_TRACKER` · `CHANGELOG` · `LEARNINGS` | team |
| Environment truth register | `dependencies/ENVIRONMENTS.md` | team |
| Machine index (generated, never hand-edited) | `MANIFEST.json` | team |
| Validator | `scripts/validate_docs.py` | team |

### Enforcement contract (hooks + mode)
- Hook entry points and semantics: **`SessionStart`** (read-in: STATUS head + memory index + open
  doc-debt; resets os-mode to strict) · **`PostToolUse(Edit|Write)`** (docs-part-of-done nudge;
  logs debt when relaxed) · **`Stop`** (won't-close-on-stale-docs: strict → block once,
  relaxed → remind; never loops).
- **`.claude/os-mode`** values: `strict` (default, auto-restored every session) · `relaxed`
  (loud, debt-logged, expires).
- Human gates are permission **`ask:`** rules, not hooks.

### Skills (names + contracts)
`/scope-lock` · `/workstream <name>` · `/handover` · `/reconcile-docs` ·
`/gating <relax|strict|status>` — installed at `.claude/skills/<name>/SKILL.md`.

### Validator contract
- Exit semantics: **0 = PASS (warnings allowed) · 1 = FAIL (= the change is not done)**.
- Modes: bare run (verify) · `--write-manifest` (regenerate the machine index) ·
  `--which-docs <paths>` (which docs own these code paths).
- The **seven knobs** (names are stable): `ALLOWED_ROOT_FILES`/`ALLOWED_DIRS` · `SCOPE_RULES`/
  `ROOT_SCOPE` · `VOCAB` · `REQUIRED_KEYS`/`STALE_DAYS` · `IMPACT_MAP` · `REQUIRED_FILES` ·
  `ID_PREFIXES`.
- Check families (a MINOR may add checks; removing or renaming one is MAJOR): FRONTMATTER ·
  VOCAB · SCOPE · STRUCTURE-LOCK · LINK · ORPHAN · CLOSURE · PLACEHOLDER · STALE · DEAD-END ·
  BOARD↔CHANGELOG · REGISTER-LAG · IMPACT-HINT · SPEC-STATUS · ENV-STATE · MANIFEST-SYNC ·
  REQUIRED-FILE.

### Frontmatter contract (team tier, every doc)
`app` · `audience` · `scope` · `status` · `covers` · `keywords` · `sources` · `related` ·
`last_verified` — with `scope` as the sharing/AI-serving fence and `status` as decision/env truth.

### Bootstrap + upgrade contract
- **Three profiles:** `poc` (constitution-lite + STATUS + CHANGELOG + the door) · `solo`
  (constitution + skeleton + skills + hooks) · `team` (shared repo + system layer + governance).
  Profile graduation never restarts an adoption.
- Every bootstrap writes: the **image-version stamp** (constitution footer, append-only across
  upgrades), the **lock** — `docs/OS-MANIFEST.lock` (poc · solo) or `./OS-MANIFEST.lock` (team
  root) — the sha256 manifest instantiated from, and **the door** (the OS report-back section in
  the constitution; `[OS]` header in LEARNINGS on team). The installer folder is removed after
  verification.
- `image/MANIFEST.json` maps every template file → sha256, per release — the basis of the
  three-way upgrade diff (new manifest vs your lock vs your files).

### Vocabulary (core terms keep their meaning)
constitution · the loop · scope-lock · doc-debt · graceful enforcement · learnings inbox ·
`[VERIFIED]`/`[INFERRED]`/`[NEEDS-CHECK]` · "the code wins" · "code is never evidence for
environment state."

## 2 · Internal (may change in a MINOR)
Template wording and layout · skeleton file *contents* · validator internals (regexes, messages,
implementation) · hook script internals (behavior contract above holds) · prompt phrasing in
BOOTSTRAP/UPGRADE · this repo's own docs structure · the `IMPACT_MAP`/`REQUIRED_FILES` example
values.

## 3 · Version meanings
- **MAJOR** — breaks §1: a renamed role/file/skill/knob/mode value, changed hook or exit
  semantics, a removed check family, a changed stamp/lock location.
- **MINOR** — adds capability (a new skill, profile, check, template) without breaking §1.
- **PATCH** — fixes and wording with no capability change.

---

*Part of documentation-as-os (`image/`). The stable surface is deliberately small: everything an
instance's muscle memory and hooks depend on, and nothing else.*
