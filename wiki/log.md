# Wiki 紀錄（只能往後追加）

列出所有紀錄：`grep "^## \[" wiki/log.md`

## [2026-11-19 23:17] issue | 來源連結查核（S1–S8）
- 2026-11-19 22:5x 用 curl 逐一下載 S1–S8 與 NIST PQC 專案頁，全部回應 HTTP 200，但 S7 的內容不是論文。
- S1：原網址 `/cybersecurity/what-post-quantum-cryptography` 會轉址到 `/cybersecurity-and-privacy/what-post-quantum-cryptography`，內容相同（標題、2026-02-27 更新日期一致）。raw 檔記錄兩個網址。
- S4：規格寫的是 IEEE Trans. Inf. Theory 2018 正式版；可公開取得的是 arXiv 1612.05572 預印本（28 頁）。本來就只用來講概念（SPEC §5.2），改用 arXiv 版，書目資料兩者都列。
- S7：TCHES 文章頁（tches.iacr.org/…/9700）回傳「Making sure you're not a bot!」驗證頁，抓不到論文。IACR ePrint 2021/1485 是同一篇論文（標題、作者相同），但 PDF 對程式回傳 403。依 SPEC §5.4 第 5 點停下來詢問使用者；使用者於 2026-11-19 以瀏覽器手動下載 ePrint 版 PDF（40 頁），放入 raw/。
- NIST PQC 專案頁只寫「HQC 於 2025-03-11 被選中」，沒有 FIPS 207 草案發布的消息（查核日期 2026-11-19）。

## [2026-11-19 23:17] issue | 規格書 §7 的 v1 流程圖在匯出時遺失
- SPEC.md 原文 §7 的嵌入圖沒有隨 Markdown 匯出。
- 處理：依 §7.1 節點表與 §7.2 graph.yaml 重畫成 mermaid，存於 workflow/graph.md；SPEC.md 該處改為指向 workflow/graph.md。待使用者在第一次跑簡報流程前確認（SPEC §0.1）。

## [2026-11-19 23:30] ingest | S1 NIST：What Is Post-Quantum Cryptography?
- 討論紀錄：discussions/01-S1-nist-pqc-explainer.md（使用者確認 2026-11-19 23:28）
- 新增：sources/S1-nist-pqc-explainer.md, concepts/quantum-threat.md, concepts/post-quantum-cryptography.md, glossary.md
- 修改：index.md
- lint：見 runs/ingest/checks/A4-lint-S1-a*.json

## [2026-11-19 23:33] issue | lint_wiki.py L7 誤判日期為參數（checker_bug）
- A4-lint-S1-a1 的 L7 腳本部分把 sources/S1 的日期「2026-02-27」裡的「2-27」當成 2^-27，判定該頁含參數數字。
- 保留原紀錄不改；修正 PARAM_NUM 正規式（指數前不可緊接數字或連字號），並在 selftest 加入日期樣本。紀錄於 runs/ingest/checker_bugs.yaml。

## [2026-11-19 23:33] lint | S1 ingest 後 lint 第 1 次不通過，修正
- 檢查紀錄：runs/ingest/checks/A4-lint-S1-a1.json → FAIL
- 修改 concepts/quantum-threat.md：時間估計都標明「S1 2026-02-27 更新版」與查核日期（L7 語意）
- 修改 concepts/post-quantum-cryptography.md、glossary.md：補來源標記、拆短說明句（L2）

## [2026-11-19 23:37] lint | S1 ingest 後 lint 第 2 次不通過，修正
- 檢查紀錄：runs/ingest/checks/A4-lint-S1-a2.json → FAIL（L7 語意：「仍在考慮中」沒標時間點）
- 修改 concepts/post-quantum-cryptography.md：頁首加時間說明；「仍在考慮中」改寫為「S1 寫作時的狀態」並加查核日期
- 修改 sources/S1-nist-pqc-explainer.md：重點清單前加時間說明（同類問題一併處理）
- 觀察：腳本 L7 的時效詞清單（尚未、預計、草案、即將）沒有「仍在」，這次只有語意檢查抓到。

