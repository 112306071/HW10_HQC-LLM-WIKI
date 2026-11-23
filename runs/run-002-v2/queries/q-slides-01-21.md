# B1 查詢結果：run-002-v2

- 執行時間：2026-11-23 14:15（Asia/Taipei）
- 問題清單：workflow/questions.yaml（21 張，和 run-001 相同）
- wiki：`wiki-snapshot-1` 之後只改了 frontmatter 的 `used_in_slides`（run-001 發布時加的）、index.md 一行指向對應表、log.md 兩筆紀錄；概念頁內文完全相同（git diff wiki-snapshot-1 HEAD -- wiki 已確認）。
- 因此各題答案與 run-001 的 queries/q-slides-01-21.md 相同，以下沿用並重新核對每個 #章節 仍存在（check_outline.py 的 O2 會再驗一次）。
- 格式：每個答案附 wiki 頁#章節，以及該段的來源代碼。

## 查詢總結

- 21 張的問題都在 wiki 找得到答案，不需要 B1 → A1 補來源。
- 發現 1：questions.yaml 第 19 張列的 `concepts/common-misconceptions.md` 不存在（SPEC §4.5 預定頁，ingest 時沒有建）。四個誤解都在其他頁的「常見誤解」一節：overview、fips-207、decryption-failure-rate、code-based-cryptography、concatenated-rm-rs。大綱改標這些頁，不算 wiki 缺資料。
- 發現 2：第 17 張 SPEC §9.4 要的「大小長條圖」只能畫 HQC-1/3/5；ML-KEM 的數字依使用者決定沒有收進 wiki，圖上不放 ML-KEM。
- 發現 3：第 21 張「延伸閱讀」要連到 sources/ 下 5 頁；S3 不在 wiki，不列。

---

## q-01 封面
- 一句話：HQC 是 NIST 在 2025 年 3 月選出的後量子加密演算法，屬於 KEM，當 ML-KEM 的備援。→ overview/hqc-overview.md#一句話定義 [S2]

## q-02 學習目標與路線圖
- 五個目標 G1–G5 見 questions.yaml；路線：為什麼 → 基礎 → 怎麼運作 → 好壞與現況 → 確認理解（SPEC §9.1）。
- wiki 依據：overview/hqc-overview.md#一句話定義、#白話解釋 [S2]

## q-03 量子威脅
- 量子電腦威脅哪一類密碼？依賴「大數分解很難」的加密；傳統電腦要數十億年，夠強的量子電腦可能幾天或幾小時。→ concepts/quantum-threat.md#白話解釋、#重點 [S1 Q4]
- 什麼是先收集後解密？攻擊者現在先存加密資料，等量子電腦出現再解開。→ concepts/quantum-threat.md#先收集、後解密（harvest now, decrypt later） [S1 Q8]
- 為什麼現在就要換？新演算法普及要 10–20 年，量子電腦何時出現無法預測；NIST 建議立即開始轉換。→ concepts/quantum-threat.md#兩個時間放在一起看：為什麼現在就要換 [S1 Q6、Q7、Q11]

## q-04 PQC 與 HQC 的位置
- PQC 是什麼？建立在傳統電腦和量子電腦都難解的數學問題上的加密；不是量子密碼學。→ concepts/post-quantum-cryptography.md#一句話定義、#常見誤解 [S1 Q5、Q12]
- HQC 排在哪？NIST 選出的第五個演算法、第四輪唯一被選中；之前三個已在 2024 年成為標準，一般加密用 ML-KEM（FIPS 203）。→ concepts/post-quantum-cryptography.md#HQC：第五個演算法（S2 補充） [S2 §0、§2]
- 扮演什麼角色？ML-KEM 的備援，數學基礎不同（錯誤更正碼 vs 結構化格）。→ overview/hqc-overview.md#白話解釋、#重點 [S2 摘要、§0、§1]

## q-05 KEM
- KEM 做什麼？兩方在公開網路上交換機密資料前的「第一次握手」。→ concepts/kem.md#一句話定義 [S2 §3]
- 三個函式：金鑰產生（公開封裝金鑰＋秘密解封裝金鑰）、封裝（只用公開金鑰得到共享金鑰 K 和密文）、解封裝（用秘密金鑰從密文算回同一把 K）。→ concepts/kem.md#HQC-KEM 的三個函式（HQC 規格 2025-08-22 版） [S5 p.26–p.28]
- 比喻：打開的掛鎖寄出去，對方把新鑰匙鎖進盒子寄回。→ concepts/kem.md#白話解釋

