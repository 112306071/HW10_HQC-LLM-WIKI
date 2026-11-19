"""第 7 張投影片的教學示例（SPEC §9.2 註）：重複碼多數決、漢明重量、漢明距離。

示例的數字由本腳本計算，貼進 wiki 時用 [示例由腳本計算] 標記。
用法：
  .venv/bin/python scripts/examples.py            # 印出 Markdown 區塊
  .venv/bin/python scripts/examples.py --selftest
"""
from __future__ import annotations

import sys


def weight(v: str) -> int:
    return v.count("1")


def distance(a: str, b: str) -> int:
    assert len(a) == len(b)
    return sum(x != y for x, y in zip(a, b))


def rep_encode(bits: str, r: int = 3) -> str:
    return "".join(b * r for b in bits)


def rep_decode(code: str, r: int = 3) -> str:
    out = []
    for i in range(0, len(code), r):
        block = code[i:i + r]
        out.append("1" if weight(block) * 2 > r else "0")
    return "".join(out)


def flip(code: str, positions: list[int]) -> str:
    c = list(code)
    for p in positions:
        c[p] = "1" if c[p] == "0" else "0"
    return "".join(c)


def markdown() -> str:
    msg = "10"
    cw = rep_encode(msg)
    e = "000100"           # 錯誤向量：第 4 位出錯
    recv = flip(cw, [i for i, b in enumerate(e) if b == "1"])
    dec = rep_decode(recv)
    e2 = "110000"          # 同一組 3 位裡錯 2 位
    recv2 = flip(cw, [i for i, b in enumerate(e2) if b == "1"])
    dec2 = rep_decode(recv2)
    a, b = "10110", "11100"
    lines = [
        "### 示例：重複碼多數決（示例由腳本計算）",
        "",
        f"- 訊息 `{msg}` 每個位元重複 3 次，編碼成 `{cw}`。[示例由腳本計算]",
        f"- 傳送時第 4 位出錯（錯誤向量 `{e}`，漢明重量 {weight(e)}），收到 `{recv}`。[示例由腳本計算]",
        f"- 每 3 位取多數決，解回 `{dec}`，和原訊息相同：錯 1 位修得回來。[示例由腳本計算]",
        f"- 若同一組錯 2 位（錯誤向量 `{e2}`），收到 `{recv2}`，多數決解成 `{dec2}`，解錯了：錯誤太多就修不回來。[示例由腳本計算]",
        "",
        "### 示例：漢明重量與漢明距離（示例由腳本計算）",
        "",
        f"- `{a}` 的漢明重量是 {weight(a)}（有 {weight(a)} 個 1）。[示例由腳本計算]",
        f"- `{a}` 和 `{b}` 有 {distance(a, b)} 個位置不同，所以漢明距離是 {distance(a, b)}。[示例由腳本計算]",
    ]
    return "\n".join(lines)


def selftest() -> int:
    assert weight("10110") == 3
    assert distance("10110", "11100") == 2
    assert rep_encode("10") == "111000"
    assert rep_decode(flip("111000", [3])) == "10"          # 錯 1 位可修正
    assert rep_decode(flip("111000", [0, 1])) == "00"       # 錯 2 位修不回來
    print("selftest PASS")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print(markdown())