## [2026-11-19 23:43] lint | S1 lint 第 3 次通過；依檢查員備註更正一句
- 檢查紀錄：runs/ingest/checks/A4-lint-S1-a3.json → PASS
- 語意檢查員在 notes 指出（不屬 L7/L8）：sources/S1 寫「S1 沒有點名橢圓曲線」不正確，S1 Q12 有提到橢圓曲線。
- 更正 sources/S1-nist-pqc-explainer.md〈可信度與限制〉：改成「講量子威脅時沒有點名 RSA 或公鑰加密」，另說明 Q12 的橢圓曲線例子為何不採用。
- 這是 lint 通過後的修改，下一次 A4（S2）會對整個 wiki 重跑 lint。

## [2026-11-20 16:45] issue | 使用者調整範圍：聚焦 HQC 技術，來源減為 5 份
- 依據：discussions/02-S2-nist-news-hqc.md 第 7 節使用者回覆（「我的主題是HQC 請著重於此……如果有些資料對於學會HQC沒幫助 幫我刪掉 反正至少五個就好」）。
- 來源：保留 S1、S2、S4、S5、S6；S3、S7、S8 不 ingest。S3 列為備用（S4–S6 若取不到就用 S3 補足 5 份）。raw/S7-guo-dont-reject-this.pdf 依 CLAUDE.md 規則 1 保留在 raw/，不登記、不 ingest。
- 簡報：22 張 → 21 張。舊 3、4 合併；舊 5 簡化為「HQC 的位置」；刪除舊 19「計時攻擊」；新增「用小數字走一遍 HQC」；誤解頁改用 HQC 技術相關的誤解。G1、G5 改寫。
- 預定頁：移除 implementation-security、nist-pqc-process、ml-kem、bike-and-classic-mceliece；新增 concepts/hqc-toy-example。
- 修改檔案：SPEC.md（開頭加變更說明，§1.1、§2.1、§2.2、§4.5、§5、§7.3、§9、§10.2、§12.2、§13）、workflow/questions.yaml、CLAUDE.md。
- 影響：SPEC §13.3 的 R1 由「至少 20 頁」改為「至少 15 頁」；R3 改為 5 份。

## [2026-11-20 16:47] ingest | S2 NIST：NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption
- 討論紀錄：discussions/02-S2-nist-news-hqc.md（使用者確認 2026-11-20 16:42）
- 新增：sources/S2-nist-news-hqc.md, overview/hqc-overview.md, concepts/kem.md, entities/fips-207.md, comparisons/hqc-vs-ml-kem.md
- 修改：concepts/post-quantum-cryptography.md（補上 HQC 是第五個）, glossary.md（新增 6 個術語）, index.md
- 依討論決定不新增：entities/nist-pqc-process.md、entities/ml-kem.md
- lint：見 runs/ingest/checks/A4-lint-S2-a*.json

## [2026-11-20 16:48] issue | A4-lint-S2-a1 是不完整的檢查（操作失誤）
- 原本想先試跑 lint_wiki.py，誤以為 `--attempt 0` 是試跑；腳本把 0 當成「未指定」，正式寫出 runs/ingest/checks/A4-lint-S2-a1.json。
- 這份只有腳本部分（L1–L9 腳本全 PASS），沒有併入 L7、L8 的語意檢查，不算一次完整的 A4。依 SPEC §10.5 保留原檔不刪不改，trace 不為它記 A4 結果。
- 完整的 A4 從 a2 開始：子代理語意檢查 → runs/ingest/semantic/A4-S2-a2.json，再以 --semantic 併入 A4-lint-S2-a2.json。
- 觀察：lint_wiki.py 沒有「只檢查、不寫檔」的模式，之後可考慮加 --dry-run（還沒改）。

