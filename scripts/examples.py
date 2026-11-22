"""投影片的教學示例（SPEC §9.2 註），數字一律由本腳本計算。

- 第 6 張：重複碼多數決、漢明重量、漢明距離（concepts/error-correcting-codes.md）
- 第 13 張：教學簡化版 HQC，照 HQC 規格 2025-08-22 版 HQC-PKE 的步驟（S5 p.23–p.25），
  但長度縮成 13、公開碼換成重複碼（討論紀錄 04 問題 1a）。不是真正的 HQC 參數。

貼進 wiki 時用 [示例由腳本計算] 標記。
用法：
  .venv/bin/python scripts/examples.py            # 印出第 6 張的 Markdown 區塊
  .venv/bin/python scripts/examples.py --toy      # 印出第 13 張的 Markdown 區塊
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


# ---------- 第 13 張：教學簡化版 HQC ----------
# 向量寫成 0/1 字串，第 0 位在最左邊；乘法是「多項式相乘、超過長度就繞回前面」（S5 p.7）。
# 在 0/1 的世界裡減法等於加法，所以 v - u·y 就是逐位 XOR。

TOY_N = 13            # 環境長度：13 是「原始質數」，和規格一樣要求（S5 p.11、p.22）
TOY_REP = 3           # 公開碼：每個位元重複 3 次（教學簡化；規格用的是 RM＋RS）
TOY_MSG = "1011"      # 4 位元訊息 → 編碼後 12 位元，最後 1 位截掉（S5 p.22 的截斷）
TOY_H = "1011001110100"
TOY_X, TOY_Y = 2, 7   # 秘密 x、y：各只有 1 個 1（位置）
TOY_OK = (2, 3, 8)    # (r1, r2, e) 的 1 所在位置：解密成功
TOY_BAD = (2, 3, 11)  # 只換掉 e 的位置：解密失敗


def tvec(pos: int) -> str:
    return "".join("1" if i == pos else "0" for i in range(TOY_N))


def txor(a: str, b: str) -> str:
    return "".join("1" if x != y else "0" for x, y in zip(a, b))


def tmul(a: str, b: str) -> str:
    c = [0] * len(a)
    for i, ai in enumerate(a):
        if ai == "1":
            for j, bj in enumerate(b):
                if bj == "1":
                    c[(i + j) % len(a)] ^= 1
    return "".join(map(str, c))


def toy_hqc(r1p: int, r2p: int, ep: int) -> dict:
    keep = len(TOY_MSG) * TOY_REP
    x, y, h = tvec(TOY_X), tvec(TOY_Y), TOY_H
    s = txor(x, tmul(h, y))                                  # 金鑰產生：s = x + h·y
    r1, r2, e = tvec(r1p), tvec(r2p), tvec(ep)
    u = txor(r1, tmul(h, r2))                                # 加密：u = r1 + h·r2
    cm = rep_encode(TOY_MSG, TOY_REP)
    noise = txor(tmul(s, r2), e)[:keep]                      # 蓋住訊息的雜訊 s·r2 + e（截斷）
    v = txor(cm, noise)                                      # 加密：v = 編碼(m) + 雜訊
    left = txor(v, tmul(u, y)[:keep])                        # 解密：v - u·y
    resid = txor(left, cm)                                   # 剩下的錯誤 = x·r2 + r1·y + e
    return {"x": x, "y": y, "h": h, "s": s, "r1": r1, "r2": r2, "e": e, "u": u,
            "cm": cm, "noise": noise, "v": v, "left": left, "resid": resid,
            "dec": rep_decode(left, TOY_REP)}


def toy_markdown() -> str:
    ok, bad = toy_hqc(*TOY_OK), toy_hqc(*TOY_BAD)
    keep = len(TOY_MSG) * TOY_REP
    m = "[示例由腳本計算]"
    lines = [
        "### 準備（教學簡化版）",
        "",
        f"- 所有向量長 {TOY_N} 位；公開碼是「每個位元重複 {TOY_REP} 次」，訊息 `{TOY_MSG}` 編碼成 `{ok['cm']}`（{keep} 位；{TOY_N} 位的雜訊只取前 {keep} 位，最後 1 位截掉）。{m}",
        f"- 公開的隨機向量 h = `{ok['h']}`。{m}",
        "",
        "### 步驟一：金鑰產生",
        "",
        f"- 秘密 x = `{ok['x']}`、y = `{ok['y']}`，各只有 1 個 1。{m}",
        f"- 公開 s = x + h·y = `{ok['s']}`。{m}",
        "",
        "### 步驟二：加密",
        "",
        f"- 寄件人挑很短的 r1 = `{ok['r1']}`、r2 = `{ok['r2']}`、e = `{ok['e']}`。{m}",
        f"- u = r1 + h·r2 = `{ok['u']}`。{m}",
        f"- 蓋在訊息上的雜訊 s·r2 + e = `{ok['noise']}`，{keep} 位裡有 {weight(ok['noise'])} 位是 1。{m}",
        f"- v = 編碼後的訊息 + 雜訊 = `{ok['v']}`；密文是 (u, v)。{m}",
        "",
        "### 步驟三：解密（成功）",
        "",
        f"- 收件人用秘密 y 算 v − u·y = `{ok['left']}`。{m}",
        f"- 和正確的編碼 `{ok['cm']}` 比，剩下的錯誤是 `{ok['resid']}`，只有 {weight(ok['resid'])} 位：從 {weight(ok['noise'])} 位降到 {weight(ok['resid'])} 位。{m}",
        f"- 每 {TOY_REP} 位取多數決，解回 `{ok['dec']}`，和原訊息 `{TOY_MSG}` 相同。{m}",
        "",
        "### 對照：解密失敗",
        "",
        f"- 同樣的金鑰與 r1、r2，只把 e 換成 `{bad['e']}`。{m}",
        f"- 剩下的錯誤變成 `{bad['resid']}`，其中 2 位落在同一組 {TOY_REP} 位裡。{m}",
        f"- 多數決解成 `{bad['dec']}`，和原訊息 `{TOY_MSG}` 不同：解密失敗。{m}",
    ]
    return "\n".join(lines)


def selftest() -> int:
    assert weight("10110") == 3
    assert distance("10110", "11100") == 2
    assert rep_encode("10") == "111000"
    assert rep_decode(flip("111000", [3])) == "10"          # 錯 1 位可修正
    assert rep_decode(flip("111000", [0, 1])) == "00"       # 錯 2 位修不回來
    ok, bad = toy_hqc(*TOY_OK), toy_hqc(*TOY_BAD)
    assert ok["dec"] == TOY_MSG and bad["dec"] != TOY_MSG
    # 剩下的錯誤必須等於 x·r2 + r1·y + e（S5 p.22 的正確性條件）
    for c, (r1p, r2p, ep) in ((ok, TOY_OK), (bad, TOY_BAD)):
        want = txor(txor(tmul(c["x"], tvec(r2p)), tmul(tvec(r1p), c["y"])), tvec(ep))[:len(c["cm"])]
        assert c["resid"] == want
    assert weight(ok["resid"]) < weight(ok["noise"])
    # 失敗案例的文字寫「2 位落在同一組」：檢查確實有一組錯了 2 位以上
    assert any(bad["resid"][i:i + TOY_REP].count("1") >= 2 for i in range(0, len(bad["resid"]), TOY_REP))
    assert tmul("1" + "0" * 12, TOY_H) == TOY_H
    # 13 是原始質數：2 在模 13 之下的階是 12，等價於 (X^13 - 1)/(X - 1) 在 F2 上不可約（S5 p.7 的定義）
    assert [pow(2, k, TOY_N) for k in range(1, TOY_N)].index(1) + 1 == TOY_N - 1
    print("selftest PASS")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print(toy_markdown() if "--toy" in sys.argv else markdown())
