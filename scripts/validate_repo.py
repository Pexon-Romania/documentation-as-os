#!/usr/bin/env python3
"""
validate_repo.py — the documentation-as-os REPO's own validator (this is the product repo's
gate, not the instance validator — that one is image/system/validate_docs.template.py).

Checks (FAIL = the change is not done; CI runs this on every push/PR + weekly):
  TREE          the locked root — required files present, nothing unexpected at root
  LINKS         every relative markdown link in root docs + image/ resolves
  TEMPLATE-LINT {{PLACEHOLDER}} tokens only inside image/ · no absolute local paths anywhere
  TRUTH-CHECK   every image/<path> named by the consumer-facing docs exists ·
                no version pins inside the bootstrap/upgrade prompts (version-truth = Releases)
  VERSION       image/VERSION has a matching CHANGELOG heading
  (MANIFEST-FRESH runs separately: scripts/gen_manifest.py --check)

Exit 0 = PASS (warnings allowed) · 1 = FAIL.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails, warns = [], []

REQUIRED_ROOT = ["README.md", "CLAUDE.md", "AGENTS.md", "METHOD.md", "GETTING-STARTED.md",
                 "UPGRADING.md", "CONTRIBUTING.md", "MAINTAINERS.md", "ADOPTERS.md",
                 "CHANGELOG.md", "SECURITY.md", "WALKTHROUGH.md"]
ALLOWED_ROOT_EXTRA = {".gitignore", "LICENSE"}
REQUIRED_DIRS = ["image", "scripts", ".github"]
CONSUMER_DOCS = ["README.md", "GETTING-STARTED.md", "UPGRADING.md", "CONTRIBUTING.md",
                 "image/BOOTSTRAP.md", "image/UPGRADE.md"]
PROMPT_FILES = ["image/BOOTSTRAP.md", "image/UPGRADE.md"]  # version pins banned here

rel = lambda p: os.path.relpath(p, ROOT).replace(os.sep, "/")

# ── TREE: no build/OS droppings anywhere in the shipped image ──
for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "image")):
    for d in list(dirnames):
        if d == "__pycache__":
            fails.append(f"TREE: '{rel(os.path.join(dirpath, d))}/' — build artifacts never ship in the image")
    for fn in filenames:
        if fn.endswith((".pyc", ".pyo")) or fn == ".DS_Store":
            fails.append(f"TREE: '{rel(os.path.join(dirpath, fn))}' — build/OS droppings never ship in the image")

# ── TREE ──
for f in REQUIRED_ROOT:
    if not os.path.isfile(os.path.join(ROOT, f)):
        fails.append(f"TREE: required root file '{f}' is missing")
for d in REQUIRED_DIRS:
    if not os.path.isdir(os.path.join(ROOT, d)):
        fails.append(f"TREE: required directory '{d}/' is missing")
for entry in sorted(os.listdir(ROOT)):
    if entry.startswith(".") and entry not in ALLOWED_ROOT_EXTRA and entry not in (".github", ".git"):
        if entry not in (".git",):
            warns.append(f"TREE: unexpected dotfile at root: '{entry}'")
        continue
    p = os.path.join(ROOT, entry)
    if os.path.isfile(p) and entry not in REQUIRED_ROOT and entry not in ALLOWED_ROOT_EXTRA:
        fails.append(f"TREE: unexpected root file '{entry}' — the root is locked (see CLAUDE.md); additions need the steward's approval FIRST")
    if os.path.isdir(p) and not entry.startswith(".") and entry not in REQUIRED_DIRS:
        fails.append(f"TREE: unexpected root directory '{entry}/' — instances and extras never live in this repo")

# ── collect md files (root + image/; .github templates excluded — different syntax) ──
md = []
for base in [ROOT, os.path.join(ROOT, "image")]:
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "scripts"]
        if base == ROOT and dirpath != ROOT:
            if not rel(dirpath).startswith("image"):
                continue
        for fn in filenames:
            if fn.endswith(".md"):
                md.append(os.path.join(dirpath, fn))
md = sorted(set(md))

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}")
ABS_PATH = re.compile(r"/Users/|/home/[a-z]|[A-Z]:\\\\")
PIN = re.compile(r"\bv?\d+\.\d+\.\d+\b")

for p in md:
    r = rel(p)
    t = open(p, encoding="utf-8").read()
    # LINKS — relative targets must exist (skip URLs, mailto, anchors, placeholder links).
    # Targets that resolve OUTSIDE the repo are the GitHub-web-relative convention
    # (../../releases, ../../issues/…) — they exist on github.com, not on disk: skip.
    for m in LINK.finditer(t):
        tg = m.group(1).strip().split("#")[0]
        if not tg or tg.startswith(("http", "mailto")) or "{{" in tg:
            continue
        full = os.path.normpath(os.path.join(os.path.dirname(p), tg))
        if not (full == ROOT or full.startswith(ROOT + os.sep)):
            continue
        if not os.path.exists(full):
            fails.append(f"LINKS: {r} -> {tg} (missing)")
    # TEMPLATE-LINT
    if not r.startswith("image/") and PLACEHOLDER.search(t):
        fails.append(f"TEMPLATE-LINT: {r} contains a {{{{PLACEHOLDER}}}} token — placeholders live only inside image/")
    for i, line in enumerate(t.splitlines(), 1):
        if ABS_PATH.search(line):
            fails.append(f"TEMPLATE-LINT: {r}:{i} contains an absolute local path — repo content must be machine-independent")
    # TRUTH-CHECK: version pins in prompts
    if r in PROMPT_FILES:
        for i, line in enumerate(t.splitlines(), 1):
            if PIN.search(line):
                fails.append(f"TRUTH-CHECK: {r}:{i} pins a version ('{PIN.search(line).group(0)}') — prompts say 'latest Release; record the tag'")

# ── TRUTH-CHECK: image/<path> references in consumer docs must exist ──
REF = re.compile(r"(?<![\w/])image/[A-Za-z0-9_./-]+")
for doc in CONSUMER_DOCS:
    p = os.path.join(ROOT, doc)
    if not os.path.isfile(p):
        continue  # TREE already failed it
    t = open(p, encoding="utf-8").read()
    base = os.path.dirname(p) if doc.startswith("image/") else ROOT
    for m in sorted(set(REF.findall(t))):
        tgt = m.rstrip(".,:;)")
        cand = os.path.join(ROOT, tgt)
        if tgt.endswith("/"):
            ok = os.path.isdir(cand)
        else:
            ok = os.path.exists(cand) or os.path.isdir(cand) or any(
                os.path.exists(os.path.join(ROOT, tgt + ext)) for ext in ("", "/"))
        # image-internal docs refer to siblings without the image/ prefix; this check covers
        # the fully-qualified references, which is what consumers copy-paste.
        if not ok and "*" not in tgt and "<" not in tgt:
            fails.append(f"TRUTH-CHECK: {doc} references '{tgt}' which does not exist")

# ── VERSION ↔ CHANGELOG ──
vp = os.path.join(ROOT, "image", "VERSION")
if os.path.isfile(vp):
    v = open(vp, encoding="utf-8").read().strip()
    cl = open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read() if os.path.isfile(os.path.join(ROOT, "CHANGELOG.md")) else ""
    if not re.search(rf"^##\s+v{re.escape(v)}\b", cl, re.M):
        fails.append(f"VERSION: image/VERSION is {v} but CHANGELOG.md has no '## v{v}' heading — one version, one record")
else:
    fails.append("VERSION: image/VERSION is missing")

# ── report ──
dedup = lambda xs: list(dict.fromkeys(xs))
fails, warns = dedup(fails), dedup(warns)
print(f"=== validate_repo — {len(md)} md files ===")
for f in fails: print("  FAIL:", f)
for w in warns: print("  warn:", w)
print(f"result: {'FAIL' if fails else 'PASS'} ({len(fails)} fail, {len(warns)} warn)")
sys.exit(1 if fails else 0)
