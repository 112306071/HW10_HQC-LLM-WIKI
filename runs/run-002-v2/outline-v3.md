# run-002-v2 大綱 v3

- v3 修改原因：H2 使用者要求修第 18 張（B5 P4 PARTIAL：FIPS 207 少了「準備中、尚未定案」）。只改這一處。

- v2 修改原因：B3 第 1 次 O6 不通過（checks/B3-outline-v1-a1.json）：第 7 張圖示與 wiki 矛盾（擦完其實不少），另 3 筆 PARTIAL。

- 依據：runs/run-002-v2/queries/q-slides-01-21.md；寫法依 workflow/outline_template.md（v2）
- 規格版本：HQC 規格 2025-08-22 版（S5）
- 讀者：完全沒有背景的一般人（CLAUDE.md 討論紀錄 01）
- 顏色約定：公開值藍色、秘密值橘色（SPEC §9.4）
- 取捨（同 run-001）：第 20 張 5 題、第 21 張四句話（O5 每張最多 4 點）；第 19 張改標各頁「常見誤解」一節。
- 干擾因素：作者看過 run-001 的檢查紀錄；本大綱的寫法已吸收 run-001 的修正（見 CHANGELOG v2）。

## slide-01 | type: cover | 目標: —
標題：HQC 是什麼？用「故意加入的錯誤」保護量子時代的金鑰
定義：無
- NIST 在 2025 年選出的後量子加密方法，當 ML-KEM 的備援 [wiki: overview/hqc-overview.md#一句話定義]
圖示：一串 0 與 1，其中幾格被塗成「錯誤」的顏色，再被一把鑰匙還原。
講者備註：今天要講的是一種「故意把資料弄錯」的加密方法。聽起來很怪，看完就知道為什麼可行。

## slide-02 | type: objectives | 目標: G1–G5
標題：看完這份簡報，你會懂 4 件事
定義：無
- 為什麼量子電腦逼我們現在就換加密 [wiki: overview/hqc-overview.md#白話解釋]
- KEM：在公開網路上交換一把鑰匙的方法 [wiki: concepts/kem.md#一句話定義]
- HQC 怎麼用「故意加錯誤」完成金鑰產生、加密、解密 [wiki: concepts/code-based-cryptography.md#白話解釋; concepts/hqc-pke.md#白話解釋]
- HQC 和 ML-KEM 差在哪、為什麼選它當備援 [wiki: overview/hqc-overview.md#重點]
圖示：路線圖：為什麼 → 基礎 → 怎麼運作 → 好壞與現況 → 誤解與小測驗。
講者備註：四點對應五個學習目標：第 3 點同時涵蓋 G3（故意加錯誤）與 G4（三個步驟）。

## slide-03 | type: motivation | 目標: G1
標題：夠強的量子電腦可能解開今天許多加密，而且資料現在就可能被偷存
定義：量子電腦, 先收集、後解密
- 今天很多加密，靠「大數很難拆回兩個質數」 [wiki: concepts/quantum-threat.md#白話解釋]
- 傳統電腦估計要數十億年；量子電腦可能幾天甚至幾小時 [wiki: concepts/quantum-threat.md#白話解釋]
- 先收集、後解密：資料今天被偷存，將來再解開 [wiki: concepts/quantum-threat.md#先收集、後解密（harvest now, decrypt later）]
- 換加密常要 10–20 年，所以現在就要開始 [wiki: concepts/quantum-threat.md#兩個時間放在一起看：為什麼現在就要換]
圖示：名詞框「量子電腦：NIST 的科普說法是，它能同時篩選所有可能的因數，所以拆大數快得多」；時間軸：今天「上鎖的保險箱被偷走」→ 將來「量子電腦打開」；下方「換新加密：常要 10–20 年」。
講者備註：量子電腦能「同時篩選」所有可能的因數，所以拆大數快得多。時間估計是 S1（2026-02-27 更新版）的說法。

## slide-04 | type: concept | 目標: G1, G5
標題：HQC 是 NIST 選出的第五個演算法，當 ML-KEM 的備援
定義：NIST, 後量子密碼學, 量子密碼學, ML-KEM, HQC
- 後量子密碼：連量子電腦也難解的新數學鎖 [wiki: concepts/post-quantum-cryptography.md#一句話定義]
- NIST 是負責挑選、發布加密標準的機構 [wiki: concepts/post-quantum-cryptography.md#重點; concepts/post-quantum-cryptography.md#NIST 怎麼選出演算法]
- NIST 2024 年定了主力 ML-KEM，2025 年再選 HQC [wiki: concepts/post-quantum-cryptography.md#HQC：第五個演算法（S2 補充）]
- HQC 的數學和 ML-KEM 不同，所以適合當備援 [wiki: overview/hqc-overview.md#重點]
圖示：車子的輪胎（ML-KEM，2024，主力）與後車廂的備胎（HQC，2025，不同材料）。
講者備註：依 S2（2025-03）的說法，HQC 是備援，不是要取代 ML-KEM。後量子密碼靠數學，和靠量子物理的「量子密碼學」是兩回事。

## slide-05 | type: concept | 目標: G2
標題：KEM：在公開網路上安全地交換一把鑰匙
定義：金鑰封裝機制, KEM, 公鑰, 私鑰, 密文
- KEM：上網交換機密之前，先「握手」換一把鑰匙 [wiki: concepts/kem.md#一句話定義]
- 先做出公開的鎖（公鑰）和秘密的鑰匙（私鑰） [wiki: concepts/kem.md#HQC-KEM 的三個函式（HQC 規格 2025-08-22 版）]
- 用對方的公鑰鎖住新鑰匙；送出的盒子叫密文 [wiki: concepts/kem.md#HQC-KEM 的三個函式（HQC 規格 2025-08-22 版）]
- 對方用私鑰打開密文，雙方拿到同一把鑰匙 [wiki: concepts/kem.md#HQC-KEM 的三個函式（HQC 規格 2025-08-22 版）]
圖示：A、B 與中間誰都看得到的網路：① 打開的掛鎖＝公鑰（藍）② 鎖好的盒子＝密文（藍）③ 用私鑰打開（橘）→ 雙方有同一把新鑰匙。
講者備註：KEM 全名是金鑰封裝機制。它本身不加密訊息，只負責讓雙方拿到同一把鑰匙。

## slide-06 | type: example | 目標: G3
標題：錯誤更正碼：多傳一點，就能修正錯誤
定義：錯誤更正碼, 編碼, 位元, 漢明重量, 漢明距離
- 錯誤更正碼：先多寫一點（編碼），錯幾位也認得回 [wiki: concepts/error-correcting-codes.md#一句話定義; concepts/error-correcting-codes.md#白話解釋]
- 例：10 的每個位元（0 或 1）寫 3 次，成為 111000 [wiki: concepts/error-correcting-codes.md#示例：重複碼多數決（示例由腳本計算）]
- 錯 1 位，多數決仍解回 10；同組錯 2 位就解錯 [wiki: concepts/error-correcting-codes.md#示例：重複碼多數決（示例由腳本計算）]
- 漢明重量＝有幾個 1；漢明距離＝幾個位置不同 [wiki: concepts/error-correcting-codes.md#重點]
圖示：111000 → 第 4 位出錯 → 111100 → 多數決 → 10 ✓；001000 → 00 ✗；10110 重量 3；10110 與 11100 距離 2。
講者備註：像在吵雜的電話裡把每個數字講三遍。示例數字由 scripts/examples.py 算出。

## slide-07 | type: concept | 目標: G3
標題：核心點子：故意加錯誤，只有握有秘密金鑰的人能把錯誤縮小到修得回來
定義：編碼式密碼
- 編碼式密碼：故意加錯誤，把訊息藏在雜訊裡 [wiki: concepts/code-based-cryptography.md#一句話定義]
- 有秘密的人能把錯誤擦少，剩下的交給錯誤更正碼修 [wiki: concepts/code-based-cryptography.md#白話解釋]
- 沒秘密的人要猜錯在哪，組合多到試不完 [wiki: concepts/syndrome-decoding.md#白話解釋]
- 這種猜錯題的一般形式研究 50 多年仍無快解 [wiki: concepts/syndrome-decoding.md#白話解釋]
圖示：潑墨的紙：左邊用去墨水劑（秘密）擦掉大半，剩下的污點其實不算少，但錯誤更正碼很會改錯、修得好；右邊沒有去墨水劑，整片墨水。圖下：「HQC 用的形式，研究社群認為很難，但這不是數學證明」。
講者備註：「50 多年」是一般線性碼的解碼問題（2016 年論文的說法）；HQC 用的準循環版本，論文只說研究社群認為很難，不是證明。

## slide-08 | type: compare | 目標: G3
標題：McEliece 把結構藏起來，HQC 乾脆不藏
定義：McEliece 密碼系統, 公開碼, 向量
- 最早的 McEliece 密碼（1978）：把好解的碼藏起來 [wiki: concepts/code-based-cryptography.md#重點]
- 風險：藏起來的結構可能被挖出，許多變體被破 [wiki: concepts/code-based-cryptography.md#重點]
- HQC 不藏：修錯用的錯誤更正碼人人皆知，叫公開碼 [wiki: concepts/code-based-cryptography.md#白話解釋; concepts/code-based-cryptography.md#重點]
- 秘密是兩個「很短」的向量：一長串 0 與 1，只少數是 1 [wiki: concepts/code-based-cryptography.md#白話解釋]
圖示：左：鎖起來的解碼說明書（秘密＝藏起來的碼，風險：結構被挖出）；右：公開碼攤開給大家，秘密是 x、y 兩個很短的向量（沒有藏起來的結構可挖）。
講者備註：向量就是一長串數字，在 HQC 裡是一長串 0 與 1；「很短」指其中只有少數幾個 1。

## slide-09 | type: concept | 目標: G3
標題：準循環：用一個向量代表一整個矩陣
定義：矩陣, 準循環碼, 循環矩陣
- 矩陣是數字排成的方格表；循環矩陣每列右轉一格 [wiki: concepts/quasi-cyclic-codes.md#白話解釋]
- 所以整個矩陣只要記住第一列就夠 [wiki: concepts/quasi-cyclic-codes.md#白話解釋]
- HQC 用準循環碼，金鑰因此小很多 [wiki: concepts/quasi-cyclic-codes.md#重點]
- 格式有規律，但裡面的數字是隨機挑的 [wiki: concepts/quasi-cyclic-codes.md#常見誤解]
圖示：名詞框「準循環碼：用循環矩陣拼成的碼，只要幾個向量就能描述」；5×5 循環矩陣，第一列高亮，箭頭標出每列右轉一格、最右邊繞回最左邊。
講者備註：比喻是旋轉壽司的轉盤：記住一開始怎麼擺，之後每轉一格都推得出來。

## slide-10 | type: process | 目標: G4
標題：步驟一：金鑰產生——秘密是兩個很短的向量
定義：無
- 秘密 x、y：很短的向量（只有少數位置是 1） [wiki: concepts/hqc-pke.md#白話解釋]
- 公開 h：一串隨機的 0 與 1 [wiki: concepts/hqc-pke.md#重點]
- 公開 s：用 h 把 y 打散，再加上 x 算出來 [wiki: concepts/hqc-pke.md#白話解釋; concepts/hqc-pke.md#重點]
- 這裡的加法：逐位比對，相同得 0、不同得 1 [wiki: concepts/hqc-toy-example.md#白話解釋]
圖示：x、y（橘）與 h（藍）→ 公式 s = x + h·y → 公鑰：h、s（藍）；私鑰：x、y（橘）。圖下：「·」是一種乘法，超過長度的部分繞回開頭；「+」「−」都是逐位比對。
講者備註：橘色是秘密、藍色是公開，接下來三張都用同樣的顏色。之後解密只用到 y。規格實際上只存能重新產生 h、x、y 的種子。

## slide-11 | type: process | 目標: G4
標題：步驟二：加密——訊息被蓋上一大片雜訊
定義：無
- 寄件人另挑三個很短的隨機向量 r1、r2、e [wiki: concepts/hqc-pke.md#白話解釋]
- 密文分兩部分 u 和 v，兩者都會公開送出 [wiki: concepts/hqc-pke.md#重點]
- 訊息先用公開碼編碼（多寫一點），放進 v [wiki: concepts/hqc-pke.md#白話解釋]
- v 裡的訊息被一大片雜訊蓋住 [wiki: concepts/hqc-pke.md#白話解釋]
圖示：上路 r1、r2 → u = r1 + h·r2；下路 訊息 → 公開碼編碼 → 加上雜訊 s·r2 + e → v。u、v 藍色（公開的密文），r1、r2、e 灰色（不公開、不放進密文）。
講者備註：比喻：訊息被潑上一大片墨水，路上的人只看到墨水。

## slide-12 | type: process | 目標: G4
標題：步驟三：解密——剩下的錯誤小到修得回來
定義：無
- 收件人用秘密 y 和 u、v 計算，把雜訊擦少 [wiki: concepts/hqc-pke.md#白話解釋]
- 結果＝編碼後的訊息＋剩下的一些錯誤 [wiki: concepts/hqc-pke.md#白話解釋]
- 剩下的錯誤不超過修錯能力，公開碼就修得掉 [wiki: concepts/hqc-pke.md#白話解釋; concepts/hqc-pke.md#常見誤解]
- 沒有 y 的人，只看得到一大片雜訊 [wiki: concepts/hqc-pke.md#白話解釋]
圖示：v − u·y（y 橘色）→「編碼後的訊息＋x·r2 − r1·y + e」（剩下的錯誤，不算少）→ 公開碼修錯 → 訊息 ✓。
講者備註：比喻：去墨水劑把墨水擦到改錯字規則對付得了的程度；擦完還有不少污點，但規則本來就很會改錯。

## slide-13 | type: example | 目標: G3, G4
標題：用小數字走一遍 HQC：雜訊從 6 位降到 3 位就解得回來
定義：解密失敗
- 縮小版：向量長 13 位，公開碼是每個位元寫 3 次 [wiki: concepts/hqc-toy-example.md#準備（教學簡化版）]
- 加密時，蓋在訊息上的雜訊有 6 位是 1 [wiki: concepts/hqc-toy-example.md#步驟二：加密]
- 用秘密 y 解密後只剩 3 位，解回 1011 [wiki: concepts/hqc-toy-example.md#步驟三：解密（成功）]
- 換一個加密用的 e，錯誤擠在同一組就解密失敗 [wiki: concepts/hqc-toy-example.md#對照：解密失敗]
圖示：公開 h = 1011001110100，秘密 x、y 各只有 1 個 1；訊息 1011 → 編碼 111000111111；雜訊 100110011010（6 格亮）；解密後剩下 000001001100（3 格亮）→ 1011 ✓；對照 000001000101 → 1010 ✗。每 3 格一組，13 位的最後 1 位截掉。
講者備註：數字全由 scripts/examples.py --toy 算出；教學簡化版，沒有安全性。

## slide-14 | type: concept | 目標: G4
標題：公開碼：Reed-Muller 與 Reed-Solomon 串起來
定義：串接碼, Reed-Muller 碼, Reed-Solomon 碼
- 公開碼分兩層：外層 Reed-Solomon、內層 Reed-Muller [wiki: concepts/concatenated-rm-rs.md#一句話定義]
- 解碼時，先修每一小塊，再整串一起修 [wiki: concepts/concatenated-rm-rs.md#白話解釋]
- 一次只帶少量資料，換來很強的修錯能力 [wiki: concepts/concatenated-rm-rs.md#重點]
- 碼公開也沒關係：沒有秘密 y，雜訊多到修不了 [wiki: concepts/concatenated-rm-rs.md#常見誤解]
圖示：訊息 → 外層 Reed-Solomon（總清單）→ 切成小塊 → 每塊內層 Reed-Muller（重複的編號）；圖下「兩層串起來叫串接碼」。
講者備註：比喻：寄一套拼圖，先附總清單，每片再印上重複的編號。

## slide-15 | type: concept | 目標: G2, G4
標題：從加密到 KEM：多一道「重新加密檢查」
定義：HQC-PKE, HQC-KEM, Fujisaki-Okamoto 轉換, FO, 隱式拒絕
- HQC-KEM＝加密版 HQC-PKE 再包一層 FO 轉換 [wiki: concepts/hqc-kem-fo-transform.md#一句話定義]
- 收件人解出訊息後，自己再加密一次來比對 [wiki: concepts/hqc-kem-fo-transform.md#白話解釋]
- 對不上就默默給假鑰匙，這叫隱式拒絕 [wiki: concepts/hqc-kem-fo-transform.md#白話解釋]
- 防的是拿假密文來試探、套話的攻擊者 [wiki: concepts/hqc-kem-fo-transform.md#白話解釋]
圖示：名詞框「FO 轉換：Fujisaki-Okamoto 轉換的簡稱，把加密版包成金鑰封裝版，核心是重新加密檢查」；流程：收到密文 → 用私鑰解出 → 重新加密 → 一樣？是 → 真鑰匙；否 → 假鑰匙（不報錯）。
講者備註：比喻：拆開包裹後照說明書重包一次，包得一模一樣才收下。

## slide-16 | type: concept | 目標: G4
標題：解碼失敗率：小到可以忽略
定義：解碼失敗率, 安全等級, HQC-1／HQC-3／HQC-5
- 解碼失敗率：錯誤太多、公開碼修不回來的機率 [wiki: concepts/decryption-failure-rate.md#一句話定義]
- HQC 有三組設定 HQC-1、3、5：數字越大越安全 [wiki: comparisons/hqc-parameter-sets.md#一句話定義]
- HQC-1 的失敗率小於 2^-128，另兩組更小 [wiki: concepts/decryption-failure-rate.md#重點]
- 2^-128 約等於連丟 128 次硬幣都是正面 [wiki: concepts/decryption-failure-rate.md#白話解釋]
圖示：名詞框「安全等級：NIST 的安全分級，HQC-1、3、5 對應等級 1、3、5（舊名 hqc-128／192／256，規格書沒明說，由表格對照得知）」；128 枚硬幣全是正面。
講者備註：數字依 HQC 規格 2025-08-22 版。安全性證明也要求失敗率夠小。

## slide-17 | type: compare | 目標: G5
標題：HQC vs ML-KEM：數學不同，HQC 比較大、比較吃資源
定義：結構化格, 位元組
- HQC 靠錯誤更正碼，ML-KEM 靠結構化格 [wiki: comparisons/hqc-vs-ml-kem.md#重點]
- HQC-1：公鑰 2,241、密文 4,433 位元組 [wiki: comparisons/hqc-parameter-sets.md#重點]
- 規格書承認：HQC 比 ML-KEM 大、效率較差 [wiki: comparisons/hqc-vs-ml-kem.md#細節]
- 審查者認為：雖然較吃資源，但運作乾淨、安全 [wiki: comparisons/hqc-vs-ml-kem.md#細節]
圖示：名詞框「結構化格：ML-KEM 所根據的另一種數學」；長條圖（HQC 規格 2025-08-22 版，HQC-1）：公鑰 2,241、密文 4,433、共享金鑰 32 位元組；圖說「位元組是電腦計算資料量的單位；安全等級越高，金鑰和密文越大」。
講者備註：ML-KEM 的數字依使用者決定不放。「比 ML-KEM 大」是規格書（S5）的說法，「乾淨、安全」是 S2 引述的審查者看法。

## slide-18 | type: concept | 目標: G5
標題：NIST 選 HQC 當備援：失敗率分析穩定，代價是資料較大
定義：無
- 備援：萬一 ML-KEM 出問題，還有數學不同的 HQC [wiki: overview/hqc-overview.md#重點]
- 理由：失敗率分析穩定；金鑰產生比另一候選快 [wiki: entities/fips-207.md#NIST 為什麼選 HQC（S6，2025-09 的說法）]
- 代價：公鑰和密文比較大 [wiki: entities/fips-207.md#NIST 為什麼選 HQC（S6，2025-09 的說法）]
- 2025-03 預估 2027 定案；2026-11-23 查未見草案 [wiki: entities/fips-207.md#重點]
圖示：時間軸：2025-03 HQC 被選中 → 2025-09 已稱為 FIPS 207（NIST 為 HQC 準備的標準名稱，尚未定案）→ 2026-11-23 查核：NIST 專案頁未列出草案（只代表沒列）→ 2027 預估定案（2025-03 的預估）。下方小字：「和 ML-KEM 比，HQC 比較大、實作效率比較差」。
講者備註：理由是 S6（2025-09）的說法；「快」是和另一個候選比。依使用者決定不點名其他候選。

## slide-19 | type: misconception | 目標: G1–G5
標題：四個常見誤解
定義：無
- 誤解：HQC 要取代 ML-KEM。其實它是備援 [wiki: overview/hqc-overview.md#常見誤解]
- 誤解：等 HQC 定案再換。其實現在就該換 [wiki: entities/fips-207.md#常見誤解]
- 誤解：故意加錯誤會常解錯。其實失敗率極小 [wiki: concepts/decryption-failure-rate.md#常見誤解]
- 誤解：碼公開就不安全。秘密是很短的向量 [wiki: concepts/code-based-cryptography.md#常見誤解]
圖示：四張「誤解 ✗ → 正確 ✓」卡片；卡片小字：S2（2025-03）的說法，查核日期 2026-11-19；HQC-1 小於 2^-128（HQC 規格 2025-08-22 版）；安全性本來就不靠藏碼。
講者備註：第二點：NIST 說組織應繼續轉換到 2024 年定案的標準（S2，2025-03）。

## slide-20 | type: quiz | 目標: G1–G5
標題：小測驗：五題確認你懂了
定義：無
- 第 1 題（G1）：資料還沒被解開，為何現在就要換？ [wiki: concepts/quantum-threat.md#常見誤解]
- 第 2 題（G2）：KEM 結束後，雙方得到什麼？ [wiki: concepts/kem.md#HQC-KEM 的三個函式（HQC 規格 2025-08-22 版）]
- 第 3 題（G3）：10110 的漢明重量是多少？ [wiki: concepts/error-correcting-codes.md#示例：漢明重量與漢明距離（示例由腳本計算）]
- 第 4、5 題（G4、G5）：哪個是秘密？HQC 的角色？ [wiki: concepts/hqc-pke.md#重點; comparisons/hqc-vs-ml-kem.md#重點]
圖示：五題選擇題，點選後顯示答對／答錯與解釋；選項只用前面教過的詞。
講者備註：答案：1 先收集後解密；2 同一把共享金鑰；3 是 3；4 y；5 ML-KEM 的備援。

## slide-21 | type: summary | 目標: —
標題：四句話記住 HQC
定義：無
- HQC 是 ML-KEM 的備援，數學基礎不同 [wiki: overview/hqc-overview.md#重點]
- 故意加錯誤，只有握有秘密 y 的人能把它縮小 [wiki: concepts/hqc-pke.md#白話解釋]
- 剩下的錯誤交給公開碼修，失敗率小到可忽略 [wiki: concepts/decryption-failure-rate.md#一句話定義]
- 代價是金鑰和密文比 ML-KEM 大 [wiki: comparisons/hqc-vs-ml-kem.md#細節]
圖示：延伸閱讀：wiki 的 S1、S2、S4、S5、S6 來源摘要頁連結；小字「定位依 S2（2025-03）的說法」。
講者備註：原訂「五句話」，因每張最多 4 個重點改成四句。
