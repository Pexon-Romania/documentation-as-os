## What & why

<!-- one or two sentences -->

## Evidence (method changes are evidence-gated — CONTRIBUTING §flow)

<!-- the issue this responds to, or the instance experience it was extracted from -->

## Checklist (CI checks most of these; you hold the rest)

- [ ] `CHANGELOG.md` entry under *Unreleased* — required for any `image/` or `scripts/` change
- [ ] `image/MANIFEST.json` regenerated (`python3 scripts/gen_manifest.py`) for any `image/` change
- [ ] Contract checked: no stable-surface break (`image/INSTANCE-CONTRACT.md`) — or this PR is an agreed MAJOR
- [ ] Gates green locally: `validate_repo.py` · `gen_manifest.py --check` · `smoke_bootstrap.sh`
- [ ] Prompts stay version-free (BOOTSTRAP / UPGRADE)
- [ ] No secrets, absolute local paths, instance internals, or personal content anywhere in the diff
