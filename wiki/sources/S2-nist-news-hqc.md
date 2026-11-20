---
title: S2 來源摘要：NIST〈NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption〉
type: source
sources: [S2]
related: [../overview/hqc-overview.md, ../concepts/kem.md, ../entities/fips-207.md, ../comparisons/hqc-vs-ml-kem.md, ../concepts/post-quantum-cryptography.md]
spec_version: none
updated: 2026-11-20
status: draft
---

## 書目資料

- NIST 新聞稿，〈NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption〉，2025-03-11 發布，2025-03-20 更新（日期取自網頁的發布資訊，登記在 raw/sources.yaml；raw 轉檔只保留正文，沒有日期，網址含 2025/03）。
- 網址：https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption
- 取得日期：2026-11-19，存於 `raw/S2-nist-news-hqc.md`
- 討論紀錄：[discussions/02-S2-nist-news-hqc.md](../../discussions/02-S2-nist-news-hqc.md)
- 引用方式：[S2 摘要] = 頁首三點摘要；[S2 §0] = 第一個內文小標題「Encryption Based on Two Math Problems」之前的導言，包含中間那行「What is post-quantum cryptography? Read an explainer.」連結列之後、NIST 後量子密碼計畫負責人 Dustin Moody 的談話（那行是連結，不當成小標題）；[S2 §1] = Encryption Based on Two Math Problems；[S2 §2] = Present and Future Standards；[S2 §3] = Draft Guidance for KEM Algorithms。

## 重點

以下是 S2（2025-03-11 發布）當時的說法，其中的時程是當時的預估，查核日期 2026-11-19。[S2 摘要、§0–§3]

- NIST 選出 HQC 當 ML-KEM 的備援；ML-KEM 是一般加密的主力演算法。[S2 摘要]
- HQC 不是要取代 ML-KEM，ML-KEM 仍是一般加密的推薦選擇；NIST 建議組織繼續轉換到 2024 年定案的標準。[S2 §0]
- 選 HQC 的原因是它和 ML-KEM 用的數學不同：ML-KEM 建立在「結構化格」上，HQC 建立在「錯誤更正碼」上。萬一 ML-KEM 被發現弱點，還有退路。[S2 摘要、§0、§1]
- HQC 比 ML-KEM 冗長，需要更多運算資源；但它運作乾淨、安全，審查者認為值得當備援。[S2 §1]
- HQC 和 ML-KEM 都是金鑰封裝機制（KEM），用在公開網路上，像是兩方交換機密資料前的「第一次握手」。[S2 §3]
- HQC 是第五個被選中的演算法，也是第四輪候選中唯一被選中的；之前選的四個裡，有三個已成為正式標準，其中 ML-KEM 的標準叫 FIPS 203。[S2 §2]
- 時程是 2025 年 3 月的預估：約一年後發布 HQC 的標準草案，經過 90 天公開意見期後，在 2027 年定案（查核日期 2026-11-19）。[S2 摘要、§2]
- 新聞稿最後提到 NIST 另有一份 KEM 實作建議的草案文件（SP 800-227）；和本主題的教學目標無關，wiki 不展開（查核日期 2026-11-19）。[S2 §3]

## 更新了哪些頁

- 新增 [HQC 總覽](../overview/hqc-overview.md)
- 新增 [金鑰封裝機制（KEM）](../concepts/kem.md)
- 新增 [HQC 的標準化進度](../entities/fips-207.md)
- 新增 [HQC 與 ML-KEM 比較](../comparisons/hqc-vs-ml-kem.md)
- 修改 [後量子密碼學](../concepts/post-quantum-cryptography.md)：補上 HQC 是第五個演算法
- 修改 [術語表](../glossary.md)：新增 6 個術語

## 可信度與限制

- 這是 NIST 官方新聞稿，對「選了誰、為什麼、定位是什麼」的說法可信度高；但它是新聞稿，沒有任何演算法細節或數字大小。[S2 §1]
- 時程是 2025 年 3 月的預估，不是現況；實際狀態要等 S6 ingest 時查核（查核日期 2026-11-19）。[S2 摘要、§2]
- 「HQC 比較冗長、比較吃資源」只是定性的說法，沒有給數字；具體大小要看 S5。[S2 §1]
- 沒有點名 FIPS 204、205 裡的演算法，也沒有提到 HQC 標準的編號。[S2 §2]
- 「量子電腦能很快篩選大量可能的解」和 S1 一樣是科普式的簡化說法。[S2 §1]
