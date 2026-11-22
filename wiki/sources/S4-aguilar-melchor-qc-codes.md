---
title: S4 來源摘要：Aguilar Melchor 等〈Efficient Encryption from Random Quasi-Cyclic Codes〉
type: source
sources: [S4]
related: [../concepts/code-based-cryptography.md, ../concepts/syndrome-decoding.md, ../concepts/quasi-cyclic-codes.md, ../overview/hqc-overview.md]
spec_version: none
updated: 2026-11-23
status: draft
---

時間說明：本頁內容都是 S4（2016-12 預印本）當時的說法，對攻擊、難度與研究現況的評價可能已經過時，查核日期 2026-11-22。[S4 p.1]

## 書目資料

- Carlos Aguilar Melchor、Olivier Blazy、Jean-Christophe Deneuville、Philippe Gaborit、Gilles Zémor，〈Efficient Encryption from Random Quasi-Cyclic Codes〉。
- 使用版本：arXiv:1612.05572v1，2016-12-16 上傳，PDF 標示 DRAFT（December 19, 2016），28 頁。
- 正式版：IEEE Transactions on Information Theory 64(5)，2018。沒有取得，內容可能和 arXiv 版不同。
- 網址：https://arxiv.org/abs/1612.05572
- 取得日期：2026-11-22，存於 `raw/S4-aguilar-melchor-qc-codes.pdf`（另有 pdftotext 轉出的 .txt）。依 SPEC §5.4 不進公開 repo，只留書目資料。
- 討論紀錄：[discussions/03-S4-aguilar-melchor-qc-codes.md](../../discussions/03-S4-aguilar-melchor-qc-codes.md)
- 引用方式：[S4 p.N] = PDF 第 N 頁（論文印的頁碼與 PDF 頁碼相同）。

## 重點

- 這是提出 HQC 的原始論文；HQC 的全名是 Hamming Quasi-Cyclic。[S4 p.1、p.14]
- 傳統的 McEliece 把好解碼的碼藏起來當秘密，但許多變體都被找出藏起來的結構而攻破。[S4 p.2]
- HQC 改用兩個碼：一個公開、好解碼的碼負責解密，一個隨機的雙循環碼負責安全，所以不需要藏任何結構。[S4 p.4、p.5、p.14]
- 秘密金鑰是一對很短的向量；解密時用它把雜訊降到公開的碼修得回來的程度，再交給公開的碼修掉。剩下的錯誤其實不少，所以要選能修很多錯的碼。[S4 p.4、p.5、p.14、p.18]
- 安全性建立在「解碼隨機準循環碼」這個問題上；論文證明要破解 HQC，至少要能解這個問題（判定版）。[S4 p.1、p.15]
- 準循環結構讓矩陣只用一個向量就能描述，金鑰因此變小。[S4 p.6、p.7、p.11]
- 解密有可能失敗；論文在簡化假設下估算失敗機率（並用模擬佐證），挑參數讓它小到可以忽略。[S4 p.4、p.13、p.18、p.21]
- 一次能加密的資料不多（加密率低），但金鑰交換、認證只需要送一把短的對稱金鑰，所以不是大問題。[S4 p.3、p.18]

## 更新了哪些頁

- 新增 [編碼式密碼](../concepts/code-based-cryptography.md)
- 新增 [伴隨式解碼問題](../concepts/syndrome-decoding.md)
- 新增 [準循環碼](../concepts/quasi-cyclic-codes.md)
- 修改 [HQC 總覽](../overview/hqc-overview.md)：補上 HQC 怎麼運作的核心想法
- 修改 [術語表](../glossary.md)：新增 6 個術語

## 可信度與限制

- 這是 HQC 設計者本人的論文，對「設計想法」的說法可信度高；但它是 2016 年的預印本，不是 HQC 規格。[S4 p.1]
- 論文自己的參數表與公開碼選擇見 p.18–p.22，本 wiki 不採用；做法與數字以 HQC 規格 2025-08-22 版（S5）為準。[S4 p.19、p.21]
- 論文的安全性證明建立在一類「社群認為很難」但沒有一般性證明的問題上，論文自己也承認，對準循環碼還沒有證明判定版和搜尋版一樣難（2016 年的說法，查核日期 2026-11-22）。[S4 p.11、p.12]
- 論文有不少篇幅在講另一個版本 RQC（秩度量），不是 HQC，wiki 不收。[S4 p.8、p.9、p.22]
- 證明細節、錯誤分布與失敗率的公式、和其他系統的比較，對一般讀者太深，wiki 只寫結論。[S4 p.15、p.16、p.24]
