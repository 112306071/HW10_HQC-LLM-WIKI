---
title: HQC 的標準化進度（FIPS 207）
type: entity
sources: [S2, S6, S5]
related: [../overview/hqc-overview.md, ../concepts/post-quantum-cryptography.md, ../comparisons/hqc-vs-ml-kem.md, ../sources/S2-nist-news-hqc.md, ../sources/S6-nist-fips207-robinson.md, ../concepts/decryption-failure-rate.md]
spec_version: 2025-08-22
updated: 2026-11-23
status: draft
used_in_slides: [18, 19]
---

狀態查核：本頁的時程、選擇理由與「考慮中」的修改，都是各來源當時的說法，不是現況：S2 是 2025-03-11 的預估，S6 是 2025-09 的會議簡報。2026-11-23 查 NIST PQC 專案頁，只寫「HQC 於 2025-03-11 被選中」，沒有列出 FIPS 207 草案；這只代表專案頁沒列，不代表確定沒有發布，查核日期 2026-11-23。[S2 摘要、§2][S6 p.1][S6 專案頁查核]

## 一句話定義

FIPS 207 是 NIST 為 HQC 準備的正式標準名稱；NIST 在 2025 年 9 月的會議簡報標題就是「FIPS 207: HQC-KEM」。[S6 p.1、書目資料]

## 重點

- HQC 是 NIST 後量子密碼計畫選出的第五個演算法，也是第四輪候選中唯一被選中的。[S2 §2]
- 在 HQC 之前，NIST 已選了四個演算法，其中三個在 2024 年成為正式標準；一般加密用的 ML-KEM 就是其中之一，標準名稱是 FIPS 203。[S2 §0、§2]
- 2025 年 3 月的預估：約一年後發布 HQC 的標準草案供公開意見，經過 90 天意見期後，在 2027 年定案（查核日期 2026-11-19）。[S2 摘要、§2]
- 2025 年 9 月，NIST 已用「FIPS 207: HQC-KEM」這個名稱，並在考慮一些細部修改。[S6 p.1、p.17、書目資料]
- 2026-11-23 查 NIST PQC 專案頁，只寫 HQC 於 2025-03-11 被選中，沒有列出 FIPS 207 草案（查核日期 2026-11-23）。[S6 專案頁查核]

## 細節

### NIST 為什麼選 HQC（S6，2025-09 的說法）

- 理由一：HQC 的解碼失敗率分析穩定，有公式也有實驗數據支持；它用的解碼器有明確的修錯能力。[S6 p.8]
- 理由二：和另一個不靠格的候選 BIKE 相比，HQC 的金鑰產生和解封裝快很多。[S6 p.3、p.11]
- 代價：同樣和 BIKE 相比，HQC 的公鑰比較大，密文大得更多。和 ML-KEM 相比，HQC 也比較大、實作效率比較差。[S6 p.3、p.11][S5 p.47]
- 另外兩個候選沒有被選上：
  - BIKE 傳輸量較小，但它的解碼失敗率分析到 2025 年才發表，還需要時間檢驗。[S6 p.8、p.11]
  - Classic McEliece 的公鑰非常大，限制了部分用途；NIST 也引用第 4 輪報告，說針對它的分析有顯著進展，「多少削弱」了「研究很久所以安全」的論點。[S6 p.10、p.11]
- 依使用者決定，簡報不點名這兩個候選。

### 2025 年 9 月 NIST 在考慮的修改

- NIST 列出幾項考慮採用的細部修改，例如改用加鹽的 FO 轉換、調整金鑰格式；這些都已出現在 HQC 規格 2025-08-22 版的修改紀錄裡。[S6 p.17–p.19][S5 p.2]
- 另有一個「一位元組確認碼」的提案，NIST 在 2025 年 9 月徵求意見中，見 [從 PKE 到 KEM](../concepts/hqc-kem-fo-transform.md)（查核日期 2026-11-23）。[S6 p.20、p.21]

## 常見誤解

- 誤解：「HQC 已經是正式標準了。」正確：依 S2 的說法，2025 年 3 月 HQC 只是「被選中」，NIST 預計 2027 年定案；2026-11-23 查 NIST 專案頁也還沒看到 FIPS 207 草案（查核日期 2026-11-23）。[S2 摘要、§2][S6 專案頁查核]
- 誤解：「既然 HQC 還沒定案，就等它定案再換加密。」正確：NIST 在 S2（2025-03）說，組織應該繼續轉換到 2024 年定案的標準（查核日期 2026-11-19）。[S2 §0]

## 相關頁面

- [HQC 總覽](../overview/hqc-overview.md)
- [後量子密碼學](../concepts/post-quantum-cryptography.md)
- [HQC 與 ML-KEM 比較](../comparisons/hqc-vs-ml-kem.md)
- [解碼失敗率](../concepts/decryption-failure-rate.md)
- [S2 來源摘要](../sources/S2-nist-news-hqc.md)
- [S6 來源摘要](../sources/S6-nist-fips207-robinson.md)
