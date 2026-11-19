---
title: S1 來源摘要：NIST〈What Is Post-Quantum Cryptography?〉
type: source
sources: [S1]
related: [../concepts/quantum-threat.md, ../concepts/post-quantum-cryptography.md]
spec_version: none
updated: 2026-11-19
status: draft
---

## 書目資料

- NIST，〈What Is Post-Quantum Cryptography?〉，2024-08-13 發布，2026-02-27 更新。
- 網址：https://www.nist.gov/cybersecurity/what-post-quantum-cryptography （會轉址到 https://www.nist.gov/cybersecurity-and-privacy/what-post-quantum-cryptography ）
- 取得日期：2026-11-19，存於 `raw/S1-nist-pqc-explainer.md`
- 討論紀錄：[discussions/01-S1-nist-pqc-explainer.md](../../discussions/01-S1-nist-pqc-explainer.md)
- 引用方式：[S1 Qn]。Q0 是開頭導言，Q1–Q12 依頁面上問答標題的順序編號（對照表見討論紀錄 01）。

## 重點

以下是 S1（2026-02-27 更新版）的內容摘要，其中的時間估計與進度都是當時的說法，查核日期 2026-11-19。[S1 Q0–Q12]

- 很多加密方法靠「大數分解很難」來保護資料，夠強的量子電腦會讓這個前提失效。[S1 Q4]
- 傳統電腦估計要數十億年才能解開的問題，量子電腦可能幾天到幾小時就能解開。[S1 Q4]
- 量子電腦何時出現沒有定論，估計從幾年到幾十年；需要好幾千個量子位元，而量子位元很容易出錯。[S1 Q6]
- 新演算法從標準化到普及要 10–20 年，所以要提前準備。[S1 Q7]
- 「先收集、後解密」讓今天傳送的加密資料將來也可能曝光。[S1 Q8]
- 後量子密碼學建立在傳統與量子電腦都難解的數學問題上，用途包括一般加密與數位簽章。[S1 Q5]
- 後量子密碼學和量子密碼學是兩回事：前者靠數學，後者靠量子物理。[S1 Q12]
- NIST 從 2016 年開始徵選，收到 69 個候選演算法，2024 年發布前三個標準，並建議立即開始轉換。[S1 Q9、Q11]

## 更新了哪些頁

- 新增 [量子威脅](../concepts/quantum-threat.md)
- 新增 [後量子密碼學](../concepts/post-quantum-cryptography.md)
- 新增 [術語表](../glossary.md) 的 7 個術語

## 可信度與限制

- 這是 NIST 官方寫給一般大眾的科普頁，可信度高，但刻意簡化，沒有任何演算法細節。[S1 Q0]
- 講量子威脅時沒有點名 RSA 或「公鑰加密」，只說「依賴大數分解的加密」；這些名稱要由其他來源補。[S1 Q4]
- Q12 提到橢圓曲線，但只是當作「PQC 用到的數學可以很古老」的例子，不是在說哪種加密會被量子電腦破解；wiki 不採用這個例子（見討論紀錄 01 第 4 節）。[S1 Q12]
- 「量子電腦能同時篩選所有可能的因數」是 NIST 的科普說法，不是量子演算法的精確描述。[S1 Q4]
- 演算法數量只寫到「最初選出的四個」，之後新增的演算法要看其他來源。[S1 Q5]
