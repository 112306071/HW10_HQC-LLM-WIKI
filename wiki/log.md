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
