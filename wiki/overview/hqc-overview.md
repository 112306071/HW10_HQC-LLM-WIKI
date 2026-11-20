---
title: HQC 總覽
type: overview
sources: [S2]
related: [../concepts/kem.md, ../comparisons/hqc-vs-ml-kem.md, ../entities/fips-207.md, ../concepts/post-quantum-cryptography.md, ../sources/S2-nist-news-hqc.md]
spec_version: none
updated: 2026-11-20
status: draft
---

時間說明：本頁目前只根據 S2（NIST 新聞稿，2025-03-11），HQC 怎麼運作要等 S4、S5 補上，查核日期 2026-11-19。[S2 摘要]

## 一句話定義

HQC 是 NIST 在 2025 年 3 月選出的後量子加密演算法，屬於金鑰封裝機制（KEM），用來當一般加密主力 ML-KEM 的備援。[S2 書目資料、摘要、§3]

## 白話解釋

NIST 已經選了 ML-KEM 當一般加密的主力，用來對抗未來的量子電腦。[S2 摘要、§0]

但萬一哪天發現 ML-KEM 有弱點，就需要一個「數學基礎不同」的備案。HQC 就是這個備案：ML-KEM 建立在一種叫「結構化格」的數學上，HQC 則建立在「錯誤更正碼」上。[S2 摘要、§0、§1]

「錯誤更正碼」這個數學概念，在資訊安全領域已經用了數十年；它到底是什麼，要等 S4、S5 補上（查核日期 2026-11-19）。[S2 §1]

> 比喻：ML-KEM 是車上正在用的輪胎，HQC 是後車廂的備胎。而且備胎用的是不同的材料，萬一哪天發現輪胎的材料有問題，還有備胎可以換。

## 重點

- 定位：依 S2（2025-03）的說法，HQC 是備援，不是要取代 ML-KEM；ML-KEM 仍是一般加密的推薦選擇（查核日期 2026-11-19）。[S2 §0]
- 為什麼要備援：HQC 和 ML-KEM 用的數學不同；萬一 ML-KEM 被發現弱點，還有數學不同的 HQC 可以用。[S2 摘要、§0]
- 取捨：HQC 比 ML-KEM 冗長，需要更多運算資源；但它運作乾淨、安全，審查者認為值得當備援。[S2 §1]
- 用途：和 ML-KEM 一樣，用來保護儲存的資料，以及在公開網路上傳送的資料。[S2 §0]

## 細節

- HQC 和 ML-KEM 都屬於金鑰封裝機制（KEM），見 [金鑰封裝機制](../concepts/kem.md)。[S2 §3]
- 兩者的詳細比較見 [HQC 與 ML-KEM 比較](../comparisons/hqc-vs-ml-kem.md)。[S2 §1]
- HQC 是 NIST 選出的第五個後量子演算法；標準化的時程見 [HQC 的標準化進度](../entities/fips-207.md)。[S2 §2]

## 常見誤解

- 誤解：「HQC 選出來，就是要取代 ML-KEM。」正確：依 S2（2025-03）的說法，HQC 是備援，ML-KEM 仍是一般加密的推薦選擇（查核日期 2026-11-19）。[S2 §0]
- 誤解：「既然還有 HQC，那就等 HQC 定案再換加密。」正確：NIST 在 S2（2025-03）說，組織應該繼續轉換到 2024 年定案的標準（查核日期 2026-11-19）。[S2 §0]

## 相關頁面

- [金鑰封裝機制（KEM）](../concepts/kem.md)
- [HQC 與 ML-KEM 比較](../comparisons/hqc-vs-ml-kem.md)
- [HQC 的標準化進度](../entities/fips-207.md)
- [後量子密碼學](../concepts/post-quantum-cryptography.md)
- [S2 來源摘要](../sources/S2-nist-news-hqc.md)
