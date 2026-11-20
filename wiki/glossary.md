---
title: 術語表
type: glossary
sources: [S1, S2]
spec_version: none
updated: 2026-11-20
status: draft
---

每個術語一句話解釋，詳細內容點「詳見」。

標「先備知識」的詞，讀者本來就知道，不另外定義。

| 中文 | English | 一句話解釋 | 詳見 |
| --- | --- | --- | --- |
| 量子電腦 | quantum computer | 利用量子世界特性來運算的新型電腦，未來可能解開今天的加密。[S1 Q2、Q4] | [量子威脅](concepts/quantum-threat.md) |
| 量子位元 | qubit | 量子電腦的基本資訊單位，相當於傳統電腦的位元，但很脆弱、容易出錯。[S1 Q6] | [量子威脅](concepts/quantum-threat.md) |
| 密碼學相關量子電腦 | cryptographically relevant quantum computer | 強到足以破解現有加密的量子電腦。[S1 Q4] | [量子威脅](concepts/quantum-threat.md) |
| 先收集、後解密 | harvest now, decrypt later | 現在先存下加密資料，等將來有能力時再解開的攻擊方式。[S1 Q8] | [量子威脅](concepts/quantum-threat.md) |
| 後量子密碼學 | post-quantum cryptography / PQC | 建立在傳統電腦和量子電腦都難解的數學問題上的加密方法。[S1 Q5] | [後量子密碼學](concepts/post-quantum-cryptography.md) |
| 量子密碼學 | quantum cryptography | 利用量子物理性質來加密的方法，和後量子密碼學是兩回事。[S1 Q12] | [後量子密碼學](concepts/post-quantum-cryptography.md) |
| 數位簽章 | digital signature | 用來驗證身分的密碼技術。[S1 Q5] | [後量子密碼學](concepts/post-quantum-cryptography.md) |
| HQC | HQC | NIST 在 2025 年選出的後量子加密演算法，建立在錯誤更正碼上；依 S2（2025-03）的說法，定位是 ML-KEM 的備援（查核日期 2026-11-19）。[S2 摘要、§1] | [HQC 總覽](overview/hqc-overview.md) |
| ML-KEM | ML-KEM | NIST 在 2024 年定案的一般加密演算法，建立在結構化格上；依 S2（2025-03）的說法，是一般加密的推薦選擇（查核日期 2026-11-19）。[S2 §0、§1] | [HQC 與 ML-KEM 比較](comparisons/hqc-vs-ml-kem.md) |
| 金鑰封裝機制 | key encapsulation mechanism / KEM | 兩方在公開網路上交換機密資料前，先做的「第一次握手」。[S2 §3] | [金鑰封裝機制](concepts/kem.md) |
| 錯誤更正碼 | error-correcting code | HQC 所根據的數學概念，已在資訊安全領域用了數十年。[S2 §1] | [HQC 總覽](overview/hqc-overview.md) |
| 結構化格 | structured lattices | ML-KEM 所根據的數學概念，和 HQC 的錯誤更正碼不同。[S1 Q5][S2 §1] | [HQC 與 ML-KEM 比較](comparisons/hqc-vs-ml-kem.md) |
| FIPS | FIPS | NIST 正式標準的名稱，例如 ML-KEM 的標準叫 FIPS 203。[S2 §2] | [HQC 的標準化進度](entities/fips-207.md) |