## [2026-11-20 16:51] lint | S2 ingest 後 lint 第 2 次不通過，修正
- 檢查紀錄：runs/ingest/checks/A4-lint-S2-a2.json → FAIL（L7 語意 4 處：「ML-KEM 仍是推薦選擇」「SP 800-227 草案」只靠頁首時間說明，句中沒寫來源時間點）
- 修改 overview/hqc-overview.md、comparisons/hqc-vs-ml-kem.md、concepts/kem.md：這 4 處都改成「依 S2（2025-03）的說法……（查核日期 2026-11-19）」
- 依檢查員 notes 一併修正（不屬 L7/L8）：
  - 講得比來源肯定：「一個出問題不會連帶拖垮另一個」「HQC 不會跟著出事」「完全不同」改成「萬一 ML-KEM 有弱點，還有 HQC 可用」；兩個比喻同步改弱。
  - kem.md：用途改成「HQC 和 ML-KEM 這兩個 KEM 的用途」；「不是交換本身」這個推論改回 NIST 原話「第一次握手」。
  - post-quantum-cryptography.md：拿掉「HQC 就是 S1 說的那類演算法」的推論，改成兩份來源各說什麼。
  - hqc-vs-ml-kem.md：「NIST 認為」改成原文的「審查者認為」。
  - sources/S1、S2〈書目資料〉：註明發布日期取自網頁發布資訊（raw/sources.yaml），raw 轉檔沒有日期。
- 未處理：檢查員指出 entities/fips-207.md 的檔名暗示編號是 FIPS 207，但 S2 沒提編號。檔名沿用 SPEC §4.5 的預定名稱，頁面標題與頁首已註明編號待 S6 查核，S6 ingest 時再確認。

## [2026-11-20 16:54] lint | S2 ingest 後 lint 第 3 次不通過，達重試上限，交使用者決定
- 檢查紀錄：runs/ingest/checks/A4-lint-S2-a3.json → FAIL（L7 語意 3 處：glossary.md 的 HQC、ML-KEM 兩列，index.md「比較」一節，「ML-KEM 主力、HQC 備援」沒標 S2 時間點與查核日期）
- 檢查紀錄編號已到 a3，但 a1 是不完整的腳本試跑（見前一筆 issue），完整的 A4 實際跑了 2 次。依 graph.yaml 的 on_limit: escalate_to_user，狀態記為 ESCALATED，停下來請使用者決定是否允許第 4 次。
- 觀察：S1、S2 兩次 ingest 失敗的都是 L7 語意（時效說法沒標時間點），而且都是修了一處又漏了別處。

## [2026-11-20 16:56] issue | 使用者同意 S2 lint 第 4 次（超過重試上限）
- 使用者聽完說明後回覆「可以修」：允許 A3 再修一次、A4 跑第 4 次。紀錄照實寫為 attempt 4。
- 範圍：補 L7 的 3 處，並一併修正檢查員 notes 的 3 點（「要求」→「鼓勵」、「收到 69 個」→「69 個通過門檻」、帶 S2 標記的編輯決定句）。

## [2026-11-20 16:58] lint | 依 lint a3 修正（使用者同意的第 4 次）
- glossary.md 的 HQC、ML-KEM 兩列與 index.md「總覽」「比較」兩行：補上「依 S2（2025-03）的說法……（查核日期 2026-11-19）」。
- post-quantum-cryptography.md：「NIST 也要求考慮」改成原文的「鼓勵」（S1 Q9：encouraged）。
- sources/S1：「收到 69 個候選演算法」改成「69 個候選演算法通過門檻」（S1 Q9：cleared the bar）。
- post-quantum-cryptography.md、entities/fips-207.md、comparisons/hqc-vs-ml-kem.md、sources/S2：把「依討論紀錄 02……」這類編輯決定從帶 [S2] 標記的事實句拆出來，改成不帶來源標記的短句。
- 未處理：entities/fips-207.md 的檔名（同前一筆，S6 時確認）。

## [2026-11-20 17:00] lint | S2 lint 第 4 次不通過，再次交使用者決定
- 檢查紀錄：runs/ingest/checks/A4-lint-S2-a4.json → FAIL（L7 語意 2 處：index.md「總覽」「實體」兩行寫了 S2／2025 年 3 月，但沒有「查核日期」）
- 「總覽」那行是第 4 次修正時新改的，漏加查核日期；「實體」那行從 a2 起就存在，前兩次語意檢查沒有指出。語意檢查的判定前後不完全一致，反思時可討論。
- 觀察：S2 四次失敗全是 L7 語意。腳本 L7 只認「尚未、預計、草案、即將」，抓不到「備援、主力、仍是」這類定位說法，只能靠語意檢查一輪一輪補。

