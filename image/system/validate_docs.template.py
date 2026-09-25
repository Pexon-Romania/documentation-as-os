#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATE — derived VERBATIM from the live validator of the production exemplar
# (an org docs repo it has gated since 2026-07: every-push CI + weekly cron;
# FAIL = unmergeable). Snapshot: 2026-09-16. Adapt SEVEN knobs, delete this
# header block, and it runs on your corpus:
#
#   1. ALLOWED_ROOT_FILES / ALLOWED_DIRS  → your locked tree (the structure lock)
#   2. SCOPE_RULES / ROOT_SCOPE           → which folders are shareable vs internal
#   3. VOCAB["audience"]                  → your audience names
#   4. REQUIRED_KEYS / STALE_DAYS         → usually keep as-is
#   5. IMPACT_MAP                         → YOUR topic→owning-doc pairs (drift hints);
#                                           starts empty — grow it from real drift
#   6. REQUIRED_FILES                     → your system-layer file list
#   7. ID_PREFIXES                        → your CONVENTIONS item-id prefix(es);
#                                           empty = the id-driven checks are skipped
#
# Keep the checks you don't understand yet — each exists because of a logged
# failure (placeholders shipped in a PR; Windows path breakage; a manifest that
# silently didn't sync; an environment claim that stood false for two months).
# The learnings log of the source system explains each.
# ═══════════════════════════════════════════════════════════════════════════════
"""
validate_docs.py — the docs-hub validator.

Verifies the documentation set stays CLOSED, CONSISTENT, and CURRENT. It never
authors content — it detects and reports; the builder reconciles (per the docs
standard). And it checks STRUCTURE and CONSISTENCY, not truth: a confidently-worded
false claim can pass every check (the ENV-STATE warn narrows that gap; only a human
looking at the environment closes it — docs standard §6).

Run from anywhere:            python3 scripts/validate_docs.py
Refresh the agent manifest:   python3 scripts/validate_docs.py --write-manifest

Exit code 0 = PASS (warnings allowed) · 1 = FAIL (contract violations).

FAIL on:  missing/invalid frontmatter · broken links (inline + related:) ·
          scope violations (folder rules) · structure-lock violations (files/folders
          outside the approved tree — additions need the steward's approval FIRST) ·
          orphan docs (unreachable from README.md) · unresolved placeholders (#<PR> etc.) ·
          stale MANIFEST.json (machine index out of sync with frontmatter — run
          --write-manifest; LEARNINGS 2026-08-17).
WARN on:  external `docs/…` mentions not marked `(repo)` · stale docs (>90 days) ·
          board↔changelog id inconsistencies · register lag (ENVIRONMENTS / WORK_TRACKER
          older than the newest changelog entry) · topic-impact hints (a dated changelog
          entry touches a topic whose owning doc was last verified before that date) ·
          spec-status ↔ changelog drift (a spec whose id sits in the Shipped titles but
          whose status isn't live-prod; LEARNINGS 2026-08-17) ·
          environment-state phrasing in a code-sourced doc without environment+date evidence
          (code can't observe data — docs standard §6; LEARNINGS 2026-09-09) ·
          docs with no outgoing links (dead ends).
"""
import os, re, sys, json, datetime
try:  # Windows cp1252 consoles choke on '→' in warnings (LEARNINGS 2026-07-23)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── The locked architecture (additions outside this tree: check with the steward FIRST) ──
BOOT_FILES = {"CLAUDE.md"}  # the installed root boot file — a CONSUMER of the docs, not a doc (exempt from the md contract)
ALLOWED_ROOT_FILES = {"README.md", "AGENTS.md", "DOCS-STANDARD.md", "DOCS-SYSTEM.md", "MANIFEST.json",
                      "BOOTSTRAP.md",  # the seed — present only until installed
                      "OS-MANIFEST.lock"} | BOOT_FILES  # the image lock the bootstrap writes (upgrade diffing)
ALLOWED_DIRS = {"app-documentation", "dependencies", "support", "leaders",
                "delivery", "delivery/incidents", "delivery/specs", "scripts"}
