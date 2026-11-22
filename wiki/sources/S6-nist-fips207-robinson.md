---
title: "S6 來源摘要：NIST〈FIPS 207: HQC-KEM〉會議簡報"
type: source
sources: [S6, S5]
related: [../entities/fips-207.md, ../concepts/hqc-kem-fo-transform.md, ../comparisons/hqc-parameter-sets.md, ../concepts/code-based-cryptography.md]
spec_version: 2025-08-22
updated: 2026-11-23
status: draft
---

時間說明：本頁內容都是 S6（2025 年 9 月會議簡報）當時的說法，「考慮中」「徵求意見」的事項之後可能已有變化，查核日期 2026-11-23。[S6 p.1、書目資料]

## 書目資料

- Angela Robinson（NIST），〈FIPS 207: HQC-KEM〉，第 6 屆 NIST PQC 標準化會議簡報，2025 年 9 月（PDF 建立日期 2025-09-25），23 頁。
- 網址：https://csrc.nist.gov/csrc/media/presentations/2025/fips-207-hqc-kem/fips_207-robinson_2.4.pdf
- 取得日期：2026-11-23，存於 `raw/S6-nist-fips207-robinson.pdf`（另有 pdftotext 轉出的 .txt）。NIST 文件，可放進 repo。
- 討論紀錄：[discussions/05-S6-nist-fips207-robinson.md](../../discussions/05-S6-nist-fips207-robinson.md)
- 引用方式：[S6 p.N] = 投影片第 N 頁；[S6 書目資料] = 登記在 raw/sources.yaml 的發布資訊（簡報投影片本身沒有印日期）。
- 狀態查核：依 SPEC §5.3，同時存下 NIST PQC 專案頁的文字快照 `raw/S6-status-nist-pqc-page-2026-11-23.md`（登記為 S6-status）；wiki 引用寫成 [S6 專案頁查核]。

## 重點

- NIST 把 HQC 的標準稱為「FIPS 207: HQC-KEM」。[S6 p.1]
- 選 HQC 的理由：解碼失敗率分析穩定、解碼器修錯能力明確；和 BIKE 相比，金鑰產生與解封裝快，代價是公鑰與密文比較大。[S6 p.3、p.8、p.11]
- 另外兩個不靠格的候選：BIKE 的安全分析還需要時間檢驗；Classic McEliece 公鑰非常大，且相關分析有進展。[S6 p.8、p.10、p.11]
- HQC 的運作概要和 S5 一致；S6 把密文寫成 c1、c2，對應 S5 的 u、v。[S6 p.15][S5 p.24]
- NIST 在考慮幾項細部修改，這些都已出現在 HQC 規格 2025-08-22 版的修改紀錄裡。[S6 p.17–p.19][S5 p.2]
- 另有「一位元組確認碼」提案，NIST 在徵求意見。[S6 p.20、p.21]

## 更新了哪些頁

- 改寫 [HQC 的標準化進度（FIPS 207）](../entities/fips-207.md)：標準名稱、選擇理由、狀態查核
- 修改 [從 PKE 到 KEM](../concepts/hqc-kem-fo-transform.md)：確認碼提案
- 修改 [HQC 參數組](../comparisons/hqc-parameter-sets.md)：記下大小數字的衝突
- 修改 [編碼式密碼](../concepts/code-based-cryptography.md)：Goppa 碼分析有進展
- 修改 [HQC 總覽](../overview/hqc-overview.md)、[術語表](../glossary.md)（新增 3 個術語）
- 修改 [S2 來源摘要](S2-nist-news-hqc.md)：時程的查核結果改指向 FIPS 207 頁
- 修改 [S1 來源摘要](S1-nist-pqc-explainer.md)：RSA 的待辦改為「五份來源都沒有，不寫」

## 可信度與限制

- 這是 NIST 的官方會議簡報，對「為什麼選 HQC」「標準叫什麼」可信度高；但簡報是條列重點，很多句子是引用第 3、4 輪報告的片段。[S6 p.3、p.11]
- 衝突：S6 第 4 頁的效能表寫等級 1 的 HQC 公鑰 2,249、密文 4,497 位元組，和 S5（2025-08-22 版）不同；S6 說表格取自演算法規格，而它列為「考慮中」的修改 S5 都已採用，本 wiki 因此推斷它是較早的規格版本。本 wiki 採用 S5，見 [HQC 參數組](../comparisons/hqc-parameter-sets.md)。[S6 p.4、p.17][S5 p.2、p.29]
- 表格裡的 ML-KEM 與 CPU 週期數字，依使用者決定不收。
- 簡報沒有給 FIPS 207 草案的發布日期。[S6 p.16]
