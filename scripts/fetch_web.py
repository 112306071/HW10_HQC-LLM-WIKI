"""A1 用：把網頁來源（S1、S2）存成 Markdown，檔頭寫網址與取得日期（SPEC §5.4）。

用法：
  .venv/bin/python scripts/fetch_web.py --url URL --out raw/S1-x.md --id S1
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import now_iso  # noqa: E402

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"


def inline(el) -> str:
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            out.append(str(c))
        elif c.name == "a" and c.get("href"):
            t = inline(c).strip()
            out.append(f"[{t}]({c['href']})" if t else "")
        elif c.name in ("strong", "b"):
            out.append(f"**{inline(c).strip()}**")
        elif c.name in ("em", "i"):
            out.append(f"*{inline(c).strip()}*")
        elif c.name == "br":
            out.append("\n")
        else:
            out.append(inline(c))
    return " ".join("".join(out).split()) if "\n" not in "".join(out) else "".join(out).strip()


def to_md(root) -> str:
    lines = []
    for el in root.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote"]):
        if el.find_parent(["li"]) and el.name != "li":
            continue
        if el.name == "li" and el.find_parent("li"):
            continue
        text = inline(el).strip()
        if not text:
            continue
        if el.name.startswith("h"):
            lines.append("#" * int(el.name[1]) + " " + text)
        elif el.name == "li":
            lines.append("- " + text)
        elif el.name == "blockquote":
            lines.append("> " + text)
        else:
            lines.append(text)
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists():
        raise SystemExit(f"{out} 已存在；raw/ 只能新增不能修改")
    # 用 curl 下載（python.org 版 Python 在 macOS 上沒有預裝根憑證）
    p = subprocess.run(["curl", "-sSL", "-A", UA, "-m", "60", "-w", "\n%{url_effective}", a.url],
                       capture_output=True, check=True)
    raw_text = p.stdout.decode("utf-8", "replace")
    html, _, final = raw_text.rpartition("\n")
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "nav", "header", "footer", "form", "noscript"]):
        t.decompose()
    title = soup.title.get_text(strip=True) if soup.title else ""
    main_el = soup.find("main") or soup.find("article") or soup.body
    body = to_md(main_el)
    head = (f"<!-- 來源 {a.id}\n原始網址：{a.url}\n實際網址：{final}\n"
            f"取得時間：{now_iso()}\n頁面標題：{title}\n"
            f"轉換方式：scripts/fetch_web.py（只保留 <main> 內的標題、段落、清單） -->\n\n")
    out.write_text(head + body, encoding="utf-8")
    print(f"{a.id} → {out}  ({len(body)} 字元)  final={final}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
