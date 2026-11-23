"""B6 發布（SPEC §7.1、§9.3）：
1. 把通過 H2 的簡報複製到 slides/index.html，頁尾的 wiki 相對連結改成 GitHub 網址。
2. 產生 reports/slide_wiki_map.md：投影片編號、標題、wiki 頁、這些頁的來源代碼。
3. 在被用到的 wiki 頁 frontmatter 寫入 used_in_slides（沒被用到的頁移除這個欄位）。

用法：
  .venv/bin/python scripts/publish.py --run run-001-v1 --html runs/run-001-v1/slides-v4.html
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, now_iso, read_frontmatter  # noqa: E402

REPO = "https://github.com/112306071/HW10_HQC-LLM-WIKI/blob/main/"


def set_used_in(path: Path, slides: list[int] | None) -> bool:
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 4)
    head, rest = text[:end], text[end:]
    head = re.sub(r"\nused_in_slides:.*", "", head)
    if slides:
        head += f"\nused_in_slides: [{', '.join(str(s) for s in slides)}]"
    new = head + rest
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--html", required=True)
    a = ap.parse_args(argv)

    src = Path(a.html)
    html = src.read_text(encoding="utf-8")
    out_html = html.replace('href="../../wiki/', f'href="{REPO}wiki/')
    dest = ROOT / "slides" / "index.html"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(out_html, encoding="utf-8")

    soup = BeautifulSoup(html, "html.parser")
    used: dict[str, list[int]] = defaultdict(list)
    rows = []
    for sec in soup.select("section[data-slide]"):
        n = int(sec["data-slide"])
        h = sec.find(["h1", "h2"])
        title = re.sub(r"\s+", " ", h.get_text(" ")).strip() if h else ""
        pages = (sec.get("data-wiki") or "").split()
        srcs = []
        for p in pages:
            used[p].append(n)
            fm, _ = read_frontmatter(ROOT / "wiki" / p)
            for s in (fm or {}).get("sources", []) or []:
                if s not in srcs:
                    srcs.append(s)
        links = "<br>".join(f"[{p}](../wiki/{p})" for p in pages)
        rows.append(f"| {n} | {title} | {links} | {', '.join(srcs)} |")

    rep = ROOT / "reports" / "slide_wiki_map.md"
    rep.parent.mkdir(exist_ok=True)
    rep.write_text("\n".join([
        "# 投影片 ↔ wiki 對應表", "",
        f"由 `scripts/publish.py` 產生，{now_iso()}。簡報：`{src.relative_to(ROOT) if src.is_absolute() else src}` → `slides/index.html`（{a.run}）。",
        "來源代碼取自各 wiki 頁 frontmatter 的 `sources`；反向對應寫在各頁 frontmatter 的 `used_in_slides`。", "",
        "| # | 標題 | wiki 頁 | 來源 |", "| --- | --- | --- | --- |", *rows, ""]), encoding="utf-8")

    changed = []
    for p in sorted((ROOT / "wiki").rglob("*.md")):
        rel = str(p.relative_to(ROOT / "wiki"))
        fm, _ = read_frontmatter(p)
        if fm is None:
            continue
        if set_used_in(p, sorted(set(used.get(rel, []))) or None):
            changed.append(rel)
    print(f"slides/index.html ← {src}；reports/slide_wiki_map.md；used_in_slides 更新 {len(changed)} 頁")
    for c in changed:
        print("  ", c, used.get(c))
    return 0


if __name__ == "__main__":
    sys.exit(main())