## q-06 錯誤更正碼
- 什麼是錯誤更正碼？「多寫一點」的格式，碼字彼此差得夠遠，錯少數位置仍能認回。→ concepts/error-correcting-codes.md#一句話定義 [S5 p.8][S4 p.7]
- 漢明重量：一串 0/1 有幾個 1；漢明距離：兩串有幾個位置不同。→ concepts/error-correcting-codes.md#重點 [S5 p.7、p.8]
- 示例（腳本計算）：`10` → `111000`，錯第 4 位收到 `111100`，多數決解回 `10`；同組錯 2 位收到 `001000`，解成 `00`。`10110` 重量 3；`10110` 與 `11100` 距離 2。→ concepts/error-correcting-codes.md#示例：重複碼多數決（示例由腳本計算）、#示例：漢明重量與漢明距離（示例由腳本計算） [示例由腳本計算]

## q-07 為什麼解碼隨機的碼很難
- 伴隨式解碼問題在 1978 年被證明是 NP 完全；研究超過 50 年，已知最好的攻擊時間隨錯誤個數指數成長（2016 論文的說法）。→ concepts/syndrome-decoding.md#重點 [S4 p.10、p.12]
- 比喻：長開關面板，只告訴你哪幾盞燈亮。→ concepts/syndrome-decoding.md#白話解釋
- 核心點子：故意加錯誤，有秘密的人修得回來，其他人修不回來。→ concepts/code-based-cryptography.md#白話解釋 [S4 p.2、p.4]
- 限制：準循環版本「社群認為很難」不是證明。→ concepts/syndrome-decoding.md#白話解釋 [S4 p.11、p.12]

## q-08 McEliece vs HQC
- McEliece（1978）把好解碼的碼藏起來當秘密；許多換用其他碼的變體被找出結構攻破。→ concepts/code-based-cryptography.md#重點 [S4 p.2]
- HQC 不藏：公開好解碼的碼負責解密，隨機碼負責安全，秘密是一對很短的向量。→ concepts/code-based-cryptography.md#白話解釋、#重點 [S4 p.4、p.5、p.14]

## q-09 準循環
- 循環矩陣每列是上一列往右轉一格，只要存第一列；HQC 用準循環碼縮短金鑰。→ concepts/quasi-cyclic-codes.md#白話解釋、#重點 [S4 p.6、p.7、p.11]
- 比喻：旋轉壽司轉盤。→ concepts/quasi-cyclic-codes.md#白話解釋
- 有規律不代表藏結構：裡面的向量是隨機挑的。→ concepts/quasi-cyclic-codes.md#常見誤解 [S4 p.4、p.5、p.11]

## q-10 金鑰產生
- 秘密 x、y：很短的向量（只有少數位置是 1）；公開 h（由種子產生）與 s = x + h·y。→ concepts/hqc-pke.md#白話解釋、#重點 [S5 p.23]
- 解密只用 y。→ concepts/hqc-pke.md#重點 [S5 p.25]

## q-11 加密
- 挑很短的 r1、r2、e；u = r1 + h·r2；v = C.Encode(m) + (s·r2 + e)。訊息藏在 v。→ concepts/hqc-pke.md#白話解釋、#重點 [S5 p.24]
- r1、r2、e 不公開、不放進密文。→ concepts/hqc-pke.md#重點 [S5 p.24]

## q-12 解密
- v − u·y = 訊息的編碼 + (x·r2 − r1·y + e)；剩下的錯誤不超過公開碼 C 的修錯能力就能解回。→ concepts/hqc-pke.md#白話解釋、#細節 [S5 p.22、p.25]
- 剩下的錯誤其實不少，要靠很會修錯的公開碼。→ concepts/hqc-pke.md#常見誤解 [S5 p.22、p.25]

## q-13 小數字示例（腳本計算）
- 長 13、重複 3 次碼、訊息 `1011` → `111000111111`；h = `1011001110100`。→ concepts/hqc-toy-example.md#準備（教學簡化版）
- x = `0010000000000`、y = `0000000100000`、s = `1100100101100`。→ concepts/hqc-toy-example.md#步驟一：金鑰產生
- 雜訊 s·r2 + e = `100110011010`（6 位是 1）；v = `011110100101`。→ concepts/hqc-toy-example.md#步驟二：加密
- 解密後剩下錯誤 `000001001100`（3 位），多數決解回 `1011`；換 e 後錯誤擠在同組，解成 `1010`。→ concepts/hqc-toy-example.md#步驟三：解密（成功）、#對照：解密失敗
- 全部 [示例由腳本計算]。

## q-14 公開碼
- 串接碼：外層 Reed-Solomon（以位元組為單位）、內層 Reed-Muller（再重複 3 或 5 次）。→ concepts/concatenated-rm-rs.md#一句話定義、#重點 [S5 p.17]
- 為什麼公開也沒關係？安全性不靠隱藏這個碼；訊息被 s·r2 + e 遮住，要先用 y 把雜訊降下來。→ concepts/concatenated-rm-rs.md#常見誤解 [S5 p.6、p.22、p.43]
- 比喻：拼圖總清單＋每片重複編號。→ concepts/concatenated-rm-rs.md#白話解釋

