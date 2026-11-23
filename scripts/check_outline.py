"""B3：大綱檢查，O1–O5 的腳本部分（SPEC §8.2）。O3 的語意部分與 O6（v2 候選）由子代理判定後以 --semantic 併入。

大綱格式（每張一個區塊）：
  ## slide-07 | type: example | 目標: G3
  標題：錯誤更正碼：多傳一點，就能修正錯誤
  定義：錯誤更正碼, 漢明距離, 漢明重量
  - 重點…… [wiki: concepts/error-correcting-codes.md#白話解釋]
  圖示：……
  講者備註：……

用法：
  .venv/bin/python scripts/check_outline.py --run run-001-v1 --outline runs/run-001-v1/outline-v1.md [--semantic X.json]
  .venv/bin/python scripts/check_outline.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ROOT, load_semantic, merge_results, overall_of, print_summary,  # noqa: E402
                    read_frontmatter, result, write_check)

HEAD = re.compile(r"^## slide-(\d+)\s*\|\s*type:\s*([\w-]+)\s*\|\s*目標:\s*(.*)$")
WIKI_TAG = re.compile(r"\[wiki:\s*([^\]]+)\]")
TYPES = {"cover", "objectives", "motivation", "concept", "example", "process", "compare",
         "misconception", "quiz", "summary"}
REQUIRED_TYPES = ["objectives", "example", "misconception", "quiz", "summary"]
O3_EXEMPT_TYPES = {"cover", "objectives"}  # 封面與學習目標是預告，不算「使用」術語


def parse_goals(s: str) -> set[str]:
    s = s.strip()
    out = set()
    for a, b in re.findall(r"G(\d)\s*[–\-~]\s*G(\d)", s):
        out.update(f"G{i}" for i in range(int(a), int(b) + 1))
    out.update(re.findall(r"G\d", s))
    return out


def parse_outline(text: str) -> list[dict]:
    slides = []
    cur = None
    for i, line in enumerate(text.splitlines(), 1):
        m = HEAD.match(line.strip())
        if m:
            cur = {"n": int(m.group(1)), "type": m.group(2), "goals": parse_goals(m.group(3)),
                   "line": i, "title": "", "defines": [], "bullets": [], "figure": "", "notes": ""}
            slides.append(cur)
            continue
        if cur is None:
            continue
        s = line.strip()
        if s.startswith("標題："):
            cur["title"] = s[3:].strip()
        elif s.startswith("定義："):
            cur["defines"] = [t.strip() for t in re.split(r"[,，、]", s[3:]) if t.strip() and t.strip() not in ("無", "—")]
        elif re.match(r"^[-*]\s+", s):
            cur["bullets"].append({"text": re.sub(r"^[-*]\s+", "", s), "line": i})
        elif s.startswith("圖示："):
            cur["figure"] = s[3:].strip()
        elif s.startswith("講者備註："):
            cur["notes"] = s[5:].strip()
    return slides


def bullet_plain(text: str) -> str:
    return re.sub(r"\s+", " ", WIKI_TAG.sub("", text)).replace("**", "").strip()


def headings_of(path: Path) -> set[str]:
    _, body = read_frontmatter(path)
    hs = set()
    for line in body.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            h = m.group(1).strip()
            hs.add(h)
            hs.add(re.sub(r"^\d+[.、]\s*", "", h))
    return hs


def glossary_terms(path: Path) -> list[dict]:
    """讀 glossary 表格：| 中文 | English | 一句話解釋 | ... 。含「先備知識」的列不檢查。"""
    terms = []
    if not path.exists():
        return terms
    _, body = read_frontmatter(path)
    for line in body.splitlines():
        if not line.startswith("|") or re.match(r"^\|[\s:\-|]+\|$", line.strip()):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in ("中文", "術語"):
            continue
        if "先備知識" in line:
            continue
        zh = re.sub(r"[（(].*?[)）]", "", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cells[0])).strip()
        en = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cells[1]).strip()
        names = [n for n in [zh] + [e.strip() for e in en.split("/")] if n]
        terms.append({"zh": zh, "names": names})
    return terms


def lay_terms(root: Path) -> list[dict]:
    """v2：workflow/lay_terms.yaml 列的「一般人看不懂、glossary 沒收」的詞，也要先定義後使用。"""
    path = root / "workflow" / "lay_terms.yaml"
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [{"zh": t["name"], "names": [t["name"]]} for t in data.get("terms", [])]


def term_in(name: str, text: str) -> bool:
    if re.match(r"^[\x00-\x7f]+$", name):
        return re.search(rf"(?<![A-Za-z0-9]){re.escape(name)}(?![A-Za-z0-9])", text) is not None
    return name in text


def check(root: Path, outline_text: str, questions: list[dict],
          min_slides: int = 18, max_slides: int = 22, max_bullets: int = 4, max_chars: int = 40) -> list[dict]:
    slides = parse_outline(outline_text)
    O = {k: [] for k in ["O1", "O2", "O3", "O4", "O5"]}
    wiki = root / "wiki"

    # O1 覆蓋
    have = {s["n"] for s in slides}
    for q in questions:
        if q["n"] not in have:
            O["O1"].append({"where": f"slide-{q['n']:02d}", "problem": "問題清單中的投影片沒有對應區塊"})
    covered = set().union(*[s["goals"] for s in slides]) if slides else set()
    for g in ["G1", "G2", "G3", "G4", "G5"]:
        if g not in covered:
            O["O1"].append({"where": g, "problem": "沒有任何一張負責這個學習目標"})

    # O2 標註
    head_cache: dict[Path, set[str]] = {}
    for s in slides:
        where = f"slide-{s['n']:02d}"
        if s["type"] != "cover" and not s["bullets"]:
            O["O2"].append({"where": where, "problem": "沒有任何重點"})
        for bi, b in enumerate(s["bullets"], 1):
            tags = WIKI_TAG.findall(b["text"])
            if not tags:
                O["O2"].append({"where": f"{where} 第 {bi} 點", "problem": "缺 wiki 標註"})
                continue
            for tag in tags:
                for ref in re.split(r"[;；]", tag):
                    ref = ref.strip()
                    path, _, anchor = ref.partition("#")
                    f = wiki / path.strip()
                    if not f.exists():
                        O["O2"].append({"where": f"{where} 第 {bi} 點", "problem": f"wiki 頁不存在：{path}"})
                        continue
                    if anchor:
                        hs = head_cache.setdefault(f, headings_of(f))
                        if anchor.strip() not in hs:
                            O["O2"].append({"where": f"{where} 第 {bi} 點", "problem": f"{path} 沒有章節「{anchor}」"})

    # O3 術語先定義後使用（腳本部分）
    terms = glossary_terms(wiki / "glossary.md") + lay_terms(root)
    ordered = sorted(slides, key=lambda s: s["n"])
    for t in terms:
        first_use = None
        def_at = None
        for s in ordered:
            if def_at is None and any(term_in(n, d) or term_in(d, n) for n in t["names"] for d in s["defines"]):
                def_at = s["n"]
            if s["type"] in O3_EXEMPT_TYPES:
                continue
            text = s["title"] + " " + " ".join(bullet_plain(b["text"]) for b in s["bullets"])
            if first_use is None and any(term_in(n, text) for n in t["names"]):
                first_use = s["n"]
        if first_use is not None and (def_at is None or def_at > first_use):
            O["O3"].append({"where": f"slide-{first_use:02d}",
                            "problem": f"術語「{t['zh']}」在第 {first_use} 張先出現，" +
                            ("但沒有任何一張定義它" if def_at is None else f"第 {def_at} 張才定義")})

    # O4 教學結構
    types = [s["type"] for s in ordered]
    for s in ordered:
        if s["type"] not in TYPES:
            O["O4"].append({"where": f"slide-{s['n']:02d}", "problem": f"未知的 type：{s['type']}"})
    for t in REQUIRED_TYPES:
        if t not in types:
            O["O4"].append({"where": "全套", "problem": f"缺少 type: {t}"})
    if types and types[0] != "cover":
        O["O4"].append({"where": "slide-01", "problem": "第一張不是 cover"})
    if "objectives" in types and types.index("objectives") > 1:
        O["O4"].append({"where": "objectives", "problem": "學習目標不在前兩張"})
    if types and types[-1] != "summary":
        O["O4"].append({"where": "最後一張", "problem": "最後一張不是 summary"})

    def first(t):
        return types.index(t) if t in types else None

    def last(t):
        return len(types) - 1 - types[::-1].index(t) if t in types else None
    order_rules = [("motivation", "process", "動機要在運作流程之前"),
                   ("misconception", "quiz", "誤解要在小測驗之前"),
                   ("quiz", "summary", "小測驗要在總結之前")]
    for a, b, msg in order_rules:
        if a in types and b in types and last(a) > first(b):
            O["O4"].append({"where": f"{a} → {b}", "problem": msg})

    # O5 份量
    if not (min_slides <= len(slides) <= max_slides):
        O["O5"].append({"where": "全套", "problem": f"共 {len(slides)} 張，應為 {min_slides}–{max_slides} 張"})
    for s in slides:
        where = f"slide-{s['n']:02d}"
        if len(s["bullets"]) > max_bullets:
            O["O5"].append({"where": where, "problem": f"{len(s['bullets'])} 個重點，上限 {max_bullets}"})
        for bi, b in enumerate(s["bullets"], 1):
            n = len(bullet_plain(b["text"]))
            if n > max_chars:
                O["O5"].append({"where": f"{where} 第 {bi} 點", "problem": f"{n} 字，上限 {max_chars}"})

    return [result(k, v) for k, v in O.items()]


def selftest() -> int:
    fx = ROOT / "tests" / "fixtures" / "outline_root"
    qs = yaml.safe_load((fx / "workflow" / "questions.yaml").read_text(encoding="utf-8"))["slides"]
    kw = dict(min_slides=8, max_slides=8)
    good = check(fx, (fx / "outline-good.md").read_text(encoding="utf-8"), qs, **kw)
    bad = check(fx, (fx / "outline-bad.md").read_text(encoding="utf-8"), qs, **kw)
    ok = True
    for r in good:
        if r["status"] != "PASS":
            ok = False
            print(f"[FAIL] outline-good 不應有 {r['id']} 錯誤：{r['details'][:2]}")
    for r in bad:
        if r["status"] != "FAIL":
            ok = False
            print(f"[FAIL] outline-bad 應該抓到 {r['id']} 但沒有")
        else:
            print(f"[ok] outline-bad 抓到 {r['id']}：{r['details'][0]['problem'][:50]}")
    # v2：lay_terms.yaml 的詞（例：向量）沒定義就使用，O3 要抓到；定義後就不抓
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tr = Path(td)
        (tr / "wiki").mkdir()
        (tr / "workflow").mkdir()
        (tr / "workflow" / "lay_terms.yaml").write_text("terms:\n  - {name: 向量, hint: x}\n", encoding="utf-8")
        (tr / "wiki" / "a.md").write_text("---\ntitle: a\n---\n## 重點\n", encoding="utf-8")
        mk = lambda d: f"## slide-03 | type: concept | 目標: G1\n標題：t\n定義：{d}\n- 秘密是向量 [wiki: a.md#重點]\n"
        miss = [r for r in check(tr, mk("無"), [], 1, 30) if r["id"] == "O3"][0]
        hit = [r for r in check(tr, mk("向量"), [], 1, 30) if r["id"] == "O3"][0]
        if miss["status"] != "FAIL" or hit["status"] != "PASS":
            ok = False
            print("[FAIL] lay_terms：未定義的「向量」應被抓、定義後應通過")
        else:
            print("[ok] lay_terms：未定義的「向量」被抓到，定義後通過")
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run")
    ap.add_argument("--outline")
    ap.add_argument("--attempt", type=int)
    ap.add_argument("--semantic")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.run and a.outline):
        ap.error("需要 --run 與 --outline")
    graph = yaml.safe_load((ROOT / "workflow" / "graph.yaml").read_text(encoding="utf-8"))
    qs = yaml.safe_load((ROOT / "workflow" / "questions.yaml").read_text(encoding="utf-8"))["slides"]
    outline = Path(a.outline)
    results = merge_results(check(ROOT, outline.read_text(encoding="utf-8"), qs), load_semantic(a.semantic))
    attempt = a.attempt or 1 + len(list((ROOT / "runs" / a.run / "checks").glob("B3-*.json")))
    overall = overall_of(results)
    path = write_check(ROOT, a.run, graph["version"], "B3", outline.stem, attempt,
                       str(outline.resolve().relative_to(ROOT)), results, "B2" if overall == "FAIL" else "B4")
    print(f"B3 {outline.name} attempt {attempt}: {overall}  → {path.relative_to(ROOT)}")
    print_summary(results)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
