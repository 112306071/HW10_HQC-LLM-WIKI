"""彙整所有 trace 與 checks，產生 reports/run_summary.md 與 reports/node_failures.svg（SPEC §10.3）。

用法：
  .venv/bin/python scripts/summarize_runs.py
只讀 runs/，不改任何紀錄。檢查腳本本身的誤判列在 runs/<run>/checker_bugs.yaml，統計時另列為 checker_bug。
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, now_iso  # noqa: E402

CHECK_NODES = ["A3S", "A4", "B3", "B5", "H1", "H2"]
RUN_ORDER = ["ingest", "run-001-v1", "run-002-v2"]


def load_run(run_dir: Path) -> dict:
    trace = [json.loads(l) for l in (run_dir / "trace.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()] \
        if (run_dir / "trace.jsonl").exists() else []
    checks = []
    for p in sorted((run_dir / "checks").glob("*.json")) if (run_dir / "checks").exists() else []:
        d = json.loads(p.read_text(encoding="utf-8"))
        d["_file"] = str(p.relative_to(ROOT))
        checks.append(d)
    bugs = []
    if (run_dir / "checker_bugs.yaml").exists():
        bugs = yaml.safe_load((run_dir / "checker_bugs.yaml").read_text(encoding="utf-8")) or []
    return {"name": run_dir.name, "trace": trace, "checks": checks, "bugs": bugs}


def fmt_dur(sec: float) -> str:
    h, rem = divmod(int(sec), 3600)
    return f"{h} 小時 {rem // 60} 分" if h else f"{rem // 60} 分"


def node_stats(run: dict) -> dict:
    runs_ = Counter(t["node"] for t in run["trace"])
    fails = Counter(t["node"] for t in run["trace"] if t["result"] in ("FAIL", "HUMAN_REVISE") and not t.get("checker_bug"))
    bugs = Counter(t["node"] for t in run["trace"] if t.get("checker_bug"))
    esc = Counter(t["node"] for t in run["trace"] if t["result"] == "ESCALATED")
    return {"runs": runs_, "fails": fails, "bugs": bugs, "esc": esc}


def check_stats(run: dict) -> tuple[Counter, Counter, dict]:
    bug_keys = {(b["check_file"], b["id"]) for b in run["bugs"]}
    fails, bug_fails = Counter(), Counter()
    by_node: dict[str, Counter] = defaultdict(Counter)
    for c in run["checks"]:
        for r in c["results"]:
            if r["status"] != "FAIL":
                continue
            key = f"{r['id']}（{'腳本' if r['by'] == 'script' else '語意'}）"
            if (c["_file"], r["id"]) in bug_keys:
                bug_fails[key] += 1
            else:
                fails[key] += 1
                by_node[c["node"]][r["id"]] += 1
    return fails, bug_fails, by_node


def last_unsupported(run: dict) -> str:
    b5 = [c for c in run["checks"] if c["node"] == "B5"]
    if not b5:
        return "—"
    last = b5[-1]
    n = 0
    for r in last["results"]:
        if r["id"] == "P4":
            n += sum(1 for d in r["details"] if "UNSUPPORTED" in d.get("problem", ""))
    return str(n)


def svg_chart(runs: list[dict], path: Path) -> None:
    nodes = ["B3", "B5", "H2"]
    series = [r for r in runs if r["name"].startswith("run-")]
    colors = ["#1f5fa8", "#b5530b", "#1b7a3a"]
    w, h, left, top, bar = 560, 300, 60, 40, 34
    vals = {r["name"]: node_stats(r)["fails"] for r in series}
    mx = max([1] + [v[n] for v in vals.values() for n in nodes])
    group = bar * max(1, len(series)) + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="各檢查節點失敗次數">',
           '<style>text{font-family:"PingFang TC","Noto Sans TC",sans-serif;font-size:14px}</style>',
           f'<text x="{left}" y="24" font-size="16" font-weight="bold">各檢查節點失敗次數（簡報階段）</text>']
    base = h - 50
    scale = (base - top) / mx
    for gi, n in enumerate(nodes):
        x0 = left + 20 + gi * group
        for si, r in enumerate(series):
            v = vals[r["name"]][n]
            x = x0 + si * bar
            out.append(f'<rect x="{x}" y="{base - v * scale:.1f}" width="{bar - 6}" height="{v * scale:.1f}" fill="{colors[si % 3]}"/>')
            out.append(f'<text x="{x + (bar - 6) / 2}" y="{base - v * scale - 6:.1f}" text-anchor="middle">{v}</text>')
        out.append(f'<text x="{x0 + bar * len(series) / 2 - 3}" y="{base + 20}" text-anchor="middle">{n}</text>')
    out.append(f'<line x1="{left}" y1="{base}" x2="{w - 20}" y2="{base}" stroke="#566070"/>')
    for si, r in enumerate(series):
        out.append(f'<rect x="{left + si * 160}" y="{h - 18}" width="12" height="12" fill="{colors[si % 3]}"/>'
                   f'<text x="{left + si * 160 + 18}" y="{h - 8}">{r["name"]}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> int:
    runs = [load_run(ROOT / "runs" / n) for n in RUN_ORDER if (ROOT / "runs" / n).exists()]
    L = ["# 執行紀錄彙整", "", f"由 `scripts/summarize_runs.py` 產生，{now_iso()}。資料來源：`runs/*/trace.jsonl`、`runs/*/checks/*.json`。", ""]

    L += ["## 1. 節點統計", ""]
    for r in runs:
        s = node_stats(r)
        _, _, by_node = check_stats(r)
        L += [f"### {r['name']}", "", "| 節點 | 執行次數 | 失敗次數 | 失敗率 | 最常失敗的檢查 | checker_bug | ESCALATED |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
        for node in sorted(s["runs"], key=lambda n: list(s["runs"]).index(n)):
            k = s["runs"][node]
            f = s["fails"][node]
            top_ = "、".join(f"{i}×{c}" for i, c in by_node[node].most_common(2)) or "—"
            L.append(f"| {node} | {k} | {f} | {f / k:.0%} | {top_} | {s['bugs'][node]} | {s['esc'][node]} |")
        L.append("")

    L += ["## 2. 檢查統計（各檢查 ID 的失敗次數）", ""]
    for r in runs:
        fails, bug_fails, _ = check_stats(r)
        L += [f"### {r['name']}", ""]
        if not fails and not bug_fails:
            L += ["沒有失敗。", ""]
            continue
        L += ["| 檢查 | 失敗次數 |", "| --- | --- |"]
        L += [f"| {k} | {v} |" for k, v in sorted(fails.items())]
        L += [f"| {k}（checker_bug，另列） | {v} |" for k, v in sorted(bug_fails.items())]
        L.append("")

    L += ["## 3. run-001 與 run-002 比較", ""]
    cmp_runs = [r for r in runs if r["name"].startswith("run-")]
    if cmp_runs:
        L += ["| 項目 | " + " | ".join(r["name"] for r in cmp_runs) + " |", "| --- |" + " --- |" * len(cmp_runs)]

        def row(label, fn):
            L.append(f"| {label} | " + " | ".join(fn(r) for r in cmp_runs) + " |")
        row("總步數", lambda r: str(len(r["trace"])))
        for n in ["B3", "B5"]:
            row(f"{n} 失敗次數", lambda r, n=n: str(node_stats(r)["fails"][n]))
        row("最後一版 P4 UNSUPPORTED 數", last_unsupported)
        row("H2 要求修改次數", lambda r: str(sum(1 for t in r["trace"] if t["node"] == "H2" and t["result"] == "HUMAN_REVISE")))

        def dur(r):
            if len(r["trace"]) < 2:
                return "—"
            a = datetime.fromisoformat(r["trace"][0]["ts"])
            b = datetime.fromisoformat(r["trace"][-1]["ts"])
            return fmt_dur((b - a).total_seconds())
        row("總耗時（第一步到最後一步）", dur)
        L.append("")
    else:
        L += ["還沒有簡報階段的紀錄。", ""]

    L += ["## 4. 時間線", ""]
    for r in runs:
        L += [f"### {r['name']}", "", "| # | 時間 | 節點 | 對象 | 第幾次 | 結果 | 下一步 | 原因 |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for t in r["trace"]:
            reason = (t.get("reason") or "").replace("|", "／")
            L.append(f"| {t['step']} | {t['ts'][5:16].replace('T', ' ')} | {t['node']} | {t.get('target', '')} | {t['attempt']} | "
                     f"{t['result']}{'（checker_bug）' if t.get('checker_bug') else ''} | {t.get('route_to') or ''} | {reason} |")
        L.append("")

    L += ["## 5. 圖", "", "![各檢查節點失敗次數](node_failures.svg)", ""]
    out = ROOT / "reports"
    out.mkdir(exist_ok=True)
    svg_chart(runs, out / "node_failures.svg")
    (out / "run_summary.md").write_text("\n".join(L), encoding="utf-8")
    print(f"寫出 {out / 'run_summary.md'} 與 {out / 'node_failures.svg'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
