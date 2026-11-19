"""A4：Wiki lint，L1–L9 的腳本部分（SPEC §8.1）。

用法：
  .venv/bin/python scripts/lint_wiki.py --run ingest --target S1 [--semantic runs/ingest/semantic/A4-S1-a1.json]
  .venv/bin/python scripts/lint_wiki.py --selftest

L7、L8 另有語意部分，由子代理判定後以 --semantic 併入同一份 JSON。
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ROOT, SOURCE_MARK, load_semantic, merge_results, overall_of,  # noqa: E402
                    print_summary, read_frontmatter, result, write_check)

REQUIRED_FM = ["title", "type", "sources", "updated", "status"]
SPECIAL = {"index.md", "log.md"}
EXEMPT_SECTIONS = {"相關頁面", "書目資料", "更新了哪些頁"}
LINK = re.compile(r"!?\[([^\]]*)\]\(([^)\s]+)\)")
LOG_HEAD = re.compile(r"^## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (ingest|query|lint|conflict|workflow-change|issue) \| (.+)$")
PARAM_NUM = re.compile(r"\d[\d,\s]*\s*(位元組|bytes?\b|位元\b|bits?\b)|2\s*\^\s*[-−]?\s*\d+|2[−-]\d{2,3}\b")
TIMELY = re.compile(r"尚未|預計|草案|即將")
CHECK_DATE = re.compile(r"查核日期\s*\d{4}-\d{2}-\d{2}")
PARAM_NAME = re.compile(r"HQC-[135](?!\d)|hqc-(?:128|192|256)|ML-KEM-(?:512|768|1024)")
QUANTITY = {"公鑰": "pk", "public key": "pk", "私鑰": "sk", "secret key": "sk",
            "密文": "ct", "ciphertext": "ct", "共享秘密": "ss", "shared secret": "ss"}


# ---------- 解析 ----------

def strip_inline(text: str) -> str:
    """移除連結網址、來源標記與 markdown 符號，留下可讀文字。"""
    text = LINK.sub(lambda m: m.group(1), text)
    text = SOURCE_MARK.sub("", text)
    text = re.sub(r"[*_`]", "", text)
    return text.strip()


def iter_blocks(body: str):
    """把內文切成區塊：(kind, text, section, line_no)。kind ∈ heading/para/item/quote/row/header_row"""
    section = ""
    in_code = False
    buf: list[str] = []
    buf_kind = None
    buf_line = 0
    table_row_idx = 0

    def flush():
        nonlocal buf, buf_kind
        if buf:
            yield (buf_kind, " ".join(s.strip() for s in buf), section, buf_line)
        buf, buf_kind = [], None

    for i, line in enumerate(body.splitlines(), 1):
        s = line.rstrip()
        if s.lstrip().startswith("```"):
            yield from flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        if not s.strip():
            yield from flush()
            table_row_idx = 0
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            yield from flush()
            section = re.sub(r"^\d+[.、]\s*", "", m.group(2)).strip()
            yield ("heading", m.group(2), section, i)
            continue
        if s.lstrip().startswith("|"):
            yield from flush()
            if re.match(r"^\s*\|[\s:\-|]+\|\s*$", s):
                continue
            table_row_idx += 1
            yield ("header_row" if table_row_idx == 1 else "row", s, section, i)
            continue
        if s.lstrip().startswith(">"):
            if buf_kind != "quote":
                yield from flush()
                buf_kind, buf_line = "quote", i
            buf.append(s.lstrip()[1:])
            continue
        if re.match(r"^\s*([-*+]|\d+\.)\s+", s):
            yield from flush()
            buf_kind, buf_line = "item", i
            buf.append(re.sub(r"^\s*([-*+]|\d+\.)\s+", "", s))
            continue
        if buf_kind is None:
            buf_kind, buf_line = "para", i
        buf.append(s)
    yield from flush()


def wiki_pages(root: Path) -> list[Path]:
    return sorted(p for p in (root / "wiki").rglob("*.md"))


def rel(root: Path, p: Path) -> str:
    return p.relative_to(root / "wiki").as_posix()


def page_links(page: Path, text: str) -> list[tuple[str, Path | None]]:
    out = []
    for m in LINK.finditer(text):
        target = m.group(2)
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        path = target.split("#", 1)[0]
        out.append((target, (page.parent / path).resolve()))
    return out


def parse_log(root: Path) -> list[dict]:
    log = root / "wiki" / "log.md"
    if not log.exists():
        return []
    entries = []
    for i, line in enumerate(log.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            m = LOG_HEAD.match(line)
            entries.append({"line": i, "raw": line, "ok": bool(m),
                            "time": m.group(1) if m else None,
                            "type": m.group(2) if m else None,
                            "title": m.group(3) if m else None})
    return entries


def code_re(code: str) -> re.Pattern:
    return re.compile(rf"(?<![A-Za-z0-9]){re.escape(code)}(?!\d)")


# ---------- 檢查 ----------

def lint(root: Path, expect_source: str | None) -> list[dict]:
    pages = wiki_pages(root)
    sources_yaml = root / "raw" / "sources.yaml"
    known = set()
    if sources_yaml.exists():
        known = {s["id"] for s in (yaml.safe_load(sources_yaml.read_text(encoding="utf-8")) or {}).get("sources", [])}

    data = {}
    off = {}  # 內文第 1 行在檔案中的行號 - 1
    for p in pages:
        fm, body = read_frontmatter(p)
        raw = p.read_text(encoding="utf-8")
        data[p] = (fm, body, raw)
        off[p] = raw[: len(raw) - len(body)].count("\n")

    L = {k: [] for k in ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9"]}

    # L1 frontmatter
    for p, (fm, body, _) in data.items():
        if p.name in SPECIAL and p.parent == root / "wiki":
            continue
        if fm is None:
            L["L1"].append({"where": rel(root, p), "problem": "沒有 frontmatter 或 YAML 無法解析"})
            continue
        missing = [k for k in REQUIRED_FM if not fm.get(k)]
        if missing:
            L["L1"].append({"where": rel(root, p), "problem": f"缺欄位：{', '.join(missing)}"})

    # L2 來源
    for p, (fm, body, _) in data.items():
        if p.name in SPECIAL and p.parent == root / "wiki":
            continue
        fm = fm or {}
        srcs = fm.get("sources") or []
        if isinstance(srcs, str):
            srcs = [srcs]
        for s in srcs:
            if s not in known:
                L["L2"].append({"where": rel(root, p), "problem": f"sources 欄位的 {s} 不在 raw/sources.yaml"})
        for kind, text, section, line in iter_blocks(body):
            if kind in ("heading", "quote", "header_row") or section in EXEMPT_SECTIONS:
                continue
            marks = [m.group(1) for m in SOURCE_MARK.finditer(text) if m.group(1)]
            for mk in marks:
                if mk not in srcs:
                    L["L2"].append({"where": f"{rel(root, p)}:{line + off[p]}", "problem": f"標記 [{mk}] 不在本頁 sources 欄位"})
            plain = strip_inline(text)
            needs = bool(re.search(r"\d", plain)) or len(plain) > 40
            if needs and not SOURCE_MARK.search(text):
                L["L2"].append({"where": f"{rel(root, p)}:{line + off[p]}", "problem": f"缺來源標記：「{plain[:30]}…」"})

    # L3 斷連（內文 + frontmatter related）
    all_links: dict[Path, list[Path]] = {}
    for p, (fm, body, raw) in data.items():
        links = page_links(p, raw)
        for target, path in links:
            if not path.exists():
                L["L3"].append({"where": rel(root, p), "problem": f"斷連：{target}"})
        for r in (fm or {}).get("related", []) or []:
            if not (p.parent / r).resolve().exists():
                L["L3"].append({"where": rel(root, p), "problem": f"related 指向不存在的檔案：{r}"})
        all_links[p] = [path for _, path in links]

    # L4 孤兒、L5 index 完整
    index = root / "wiki" / "index.md"
    log = root / "wiki" / "log.md"
    if not index.exists():
        L["L5"].append({"where": "index.md", "problem": "index.md 不存在"})
    index_targets = set(all_links.get(index, []))
    for p in pages:
        if p in (index,):
            continue
        rp = p.resolve()
        if rp not in index_targets:
            L["L5"].append({"where": rel(root, p), "problem": "沒有列在 index.md"})
        if p == log:
            continue
        inbound = [q for q, ls in all_links.items() if q not in (index, log, p) and rp in ls]
        if rp not in index_targets or not inbound:
            L["L4"].append({"where": rel(root, p), "problem": "孤兒頁：需被 index.md 與至少一個其他頁連到"
                            + ("" if inbound else "（沒有其他頁連到）")})
    for t in index_targets:
        if t.suffix == ".md" and not t.exists():
            L["L5"].append({"where": "index.md", "problem": f"列了不存在的頁：{t.name}"})

    # L6 log
    entries = parse_log(root)
    if not entries:
        L["L6"].append({"where": "log.md", "problem": "log.md 沒有任何紀錄"})
    else:
        for e in entries:
            if not e["ok"]:
                L["L6"].append({"where": f"log.md:{e['line']}", "problem": f"格式錯誤：{e['raw'][:50]}"})
        times = [e["time"] for e in entries if e["ok"]]
        if times != sorted(times):
            L["L6"].append({"where": "log.md", "problem": "紀錄時間不是遞增（log 只能往後加）"})
        if expect_source:
            ingests = [e for e in entries if e["type"] == "ingest"]
            if not ingests or not code_re(expect_source).search(ingests[-1]["title"]):
                L["L6"].append({"where": "log.md", "problem": f"最新一筆 ingest 不是 {expect_source}"})

    # L7 版本與時效
    for p, (fm, body, _) in data.items():
        if p.name in SPECIAL and p.parent == root / "wiki":
            continue
        fm = fm or {}
        has_param = False
        for kind, text, section, line in iter_blocks(body):
            if kind == "heading":
                continue
            plain = SOURCE_MARK.sub("", text)
            if PARAM_NUM.search(plain):
                has_param = True
            if TIMELY.search(plain) and not CHECK_DATE.search(text):
                L["L7"].append({"where": f"{rel(root, p)}:{line + off[p]}", "problem": f"時效說法缺查核日期：「{strip_inline(text)[:30]}…」"})
        sv = str(fm.get("spec_version", "none")).strip().lower()
        if has_param and sv in ("none", "", "null"):
            L["L7"].append({"where": rel(root, p), "problem": "含參數數字，但 spec_version 是 none"})

    # L8 跨頁一致（腳本部分：參數組 × 量 × 版本 的數值）
    values: dict[tuple, dict[int, list[str]]] = {}
    for p, (fm, body, _) in data.items():
        # 未標版本的頁視同專案的標準版本（CLAUDE.md：一律以 2025-08-22 版為準）
        page_ver = str((fm or {}).get("spec_version", "none"))
        if page_ver.strip().lower() in ("none", "", "null"):
            page_ver = "HQC 2025-08-22"
        header: list[str] = []
        for kind, text, section, line in iter_blocks(body):
            where = f"{rel(root, p)}:{line + off[p]}"
            ver = page_ver
            vm = re.search(r"(舊版|20\d\d-\d\d-\d\d 版|20\d\d 版)", text)
            if vm:
                ver = vm.group(1)
            if kind == "header_row":
                header = [c.strip() for c in text.strip().strip("|").split("|")]
                continue
            if kind == "row" and header:
                cells = [c.strip() for c in text.strip().strip("|").split("|")]
                pm = PARAM_NAME.search(cells[0]) if cells else None
                if pm:
                    for h, c in zip(header[1:], cells[1:]):
                        q = next((v for k, v in QUANTITY.items() if k in h.lower() or k in h), None)
                        n = re.search(r"\d[\d,\s]*\d|\d", SOURCE_MARK.sub("", c))
                        if q and n:
                            val = int(re.sub(r"[,\s]", "", n.group(0)))
                            values.setdefault((pm.group(0), q, ver), {}).setdefault(val, []).append(where)
                continue
            if kind in ("para", "item", "quote"):
                plain = SOURCE_MARK.sub("", text)
                for m in re.finditer(r"(HQC-[135](?!\d)|hqc-(?:128|192|256)|ML-KEM-(?:512|768|1024))[^。；;\n]{0,20}?"
                                     r"(公鑰|私鑰|密文|共享秘密)[^。；;\n\d]{0,12}(\d[\d,\s]*\d)\s*位元組", plain):
                    val = int(re.sub(r"[,\s]", "", m.group(3)))
                    values.setdefault((m.group(1), QUANTITY[m.group(2)], ver), {}).setdefault(val, []).append(where)
    for key, vals in values.items():
        if len(vals) > 1:
            desc = "；".join(f"{v}（{', '.join(ws[:2])}）" for v, ws in vals.items())
            L["L8"].append({"where": f"{key[0]} {key[1]} @ {key[2]}", "problem": f"同一個量有不同數值：{desc}"})

    # L9 先討論後生成
    used = set()
    for p, (fm, _, _) in data.items():
        srcs = (fm or {}).get("sources") or []
        used.update([srcs] if isinstance(srcs, str) else srcs)
    disc_dir = root / "discussions"
    for code in sorted(used):
        files = sorted(disc_dir.glob(f"*-{code}-*.md")) if disc_dir.exists() else []
        if not files:
            L["L9"].append({"where": code, "problem": "沒有討論紀錄"})
            continue
        text = files[-1].read_text(encoding="utf-8")
        m7 = re.search(r"^## 7\.[^\n]*\n(.*?)(?=^## 8\.)", text, re.S | re.M)
        sec7 = re.sub(r"<!--.*?-->", "", m7.group(1), flags=re.S).strip() if m7 else ""
        if not sec7:
            L["L9"].append({"where": files[-1].name, "problem": "第 7 節（使用者回覆）是空的"})
        mt = re.search(r"確認時間：\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", text)
        if not mt:
            L["L9"].append({"where": files[-1].name, "problem": "第 8 節沒有確認時間"})
            continue
        confirm = datetime.strptime(mt.group(1), "%Y-%m-%d %H:%M")
        ing = [e for e in entries if e["type"] == "ingest" and code_re(code).search(e["title"])]
        if not ing:
            L["L9"].append({"where": code, "problem": "log.md 沒有這份來源的 ingest 紀錄"})
            continue
        first = datetime.strptime(ing[0]["time"], "%Y-%m-%d %H:%M")
        if first < confirm:
            L["L9"].append({"where": code, "problem": f"ingest（{ing[0]['time']}）早於確認時間（{mt.group(1)}）"})

    return [result(k, v) for k, v in L.items()]


# ---------- 自我測試 ----------

def selftest() -> int:
    fx = ROOT / "tests" / "fixtures"
    good = lint(fx / "lint_good", "S1")
    bad = lint(fx / "lint_bad", "S1")
    ok = True
    for r in good:
        if r["status"] != "PASS":
            ok = False
            print(f"[FAIL] lint_good 不應有 {r['id']} 錯誤：{r['details'][:2]}")
    for r in bad:
        if r["status"] != "FAIL":
            ok = False
            print(f"[FAIL] lint_bad 應該抓到 {r['id']} 但沒有")
        else:
            print(f"[ok] lint_bad 抓到 {r['id']}：{r['details'][0]['problem'][:50]}")
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default="ingest")
    ap.add_argument("--target", help="這次 ingest 的來源代碼，例如 S1；全域 lint 用 all")
    ap.add_argument("--attempt", type=int)
    ap.add_argument("--semantic", help="子代理的語意檢查 JSON")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.target:
        ap.error("需要 --target")
    expect = a.target if re.match(r"^S\d+$", a.target) else None
    results = merge_results(lint(ROOT, expect), load_semantic(a.semantic))
    attempt = a.attempt or 1 + len(list((ROOT / "runs" / a.run / "checks").glob(f"A4-lint-{a.target}-a*.json")))
    overall = overall_of(results)
    version = yaml.safe_load((ROOT / "workflow" / "graph.yaml").read_text(encoding="utf-8"))["version"]
    path = write_check(ROOT, a.run, version, "A4", f"lint-{a.target}", attempt, "wiki/", results,
                       "A3" if overall == "FAIL" else None)
    print(f"A4 lint {a.target} attempt {attempt}: {overall}  → {path.relative_to(ROOT)}")
    print_summary(results)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
