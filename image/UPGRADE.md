# UPGRADE — the prompt that moves an instance between image versions

> Instances customize what the bootstrap installed — that is by design. So an upgrade is never
> "re-copy the image": it is a **three-way diff** between (1) the NEW image's `MANIFEST.json`,
> (2) your instance's `OS-MANIFEST.lock` (what you installed from), and (3) your current files.
> Unchanged-since-install → apply the new template mechanically. Customized → hand-merge,
> guided. The stable surface upgrades protect: [`INSTANCE-CONTRACT.md`](INSTANCE-CONTRACT.md).
> Release notes always open with **"Impact on existing instances"** — read them first.

## How to use

1. Get the **latest Release** of `flaviusmoldovan-pexon/documentation-as-os` (record the tag) and place its
   `image/` beside your repo.
2. Open Claude Code in your instance's repo and paste the prompt. It reports before it writes.

## The prompt

```
You are UPGRADING this repository's documentation-as-os instance to the image version I just
placed at ./image/ (or the path I give you). Work carefully, ASK before anything irreversible,
VERIFY — don't assume.

STEP 0 · Establish the three points.
  (a) CURRENT: read the constitution footer stamp (version · profile · installed date) and
      the lock — docs/OS-MANIFEST.lock (poc/solo) or ./OS-MANIFEST.lock (team).
  (b) NEW: read image/VERSION + image/MANIFEST.json.
  (c) NOTES: read the Release notes between my version and the new one — start with every
      "Impact on existing instances" line. List what applies to THIS instance's profile.
  No stamp or lock found? This is a PRE-VERSIONED instance — switch to the §pre-versioned
  procedure below instead of this one.

STEP 1 · Classify every image file (the three-way diff). For each path in the NEW
  image/MANIFEST.json, compare: new-hash vs lock-hash vs the sha256 of the corresponding
  INSTALLED file in this repo (map template → installed location; a template the profile never
  installs is out of scope). Two file classes upgrade differently:
  - VERBATIM-installed (hooks · skills · system/validator · settings): installed byte-identical
    at bootstrap, so the hash test is meaningful:
      lock == new                     -> unchanged upstream: skip.
      lock != new, installed == lock  -> you never customized it: STAGE the mechanical update.
      lock != new, installed != lock  -> BOTH moved: mark for guided HAND-MERGE.
  - INSTANTIATED (constitution · skeleton/STATUS/doc-debt · team templates): the installed file
    is content-bearing by design (placeholders filled, your state inside) — never overwrite.
    lock != new here means REVIEW THE TEMPLATE DELTA and hand-apply structural additions only
    (a new rule/section), leaving your content untouched.
  - in new manifest, not in lock      -> new capability: stage per the notes (profile-gated).
  Present the full classification table and WAIT for my go before writing anything.

STEP 2 · Apply. Mechanical updates first (re-fill the same placeholders from the live values —
  never regress a filled value to a placeholder). Then hand-merges one file at a time: show the
  upstream delta vs my customization, propose the merged text, ask. Constitution rules: additive
  sections merge in; a changed rule that conflicts with a local locked decision is MINE to
  decide — flag it, don't pick.

STEP 3 · Re-verify the instance. Solo/poc: constitution boots, skeleton intact, skills/hooks
  still executable, os-mode present, no unfilled {{PLACEHOLDER}}. Team: run
  scripts/validate_docs.py — PASS with 0 fails; if the new image changed the validator template,
  re-apply the seven knobs to the new template rather than diffing my old copy line-by-line.

STEP 4 · Re-stamp + re-lock. Append a NEW stamp line to the constitution footer — keep the
  install history, never overwrite — in EXACTLY this format (the census and the next upgrade's
  STEP 0 parse it):
  "<!-- documentation-as-os · image <new version> · profile: <same> · upgraded <today>
  (from <old version>) · upstream: https://github.com/flaviusmoldovan-pexon/documentation-as-os -->".
  Replace the lock with the NEW image/MANIFEST.json. Log one line in the instance CHANGELOG
  ("docs-as-os image upgraded <old> → <new>: <what changed here>").

STEP 5 · Close the loop. Anything that surprised you during this upgrade (a template that
  didn't merge cleanly, a note that didn't match reality) is an [OS] finding — draft the
  upstream issue (improvement template, both versions named) per the constitution's report-back
  section. Then DELETE the image folder used for the upgrade (ask first if inside the repo).

STEP 6 · Report honestly: table of applied / hand-merged / skipped / deferred, what you could
  not verify, and the new stamp line.
```

## §pre-versioned instances (no stamp, no lock)

An instance bootstrapped before versioning existed has nothing to diff against. Procedure:
treat it as a **guided adoption diff**, not an upgrade — inventory what exists and map it to
the image's roles (constitution · STATUS · doc-debt · skills · hooks · system layer), apply
each delta from the notes by hand with the human deciding, then **write the stamp + lock as of
the new version** at the end (STEP 4 above). From then on it upgrades like any versioned
instance. The current pre-versioned org instances are listed in the repo's `ADOPTERS.md`.

---

*Part of documentation-as-os (`image/`). Upgrades are engineered prompts for the same reason
installs are — the magic is the image + the lock, not the sentence. The artifact wins.*
