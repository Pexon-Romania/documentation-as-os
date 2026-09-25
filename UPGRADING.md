# Upgrading — how instances move between image versions

Instances **customize what the bootstrap installs — by design**: your constitution carries your
locked decisions, your knobs are set to your tree. So an upgrade is never "re-copy the image."
It is a **guided three-way diff** between the new image's manifest, your instance's
`OS-MANIFEST.lock` (what you installed from), and your current files — mechanical where you
never customized, hand-merged where you did, human-decided where a new rule meets a local
locked decision.

## The stable surface vs internals

**Stable (semver-protected):** the file roles, hook entry points + `os-mode` semantics, skill
names, validator knobs + check families, frontmatter fields, bootstrap placeholders, and stamp/
lock locations — the full list is [`image/INSTANCE-CONTRACT.md`](image/INSTANCE-CONTRACT.md).
If your instance only depends on that surface (it should — see AGENTS §2.3), upgrades are
mechanical or close to it.

**Internal (may move in a MINOR):** template wording, skeleton layout details, validator
internals, prompt phrasing, this repo's docs structure.

## Standard upgrade procedure

1. Read the Release notes since your version — every release opens with **"Impact on existing
   instances"**; list what applies to your profile.
2. Download the new Release's image and place `image/` beside your repo.
3. Paste the prompt in [`image/UPGRADE.md`](image/UPGRADE.md) into a session in your repo. It
   classifies every file (unchanged / mechanical update / hand-merge / new capability),
   **shows you the table before writing anything**, applies on your go, re-runs your
   validator, re-stamps the constitution footer (append — the stamp keeps your upgrade
   history), replaces the lock, and logs one line in your instance CHANGELOG.
4. Anything that surprised you during the upgrade is an **[improvement]** issue here — both
   versions named. The upgrade prompt reminds you.

## Coming from a pre-versioned instance (installed before releases existed)

Instances bootstrapped before versioning carry **no stamp and no lock** — there is nothing to
diff against. Treat the move as a **guided adoption diff**, not an upgrade:
[`image/UPGRADE.md`](image/UPGRADE.md) §pre-versioned walks it — inventory what exists, map it
to the image's roles, apply the deltas by hand with the human deciding, then **write the stamp
+ lock as of the new version**. From then on it upgrades like any versioned instance.

Known deltas for all pre-versioned instances (see [`ADOPTERS.md`](ADOPTERS.md) for the list):
no footer stamp or `OS-MANIFEST.lock` · a validator predating the ENV-STATE / MANIFEST-SYNC /
SPEC-STATUS checks and the `ID_PREFIXES` knob · a constitution predating the
environment-state rule and the OS report-back section · no `[OS]` header in LEARNINGS.

## The one rule that keeps upgrades cheap

**Don't patch OS internals in your copy** (hooks, skills, validator machinery). A local patch
turns the next upgrade's mechanical file into a hand-merge forever — bring the change here as
an issue or PR instead; that's how it stops being your fork and starts being everyone's fix.

---

*documentation-as-os. Version-truth lives in Releases; your version lives in your stamp.*