SCOPE_RULES = {  # folder → required scope (None = per-file exceptions below)
    "app-documentation": "shareable", "support": "shareable", "leaders": "shareable",
    "dependencies": "internal", "delivery": "internal",
}
ROOT_SCOPE = {"README.md": "shareable", "DOCS-SYSTEM.md": "shareable", "BOOTSTRAP.md": "shareable",
              "AGENTS.md": "internal", "DOCS-STANDARD.md": "internal"}
VOCAB = {"scope": {"shareable", "internal"},
         "status": {"live-prod", "dev-only", "flagged-off", "planned", "deprecated"},
         "audience": {"all", "leaders", "support", "engineers", "ops"}}
REQUIRED_KEYS = ["app", "audience", "scope", "status", "covers", "keywords",
                 "sources", "related", "last_verified"]
STALE_DAYS = 90
# topic keywords → the doc that owns them (drift hints, changelog → reference docs).
# Starts EMPTY — grow it from real drift. Shape (examples):
#   (r"\bmigration\b|\bschema\b",   ["<your data-model doc>", "<your environments register>"]),
#   (r"\bSSO\b|\bauth\b|\brole\b",  ["<your auth doc>"]),
IMPACT_MAP = []
# your item-id prefix(es) from CONVENTIONS, e.g. ("PL",) or ("MYB", "PL").
# Empty = the board↔changelog and spec-status checks are skipped until you set it.
ID_PREFIXES = ()
_ID = "(?:%s)-\\d+" % "|".join(map(re.escape, ID_PREFIXES)) if ID_PREFIXES else None

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
fails, warns = [], []

def rel(p): return os.path.relpath(p, HUB).replace(os.sep, "/")  # posix paths everywhere — Windows backslashes broke the structure lock (LEARNINGS 2026-07-23)

def parse_fm(text):
    if not text.startswith("---\n"): return None
    end = text.find("\n---", 4)
    if end < 0: return None
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            k, v = line.split(":", 1); fm[k.strip()] = v.strip()
    return fm

def listify(v):
    return [x.strip().strip("\"'") for x in v.strip("[]").split(",") if x.strip()] if v else []

# ── --which-docs: "I changed these code paths — which docs own them?" ──
if "--which-docs" in sys.argv:
    args = sys.argv[sys.argv.index("--which-docs") + 1:]
    if not args:
        print("usage: validate_docs.py --which-docs <changed-path> [...]"); sys.exit(2)
    src_map = []
    for dirpath, dirnames, filenames in os.walk(HUB):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if not fn.endswith(".md"): continue
            fm = parse_fm(open(os.path.join(dirpath, fn), encoding="utf-8").read()) or {}
            for s in listify(fm.get("sources", "")):
                src_map.append((rel(os.path.join(dirpath, fn)), s))
    def expand(s):  # path shorthands your sources: use — adapt or delete (see your docs standard §2)
        c = [s]
        # example: if s.startswith(("app/", "main.py")): c.append("<service-root>/" + s)
        return c
    for p in [a.lstrip("./") for a in args]:
        hits = sorted({doc for doc, s in src_map for c in expand(s)
                       if p == c or p.startswith(c.rstrip("/") + "/") or c.startswith(p.rstrip("/") + "/")})
        print(f"\n{p}")
        for h in hits: print(f"  → update/confirm: {h}")
        if not hits:
            print("  → no doc declares this path — check the change→docs map (your docs standard);")
            print("    a genuinely new area may need a new doc: ask the steward FIRST.")
        print("  → always: delivery/CHANGELOG.md (+ the WORK_TRACKER stage) · promoted to prod? dependencies/ENVIRONMENTS.md too")
    sys.exit(0)

# ── collect files ──
md_files, structure_violations = [], []
for dirpath, dirnames, filenames in os.walk(HUB):
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]
    d = rel(dirpath)
    for fn in filenames:
        if fn.startswith("."): continue
        p = os.path.join(dirpath, fn); r = rel(p)
        if d == ".":
            if fn not in ALLOWED_ROOT_FILES and fn != os.path.basename(__file__):
                structure_violations.append(r)
        elif d == "scripts":
            if not fn.endswith((".py", ".md", ".sh")): structure_violations.append(r)
        elif d not in ALLOWED_DIRS:
            structure_violations.append(r)
        if fn.endswith(".md") and not (d == "." and fn in BOOT_FILES): md_files.append(p)