## [2026-11-20 17:04] lint | 依 lint a4 修正（使用者同意的第 5 次）
- 使用者回覆「可以修」，同意第 5 次。
- 這次先自己全頁掃描「備援、主力、推薦、仍、預估、預計、草案、時程、目前、尚未、即將、制定、被選中、定案」：有頁首時間說明的頁都已涵蓋；沒有頁首說明的 index.md 只缺語意檢查點名的兩行。
- index.md：「總覽」「實體」兩行補上「（S2 的說法，查核日期 2026-11-19）」，並在開頭加時間說明。

## [2026-11-20 17:07] lint | S2 lint 第 5 次通過；依檢查員備註小修
- 檢查紀錄：runs/ingest/checks/A4-lint-S2-a5.json → PASS（使用者同意超過上限後的第 5 次；a1 為不完整試跑，完整 A4 共 4 次，失敗 3 次，全是 L7 語意）
- 依 notes 小修（不屬 L7/L8）：sources/S2 寫清楚 [S2 §0] 的範圍（含連結列之後 Moody 的談話）；hqc-overview「ML-KEM 是主力」補 [S2 摘要]；post-quantum-cryptography 把兩份來源合併的推論標明「本 wiki 的整理」。
- 這是 lint 通過後的修改，下一次 A4（S4）會對整個 wiki 重跑 lint。

## [2026-11-20 17:10] workflow-change | v1 → v1.1：A3 後加腳本自查 A3S，L7 腳本加定位詞
- 依據：S1、S2 ingest 的 A4 失敗幾乎都是 L7 語意（時效、定位說法沒標查核日期），v1 腳本抓不到「主力、備援、仍是」這類詞。使用者看過說明後決定「現在改」。
- 修改：scripts/lint_wiki.py（L7 詞表、時間說明段涵蓋規則、--dry-run、selftest）、workflow/graph.yaml（v1.1，新增 A3S）、workflow/graph.md（重畫，修改處綠框）、CLAUDE.md、SPEC.md 開頭註記。
- v1 快照：workflow/v1/（graph.yaml、graph.md、lint_wiki.py.snapshot）。
- 回頭驗證：S2 a3、a4 語意檢查指出的 5 行，新腳本全部抓到；a2 的 4 處因頁首時間說明而不抓，與 a3 起的語意判定一致。細節見 workflow/CHANGELOG.md。
- 新規則對目前 wiki 跑 dry-run：PASS。

## [2026-11-22 18:23] issue | 簡報第 7 張標題修改（討論紀錄 03 問題 1）
- 原標題「核心點子：故意加錯誤，只有懂結構的人修得回來」描述的是 McEliece；HQC 的公開碼人人皆知，關鍵是秘密金鑰能把錯誤縮小。
- 使用者選 (a)，改為「核心點子：故意加錯誤，只有握有秘密金鑰的人能把錯誤縮小到修得回來」。修改 SPEC.md §9.2、workflow/questions.yaml。
- 另：討論紀錄 03 的「建立時間」原寫 18:25，與 trace（A2 於 18:20 完成）不符，更正為 18:20。

## [2026-11-22 18:26] ingest | S4 Aguilar Melchor 等：Efficient Encryption from Random Quasi-Cyclic Codes
- 討論紀錄：discussions/03-S4-aguilar-melchor-qc-codes.md（使用者確認 2026-11-22 18:22；問題 1a、2a、3b）
- 新增：sources/S4-aguilar-melchor-qc-codes.md, concepts/code-based-cryptography.md, concepts/syndrome-decoding.md, concepts/quasi-cyclic-codes.md
- 修改：overview/hqc-overview.md（HQC 怎麼運作的核心想法）、glossary.md（新增 6 個術語）、index.md
- 不寫：RQC、證明與公式細節、2016 年參數表、2016 年版公開碼 BCH＋重複碼（問題 3b，等 S5）、IND-CPA 遊戲（問題 2a）
- 時效：新頁都在頁首加時間說明（S4 為 2016-12 預印本，查核日期 2026-11-22），沒等 lint 抓。

