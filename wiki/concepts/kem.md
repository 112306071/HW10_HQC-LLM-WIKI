---
title: 金鑰封裝機制（KEM）
type: concept
sources: [S2, S5]
related: [hqc-kem-fo-transform.md, hqc-pke.md, ../sources/S5-hqc-spec-2025-08-22.md, ../overview/hqc-overview.md, ../comparisons/hqc-vs-ml-kem.md, ../sources/S2-nist-news-hqc.md]
spec_version: none
updated: 2026-11-23
status: draft
used_in_slides: [2, 5, 20]
---

時間說明：本頁的定位說法來自 S2（NIST 新聞稿，2025-03-11），查核日期 2026-11-19；三個函式依 HQC 規格 2025-08-22 版（S5）。[S2 §3][S5 p.26]

## 一句話定義

金鑰封裝機制（key encapsulation mechanism，KEM）是兩方要在公開網路上交換機密資料前，先做的「第一次握手」。[S2 §3]

## 白話解釋

KEM 用在公開網路上。NIST 把它形容成：兩方要交換機密資料之前，先做的一種「第一次握手」。[S2 §3]

> 比喻：網路像一條誰都能偷看的郵路。A 寄給 B 一個「打開的掛鎖」。任何人都拿得到這個掛鎖，但只有 A 有鑰匙能打開它。B 把一把新做的鑰匙放進盒子，用掛鎖「喀」一聲鎖上寄回去。路上的人只看到鎖住的盒子，只有 A 打得開。於是 A 和 B 都拿到了同一把新鑰匙，之後就用它來加密對話。

## 重點

- KEM 用在公開網路上，是兩方交換機密資料前的「第一次握手」。[S2 §3]
- HQC 和 ML-KEM 都是 KEM。[S2 §3]
- HQC 和 ML-KEM 這兩個 KEM 的用途，是保護儲存的資料，以及在公開網路上傳送的資料。[S2 §0]

## 細節

### HQC-KEM 的三個函式（HQC 規格 2025-08-22 版）

- 金鑰產生（Keygen）：做出一把公開的封裝金鑰和一把秘密的解封裝金鑰。[S5 p.26]
- 封裝（Encaps）：寄件人只用對方的公開金鑰，就同時得到一把共享金鑰 K 和一份密文，把密文送出去。[S5 p.27]
- 解封裝（Decaps）：收件人用秘密金鑰從密文算回同一把 K；HQC 在這一步會做「重新加密檢查」，見 [從 PKE 到 KEM](hqc-kem-fo-transform.md)。[S5 p.28]
- 用詞差異：S5 第 6 頁把 KEM 寫成「Key Exchange Mechanism」（金鑰交換機制），但它的函式是封裝與解封裝，S2 與 S5 第 12 頁也都寫 key encapsulation mechanism；本 wiki 用「金鑰封裝機制」。[S5 p.6、p.12、p.26][S2 §3]

### 其他

- 一般加密的主力 ML-KEM 和備援 HQC 都是 KEM。[S2 摘要、§3]
- 依 S2（2025-03）當時的說法，NIST 另有一份 KEM 實作建議的草案文件（SP 800-227），說明 KEM 的定義、性質與安全用法；它現在的狀態本 wiki 沒有查，也不展開（查核日期 2026-11-19）。[S2 §3]

## 常見誤解

- 誤解：「KEM 就是直接把訊息加密。」正確：NIST 把 KEM 形容成兩方交換機密資料「之前」的第一次握手。[S2 §3]

## 相關頁面

- [HQC 總覽](../overview/hqc-overview.md)
- [HQC 與 ML-KEM 比較](../comparisons/hqc-vs-ml-kem.md)
- [S2 來源摘要](../sources/S2-nist-news-hqc.md)
- [從 PKE 到 KEM：FO 轉換](hqc-kem-fo-transform.md)
- [HQC-PKE](hqc-pke.md)
- [S5 來源摘要](../sources/S5-hqc-spec-2025-08-22.md)
- [術語表](../glossary.md)
