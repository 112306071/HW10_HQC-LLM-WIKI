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