## [2026-11-22 18:32] lint | S4 ingest 後 lint 第 1 次不通過，修正
- 檢查紀錄：runs/ingest/checks/A4-lint-S4-a1.json → FAIL（腳本 L1–L9 全 PASS；A3S 自查也是第 1 次就 PASS）
- L7 語意 3 處：sources/S4 的時間說明放在〈重點〉下、涵蓋不到〈可信度與限制〉；index.md 伴隨式一行「公認很難」沒標 S4 時間點與查核日期；glossary.md 錯誤更正碼一列「用了數十年」沒標 S2 時間點與查核日期（S2 時期就有，當時未被指出）。
- 依 v1.1 的做法，先對全 wiki 掃「小錯、公認、小到可以忽略、四分之一、多寫一點、大部分雜訊、至今、研究超過、數十年、最好的攻擊」再修，不只修被點名處。
- 修正（L7）：sources/S4 的時間說明移到頁首並涵蓋全頁；限制一節那句再補時間點與查核日期；index、glossary 兩行補來源時間點與查核日期。
- 依檢查員 notes 修正內容錯誤（不屬 L7/L8，但比 L7 重要）：
  - 「解密後剩下一個小錯誤」與原文不符：S4 p.5、p.18 說剩下的錯誤約占三分之一位元，所以要用能修很多錯的碼。overview、code-based-cryptography、sources/S4 三頁改寫；比喻「擦完只剩幾個小錯字」改成「擦完還有不少錯字，但規則本來就很會改錯」。
  - 「公認很難」頁碼改為 p.11；「一個問題」改為「一類問題」（證明用到兩種長度的版本）。
  - 「小到可以忽略」補 p.13、p.21；雙循環碼「提供安全」補 p.5；NP 完全的年份補 p.26。
  - sources/S4「參數、符號和之後的規格不同」是 S4 無法支持的比較，改成「本 wiki 不採用論文的參數表與公開碼，現行做法等 S5 查核」；「約四分之一篇幅講 RQC」是自行估計，改成不帶比例。
  - 錯誤更正碼的白話說明改成貼近 S4 p.7 定義（碼字之間差得夠遠，錯少數位置仍認得出來），拿掉原文沒有的「途中／收方」情境。

## [2026-11-22 18:39] lint | S4 lint 第 2 次通過；依檢查員備註小修
- 檢查紀錄：runs/ingest/checks/A4-lint-S4-a2.json → PASS（A3S 兩次都第 1 次就 PASS；A4 共 2 次，失敗 1 次，L7 語意 3 處）
- 依 notes 小修（不屬 L7/L8）：
  - overview、code-based-cryptography 頁首拿掉「現行規格（2025-08-22 版）」：這個版本號來自本 wiki 規則，已 ingest 的來源不支持。
  - 「公認很難」的說明分開寫：一般線性碼研究超過 50 年；HQC 用的準循環版本，論文只說社群認為很難。overview、syndrome-decoding 的安全性句改寫為「至少要能解準循環碼的解碼問題（判定版）」，並指向限制說明。
  - 頁碼與措辭：秘密金鑰補 p.4；「兩種長度」改「兩種大小」；「讓攻擊失效」改「變得沒有效率」（原文 inefficient）；參數表頁碼改 p.18–p.22；失敗率補「簡化假設、模擬佐證」（p.18）。
  - syndrome-decoding、quasi-cyclic-codes 頁首時間說明改成「這類評價」，涵蓋範圍更明確。
- 這是 lint 通過後的修改，下一次 A4（S5）會對整個 wiki 重跑。

