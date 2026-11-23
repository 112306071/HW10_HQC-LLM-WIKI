# 投影片 ↔ wiki 對應表

由 `scripts/publish.py` 產生，2026-11-23T13:55:20+08:00。簡報：`runs/run-001-v1/slides-v4.html` → `slides/index.html`（run-001-v1）。
來源代碼取自各 wiki 頁 frontmatter 的 `sources`；反向對應寫在各頁 frontmatter 的 `used_in_slides`。

| # | 標題 | wiki 頁 | 來源 |
| --- | --- | --- | --- |
| 1 | HQC 是什麼？ 用「故意加入的錯誤」保護量子時代的金鑰 | [overview/hqc-overview.md](../wiki/overview/hqc-overview.md) | S2, S4, S5, S6 |
| 2 | 看完這份簡報，你會懂 4 件事 | [overview/hqc-overview.md](../wiki/overview/hqc-overview.md)<br>[concepts/kem.md](../wiki/concepts/kem.md)<br>[concepts/code-based-cryptography.md](../wiki/concepts/code-based-cryptography.md)<br>[concepts/hqc-pke.md](../wiki/concepts/hqc-pke.md) | S2, S4, S5, S6 |
| 3 | 夠強的量子電腦可能解開今天許多加密，而且資料現在就可能被偷存 | [concepts/quantum-threat.md](../wiki/concepts/quantum-threat.md) | S1 |
| 4 | HQC 是 NIST 選出的第五個演算法，當 ML-KEM 的備援 | [concepts/post-quantum-cryptography.md](../wiki/concepts/post-quantum-cryptography.md)<br>[overview/hqc-overview.md](../wiki/overview/hqc-overview.md) | S1, S2, S4, S5, S6 |
| 5 | KEM：在公開網路上安全地交換一把鑰匙 | [concepts/kem.md](../wiki/concepts/kem.md) | S2, S5 |
| 6 | 錯誤更正碼：多傳一點，就能修正錯誤 | [concepts/error-correcting-codes.md](../wiki/concepts/error-correcting-codes.md) | S5, S4, S2 |
| 7 | 核心點子：故意加錯誤，只有握有秘密金鑰的人能把錯誤縮小到修得回來 | [concepts/code-based-cryptography.md](../wiki/concepts/code-based-cryptography.md)<br>[concepts/syndrome-decoding.md](../wiki/concepts/syndrome-decoding.md) | S4, S5, S6 |
| 8 | McEliece 把結構藏起來，HQC 乾脆不藏 | [concepts/code-based-cryptography.md](../wiki/concepts/code-based-cryptography.md) | S4, S5, S6 |
| 9 | 準循環：用一個向量代表一整個矩陣 | [concepts/quasi-cyclic-codes.md](../wiki/concepts/quasi-cyclic-codes.md) | S4, S5 |
| 10 | 步驟一：金鑰產生——秘密是兩個很短的向量 | [concepts/hqc-pke.md](../wiki/concepts/hqc-pke.md)<br>[concepts/hqc-toy-example.md](../wiki/concepts/hqc-toy-example.md) | S5, S4 |
| 11 | 步驟二：加密——訊息被蓋上一大片雜訊 | [concepts/hqc-pke.md](../wiki/concepts/hqc-pke.md) | S5, S4 |
| 12 | 步驟三：解密——剩下的錯誤小到修得回來 | [concepts/hqc-pke.md](../wiki/concepts/hqc-pke.md) | S5, S4 |
| 13 | 用小數字走一遍 HQC：雜訊從 6 位降到 3 位就解得回來 | [concepts/hqc-toy-example.md](../wiki/concepts/hqc-toy-example.md) | S5 |
| 14 | 公開碼：Reed-Muller 與 Reed-Solomon 串起來 | [concepts/concatenated-rm-rs.md](../wiki/concepts/concatenated-rm-rs.md) | S5, S4 |
| 15 | 從加密到 KEM：多一道「重新加密檢查」 | [concepts/hqc-kem-fo-transform.md](../wiki/concepts/hqc-kem-fo-transform.md) | S5, S6 |
| 16 | 解碼失敗率：小到可以忽略 | [concepts/decryption-failure-rate.md](../wiki/concepts/decryption-failure-rate.md)<br>[comparisons/hqc-parameter-sets.md](../wiki/comparisons/hqc-parameter-sets.md) | S5, S4, S6 |
| 17 | HQC vs ML-KEM：數學不同，HQC 比較大、比較吃資源 | [comparisons/hqc-vs-ml-kem.md](../wiki/comparisons/hqc-vs-ml-kem.md)<br>[comparisons/hqc-parameter-sets.md](../wiki/comparisons/hqc-parameter-sets.md) | S2, S5, S6 |
| 18 | NIST 選 HQC 當備援：失敗率分析穩定，代價是資料較大 | [overview/hqc-overview.md](../wiki/overview/hqc-overview.md)<br>[entities/fips-207.md](../wiki/entities/fips-207.md) | S2, S4, S5, S6 |
| 19 | 四個常見誤解 | [overview/hqc-overview.md](../wiki/overview/hqc-overview.md)<br>[entities/fips-207.md](../wiki/entities/fips-207.md)<br>[concepts/decryption-failure-rate.md](../wiki/concepts/decryption-failure-rate.md)<br>[concepts/code-based-cryptography.md](../wiki/concepts/code-based-cryptography.md) | S2, S4, S5, S6 |
| 20 | 小測驗：五題確認你懂了 | [concepts/quantum-threat.md](../wiki/concepts/quantum-threat.md)<br>[concepts/kem.md](../wiki/concepts/kem.md)<br>[concepts/error-correcting-codes.md](../wiki/concepts/error-correcting-codes.md)<br>[concepts/hqc-pke.md](../wiki/concepts/hqc-pke.md)<br>[comparisons/hqc-vs-ml-kem.md](../wiki/comparisons/hqc-vs-ml-kem.md) | S1, S2, S5, S4 |
| 21 | 四句話記住 HQC | [overview/hqc-overview.md](../wiki/overview/hqc-overview.md)<br>[concepts/hqc-pke.md](../wiki/concepts/hqc-pke.md)<br>[concepts/decryption-failure-rate.md](../wiki/concepts/decryption-failure-rate.md)<br>[comparisons/hqc-vs-ml-kem.md](../wiki/comparisons/hqc-vs-ml-kem.md) | S2, S4, S5, S6 |