## q-15 FO 轉換
- 重新加密檢查：解出訊息後自己再加密一次比對；不一樣就默默給假金鑰（隱式拒絕）。→ concepts/hqc-kem-fo-transform.md#白話解釋 [S5 p.27、p.28]
- 目的：擋住能送自製密文去試的攻擊者（IND-CCA2）。→ concepts/hqc-kem-fo-transform.md#白話解釋 [S5 p.12、p.26]
- 確認碼提案只在 wiki，簡報不提（討論紀錄 05 Q2a）。

## q-16 解碼失敗率
- 定義：剩下錯誤太多、公開碼修不回來的機率。→ concepts/decryption-failure-rate.md#一句話定義 [S5 p.22、p.29]
- HQC-1 < 2^-128、HQC-3 < 2^-192、HQC-5 < 2^-256（HQC 規格 2025-08-22 版）。→ concepts/decryption-failure-rate.md#重點 [S5 p.29]
- 為什麼要這麼小？安全性證明要求解碼失敗率夠小。→ concepts/decryption-failure-rate.md#重點 [S5 p.44]
- 2^-128 ≈ 連續丟 128 次硬幣都正面（本 wiki 的說明）。→ concepts/decryption-failure-rate.md#白話解釋

## q-17 HQC vs ML-KEM
- HQC-1/3/5 大小（位元組，HQC 規格 2025-08-22 版）：公鑰 2,241／4,514／7,237；密文 4,433／8,978／14,421；共享金鑰 32。→ comparisons/hqc-parameter-sets.md#重點 [S5 p.29]
- 數學基礎：HQC 錯誤更正碼、ML-KEM 結構化格。→ comparisons/hqc-vs-ml-kem.md#重點 [S2 §1]
- 取捨：HQC 比較大、需要更多運算資源，但運作乾淨、安全，值得當備援。→ comparisons/hqc-vs-ml-kem.md#重點、#細節 [S2 §1][S5 p.47]

## q-18 NIST 為什麼選 HQC
- 為什麼要備援：萬一 ML-KEM 被發現弱點，還有數學不同的 HQC。→ overview/hqc-overview.md#重點 [S2 摘要、§0]（不在 questions.yaml 列的 wiki 頁，大綱要加標）
- 選 HQC 的理由（2025-09 的說法）：解碼失敗率分析穩定；和另一個候選相比金鑰產生與解封裝快很多。代價：資料比較大。→ entities/fips-207.md#NIST 為什麼選 HQC（S6，2025-09 的說法） [S6 p.3、p.8、p.11]
- 注意：「快」是跟另一個候選比，不是跟 ML-KEM 比；跟 ML-KEM 比，HQC 比較大、比較慢。
- 標準化：2025-03 預估約一年後草案、2027 定案；2025-09 已用 FIPS 207 名稱；2026-11-23 查 NIST 專案頁未見草案。→ entities/fips-207.md#重點 [S2 摘要、§2][S6 p.1][S6 專案頁查核]

## q-19 四個常見誤解
- HQC 要取代 ML-KEM？不，HQC 是備援。→ overview/hqc-overview.md#常見誤解 [S2 §0]
- 應該等 HQC 再遷移？不，NIST 說繼續轉換到 2024 年的標準。→ entities/fips-207.md#常見誤解 [S2 §0]
- 故意加錯誤會讓解密常常出錯？不，失敗率 < 2^-128。→ concepts/decryption-failure-rate.md#常見誤解 [S5 p.29]
- 碼是公開的，不就不安全？不，安全性不靠藏碼，秘密是很短的向量。→ concepts/code-based-cryptography.md#常見誤解 [S4 p.14]；concepts/concatenated-rm-rs.md#常見誤解 [S5 p.6]

## q-20 小測驗（5 題，各對應一個目標）
- G1：為什麼現在就要換？先收集後解密。→ concepts/quantum-threat.md#常見誤解 [S1 Q8]
- G2：KEM 的結果是什麼？雙方得到同一把共享金鑰。→ concepts/kem.md#HQC-KEM 的三個函式（HQC 規格 2025-08-22 版） [S5 p.27、p.28]
- G3：漢明重量是什麼？→ concepts/error-correcting-codes.md#重點 [S5 p.7]
- G4：哪個是秘密？y（x、y）。→ concepts/hqc-pke.md#重點 [S5 p.23]
- G5：HQC 的角色？ML-KEM 的備援。→ comparisons/hqc-vs-ml-kem.md#重點 [S2 §0]

## q-21 總結
- 五句話分別取自 overview、code-based-cryptography、hqc-pke、decryption-failure-rate、hqc-vs-ml-kem。
- 延伸閱讀：sources/ 下 S1、S2、S4、S5、S6 五頁。
