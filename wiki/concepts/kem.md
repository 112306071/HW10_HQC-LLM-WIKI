---
title: 金鑰封裝機制（KEM）
type: concept
sources: [S2]
related: [../overview/hqc-overview.md, ../comparisons/hqc-vs-ml-kem.md, ../sources/S2-nist-news-hqc.md]
spec_version: none
updated: 2026-11-20
status: draft
---

時間說明：本頁目前只根據 S2（NIST 新聞稿，2025-03-11）；KEM 的三個函式（金鑰產生、封裝、解封裝）要等 S5 補上，查核日期 2026-11-19。[S2 §3]

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

- 一般加密的主力 ML-KEM 和備援 HQC 都是 KEM。[S2 摘要、§3]
- 依 S2（2025-03）當時的說法，NIST 另有一份 KEM 實作建議的草案文件（SP 800-227），說明 KEM 的定義、性質與安全用法；它現在的狀態本 wiki 沒有查，也不展開（查核日期 2026-11-19）。[S2 §3]

## 常見誤解

- 誤解：「KEM 就是直接把訊息加密。」正確：NIST 把 KEM 形容成兩方交換機密資料「之前」的第一次握手。[S2 §3]

## 相關頁面

- [HQC 總覽](../overview/hqc-overview.md)
- [HQC 與 ML-KEM 比較](../comparisons/hqc-vs-ml-kem.md)
- [S2 來源摘要](../sources/S2-nist-news-hqc.md)
- [術語表](../glossary.md)
