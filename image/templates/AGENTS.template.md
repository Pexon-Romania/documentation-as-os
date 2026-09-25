# {{APP}} — the working protocol (AGENTS.md)

> The non-negotiables every agent and dev works by. The boot file points here; this file is the law.

## 1 · Start every session
1. This file. 2. `README.md` — route to your line. 3. The board — where we are, what's next.
4. Freshness: pull the docs repo (and refresh any read-only mirrors) before trusting state.
5. **Reconcile, don't just read:** a forward-looking line ("do X next", "restart to activate") —
   check whether it already happened and fix it on the spot; a `last_verified` date doesn't make
   a future-tense claim true.

## 2 · Verify before you act — the five instrumentation rules
1. **Two instruments** — a "does X exist / require Y" conclusion needs two independent
   instruments, or one instrument + empirical confirmation. One endpoint/grep is a hypothesis.
2. **No absence from truncated output** — never conclude absence from output that passed through
   `head`/`limit`/filters; count first.
3. **Attribute every finding** to its source object (file:line, id, PR#) — unattributed = unverified.
4. **State the discovery command** with the claim, so its blind spots are visible.
5. **Lived knowledge is a test** — a human's contradicting experience means your instrument is
   incomplete until proven otherwise.

## 3 · "Done" = code + docs in sync
Before writing: `validate_docs.py --which-docs <paths>` names the docs you owe. Before stopping:
run the full validator — **FAIL = not done.** Ship = beat 1; promote = beat 2 (CONVENTIONS).
**Code is never evidence for environment state:** what an environment *contains* (rows, config,
whether a table is populated) is never sourced from the repo — state it only with the environment,
the check, and the date named, else `[NEEDS-CHECK]`. *Absence of a seed is not absence of data*
(the validator's ENV-STATE warn holds this line; only a human at the environment closes it).

## 4 · The standing duties
- **Log learnings unprompted** → the LEARNINGS inbox.
- **The tree is locked** — propose additions in LEARNINGS; never improvise structure.
- **The code is the source of truth** for behavior — a disagreeing doc is the bug; fix + re-stamp.
- **Docs edits happen in a clone, branch → signed commit → PR** — main is ruleset-protected;
  agents may prepare branches and edits after in-chat approval; **git stays human-run.**

## 5 · Forbidden
Force-push to shared branches · secrets/credentials/hostnames in any doc · editing a read-only
mirror · concluding from a single instrument · closing a session with a failing validator.
