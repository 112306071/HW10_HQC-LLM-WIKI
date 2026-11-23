# HQC LLM Wiki 索引

主題：HQC 是什麼？一個用錯誤更正碼做成的後量子加密。
讀者：知道公鑰／私鑰、但沒學過編碼理論的大學生。
規則見 [CLAUDE.md](../CLAUDE.md)；每份來源的討論紀錄在 [discussions/](../discussions/)。
簡報各張用到哪些頁見 [reports/slide_wiki_map.md](../reports/slide_wiki_map.md)；各頁 frontmatter 的 `used_in_slides` 是反向對應。

時間說明：下列各頁的一句話摘要若提到定位、時程或狀態，都是該頁來源當時的說法，不代表現況；查核日期寫在各行與各頁。

## 總覽
- [HQC 總覽](overview/hqc-overview.md) — HQC 是什麼、NIST 為什麼在 2025 年 3 月選它當 ML-KEM 的備援（S2 的說法，查核日期 2026-11-19）、HQC 怎麼運作。來源：S2, S4, S5, S6

## 概念
- [量子威脅](concepts/quantum-threat.md) — 為什麼量子電腦會危及今天的加密、為什麼現在就要換。來源：S1
- [後量子密碼學（PQC）](concepts/post-quantum-cryptography.md) — 連量子電腦也難解的新加密方法，和量子密碼學不同；HQC 是 NIST 選的第五個。來源：S1, S2
- [金鑰封裝機制（KEM）](concepts/kem.md) — 兩方在公開網路上交換機密前的「第一次握手」；HQC-KEM 的三個函式。來源：S2, S5
- [編碼式密碼](concepts/code-based-cryptography.md) — 故意加錯誤的加密；McEliece 藏結構，HQC 不藏。來源：S4, S5, S6
- [伴隨式解碼問題](concepts/syndrome-decoding.md) — HQC 的安全性建立在這類解碼問題上，S4（2016）說研究社群認為它很難（查核日期 2026-11-22）。來源：S4, S5
- [準循環碼](concepts/quasi-cyclic-codes.md) — 用一個向量代表整個矩陣，讓金鑰變小。來源：S4, S5
- [錯誤更正碼](concepts/error-correcting-codes.md) — 多寫一點就能修錯；漢明重量、最小距離、重複碼示例。來源：S5, S4, S2
- [HQC-PKE：金鑰產生、加密、解密](concepts/hqc-pke.md) — 2025-08-22 版的三個步驟，哪些公開、哪些秘密。來源：S5, S4
- [用小數字走一遍 HQC](concepts/hqc-toy-example.md) — 教學簡化版，一次解密成功、一次失敗（示例由腳本計算）。來源：S5
- [公開碼：Reed-Muller＋Reed-Solomon](concepts/concatenated-rm-rs.md) — 解密最後一步用的兩層公開碼。來源：S5, S4
- [從 PKE 到 KEM：FO 轉換](concepts/hqc-kem-fo-transform.md) — 重新加密檢查，對不上就給假金鑰。來源：S5, S6
- [解碼失敗率](concepts/decryption-failure-rate.md) — 故意加錯誤為什麼不會常常解錯。來源：S5, S4

## 實體
- [HQC 的標準化進度（FIPS 207）](entities/fips-207.md) — HQC 是第五個演算法、標準名稱 FIPS 207、NIST 為什麼選它；2025 年 3 月預估的時程與 2026-11-23 的狀態查核（查核日期 2026-11-23）。來源：S2, S6, S5

## 比較
- [HQC 與 ML-KEM 比較](comparisons/hqc-vs-ml-kem.md) — 同樣是 KEM，數學基礎不同；依 S2（2025-03）的說法，ML-KEM 是主力、HQC 是備援（查核日期 2026-11-19）；HQC 的大小與優缺點依 S5。來源：S2, S5
- [HQC 參數組](comparisons/hqc-parameter-sets.md) — HQC-1/3/5 的金鑰、密文大小與解碼失敗率（HQC 規格 2025-08-22 版）；S6 的較早數字記為衝突。來源：S5, S6

## 來源摘要
- [S1 NIST：What Is Post-Quantum Cryptography?](sources/S1-nist-pqc-explainer.md) — 官方科普問答頁，入門。
- [S2 NIST：NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption](sources/S2-nist-news-hqc.md) — 官方新聞稿，選 HQC 的理由與定位。
- [S4 Aguilar Melchor 等：Efficient Encryption from Random Quasi-Cyclic Codes](sources/S4-aguilar-melchor-qc-codes.md) — HQC 的原始論文（2016 預印本），設計想法與安全性。
- [S5 HQC 規格書 2025-08-22 版](sources/S5-hqc-spec-2025-08-22.md) — 官方規格：步驟、參數、大小、解碼失敗率、優缺點。
- [S6 NIST：FIPS 207: HQC-KEM 簡報](sources/S6-nist-fips207-robinson.md) — 2025 年 9 月會議簡報：標準名稱、為什麼選 HQC、考慮中的修改。

## 工具頁
- [術語表](glossary.md) — 中文、英文、一句話解釋。來源：S1, S2, S4, S5, S6
- [Wiki 紀錄](log.md) — ingest、lint、issue 等所有變動的時間紀錄。
