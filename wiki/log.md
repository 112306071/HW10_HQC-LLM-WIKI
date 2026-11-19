# Wiki 紀錄（只能往後追加）

列出所有紀錄：`grep "^## \[" wiki/log.md`

## [2026-11-19 23:17] issue | 來源連結查核（S1–S8）
- 2026-11-19 22:5x 用 curl 逐一下載 S1–S8 與 NIST PQC 專案頁，全部回應 HTTP 200，但 S7 的內容不是論文。
- S1：原網址 `/cybersecurity/what-post-quantum-cryptography` 會轉址到 `/cybersecurity-and-privacy/what-post-quantum-cryptography`，內容相同（標題、2026-02-27 更新日期一致）。raw 檔記錄兩個網址。
- S4：規格寫的是 IEEE Trans. Inf. Theory 2018 正式版；可公開取得的是 arXiv 1612.05572 預印本（28 頁）。本來就只用來講概念（SPEC §5.2），改用 arXiv 版，書目資料兩者都列。
- S7：TCHES 文章頁（tches.iacr.org/…/9700）回傳「Making sure you're not a bot!」驗證頁，抓不到論文。IACR ePrint 2021/1485 是同一篇論文（標題、作者相同），但 PDF 對程式回傳 403。依 SPEC §5.4 第 5 點停下來詢問使用者；使用者於 2026-11-19 以瀏覽器手動下載 ePrint 版 PDF（40 頁），放入 raw/。
- NIST PQC 專案頁只寫「HQC 於 2025-03-11 被選中」，沒有 FIPS 207 草案發布的消息（查核日期 2026-11-19）。

## [2026-11-19 23:17] issue | 規格書 §7 的 v1 流程圖在匯出時遺失
- SPEC.md 原文 §7 的嵌入圖沒有隨 Markdown 匯出。
- 處理：依 §7.1 節點表與 §7.2 graph.yaml 重畫成 mermaid，存於 workflow/graph.md；SPEC.md 該處改為指向 workflow/graph.md。待使用者在第一次跑簡報流程前確認（SPEC §0.1）。

## [2026-11-19 23:30] ingest | S1 NIST：What Is Post-Quantum Cryptography?
- 討論紀錄：discussions/01-S1-nist-pqc-explainer.md（使用者確認 2026-11-19 23:28）
- 新增：sources/S1-nist-pqc-explainer.md, concepts/quantum-threat.md, concepts/post-quantum-cryptography.md, glossary.md
- 修改：index.md
- lint：見 runs/ingest/checks/A4-lint-S1-a*.json

## [2026-11-19 23:33] issue | lint_wiki.py L7 誤判日期為參數（checker_bug）
- A4-lint-S1-a1 的 L7 腳本部分把 sources/S1 的日期「2026-02-27」裡的「2-27」當成 2^-27，判定該頁含參數數字。
- 保留原紀錄不改；修正 PARAM_NUM 正規式（指數前不可緊接數字或連字號），並在 selftest 加入日期樣本。紀錄於 runs/ingest/checker_bugs.yaml。

## [2026-11-19 23:33] lint | S1 ingest 後 lint 第 1 次不通過，修正
- 檢查紀錄：runs/ingest/checks/A4-lint-S1-a1.json → FAIL
- 修改 concepts/quantum-threat.md：時間估計都標明「S1 2026-02-27 更新版」與查核日期（L7 語意）
- 修改 concepts/post-quantum-cryptography.md、glossary.md：補來源標記、拆短說明句（L2）

## [2026-11-19 23:37] lint | S1 ingest 後 lint 第 2 次不通過，修正
- 檢查紀錄：runs/ingest/checks/A4-lint-S1-a2.json → FAIL（L7 語意：「仍在考慮中」沒標時間點）
- 修改 concepts/post-quantum-cryptography.md：頁首加時間說明；「仍在考慮中」改寫為「S1 寫作時的狀態」並加查核日期
- 修改 sources/S1-nist-pqc-explainer.md：重點清單前加時間說明（同類問題一併處理）
- 觀察：腳本 L7 的時效詞清單（尚未、預計、草案、即將）沒有「仍在」，這次只有語意檢查抓到。

## [2026-11-19 23:43] lint | S1 lint 第 3 次通過；依檢查員備註更正一句
- 檢查紀錄：runs/ingest/checks/A4-lint-S1-a3.json → PASS
- 語意檢查員在 notes 指出（不屬 L7/L8）：sources/S1 寫「S1 沒有點名橢圓曲線」不正確，S1 Q12 有提到橢圓曲線。
- 更正 sources/S1-nist-pqc-explainer.md〈可信度與限制〉：改成「講量子威脅時沒有點名 RSA 或公鑰加密」，另說明 Q12 的橢圓曲線例子為何不採用。
- 這是 lint 通過後的修改，下一次 A4（S2）會對整個 wiki 重跑 lint。
