"""B5：成品檢查，P1–P3、P6、P7 的腳本部分（SPEC §8.3）。P4、P5、P8 由子代理判定後以 --semantic 併入。

簡報 HTML 約定（B4 產生時遵守）：
  <section class="slide" data-slide="07" data-type="example" data-wiki="concepts/a.md concepts/b.md">
  .nonfact      不算事實的文字（頁尾、導覽），P3 不檢查
  aside.notes   講者備註，按 N 顯示
  #prev #next   換頁按鈕；#counter 顯示「7 / 22」；#progress 進度條（style width 百分比）
  section.active 目前這張
  小測驗：.quiz-q 內有 button.opt[data-correct="true|false"]，點選後 .feedback 顯示「答對／答錯」與解釋

用法：
  .venv/bin/python scripts/check_slides.py --run run-001-v1 --html runs/run-001-v1/slides-v1.html \
      --outline runs/run-001-v1/outline-v2.md [--semantic X.json]
  .venv/bin/python scripts/check_slides.py --selftest
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_outline import WIKI_TAG, parse_outline  # noqa: E402
from common import (ROOT, load_semantic, merge_results, overall_of, print_summary,  # noqa: E402
                    result, write_check)

FORMAT_IDS = {"P1", "P6", "P7"}
CONTENT_IDS = {"P3", "P4", "P5", "P8"}
NUM = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")


def norm_numbers(text: str) -> set[str]:
    """抽出 2 位數以上的數字（去掉千分位逗號與空白）。單一位數多半是序號，不檢查。"""
    text = re.sub(r"(?<=\d)[,   ](?=\d{3}(?!\d))", "", text)
    out = set()
    for m in NUM.finditer(text):
        n = m.group(0).replace(",", "")
        if len(n.replace(".", "")) >= 2:
            out.add(n)
    return out


# ---------- 靜態檢查 ----------

def static_checks(root: Path, html_path: Path, outline_text: str | None) -> tuple[list[dict], bool]:
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    P1, P2, P3 = [], [], []
    p2_outline_missing = False

    # P1 合法、獨立
    size = html_path.stat().st_size
    if size > 500 * 1024:
        P1.append({"where": html_path.name, "problem": f"檔案 {size // 1024} KB，超過 500 KB"})
    h = soup.find("html")
    if not h or h.get("lang") != "zh-Hant":
        P1.append({"where": "<html>", "problem": "缺少 lang=\"zh-Hant\""})
    for tag in soup.find_all("script", src=True):
        P1.append({"where": "<script>", "problem": f"載入外部 JS：{tag['src']}"})
    for tag in soup.find_all("link", href=True):
        if not tag["href"].startswith("data:"):
            P1.append({"where": "<link>", "problem": f"載入外部資源：{tag['href']}"})
    for name in ("img", "iframe", "embed", "object", "audio", "video", "source"):
        for tag in soup.find_all(name):
            src = tag.get("src") or tag.get("data") or ""
            if src and not src.startswith("data:"):
                P1.append({"where": f"<{name}>", "problem": f"引用外部檔案：{src}"})
    css = " ".join(s.get_text() for s in soup.find_all("style")) + " " + " ".join(
        t.get("style", "") for t in soup.find_all(style=True))
    for m in re.finditer(r"@import[^;]+;|url\(\s*['\"]?(?!data:|#)[^)]+\)", css):
        P1.append({"where": "<style>", "problem": f"CSS 載入外部資源：{m.group(0)[:60]}"})

    sections = soup.select("section[data-slide]")
    if not sections:
        P1.append({"where": "全檔", "problem": "找不到 section[data-slide]"})

    # P2 對應
    outline = {s["n"]: s for s in parse_outline(outline_text)} if outline_text else {}
    for sec in sections:
        n = int(sec["data-slide"])
        where = f"slide-{n:02d}"
        pages = (sec.get("data-wiki") or "").split()
        o = outline.get(n)
        o_pages = set()
        if o:
            for b in o["bullets"]:
                for tag in WIKI_TAG.findall(b["text"]):
                    for ref in re.split(r"[;；]", tag):
                        o_pages.add(ref.split("#")[0].strip())
        if not pages:
            P2.append({"where": where, "problem": "缺 data-wiki"})
            if not o_pages:
                p2_outline_missing = True
            continue
        for pg in pages:
            if not (root / "wiki" / pg).exists():
                P2.append({"where": where, "problem": f"data-wiki 頁不存在：{pg}"})
        if outline_text:
            if o is None:
                P2.append({"where": where, "problem": "大綱沒有這一張"})
                p2_outline_missing = True
            elif o_pages and set(pages) != o_pages:
                P2.append({"where": where, "problem": f"data-wiki {sorted(pages)} 與大綱 {sorted(o_pages)} 不一致"})
            elif not o_pages and o["type"] != "cover":
                P2.append({"where": where, "problem": "大綱這一張沒有 wiki 標註"})
                p2_outline_missing = True
    if outline_text:
        missing = set(outline) - {int(s["data-slide"]) for s in sections}
        for n in sorted(missing):
            P2.append({"where": f"slide-{n:02d}", "problem": "大綱有這一張，HTML 沒有"})

    # P3 數字一致
    for sec in sections:
        n = int(sec["data-slide"])
        pages = (sec.get("data-wiki") or "").split()
        wiki_text = " ".join((root / "wiki" / p).read_text(encoding="utf-8")
                             for p in pages if (root / "wiki" / p).exists())
        wiki_nums = norm_numbers(wiki_text)
        clone = BeautifulSoup(str(sec), "html.parser")
        for el in clone.select(".nonfact"):
            el.decompose()
        for num in sorted(norm_numbers(clone.get_text(" "))):
            if num not in wiki_nums:
                P3.append({"where": f"slide-{n:02d}", "problem": f"數字 {num} 不在 data-wiki 頁中"})

    p2_route_b2 = bool(P2) and p2_outline_missing
    return [result("P1", P1), result("P2", P2), result("P3", P3)], p2_route_b2


# ---------- 瀏覽器檢查 ----------

OVERFLOW_JS = """
(sel) => {
  const s = document.querySelector(sel);
  if (!s) return ['找不到 ' + sel];
  const bad = [];
  const sr = s.getBoundingClientRect();
  if (getComputedStyle(s).overflowY !== 'visible' || true) {
    if (s.scrollHeight > s.clientHeight + 2 && window.innerWidth > 700)
      bad.push('整張垂直溢出 ' + s.scrollHeight + '>' + s.clientHeight);
  }
  s.querySelectorAll('*').forEach(e => {
    if (e.closest('aside.notes')) return;
    const tag = e.tagName.toLowerCase();
    if (e.closest('svg') && tag !== 'svg') return;
    const r = e.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    if (e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX !== 'auto')
      bad.push(tag + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '') +
               ' 水平溢出 ' + e.scrollWidth + '>' + e.clientWidth);
    if (r.right > sr.right + 1 || r.left < sr.left - 1)
      bad.push(tag + ' 超出投影片左右邊界');
    if (window.innerWidth > 700 && r.bottom > sr.bottom + 1)
      bad.push(tag + ' 超出投影片下緣');
  });
  return [...new Set(bad)].slice(0, 6);
}
"""


def browser_checks(html_path: Path, shot_dir: Path | None) -> list[dict]:
    from playwright.sync_api import sync_playwright
    P6, P7 = [], []
    url = html_path.resolve().as_uri()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        # ----- P6 桌面 -----
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors: list[str] = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(url)
        page.wait_for_timeout(300)
        n = page.locator("section[data-slide]").count()
        for i in range(1, n + 1):
            # 直接切換 active，不依賴簡報自己的導覽（導覽由 P7 另外檢查）
            page.evaluate(f"""(() => {{ const all = document.querySelectorAll('section[data-slide]');
                all.forEach((s, k) => s.classList.toggle('active', k === {i - 1})); }})()""")
            page.wait_for_timeout(120)
            active = page.locator("section.slide.active")
            if active.count() != 1:
                P6.append({"where": f"desktop slide-{i:02d}", "problem": "找不到唯一的 active 投影片"})
                continue
            for b in page.evaluate(OVERFLOW_JS, "section.slide.active"):
                P6.append({"where": f"desktop slide-{i:02d}", "problem": b})
            if shot_dir:
                page.screenshot(path=str(shot_dir / f"desktop-{i:02d}.png"))
        # ----- P7 導覽與互動 -----
        P7 += nav_checks(page, url, n)
        for e in errors:
            P6.append({"where": "console", "problem": e[:120]})
        page.close()

        # ----- P6 手機 -----
        mpage = browser.new_page(viewport={"width": 390, "height": 844})
        merrors: list[str] = []
        mpage.on("pageerror", lambda e: merrors.append(str(e)))
        mpage.goto(url)
        mpage.wait_for_timeout(300)
        if mpage.evaluate("document.documentElement.scrollWidth") > 391:
            P6.append({"where": "mobile", "problem": "頁面出現水平捲動"})
        for i in range(1, n + 1):
            sel = f"section[data-slide='{i:02d}'], section[data-slide='{i}']"
            loc = mpage.locator(sel).first
            if loc.count() == 0 or not loc.is_visible():
                P6.append({"where": f"mobile slide-{i:02d}", "problem": "手機版看不到這一張（應改為直式捲動）"})
                continue
            loc.scroll_into_view_if_needed()
            sid = mpage.evaluate(f"(() => {{ const e = document.querySelector(\"{sel}\"); e.id = e.id || 'chk-{i}'; return e.id; }})()")
            for b in mpage.evaluate(OVERFLOW_JS, f"#{sid}"):
                P6.append({"where": f"mobile slide-{i:02d}", "problem": b})
            if shot_dir:
                loc.screenshot(path=str(shot_dir / f"mobile-{i:02d}.png"))
        for e in merrors:
            P6.append({"where": "mobile console", "problem": e[:120]})
        browser.close()
    return [result("P6", P6), result("P7", P7)]


def nav_checks(page, url: str, n: int) -> list[dict]:
    P7 = []

    def state():
        return page.evaluate("""() => {
          const a = document.querySelector('section.slide.active');
          const c = document.querySelector('#counter');
          const p = document.querySelector('#progress');
          return {active: a ? parseInt(a.dataset.slide, 10) : null,
                  counter: c ? c.textContent.replace(/\\s+/g, ' ').trim() : null,
                  progress: p ? p.getBoundingClientRect().width / p.parentElement.getBoundingClientRect().width : null};
        }""")

    def expect(label, k):
        s = state()
        if s["active"] != k:
            P7.append({"where": label, "problem": f"應在第 {k} 張，實際 {s['active']}"})
        if s["counter"] != f"{k} / {n}":
            P7.append({"where": label, "problem": f"頁碼應為「{k} / {n}」，實際「{s['counter']}」"})
        if s["progress"] is None or abs(s["progress"] - k / n) > 0.03:
            P7.append({"where": label, "problem": f"進度條比例 {s['progress']}，應約為 {k / n:.2f}"})

    page.goto(url)  # 從頭開始（無 hash）
    page.wait_for_timeout(300)
    if n < 3:
        return [{"where": "全套", "problem": "投影片少於 3 張，無法測導覽"}]
    expect("初始", 1)
    page.keyboard.press("ArrowRight"); page.wait_for_timeout(100); expect("→ 鍵", 2)
    page.keyboard.press("Space"); page.wait_for_timeout(100); expect("空白鍵", 3)
    page.keyboard.press("ArrowLeft"); page.wait_for_timeout(100); expect("← 鍵", 2)
    for sel, label, k in (("#next", "下一頁按鈕", 3), ("#prev", "上一頁按鈕", 2)):
        try:
            page.click(sel, timeout=2000)
            page.wait_for_timeout(100)
            expect(label, k)
        except Exception:
            P7.append({"where": sel, "problem": f"沒有可點的{label}"})
    target = min(7, n)
    page.goto(url + f"#{target}")
    page.reload()
    page.wait_for_timeout(300)
    expect(f"網址 #{target}", target)
    # N 鍵顯示講者備註
    page.keyboard.press("n"); page.wait_for_timeout(100)
    if not page.evaluate("(() => { const a = document.querySelector('section.slide.active aside.notes'); return !!a && a.offsetParent !== null; })()"):
        P7.append({"where": "N 鍵", "problem": "按 N 後看不到講者備註"})
    page.keyboard.press("n")
    # 小測驗
    qs = page.locator(".quiz-q")
    if qs.count() == 0:
        P7.append({"where": "小測驗", "problem": "找不到 .quiz-q"})
    else:
        quiz_slide = page.evaluate("parseInt(document.querySelector('.quiz-q').closest('section').dataset.slide, 10)")
        page.evaluate(f"location.hash = '#{quiz_slide}'"); page.wait_for_timeout(150)
        for qi in range(qs.count()):
            q = qs.nth(qi)
            want = "false" if qi % 2 == 0 else "true"
            opt = q.locator(f"button.opt[data-correct='{want}']").first
            if opt.count() == 0:
                P7.append({"where": f"小測驗第 {qi + 1} 題", "problem": f"沒有 data-correct={want} 的選項"})
                continue
            try:
                opt.click(timeout=2000)
            except Exception:
                P7.append({"where": f"小測驗第 {qi + 1} 題", "problem": "選項無法點選（看不到或被遮住）"})
                continue
            page.wait_for_timeout(80)
            fb = q.locator(".feedback")
            text = fb.inner_text() if fb.count() and fb.is_visible() else ""
            expect_word = "答對" if want == "true" else "答錯"
            if expect_word not in text:
                P7.append({"where": f"小測驗第 {qi + 1} 題", "problem": f"點選後應顯示「{expect_word}」，實際「{text[:20]}」"})
    return P7


# ---------- 主程式 ----------

def run_all(root: Path, html: Path, outline_text: str | None, shot_dir: Path | None, browser: bool = True):
    res, p2_b2 = static_checks(root, html, outline_text)
    if browser:
        res += browser_checks(html, shot_dir)
    return res, p2_b2


def route(results: list[dict], p2_b2: bool) -> str:
    failed = {r["id"] for r in results if r["status"] == "FAIL"}
    if not failed:
        return "H2"
    if failed & CONTENT_IDS or ("P2" in failed and p2_b2):
        return "B2"
    return "B4"


def selftest() -> int:
    fx = ROOT / "tests" / "fixtures" / "slides_root"
    outline = (fx / "outline.md").read_text(encoding="utf-8")
    good, _ = run_all(fx, fx / "good.html", outline, None)
    bad, _ = run_all(fx, fx / "bad.html", outline, None)
    ok = True
    for r in good:
        if r["status"] != "PASS":
            ok = False
            print(f"[FAIL] good.html 不應有 {r['id']} 錯誤：{r['details'][:3]}")
    for r in bad:
        if r["status"] != "FAIL":
            ok = False
            print(f"[FAIL] bad.html 應該抓到 {r['id']} 但沒有")
        else:
            print(f"[ok] bad.html 抓到 {r['id']}：{r['details'][0]['problem'][:60]}")
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run")
    ap.add_argument("--html")
    ap.add_argument("--outline")
    ap.add_argument("--attempt", type=int)
    ap.add_argument("--semantic")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.run and a.html and a.outline):
        ap.error("需要 --run、--html、--outline")
    graph = yaml.safe_load((ROOT / "workflow" / "graph.yaml").read_text(encoding="utf-8"))
    html = Path(a.html)
    attempt = a.attempt or 1 + len(list((ROOT / "runs" / a.run / "checks").glob("B5-*.json")))
    shot_dir = ROOT / "runs" / a.run / "screenshots" / f"{html.stem}-a{attempt}"
    shot_dir.mkdir(parents=True, exist_ok=True)
    res, p2_b2 = run_all(ROOT, html, Path(a.outline).read_text(encoding="utf-8"), shot_dir)
    results = merge_results(res, load_semantic(a.semantic))
    to = route(results, p2_b2)
    path = write_check(ROOT, a.run, graph["version"], "B5", html.stem, attempt,
                       str(html.resolve().relative_to(ROOT)), results, to,
                       extra={"screenshots": str(shot_dir.relative_to(ROOT))})
    print(f"B5 {html.name} attempt {attempt}: {overall_of(results)} → {to}  ({path.relative_to(ROOT)})")
    print_summary(results)
    return 0 if overall_of(results) == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