## [2026-11-23 00:17] ingest | S5 HQC 規格書 2025-08-22 版
- 討論紀錄：discussions/04-S5-hqc-spec-2025-08-22.md（使用者確認 2026-11-22 18:46；問題 1a、2a、3a）
- 新增：sources/S5-hqc-spec-2025-08-22.md, concepts/error-correcting-codes.md, concepts/hqc-pke.md, concepts/hqc-toy-example.md, concepts/concatenated-rm-rs.md, concepts/hqc-kem-fo-transform.md, concepts/decryption-failure-rate.md, comparisons/hqc-parameter-sets.md
- 修改：concepts/kem.md（三個函式、用詞差異）、overview/hqc-overview.md（運作方式改以 2025-08-22 版為主，S4 降為由來）、comparisons/hqc-vs-ml-kem.md（HQC 大小、S5 自列限制；仍不收 ML-KEM 數字）、concepts/syndrome-decoding.md、concepts/quasi-cyclic-codes.md、glossary.md（新增 11 個術語）、index.md
- scripts/examples.py：新增 --toy（問題 1a），長度 13、重複碼的教學簡化版 HQC，示範一次成功、一次失敗；selftest 檢查剩下的錯誤等於 x·r2 + r1·y + e、成功與失敗結果。第 6 張的重複碼示例也一併寫進 error-correcting-codes。
- 用詞差異（不是事實衝突）：S5 p.6 把 KEM 寫成 Key Exchange Mechanism；S2 與 S5 的函式名稱都是封裝。wiki 用「金鑰封裝機制」，兩種寫法都記在 kem.md 與 sources/S5。
- 舊名稱：S5 實作章節仍用 HQC-128/192/256，沒有明說等於 HQC-1/3/5；wiki 依安全等級對照並標明是 wiki 的整理。SPEC §5.2 提到的舊大小 2,249 位元組不在 S5，不寫。
- 寫作時自行發現並修正：hqc-pke 的比喻原寫「擦掉大部分墨水、只剩少數污點」，和 S4 a1 已指出的「剩下的錯誤不少」矛盾，改成「擦到規則對付得了的程度，其實還有不少污點」。

## [2026-11-23 00:21] lint | S5 寫入後腳本自查（A3S）第 1 次不通過，修正
- A3S（v1.1 新增的節點）擋下 L2 共 13 處缺來源標記：參數表的 6 列資料、表格前說明 1 行、FO 頁編號清單 2 項與函式清單引言 1 行、PKE 頁三步驟中的 2 項、錯誤更正碼頁 1 段。
- 補上 [S5 p.N] 或 [示例由腳本計算] 後 A3S 第 2 次 PASS，再進 A4。A3S 不寫 checks JSON，次數記在 trace。

## [2026-11-23 00:30] lint | S5 ingest 後 lint 第 1 次不通過，修正
- 檢查紀錄：runs/ingest/checks/A4-lint-S5-a1.json → FAIL（腳本 L1–L9 全 PASS）
- L7 語意 3 處：syndrome-decoding 新增的 S5 評價沒有 S5 的查核日期（頁首時間說明只涵蓋 S4）；error-correcting-codes 寫了 HQC-1 向量長度但 spec_version 是 none；glossary 的 Reed-Muller 列沒標規格版本。
- L8 語意 1 處：code-based-cryptography 頁首仍寫「現行規格的做法要等 S5 補上」，和已寫入的 hqc-pke 矛盾。
- 先全 wiki 掃「等 S5、S5 補上、S5 查核、2020-10-01、用完即丟、量不出來、驗證假設、只有 IND-CPA、只能擋住」再修：
  - L7/L8：syndrome-decoding 頁首加 S5 的時間點與查核日期 2026-11-23；error-correcting-codes 改 spec_version 2025-08-22；glossary RM、RS 兩列標版本；code-based-cryptography 頁首改指向 hqc-pke；sources/S4 的「等 S5 查核」改為「以 S5 為準」。
  - notes：RM＋RS 是 2020-05-04 版引入、2020-10-01 版才移除舊碼（concatenated-rm-rs、sources/S5）；hqc-pke 誤解一節分清搜尋版與判定版；IND-CCA2 補上「隨機預言機模型、解碼問題難、失敗率夠小」三個前提；「只能擋住只看密文的攻擊者」改成 IND-CPA 的設定說明；「用模擬驗證」改「佐證」、拿掉「量不出來」；公開碼頁拿掉 S5 沒說的「沒有 y 就無法降雜訊」，「能修很多錯」改引 S4 p.18；r1、r2、e「用完即丟」改成「由 θ 產生、不放進密文」；截斷那句補 p.46。
  - concatenated-rm-rs 不再點名 BCH＋重複碼（維持討論紀錄 03 的 3b，只在 sources/S5 的修改紀錄提）。

