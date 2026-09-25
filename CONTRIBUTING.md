# Contributing — changing the method itself

(Adopting the OS in your repo? You want [`GETTING-STARTED.md`](GETTING-STARTED.md) — this file
is Mode B: changes to the method. Protocol: [`AGENTS.md`](AGENTS.md) §3.)

## The flow

1. Branch off current `main` (`git pull` first). Read `CHANGELOG.md` (top) + the open issues.
2. Make the change — **evidence-gated**: it cites a real instance's experience (link the issue,
   or name the maintainer-run instance and what happened there). A gate nobody hit doesn't ship.
3. **Check the contract:** [`image/INSTANCE-CONTRACT.md`](image/INSTANCE-CONTRACT.md) decides
   the semver class. Touching the stable surface = a MAJOR conversation with the steward FIRST.
4. **Log + regenerate:** a `CHANGELOG.md` entry under the *Unreleased* heading, and
   `python3 scripts/gen_manifest.py` for any `image/` change. CI fails a PR missing either.
5. **Gates green locally, then PR:**
   `python3 scripts/validate_repo.py && python3 scripts/gen_manifest.py --check && bash scripts/smoke_bootstrap.sh`
   The PR template carries the checklist; review routes per
   [`.github/CODEOWNERS`](.github/CODEOWNERS). **Git is human-run** — sessions prepare branches
   and edits; the human commits (signed), pushes, merges. No AI trailers.

## Semver (what a version means)

- **MAJOR** — breaks the instance contract: a renamed file role, skill, knob, or mode value; a
  changed hook or exit semantic; a removed check family; a moved stamp/lock location.
- **MINOR** — new capability that keeps the contract: a new skill, profile, template, or
  validator check; strengthened prompts.
- **PATCH** — fixes and wording, no capability change.

## Releasing

1. All checks green on `main`; `image/VERSION` bumped; the *Unreleased* CHANGELOG section
   retitled to the version with today's date.
2. **The live bootstrap pass (not CI-able — an agent run):** on a scratch repo, execute the
   `solo` profile prompt end-to-end from this exact tree; verify the report, the stamp, the
   lock, the door, and the installer self-removal. MINOR/MAJOR releases also re-run the `poc`
   prompt (it's two files — cheap). Any failure = fix first; **never tag red.**
3. The human tags `vX.Y.Z` on `main` (signed) and pushes the tag — the release workflow builds
   `image-vX.Y.Z.zip` and attaches it to the GitHub Release.
4. **Edit the Release notes to lead with "Impact on existing instances"** — what an instance on
   the previous version must do (often: nothing; sometimes: run the upgrade prompt; rarely: a
   named migration). Check [`UPGRADING.md`](UPGRADING.md) §pre-versioned is still true.

## Issues — the triage loop (the method's learning inbox)

Labels mirror the templates: `os-bug` · `improvement` · `suggestion` · `adopted` (registration —
add the ADOPTERS row, close; no codification needed), plus two parking labels:
`knowledge-candidate` (belongs in the future shared knowledge product — park, don't lose) and
`runtime-port` (demand for a non-Claude runtime image — park, count).

Triage weekly (the CI cron's Monday run is the reminder): reproduce or verify against an
instance → then either **ADOPT** — codify it (a rule, a template change, a validator check),
add the CHANGELOG entry, close the issue *naming where it got codified* — or **REJECT**,
closing with the honest why. Every adopted finding must point at its codification; "fixed in
spirit" doesn't close issues.

---

*documentation-as-os. Maintained per [`MAINTAINERS.md`](MAINTAINERS.md); the artifact wins.*