for v in structure_violations:
    fails.append(f"STRUCTURE-LOCK: '{v}' is outside the approved architecture — new files/folders need the steward's approval FIRST (see the docs standard)")

# ── per-file checks ──
today = datetime.date.today()
meta, outgoing = {}, {}

# environment-state phrasing a repo can never evidence (docs standard §6; LEARNINGS 2026-09-09 —
# "ships empty" stood for ~2 months because the repo agreed and nobody looked at an environment)
ENV_STATE = re.compile(
    r"ship(s|ped)? empty|\b(is|are|remains?|stays?) dormant\b|\bempty (in practice|today)\b"
    r"|\bno (rules?|rows?|records?|data) (are |is )?(configured|seeded|present|exists?)\b"
    r"|\b(zero|0) (rows?|rules?|records?)\b", re.I)
ENV_EVIDENCE = re.compile(r"20\d\d-\d\d-\d\d|\[NEEDS-CHECK\]|admin panel|verif|quer(y|ied)", re.I)

for p in md_files:
    r = rel(p); t = open(p, encoding="utf-8").read()
    fm = parse_fm(t)
    if fm is None:
        fails.append(f"FRONTMATTER: {r} has none"); continue
    meta[r] = fm
    for k in REQUIRED_KEYS:
        if k not in fm: fails.append(f"FRONTMATTER: {r} missing '{k}'")
    if fm.get("scope") not in VOCAB["scope"]:
        fails.append(f"VOCAB: {r} scope='{fm.get('scope')}'")
    if fm.get("status") not in VOCAB["status"]:
        fails.append(f"VOCAB: {r} status='{fm.get('status')}'")
    for a in listify(fm.get("audience", "")):
        if a not in VOCAB["audience"]: fails.append(f"VOCAB: {r} audience '{a}'")
    # scope rules
    top = r.split("/")[0]
    want = ROOT_SCOPE.get(r) if "/" not in r else SCOPE_RULES.get(top)
    if want and fm.get("scope") != want:
        fails.append(f"SCOPE: {r} must be '{want}' (folder rule), is '{fm.get('scope')}'")
    # freshness
    try:
        lv = datetime.date.fromisoformat(fm.get("last_verified", ""))
        if (today - lv).days > STALE_DAYS:
            warns.append(f"STALE: {r} last verified {lv} (> {STALE_DAYS}d)")
    except ValueError:
        fails.append(f"FRONTMATTER: {r} bad last_verified '{fm.get('last_verified')}'")
    # links (inline + related)
    d = os.path.dirname(p); outs = set()
    targets = [m.group(1) for m in LINK.finditer(t)] + listify(fm.get("related", ""))
    for tg in targets:
        tg = tg.strip().split("#")[0]
        if not tg or tg.startswith(("http", "mailto")): continue
        full = os.path.normpath(os.path.join(d, tg))
        if not os.path.exists(full):
            fails.append(f"LINK: {r} -> {tg} (missing)")
        elif full.endswith(".md"):
            outs.add(rel(full))
    outgoing[r] = outs
    # closure: external docs/ mentions must carry the (repo) marker on the line
    for i, line in enumerate(t.splitlines(), 1):
        if re.search(r"(?<![\w-])docs/\S+\.(md|sql|py|txt|json)\b|(?<![\w-])docs/[A-Za-z0-9_-]+/", line) and "(repo)" not in line:
            warns.append(f"CLOSURE: {r}:{i} references external 'docs/…' without a '(repo)' marker")
    if not outs:
        warns.append(f"DEAD-END: {r} has no outgoing in-hub links")
    # placeholders: unresolved tokens must never ship (LEARNINGS 2026-08-03 — '#<PR>' reached a PR)
    if r not in ("DOCS-STANDARD.md", "delivery/LEARNINGS.md"):  # these quote placeholder patterns by design
        for i, line in enumerate(t.splitlines(), 1):
            if re.search(r"#<PR>|<PR#?>|\[NEEDS-PR\]", line):
                fails.append(f"PLACEHOLDER: {r}:{i} unresolved token — fill the real value before merge")
    # env-state claims: sources: admits only code paths, and code cannot observe environment
    # data — such claims need environment + check + date nearby, or [NEEDS-CHECK] (docs standard §6)
    if listify(fm.get("sources", "")) and r not in ("DOCS-STANDARD.md", "delivery/LEARNINGS.md"):
        _ls = t.splitlines()
        for i, line in enumerate(_ls, 1):
            m = ENV_STATE.search(line)
            if m and not ENV_EVIDENCE.search(" ".join(_ls[max(0, i - 2):i + 1])):
                warns.append(f"ENV-STATE: {r}:{i} '{m.group(0)}' reads as an environment-state claim "
                             f"in a code-sourced doc — name the environment + the check + the date, "
                             f"or tag [NEEDS-CHECK] (docs standard §6)")

