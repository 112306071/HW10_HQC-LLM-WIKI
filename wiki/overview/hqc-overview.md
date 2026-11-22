---
title: HQC 總覽
type: overview
sources: [S2, S4]
related: [../concepts/kem.md, ../concepts/code-based-cryptography.md, ../concepts/syndrome-decoding.md, ../concepts/quasi-cyclic-codes.md, ../sources/S4-aguilar-melchor-qc-codes.md, ../comparisons/hqc-vs-ml-kem.md, ../entities/fips-207.md, ../concepts/post-quantum-cryptography.md, ../sources/S2-nist-news-hqc.md]
spec_version: none
updated: 2026-11-22
status: draft
---

時間說明：本頁根據 S2（NIST 新聞稿，2025-03-11）與 S4（HQC 原始論文，2016-12 預印本），定位與評價都是各來源當時的說法；HQC 現行規格的細節要等 S5 補上，查核日期 2026-11-19（S2 部分）、2026-11-22（S4 部分）。[S2 摘要][S4 p.1]

## 一句話定義

HQC 是 NIST 在 2025 年 3 月選出的後量子加密演算法，屬於金鑰封裝機制（KEM），用來當一般加密主力 ML-KEM 的備援。[S2 書目資料、摘要、§3]

## 白話解釋

NIST 已經選了 ML-KEM 當一般加密的主力，用來對抗未來的量子電腦。[S2 摘要、§0]

但萬一哪天發現 ML-KEM 有弱點，就需要一個「數學基礎不同」的備案。HQC 就是這個備案：ML-KEM 建立在一種叫「結構化格」的數學上，HQC 則建立在「錯誤更正碼」上。[S2 摘要、§0、§1]

「錯誤更正碼」這個數學概念，在資訊安全領域已經用了數十年。[S2 §1] 錯誤更正碼是一種「多寫一點」的資料格式：任兩個合法的碼字之間差得夠遠，所以資料錯了少數幾個位置，仍能認出原本是哪個碼字。[S4 p.7]

> 比喻：ML-KEM 是車上正在用的輪胎，HQC 是後車廂的備胎。而且備胎用的是不同的材料，萬一哪天發現輪胎的材料有問題，還有備胎可以換。

## 重點

- 定位：依 S2（2025-03）的說法，HQC 是備援，不是要取代 ML-KEM；ML-KEM 仍是一般加密的推薦選擇（查核日期 2026-11-19）。[S2 §0]
- 為什麼要備援：HQC 和 ML-KEM 用的數學不同；萬一 ML-KEM 被發現弱點，還有數學不同的 HQC 可以用。[S2 摘要、§0]
- 取捨：HQC 比 ML-KEM 冗長，需要更多運算資源；但它運作乾淨、安全，審查者認為值得當備援。[S2 §1]
- 用途：和 ML-KEM 一樣，用來保護儲存的資料，以及在公開網路上傳送的資料。[S2 §0]

## 細節

### HQC 怎麼運作（S4 論文的核心想法，2016 版）

- HQC 用兩個碼：一個公開、好解碼的碼負責解密，一個隨機的碼負責製造雜訊、提供安全，所以不需要藏任何結構；詳見 [編碼式密碼](../concepts/code-based-cryptography.md)。[S4 p.4、p.5]
- 秘密金鑰是一對「很短」的向量，也就是大部分位置是 0、只有少數位置是 1。[S4 p.4、p.8、p.14]
- 加密：先用公開的碼把訊息編碼，再用公鑰和另一組很短的隨機向量把它蓋住，外加一個很短的錯誤向量。[S4 p.4、p.14]
- 解密：用秘密金鑰把雜訊降到公開的碼修得回來的程度，剩下「訊息的編碼＋一些錯誤」，再用公開的碼把錯誤修掉。[S4 p.4、p.14]
- 剩下的錯誤其實不少（2016 論文版約為三分之一的位元），所以公開的碼要選一次只帶少量資料、但能修很多錯的碼。[S4 p.5、p.18]
- 剩下的錯誤如果太多，就會解密失敗；論文在簡化假設下估算失敗機率（並用模擬佐證），挑參數讓它小到可以忽略。[S4 p.4、p.13、p.18、p.21]
- 安全性：論文證明，要破解 HQC，至少要能解準循環碼的解碼問題（判定版）；這類問題社群公認很難，但不是數學上證明不可能，限制見 [伴隨式解碼問題](../concepts/syndrome-decoding.md)。[S4 p.11、p.12、p.15]
- 金鑰能變小，是因為用了準循環結構；詳見 [準循環碼](../concepts/quasi-cyclic-codes.md)。[S4 p.7、p.11]
- 取捨：一次能加密的資料不多，但金鑰交換只需要送一把短的對稱金鑰，所以夠用。[S4 p.3、p.18]
- 這裡的步驟用的是 2016 年論文的說法；現行規格的步驟、符號與參數要等 S5。[S4 p.1]

### 其他頁面

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
- [編碼式密碼](../concepts/code-based-cryptography.md)
- [伴隨式解碼問題](../concepts/syndrome-decoding.md)
- [準循環碼](../concepts/quasi-cyclic-codes.md)
- [S4 來源摘要](../sources/S4-aguilar-melchor-qc-codes.md)
