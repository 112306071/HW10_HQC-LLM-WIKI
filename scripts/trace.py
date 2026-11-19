"""寫一筆節點執行紀錄到 runs/<run_id>/trace.jsonl，並更新 state.json（SPEC §10.1、§7.2）。

用法：
  .venv/bin/python scripts/trace.py --run ingest --node A1 --result DONE \
      --inputs "https://..." --outputs raw/S1-x.md --route-to A2 --reason "S1 取得" --duration 30

trace 只能往後加。step 自動遞增；attempt 未指定時，檢查節點自動以「該節點在本 run、同一 target 的已執行次數 + 1」計。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, now_iso  # noqa: E402

RESULTS = {"DONE", "PASS", "FAIL", "ESCALATED", "HUMAN_APPROVED", "HUMAN_REVISE"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, help="run_id，例如 ingest、run-001-v1")
    ap.add_argument("--version", default=None, help="workflow 版本；預設讀 workflow/graph.yaml")
    ap.add_argument("--node", required=True)
    ap.add_argument("--attempt", type=int, default=None)
    ap.add_argument("--target", default="", help="這次處理的對象，例如 S1、outline-v2（用來計算 attempt）")
    ap.add_argument("--inputs", nargs="*", default=[])
    ap.add_argument("--outputs", nargs="*", default=[])
    ap.add_argument("--result", required=True, choices=sorted(RESULTS))
    ap.add_argument("--route-to", default=None)
    ap.add_argument("--reason", default="")
    ap.add_argument("--duration", type=float, default=None, help="秒")
    ap.add_argument("--checker-bug", action="store_true", help="這次失敗是檢查腳本本身的 bug（§10.5）")
    a = ap.parse_args(argv)

    graph = yaml.safe_load((ROOT / "workflow" / "graph.yaml").read_text(encoding="utf-8"))
    if a.node not in graph["nodes"]:
        ap.error(f"未知節點 {a.node}")
    version = a.version or graph["version"]

    run_dir = ROOT / "runs" / a.run
    run_dir.mkdir(parents=True, exist_ok=True)
    trace_path = run_dir / "trace.jsonl"
    lines = []
    if trace_path.exists():
        lines = [json.loads(l) for l in trace_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    attempt = a.attempt
    if attempt is None:
        attempt = 1 + sum(1 for l in lines if l["node"] == a.node and l.get("target", "") == a.target)

    rec = {
        "ts": now_iso(),
        "run_id": a.run,
        "workflow_version": version,
        "step": len(lines) + 1,
        "node": a.node,
        "target": a.target,
        "attempt": attempt,
        "inputs": a.inputs,
        "outputs": a.outputs,
        "result": a.result,
        "route_to": a.route_to,
        "reason": a.reason,
        "duration_s": a.duration,
    }
    if a.checker_bug:
        rec["checker_bug"] = True
    with trace_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # state.json：目前節點與各檢查點嘗試次數
    state_path = run_dir / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {
        "run_id": a.run, "workflow_version": version, "attempts": {}, "extra_sources": [], "history_len": 0}
    state["last_node"] = a.node
    state["last_result"] = a.result
    state["current_node"] = a.route_to
    state["target"] = a.target
    if graph["nodes"][a.node]["type"] == "check":
        key = f"{a.node}:{a.target}" if a.target else a.node
        state["attempts"][key] = attempt
    state["history_len"] = rec["step"]
    state["updated"] = rec["ts"]
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"trace #{rec['step']} {a.node} {a.result} → {a.route_to}  ({trace_path.relative_to(ROOT)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