# ── reachability from the map ──
seen, queue = {"README.md"}, ["README.md"]
while queue:
    for nxt in outgoing.get(queue.pop(), set()):
        if nxt not in seen: seen.add(nxt); queue.append(nxt)
for r in sorted(set(map(rel, md_files)) - seen):
    fails.append(f"ORPHAN: {r} unreachable from README.md")

# ── cross-folder consistency (delivery ↔ registers ↔ reference docs) ──
def read(rp):
    p = os.path.join(HUB, rp)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""
cl, wt = read("delivery/CHANGELOG.md"), read("delivery/WORK_TRACKER.md")
if cl and wt and _ID:
    shipped = set()  # only ids named in a shipped entry's bold TITLE (mentions in bodies are context)
    for title in re.findall(r"^- \*\*(.+?)\*\*", cl.split("## Shipped to prod", 1)[-1], re.M):
        shipped |= set(re.findall(r"\b(%s)\b" % _ID, title))
    active_rows = set(re.findall(r"^\|\s*(%s)\s*\|" % _ID, wt, re.M))
    for i_ in sorted(shipped & active_rows, key=lambda x: (x.rsplit("-", 1)[0], int(x.rsplit("-", 1)[1]))):
        row = re.search(rf"^\|\s*{re.escape(i_)}\s*\|.*$", wt, re.M).group(0)
        if not re.search(r"SHIPPED|PROD #|prod #", row):
            warns.append(f"BOARD↔CHANGELOG: {i_} appears shipped in CHANGELOG but its Active row shows no shipped stage")
    dates = re.findall(r"^### (\d{4}-\d{2}-\d{2})", cl, re.M)
    if dates:
        newest = max(dates)
        for reg in ("dependencies/ENVIRONMENTS.md", "delivery/WORK_TRACKER.md"):
            lv = meta.get(reg, {}).get("last_verified", "1970-01-01")
            if lv < newest:
                warns.append(f"REGISTER-LAG: {reg} (verified {lv}) is older than the newest changelog entry ({newest})")
        # topic-impact hints: newest-dated entries vs owning docs
        for block in re.split(r"^### ", cl, flags=re.M)[1:]:
            bdate = block[:10]
            if not re.match(r"\d{4}-\d{2}-\d{2}", bdate): continue
            for pat, docs_ in IMPACT_MAP:
                if re.search(pat, block, re.I):
                    for dd in docs_:
                        lv = meta.get(dd, {}).get("last_verified", "1970-01-01")
                        if lv < bdate:
                            warns.append(f"IMPACT-HINT: changelog {bdate} touches /{pat}/ → confirm '{dd}' (verified {lv}) still true, then re-stamp")

# ── spec-status ↔ changelog (one status vocabulary — LEARNINGS 2026-08-17) ──
if cl and _ID:
    def _section(text, start, end=None):
        i = text.find(start)
        if i < 0: return ""
        if end:
            j = text.find(end, i)
            if j >= 0: return text[i:j]
        return text[i:]
    _shipped_t = " ".join(re.findall(r"^\s*- \*\*(.+?)\*\*", _section(cl, "## Shipped to prod"), re.M))
    _ondev_t = " ".join(re.findall(r"^\s*- \*\*(.+?)\*\*", _section(cl, "## On dev", "## Shipped to prod"), re.M))
    _shipped_ids = set(re.findall(r"\b(%s)\b" % _ID, _shipped_t))
    _ondev_ids = set(re.findall(r"\b(%s)\b" % _ID, _ondev_t))
    for r in sorted(meta):
        if not r.startswith("delivery/specs/") or r.endswith("README.md"): continue
        _ids = set(re.findall(r"\b(%s)\b" % _ID, read(r)[:2000]))
        _st = meta[r].get("status")
        if _ids & _shipped_ids and _st not in ("live-prod", "deprecated"):
            warns.append(f"SPEC-STATUS: {r} status='{_st}' but {sorted(_ids & _shipped_ids)} appear in the changelog's Shipped titles — flip to live-prod (one status vocabulary)")
        elif _st == "live-prod" and _ids & _ondev_ids and not (_ids & _shipped_ids):
            warns.append(f"SPEC-STATUS: {r} status='live-prod' but {sorted(_ids & _ondev_ids)} appear only in the changelog's On-dev titles")

