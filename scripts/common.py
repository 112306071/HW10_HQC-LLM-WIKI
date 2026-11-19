"""共用工具：路徑、時間、frontmatter 解析、檢查結果 JSON 的寫入（SPEC §8.0）。"""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TZ = timezone(timedelta(hours=8))  # Asia/Taipei

SOURCE_MARK = re.compile(r"\[(S\d+)[^\]]*\]|\[示例由腳本計算[^\]]*\]")


def now_iso() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def read_frontmatter(path: Path) -> tuple[dict | None, str]:
    """回傳 (frontmatter dict 或 None, 內文)。"""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    try:
        fm = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        fm = None
    body = text[end + 4:].lstrip("\n")
    return fm, body


def load_semantic(path: str | None) -> list[dict]:
    """讀子代理寫的語意檢查結果：{"results": [{"id":..., "status":..., "details": [...]}]}"""
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    out = []
    for r in data.get("results", []):
        r = dict(r)
        r["by"] = "semantic"
        out.append(r)
    return out


def merge_results(script_results: list[dict], semantic_results: list[dict]) -> list[dict]:
    """同一個 ID 同時有腳本與語意結果時，兩筆都保留（by 不同）。"""
    return script_results + semantic_results


def overall_of(results: list[dict]) -> str:
    return "FAIL" if any(r["status"] == "FAIL" for r in results) else "PASS"


def write_check(root: Path, run_id: str, version: str, node: str, target_name: str,
                attempt: int, target: str, results: list[dict], route_to: str | None,
                extra: dict | None = None) -> Path:
    out_dir = root / "runs" / run_id / "checks"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{node}-{target_name}-a{attempt}.json"
    if path.exists():
        raise SystemExit(f"拒絕覆寫既有檢查紀錄：{path}（紀錄只能新增）")
    data = {
        "run_id": run_id,
        "workflow_version": version,
        "node": node,
        "attempt": attempt,
        "timestamp": now_iso(),
        "target": target,
        "results": results,
        "overall": overall_of(results),
        "route_to": route_to,
    }
    if extra:
        data.update(extra)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def result(cid: str, details: list[dict], by: str = "script") -> dict:
    return {"id": cid, "by": by, "status": "FAIL" if details else "PASS", "details": details}


def print_summary(results: list[dict]) -> None:
    for r in results:
        print(f"  {r['id']:<3} [{r['by']}] {r['status']}")
        for d in r["details"][:8]:
            print(f"      - {d.get('where', '')}: {d.get('problem', '')}")
        if len(r["details"]) > 8:
            print(f"      … 另有 {len(r['details']) - 8} 筆")