## [2026-11-23 00:38] lint | S5 lint 第 2 次不通過，修正（下一次是第 3 次，達重試上限）
- 檢查紀錄：runs/ingest/checks/A4-lint-S5-a2.json → FAIL（腳本全 PASS；L8 PASS）
- L7 語意 4 處，全是「研究現況／安全性評價」缺查核日期：hqc-vs-ml-kem 的「使用數十年」（上一輪改頁首時把它的涵蓋範圍縮掉了）、hqc-pke 的「沒有證明兩版一樣難」、sources/S5 的限制一行、hqc-parameter-sets 的「已知最好的攻擊」。
- 根本原因：S5 頁面沒有頁首時間說明。這次不再逐句補，改成每個以 S5 為主的頁（hqc-pke、hqc-toy-example、concatenated-rm-rs、hqc-kem-fo-transform、decryption-failure-rate、error-correcting-codes、hqc-parameter-sets、sources/S5）都加同一段頁首時間說明，涵蓋全頁的評價說法；hqc-vs-ml-kem 的頁首把「使用數十年」放回涵蓋範圍。
- 依 notes 修正：「公認很難」改為「研究社群認為很難」（S4 p.11、S5 p.10 的原文是 considered hard by the community）；S4 失敗率改為「簡化假設下估算」；隨機預言機模型補 S5 p.43；重複 3／5 次補 S5 p.21；salt 與公開金鑰納入 θ 是 2022-10-01 版、2025-08-22 版才放進 K；舊名 HQC-128/192/256 的出處改為 S5 §3.3 與表 2（p.15–p.16）；code-based-cryptography、sources/S4 的 updated 改 2026-11-23，並列進 sources/S5 的更新頁；quasi-cyclic-codes 頁首註明也用 S5；index 的 concatenated-rm-rs 來源補 S4。

## [2026-11-23 00:48] lint | S5 lint 第 3 次通過；依檢查員備註小修
- 檢查紀錄：runs/ingest/checks/A4-lint-S5-a3.json → PASS（在重試上限內）
- S5 統計：A3S 3 次，失敗 1 次（L2 缺來源標記 13 處）；A4 3 次，失敗 2 次，全是 L7 語意（研究現況評價缺查核日期）＋1 次 L8（過時的「等 S5」待辦說法）。
- 依 notes 小修（不屬 L7/L8）：hqc-pke、syndrome-decoding 補 S5 p.43；hqc-pke「搜尋版」標明是 wiki 的說明；concatenated-rm-rs 改為規格書原話「HQC-PKE 的加密率低」，總覽頁「能修很多錯」只引 S4 p.18；syndrome-decoding「長期研究的共識」改「研究社群的看法」；sources/S5 拿掉無出處的「不是 NIST 正式標準」，改指向 fips-207；解碼失敗率頁的硬幣換算標明是 wiki 的說明，並說 2^-128 是 HQC-1 的上限；FO 頁補上 2024-10-30 版只放公鑰前 32 位元組的變動；code-based-cryptography 的「很短向量」改引 S5 p.7（原引 S4 p.8 講的是秩度量）；kem 的用詞差異補引 S5 p.12。
- 使用者提議「語意分塊、markdown 註記讓每句導向來源段落」：分析後判斷它能處理「來源對不上」類錯誤（頁碼、推論寫成原文），對 L7 時效標註幫助不大；決定先不中途改 workflow，列為 v2 候選（輕量版：raw 依頁／段切塊編號，lint 檢查句中數字出現在被引用的那一頁）。