# ── manifest for MCP / AI agents ──
def build_manifest_files():
    files = {}
    for r in sorted(meta):
        fm = meta[r]
        files[r] = {"audience": listify(fm.get("audience", "")), "scope": fm.get("scope"),
                    "status": fm.get("status"), "covers": fm.get("covers", ""),
                    "keywords": listify(fm.get("keywords", "")), "sources": listify(fm.get("sources", "")),
                    "last_verified": fm.get("last_verified")}
    return files

if "--write-manifest" in sys.argv:
    man = {"_generated": f"by scripts/validate_docs.py on {today.isoformat()} — do NOT hand-edit; regenerate with --write-manifest",
           "_router": "README.md", "_system": "DOCS-SYSTEM.md",
           "_current_state": ["delivery/WORK_TRACKER.md", "dependencies/ENVIRONMENTS.md"],
           "_history": ["delivery/CHANGELOG.md", "delivery/incidents/"],
           "_learnings_inbox": "delivery/LEARNINGS.md",
           "files": build_manifest_files()}
    open(os.path.join(HUB, "MANIFEST.json"), "w", encoding="utf-8").write(json.dumps(man, indent=1, ensure_ascii=False))
    print(f"MANIFEST.json written ({len(man['files'])} files)")
else:
    # MANIFEST-SYNC: the committed machine index (what MCP/AI readers load first) must match the
    # frontmatter it was generated from — a stale index misled readers for 10 days (LEARNINGS 2026-08-17).
    _mp = os.path.join(HUB, "MANIFEST.json")
    if os.path.exists(_mp):
        try:
            _committed = json.load(open(_mp, encoding="utf-8")).get("files")
        except Exception:
            _committed = None
        if _committed is None:
            fails.append("MANIFEST-SYNC: MANIFEST.json is unreadable — regenerate with --write-manifest")
        else:
            _fresh = build_manifest_files()
            if _committed != _fresh:
                _diff = [k for k in sorted(set(_committed) | set(_fresh)) if _committed.get(k) != _fresh.get(k)]
                fails.append(f"MANIFEST-SYNC: MANIFEST.json is stale vs frontmatter ({len(_diff)} entries: "
                             f"{', '.join(_diff[:3])}{'…' if len(_diff) > 3 else ''}) — run --write-manifest and commit it")

# ── required files: the system ships as a unit; a sync must never strip these ──
REQUIRED_FILES = ["README.md", "AGENTS.md", "DOCS-STANDARD.md", "DOCS-SYSTEM.md", "MANIFEST.json",
                  "scripts/validate_docs.py",
                  ".github/workflows/validate-docs.yml"]
for rf in REQUIRED_FILES:
    if not os.path.exists(os.path.join(HUB, rf)):
        fails.append(f"REQUIRED-FILE: '{rf}' is missing — restore it before merging (the system ships as a unit)")
if not any(os.path.exists(os.path.join(HUB, b)) for b in ("CLAUDE.md", "BOOTSTRAP.md")):
    fails.append("REQUIRED-FILE: no root boot file — need CLAUDE.md (installed) or BOOTSTRAP.md (seed)")

# ── report ──
dedup = lambda xs: list(dict.fromkeys(xs))
fails, warns = dedup(fails), dedup(warns)
print(f"\n=== validate_docs — {len(md_files)} md files ===")
for f_ in fails: print("  FAIL:", f_)
for w in warns: print("  warn:", w)
print(f"result: {'FAIL' if fails else 'PASS'} ({len(fails)} fail, {len(warns)} warn)")
sys.exit(1 if fails else 0)
