# HQC 教學 LLM Wiki 與 HTML 簡報：完整規格書

2026-11-19

> 本檔由使用者提供的規格書轉存。原文 §7 的 workflow v1 嵌入圖在匯出時遺失，已依 §7.1 節點表與 §7.2 graph.yaml 重畫於 `workflow/graph.md`（見 `wiki/log.md` 的 issue 紀錄）。
>
> **2026-11-20 範圍調整**：依使用者在討論紀錄 02 的要求（簡報著重 HQC 技術；對學會 HQC 沒幫助的資料刪掉，至少 5 份），來源由 8 份減為 5 份（S1、S2、S4、S5、S6），簡報由 22 張改為 21 張。改動處：§1.1、§2.1、§2.2、§4.5、§5、§9.1、§9.2、§9.4、§10.2、§12.2、§13。原因與明細見 `discussions/02-S2-nist-news-hqc.md` 第 8 節、`wiki/log.md` 2026-11-20 issue。

## 0. 這份規格書怎麼用

把這份文件匯出成 Markdown，存成專案根目錄的 `SPEC.md`，然後對 Claude Code 說：「依照 SPEC.md 執行，遇到【人工關卡】一定要停下來等我。」文中「必須」是硬性要求，「建議」可以視情況調整。

### 0.1 你必須親自做的 5 件事

Claude Code 可以做完幾乎所有工作，但下面這些必須是你本人。作業要求「先討論、後生成」，也有抄襲規定；這些關卡的紀錄就是你有參與的證據。

| 時機 | 你要做什麼 | 為什麼 |
| --- | --- | --- |
| 每篇資料 ingest 前（至少 5 次） | 讀 AI 的討論備忘錄，回答它的問題，決定哪些重點要寫入 wiki | 「先討論、後生成」的要求；你的回覆會原文存進 `discussions/` |
| 第一次跑簡報流程前 | 看過 workflow v1 的流程圖，回覆「開始」 | 確認設計是你同意的 |
| 簡報發布前 | 用瀏覽器實際翻一次，回覆「通過」或列出問題 | 成品檢查的最後一關，也會記錄進檢查紀錄 |
| 反思定稿 | 讀 AI 根據紀錄寫的初稿，改成你自己的話 | 反思要是你的判斷 |
| 繳交 | 填入學校、學號、系級、姓名，上傳 | 個人資料不交給 AI 亂填 |

### 0.2 給 Claude Code 的總規則

1. **來源鍊**：簡報裡的每個事實都必須來自 wiki；wiki 裡的每個事實都必須來自 `raw/` 的來源。沒有來源就不寫。
2. **誠實紀錄**：不准捏造或美化執行紀錄。失敗照實記，通過也照實記。不准為了「有東西可以反思」而故意製造錯誤。
3. **人工關卡**：遇到【人工關卡】一定停下等使用者回覆，不可自行假設同意。
4. **每個節點都留痕跡**：每執行完一個節點，就寫一筆 trace（格式見第 10 節）。
5. **規格衝突先問**：規格和實際狀況衝突時（例如來源連結失效），記錄在 `wiki/log.md` 並詢問使用者，不要默默改規格。
6. **語言**：wiki、簡報、報告一律用繁體中文；專有名詞第一次出現時附英文，例如「金鑰封裝機制（KEM）」。

## 1. 作業要求對照表

作業的每一條要求、每一個繳交項目、每一個 9–10 分條件，都對應到本規格的一節和一個實際檔案。最後驗收時（第 13 節）逐列打勾。

### 1.1 作業內容要求

| # | 作業要求 | 規格節 | 交付物 |
| --- | --- | --- | --- |
| R1 | 建立自己主題的 LLM Wiki | §2、§4 | `wiki/` 整個資料夾 |
| R2 | 用「先討論、後生成」建立 Wiki | §6 | `discussions/NN-*.md`（每篇一份，含你的回覆原文） |
| R3 | 至少 ingest 5 篇資料 | §5 | `raw/` 5 份採用的來源、`wiki/sources/` 5 頁摘要、`wiki/log.md` 5 筆 ingest |
| R4 | 讓 AI 以 Wiki 為知識來源製作教學型 HTML 簡報 | §7、§9 | `slides/index.html`（GitHub Pages 公開連結） |
| R5 | 讓不熟悉主題的人理解基本概念 | §9.1、§8.2 的 O3–O5 | 教學結構、初學者檢查結果 |
| R6 | 說明流程（取得 → 查詢 → 整理 → 檢查 → 產生） | §7 | `workflow/graph.yaml`、`workflow/graph.md`（流程圖） |
| R7 | 哪些步驟會重複執行 | §7.4 | 同上 |
| R8 | 哪些地方需要檢查或重新生成 | §7.4、§8 | `scripts/check_*.py`、`runs/*/checks/` |
| R9 | 為什麼這樣設計 | §7.5 | REPORT.md 第 4 節 |
| R10 | 完成一次實際執行 | §10 | `runs/run-001-v1/`、`runs/run-002-v2/` |
| R11 | 哪一個節點最常出錯 | §11 | `reports/run_summary.md`（按節點統計失敗次數） |
| R12 | 發現問題後，把檢查往前移到哪一步 | §11 | `workflow/CHANGELOG.md`、v1/v2 流程圖 |
| R13 | 有沒有因此修改 workflow／為什麼 | §7.6、§11 | 同上，加上前後兩次執行的數字比較 |

### 1.2 繳交項目

| 繳交項目 | 規格節 | REPORT.md 的位置 |
| --- | --- | --- |
| 1. LLM Wiki 主題與簡短介紹 | §2、§12 | 第 1 節 |
| 2. LLM Wiki 連結或成果 | §4、§12 | 第 2 節（GitHub repo 連結 + 截圖） |
| 3. 教學 HTML 簡報連結 | §9.5 | 第 3 節（GitHub Pages 連結） |
| 4. loop / graph 的流程圖或文字說明 | §7 | 第 4 節 |
| 5. 一次實際執行的結果或檢查紀錄 | §10 | 第 5 節 |
| 6. 反思：哪個節點最常出錯？如何調整檢查流程？ | §11 | 第 6 節 |

### 1.3 9–10 分條件

| 評分條件 | 本規格怎麼做到 |
| --- | --- |
| Wiki 資料與簡報內容有明確對應 | 每張投影片用 `data-wiki` 標註來源頁，頁尾顯示可點連結；報告附「投影片 ↔ wiki 頁」對應表；檢查腳本自動驗證對應存在（§9.3、§8.3） |
| loop / graph 設計合理且說明清楚 | 節點表、條件邊、重試上限、流程圖、逐項設計理由（§7） |
| 有實際執行與檢查紀錄 | 自動產生的 trace、每次檢查的 JSON 結果、彙整表（§10） |
| 能反思哪個節點容易出錯，以及如何調整或提前檢查流程 | 至少兩次完整執行（v1、v2），用數字比較修改前後（§11） |
| 簡報具有清楚的教學結構 | 學習目標 → 動機 → 基礎 → 核心 → 應用 → 誤解 → 小測驗 → 總結（§9.1） |

## 2. 專案概述

主題是「HQC 是什麼？一個用錯誤更正碼做成的後量子加密」。HQC（Hamming Quasi-Cyclic）是 NIST 在 2025 年 3 月 11 日選出、做為 ML-KEM 備援的後量子金鑰封裝機制，正在制定成 FIPS 207。

- **專案名稱**：`hqc-llm-wiki`
- **簡報標題**：「HQC 是什麼？用『故意加入的錯誤』保護量子時代的金鑰」
- **目標受眾**：修過基礎程式或離散數學的大學生。知道「公鑰／私鑰」是什麼，但沒學過編碼理論、不知道後量子密碼學。
- **簡報長度**：18–22 張，講解時間約 20 分鐘。

### 2.1 學習目標

看完簡報後，學習者應該能夠：

1. 說出為什麼量子電腦會威脅現在的加密，以及 HQC 在後量子密碼中扮演的角色（ML-KEM 的備援）。
2. 用自己的話解釋金鑰封裝機制（KEM）在做什麼。
3. 說明錯誤更正碼、漢明重量的意思，以及「故意加錯誤」為什麼能拿來加密。
4. 依序描述 HQC 的金鑰產生、加密、解密三步，並指出哪個值是公開的、哪個是秘密的。
5. 比較 HQC 與 ML-KEM 的數學基礎與取捨，說出 NIST 選 HQC 當備援的理由。

（2026-11-20 修改 G1、G5：G1 把「為什麼現在就要準備」縮成一句，加上 HQC 的定位；G5 的「大小差異」改成「取捨」，因為不再 ingest 提供 ML-KEM 數字的 S8。）

### 2.2 範圍

| 包含 | 不包含 |
| --- | --- |
| 量子威脅的直觀說明（不推導 Shor 演算法） | 量子計算的數學細節 |
| 錯誤更正碼、漢明距離／重量、伴隨式解碼問題的直觀意義 | Reed-Muller、Reed-Solomon 的解碼演算法細節 |
| HQC-PKE 三個步驟、從 PKE 到 KEM 的概念 | 安全性證明的推導 |
| 參數與大小（標明規格版本）、解碼失敗率 | 實際程式實作、效能跑分、實作攻擊（計時攻擊）（2026-11-20 移出） |
| 用小數字走一遍 HQC 的完整示例（由腳本計算） | 其他國家的標準 |
| HQC 在 NIST 標準化中的位置與 FIPS 207 狀態（其他 FIPS 只提一句） | 其他 PQC 演算法的細節（FIPS 204–206） |

## 3. 技術選型與目錄結構

由 Claude Code 當執行者，依照機器可讀的 graph 定義檔逐節點執行；檢查盡量用 Python 腳本自動跑，結果存成 JSON。這樣檢查紀錄是程式輸出的，可以重現，不是 AI 自己寫的感想。

### 3.1 選型

| 項目 | 選擇 | 理由 |
| --- | --- | --- |
| 執行者 | Claude Code | 使用者指定；可讀寫檔案、執行腳本、在人工關卡停下 |
| Graph 定義 | `workflow/graph.yaml`（節點、邊、條件、重試上限）+ `workflow/graph.md`（mermaid 流程圖） | 流程是明確寫下來的狀態機，不是寫在對話裡的口頭約定 |
| 自動檢查 | Python 3.10+：`pyyaml`、`beautifulsoup4`；成品渲染檢查用 `playwright`（headless Chromium） | 檢查可重複、可統計。`playwright` 裝不起來時，渲染檢查改由使用者截圖，並在 log.md 註明 |
| 語意檢查 | Claude Code 依固定評分表判定，結果寫成 JSON | 「是否有來源支持」、「初學者看不看得懂」這類問題腳本無法判斷 |
| Wiki 格式 | Markdown + YAML frontmatter；頁面互連用標準相對連結 `[KEM](../concepts/kem.md)` | GitHub 能直接渲染並點擊。不用 Obsidian 的 `[[...]]`，因為 GitHub 上會變成廢連結 |
| 簡報 | 單一 HTML 檔，原生 CSS/JS，不引用外部 CDN | 任何瀏覽器都能開，不會因為外部資源失效而壞掉 |
| 部署 | GitHub 公開 repo + GitHub Pages | Wiki 與簡報各有一個穩定公開連結，助教不用下載 |
| 版本紀錄 | git，每完成一個里程碑就 commit | commit 歷史本身也是執行證據 |

不採用 LangGraph：它需要另外申請 API 金鑰並付費，而作業要求的是「流程圖或文字說明」，明確的 graph 定義檔加上實際執行紀錄已經足夠。若之後想升級，`graph.yaml` 可以直接對應成 LangGraph 的節點與條件邊。

### 3.2 目錄結構

```
hqc-llm-wiki/
├── SPEC.md                  # 本規格書
├── CLAUDE.md                # wiki schema 與規則（§4.2）
├── README.md                # 專案入口，連到 wiki、簡報、報告
├── REPORT.md                # 繳交用文字說明（§12）
├── raw/                     # 原始來源，只新增不修改
├── discussions/             # 先討論、後生成的紀錄（§6）
├── wiki/                    # LLM 維護的 wiki（§4）
│   ├── index.md
│   ├── log.md
│   ├── glossary.md
│   ├── overview/
│   ├── concepts/
│   ├── entities/
│   ├── comparisons/
│   └── sources/
├── workflow/
│   ├── graph.yaml           # 目前版本
│   ├── graph.md             # 目前版本的流程圖
│   ├── v1/                  # v1 的 graph.yaml + graph.md 快照
│   ├── v2/                  # v2 快照
│   └── CHANGELOG.md         # 改了什麼、根據哪些紀錄、為什麼
├── scripts/
│   ├── trace.py             # 寫一筆節點執行紀錄
│   ├── lint_wiki.py         # §8.1 的自動檢查
│   ├── check_outline.py     # §8.2 的自動檢查
│   ├── check_slides.py      # §8.3 的自動檢查（含截圖）
│   └── summarize_runs.py    # 產生 reports/run_summary.md
├── runs/
│   ├── run-001-v1/
│   │   ├── trace.jsonl
│   │   ├── checks/          # 每次檢查一個 JSON
│   │   ├── queries/         # 查詢 wiki 的結果
│   │   ├── outline-v*.md    # 每次大綱都保留
│   │   ├── slides-v*.html   # 每次產生的簡報都保留
│   │   └── screenshots/
│   └── run-002-v2/
├── reports/
│   ├── run_summary.md
│   └── slide_wiki_map.md    # 投影片 ↔ wiki 對應表
└── slides/
    └── index.html           # 最後發布的版本
```

## 4. LLM Wiki 規格

Wiki 採用 Karpathy 的 LLM Wiki 做法：來源只讀、wiki 由 LLM 維護、規則寫在 schema 檔。和「每次問問題都重新翻原始文件」不同，知識在 ingest 時就整理好、互相連結，後面做簡報時直接查 wiki。

### 4.1 三層架構與三種操作

| 層 | 位置 | 誰可以改 | 內容 |
| --- | --- | --- | --- |
| 原始來源 | `raw/` | 只能新增，不能修改 | 來源檔案（PDF 或網頁存成 Markdown）與抽出的純文字 |
| Wiki | `wiki/` | Claude Code（經討論確認後） | 概念頁、實體頁、比較頁、來源摘要頁、index、log |
| Schema | `CLAUDE.md` | 使用者與 Claude Code 共同維護 | 命名、模板、引用、版本等規則 |

| 操作 | 何時做 | 做什麼 |
| --- | --- | --- |
| Ingest | 每加入一份來源 | 討論 → 寫來源摘要頁 → 新增或更新相關頁 → 更新 index、log（§6） |
| Query | 做簡報時 | 針對問題清單查 wiki，答案附上 wiki 頁與來源代碼；好的答案可以回寫成新頁 |
| Lint | 每次 ingest 後，加上做簡報前一次 | 斷連、孤兒頁、缺來源、版本矛盾、過時資訊（§8.1） |

### 4.2 CLAUDE.md 內容

見專案根目錄 `CLAUDE.md`。

### 4.3 頁面類型與模板

每一頁都以 YAML frontmatter 開頭：

```yaml
---
title: 金鑰封裝機制（KEM）
type: concept          # overview | concept | entity | comparison | source | glossary
sources: [S2, S5]      # 至少一個，必須是 §5 清單裡的代碼
related: [../concepts/hqc-pke.md, ../comparisons/hqc-vs-ml-kem.md]
spec_version: "HQC 2025-08-22"   # 有數字或演算法細節時必填，否則寫 none
updated: 2026-11-20
status: draft          # draft | reviewed（通過 lint 後改成 reviewed）
---
```

概念頁的內文依序包含：一句話定義、白話解釋（可含比喻）、重點（3–5 點）、細節、常見誤解、相關頁面。來源摘要頁（`sources/S1-*.md`）包含：書目資料與連結、取得日期、5–10 個重點（用自己的話改寫，不整段照抄）、這份來源更新了哪些頁、可信度與限制。

### 4.4 index.md 與 log.md

`index.md` 按類型分組，每頁一行：

```markdown
## 概念
- [金鑰封裝機制（KEM）](concepts/kem.md) — 兩方在公開網路上建立共享秘密的機制。來源：S2, S5
```

`log.md` 只能往後追加，每筆用固定前綴，可以用 `grep "^## \[" wiki/log.md` 列出：

```markdown
## [2026-11-20 14:05] ingest | S1 NIST：What Is Post-Quantum Cryptography?
- 討論紀錄：discussions/01-S1-nist-pqc-explainer.md
- 新增：sources/S1-nist-pqc-explainer.md, concepts/quantum-threat.md
- 修改：index.md, glossary.md
- lint：runs/ingest/checks/lint-S1-a1.json → PASS
```

其他類型：`query`、`lint`、`conflict`（來源衝突）、`workflow-change`（修改 graph）、`issue`（規格與實際衝突、連結失效等）。

### 4.5 預定頁面清單

下表是預計要有的頁面。ingest 時可以新增或合併，但變動要寫進 log.md。「投影片」欄對應 §9.2 的編號。

| 頁面 | 內容 | 主要來源 | 投影片 |
| --- | --- | --- | --- |
| `overview/hqc-overview.md` | HQC 是什麼、為什麼重要、一張圖看全貌 | S2, S4, S5 | 1, 2, 4, 21 |
| `concepts/quantum-threat.md` | 量子電腦為什麼威脅今天的加密、先收集後解密 | S1 | 3 |
| `concepts/post-quantum-cryptography.md` | 後量子密碼學的定義、和量子密碼學的差別、HQC 是第五個 | S1, S2 | 4 |
| `concepts/kem.md` | 金鑰封裝機制的用途與三個函式 | S2, S5 | 5 |
| `concepts/error-correcting-codes.md` | 錯誤更正碼、漢明距離與漢明重量 | S5, S4 | 6 |
| `concepts/syndrome-decoding.md` | 伴隨式解碼問題（SD、QCSD）的直觀意義 | S4, S5 | 7 |
| `concepts/code-based-cryptography.md` | 編碼式密碼：McEliece 藏結構 vs HQC 不藏結構 | S4, S6 | 7, 8 |
| `concepts/quasi-cyclic-codes.md` | 準循環結構為什麼讓金鑰變小 | S4, S5 | 9 |
| `concepts/hqc-pke.md` | 金鑰產生、加密、解密，每個變數是公開或秘密 | S5, S6 | 10, 11, 12 |
| `concepts/hqc-toy-example.md` | 用很小的參數實際走一次 HQC（數字由 scripts/examples.py 計算） | S5 | 13 |
| `concepts/concatenated-rm-rs.md` | 公開碼：Reed-Muller + Reed-Solomon 串接（只講用途） | S5 | 14 |
| `concepts/hqc-kem-fo-transform.md` | 從 PKE 到 KEM：Fujisaki-Okamoto 轉換的概念 | S5, S6 | 15 |
| `concepts/decryption-failure-rate.md` | 解碼失敗率是什麼、為什麼要小於 2^-128 | S5, S6 | 16 |
| `concepts/common-misconceptions.md` | 常見誤解與正確說法 | 多份 | 19 |
| `entities/fips-207.md` | HQC 的標準化：第五個演算法、時程、為什麼不是其他第四輪候選、考慮中的修改（附「狀態查核日期」） | S2, S6 | 4, 18 |
| `comparisons/hqc-vs-ml-kem.md` | 數學基礎、定位、取捨（ML-KEM 的內容放這頁，不另開實體頁） | S2, S5, S6 | 17 |
| `comparisons/hqc-parameter-sets.md` | HQC-1/3/5 參數表與舊版名稱對照 | S5 | 17 |
| `glossary.md` | 術語表：中文、英文、一句話解釋、連到概念頁 | 全部 | 全部 |
| `sources/S1、S2、S4–S6-*.md` | 每份來源一頁摘要 | 各自 | — |

2026-11-20 移除的預定頁：`concepts/implementation-security.md`（S7 不採用）、`entities/nist-pqc-process.md`（五個演算法只講結構，併入 post-quantum-cryptography 與 fips-207）、`entities/ml-kem.md`（併入 hqc-vs-ml-kem）、`entities/bike-and-classic-mceliece.md`（併入 fips-207，來源改用 S6）。新增 `concepts/hqc-toy-example.md`。

## 5. 資料來源清單

採用 5 份來源：S1、S2、S4、S5、S6（剛好是作業要求的 5 篇）。依 S1 → S2 → S4 → S5 → S6 的順序 ingest：先入門、再核心、最後標準化現況，讓 wiki 先有骨架再補細節。所有連結已於 2026-11-19 確認可開啟。

2026-11-20 使用者要求「著重 HQC 技術、對學會 HQC 沒幫助的資料刪掉，至少五個」，因此 S3、S7、S8 不採用（理由見下表「狀態」欄與討論紀錄 02 第 8 節）。S3 列為備用：S4–S6 若有一份取不到，改用 S3 補足 5 份。表中保留這三列，方便對照原本的規劃。

### 5.1 來源表

| ID | 來源 | 類型與難度 | 用來提供什麼 | 主要更新的 wiki 頁 | 狀態 |
| --- | --- | --- | --- | --- | --- |
| S1 | [NIST：What Is Post-Quantum Cryptography?](https://www.nist.gov/cybersecurity/what-post-quantum-cryptography)（2024-08-13 發布，2026-02-27 更新） | 政府科普頁，入門 | 量子威脅、先收集後解密、PQC 與量子密碼學的差別 | quantum-threat、post-quantum-cryptography | 採用 |
| S2 | [NIST：NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption)（2025-03-11） | 官方新聞稿，入門 | 選 HQC 的理由、KEM 的白話解釋、標準化時程 | kem、fips-207、hqc-overview、hqc-vs-ml-kem | 採用 |
| S3 | [NIST IR 8545：Status Report on the Fourth Round](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf)（2025-03） | 官方技術報告，中等 | 第四輪候選（BIKE、Classic McEliece、HQC、SIKE）評估與選擇理由 | — | 不採用（備用）：34 頁大多在評估其他候選；HQC 的選擇理由 S2、S6 已涵蓋 |
| S4 | [Aguilar-Melchor 等：Efficient Encryption from Random Quasi-Cyclic Codes](https://arxiv.org/abs/1612.05572)（IEEE Trans. Inf. Theory 64(5)，2018） | 原始論文，進階 | 核心想法：不在公鑰裡藏結構、安全性建立在準循環碼解碼問題 | code-based-cryptography、syndrome-decoding、quasi-cyclic-codes | 採用 |
| S5 | [HQC 官方規格書 2025-08-22 版](https://www.pqc-hqc.org/doc/hqc_specifications_2025_08_22.pdf) | 演算法規格，進階 | 金鑰產生／加密／解密、公開碼、參數與大小、解碼失敗率、版本修改紀錄 | hqc-pke、hqc-toy-example、concatenated-rm-rs、hqc-kem-fo-transform、hqc-parameter-sets | 採用 |
| S6 | [NIST（Angela Robinson）：FIPS 207: HQC-KEM 簡報](https://csrc.nist.gov/csrc/media/presentations/2025/fips-207-hqc-kem/fips_207-robinson_2.4.pdf)（第 6 屆 PQC 標準化會議，2025-09） | 官方簡報，中等 | 為什麼選 HQC 而非 BIKE／Classic McEliece、轉成 FIPS 的計畫、考慮中的修改 | fips-207、hqc-kem-fo-transform | 採用 |
| S7 | [Guo 等：Don’t Reject This: Key-Recovery Timing Attacks Due to Rejection-Sampling in HQC and BIKE](https://tches.iacr.org/index.php/TCHES/article/view/9700)（TCHES 2022 第 3 期） | 學術論文，進階 | 實作層的計時攻擊與對策 | — | 不採用：講實作攻擊，不是 HQC 怎麼運作（raw/ 的 PDF 依規則 1 保留） |
| S8（補充） | [FIPS 203：ML-KEM 標準](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)（2024-08） | 官方標準，只取大小表 | ML-KEM 的金鑰與密文大小，用於和 HQC 比較 | — | 不採用：只提供 ML-KEM 的數字，對學會 HQC 幫助小 |

### 5.2 每份來源的注意事項

這些是已知容易出錯的地方，討論備忘錄裡要提出來問使用者。

- **S1**：只講一般概念，沒有列出標準名稱。標準清單改由 S2 提供。
- **S2**：發布時說草案「約一年後」公布。這是 2025 年的預估，必須再查現況（見 5.3）。
- **S3**（不採用，備用）：全文 34 頁，只需讀 HQC、BIKE、Classic McEliece 相關段落。表 5 的 Classic McEliece 效能數字有人提出更正請求，簡報不要引用那個數字。
- **S4**：2016–2018 年的論文，參數與細節已經過時。只用來講概念與設計動機，數字一律以 S5 為準。
- **S5**：參數組命名是 HQC-1/3/5，舊版和外部資料常用 hqc-128/192/256。公鑰大小也和舊版不同（例：舊版 hqc-128 的 2,249 位元組，新版 HQC-1 是 2,241）。wiki 的每個數字都要標版本。
- **S6**：裡面的修改是「考慮中」的提案，不是定案。wiki 要寫成「2025 年 9 月 NIST 提出考慮……」。
- **S7**（不採用）：攻擊的對象是當時的實作；S5 的修改紀錄顯示 2022 年已改採樣方式來對應計時攻擊。簡報不可以寫成「HQC 已被攻破」。
- **S8**（不採用）：只取金鑰與密文大小表，不要展開 ML-KEM 的數學。

### 5.3 時效查核

FIPS 207 的狀態會變。2026-11-19 查到的最新公開資訊（2026 年 10 月的 IETF 草案）仍表示 FIPS 207 尚未發布。Claude Code ingest S6 時必須再開一次 [NIST PQC 專案頁](https://csrc.nist.gov/Projects/post-quantum-cryptography/post-quantum-cryptography-standardization) 確認，把結果和查核日期寫進 `entities/fips-207.md`。若草案已發布，就作為 S9 ingest（一樣要經過討論關卡）。

### 5.4 取得與儲存規則

1. 網頁來源（S1、S2）存成 Markdown，檔頭寫上網址與取得日期。
2. PDF 來源存原檔，再用 `pdftotext -layout` 轉出 `.txt` 放在旁邊，方便搜尋。
3. `raw/sources.yaml` 記錄每份來源的 ID、標題、作者、日期、網址、取得日期、檔案路徑。
4. 版權：NIST 文件（S1、S2、S3、S6、S8）可以放進公開 repo。S4、S5、S7 的 PDF 加進 `.gitignore`，只提交書目資料與連結。
5. 連結打不開時：寫一筆 `issue` 到 log.md，停下來問使用者要換哪份來源，不要自己找替代品。

## 6. Ingest 流程：先討論、後生成

一次只處理一份來源，而且必須先寫討論備忘錄、等使用者回覆「確認」，才能動 wiki。禁止把多份來源一次丟進去生成。

### 6.1 每份來源的步驟

1. **A1 取得**：下載到 `raw/`，更新 `raw/sources.yaml`，寫 trace。
2. **A2 討論**：讀完來源，依 6.2 的模板寫 `discussions/NN-Sx-*.md`。
3. **【人工關卡】**：在對話中貼出備忘錄的第 2–6 節，停下來等使用者回覆。
   - 使用者提出修改 → 修改備忘錄，再問一次（記為第 2 輪討論）。
   - 使用者回覆「確認」→ 把回覆原文貼進第 7 節，寫第 8 節最終決定，附上確認時間。
4. **A3 寫入**：只寫第 8 節決定要寫的內容。寫來源摘要頁、新增或更新概念頁、更新 `index.md`、`glossary.md`、`log.md`。
5. **A4 Lint**：跑 `scripts/lint_wiki.py` 與語意檢查（§8.1）。失敗就回 A3 修正，最多 3 次；第 3 次還失敗就停下來問使用者。
6. **Commit**：`git commit -m "ingest S1: NIST What Is PQC"`。

### 6.2 討論備忘錄模板

```markdown
# 討論紀錄 01：S1 NIST：What Is Post-Quantum Cryptography?
- 建立時間：2026-11-20 14:00
- 來源：S1（raw/S1-nist-pqc-explainer.md）

## 1. 這份來源在講什麼（3 句以內）
## 2. 建議寫進 wiki 的重點（5–8 點，每點附原文位置）
## 3. 和現有 wiki 的關係
- 要新增的頁：
- 要修改的頁：
- 和既有內容可能衝突的地方：
## 4. 建議不寫的內容與理由
## 5. 對教學簡報的用處（可能對應哪幾張投影片）
## 6. 想問你的問題（2–3 題）
## 7. 使用者回覆（原文照貼，不可修改）
## 8. 最終決定
- 確認時間：
- 寫入：
- 不寫入：
- 因討論而改變的地方：
```

第 6 節的問題要讓使用者做決定，例如：這個概念簡報要講到多深？兩個比喻選哪個？兩份來源數字不同時採用哪個？不要問「可以嗎？」這種只能回答是否的問題。

### 6.3 給使用者：怎麼回覆才算「有討論」

只回「確認」的話，紀錄看起來就是 AI 自己生成。每份備忘錄至少做一件事：

- 刪掉或降級一個太深的重點（例：「第 4 點的安全性約化不用進簡報，放 wiki 就好」）。
- 指定比喻或講法（例：「KEM 用寄上鎖的保險箱來比喻」）。
- 裁決衝突（例：「數字一律用 2025-08-22 版，舊版放在對照表」）。
- 補一個你自己的疑問，讓 AI 去來源裡找答案。

### 6.4 怎麼驗證「先討論、後生成」有做到

`lint_wiki.py` 的 L9 會自動檢查：每個出現在 wiki `sources` 欄位的來源，都有對應的討論紀錄；紀錄的第 7 節不是空的；「確認時間」早於 log.md 中那筆 ingest 的時間。

## 7. Loop / Graph 設計

流程分兩個階段，共 12 個節點：3 個自動檢查點、2 個人工關卡。任何檢查不通過，只退回「能修正這個錯誤的最近一步」，不從頭重跑。以下是 workflow v1；v2 會依第一次執行的紀錄修改（§7.6）。

（流程圖：見 `workflow/graph.md`）

左欄對每份來源各跑一次；全部完成後進入右欄。虛線是跨階段的回頭路：做簡報時發現 wiki 缺資料，就回到 A1 補一份來源。

### 7.1 節點表

| 節點 | 做什麼 | 輸入 → 輸出 | 執行者 | 下一步 |
| --- | --- | --- | --- | --- |
| A1 取得來源 | 下載一份來源、登記 sources.yaml | §5 清單 → `raw/Sx.*` | Claude Code | → A2；連結失效 → 停下問你 |
| A2 寫討論備忘錄 | 依 §6.2 模板列重點、衝突、問題 | `raw/Sx` → `discussions/NN-*.md` | Claude Code | → H1 |
| H1 你確認了嗎？【人工關卡】 | 你讀備忘錄並回覆 | 備忘錄 → 你的回覆 | 你 | 確認 → A3；要修改 → A2 |
| A3 寫入 Wiki | 依最終決定寫頁面，更新 index、log、glossary | 備忘錄第 8 節 → `wiki/` | Claude Code | → A4 |
| A4 Lint 通過？ | §8.1 的 L1–L9 | `wiki/` → `checks/lint-*.json` | 腳本 + Claude Code | 還有來源 → A1；全部完成 → B1；不通過 → A3（最多 3 次） |
| B1 查詢 Wiki | 回答 §9.2 每張投影片的問題，每個答案附 wiki 頁與來源代碼 | `workflow/questions.yaml` → `queries/q-*.md` | Claude Code | → B2；查不到 → A1 補來源（每次執行最多補 2 份） |
| B2 整理大綱 | 把答案排成教學順序，每條標註 wiki 頁 | `queries/` → `outline-vN.md` | Claude Code | → B3 |
| B3 大綱通過？ | §8.2 的 O1–O5 | 大綱 → `checks/outline-*.json` | 腳本 + Claude Code | → B4；不通過 → B2（最多 3 次） |
| B4 產生 HTML | 依 §9.4 產生單一 HTML | 大綱 → `slides-vN.html` | Claude Code | → B5 |
| B5 成品通過？ | §8.3 的 P1–P8 | HTML → `checks/slides-*.json` + 截圖 | 腳本 + Claude Code | → H2；格式錯 → B4；內容錯 → B2（合計最多 3 次） |
| H2 你看過了嗎？【人工關卡】 | 你用瀏覽器翻一遍 | 預覽網址 → 你的回覆 | 你 | 通過 → B6；內容問題 → B2；版面問題 → B4 |
| B6 發布 | 複製到 `slides/index.html`、更新對應表、commit、push | → GitHub Pages | Claude Code | 結束 |

任一節點達到重試上限時，狀態標為 `ESCALATED`，停下來把問題與檢查結果拿給你決定，不自行放行。

### 7.2 graph.yaml

見 `workflow/graph.yaml`。每次執行的狀態存在 `runs/<run_id>/state.json`：目前節點、各檢查點已試次數、大綱與簡報目前版本、已補充的來源。Claude Code 每次決定下一步前都要先讀 `graph.yaml` 與 `state.json`，依 `when` 條件選邊，不可自行跳步。

### 7.3 哪些步驟會重複執行

1. **Ingest 迴圈 A1→A4**：每份來源一次，共 5 次（2026-11-20 前規劃為 8 次）。
2. **討論迴圈 A2↔H1**：你要求修改就再來一輪。
3. **Wiki 修正迴圈 A3↔A4**：lint 不過就修。
4. **大綱迴圈 B2↔B3**：大綱不合格就重寫。
5. **生成迴圈 B4↔B5**：版面或格式問題只重做 HTML。
6. **內容退回 B5→B2、H2→B2**：事實或教學問題回到大綱。
7. **補資料 B1→A1**：wiki 缺資料時跨回階段一，而且一樣要經過討論關卡。

### 7.4 哪些地方需要檢查或重新生成

| 檢查點 | 檢查什麼 | 方式 | 不通過時重新生成什麼 |
| --- | --- | --- | --- |
| H1 | 重點選得對不對、深度合不合適 | 人工 | 討論備忘錄 |
| A4 | 結構、來源、版本、衝突、討論紀錄 | 腳本 + 語意 | 出問題的 wiki 頁 |
| B3 | 覆蓋度、引用是否存在、教學順序、術語先定義 | 腳本 + 語意 | 大綱 |
| B5 | 對應、數字一致、內容有來源支持、渲染、導覽 | 腳本 + 語意 + 截圖 | HTML（格式）或大綱（內容） |
| H2 | 整體好不好懂、有沒有奇怪的地方 | 人工 | 大綱或 HTML |

### 7.5 為什麼這樣設計

1. **分兩個階段**：wiki 是會累積的知識，簡報是一次性的產物。查證放在 ingest，做簡報時只需要查 wiki，不用每次重讀原文。
2. **人工關卡放在入口與出口**：錯的知識一旦進了 wiki，會被後面每張投影片引用，所以在入口（H1）擋；發布前（H2）再確認一次整體效果。
3. **生成 HTML 前先檢查大綱**：改大綱比改 HTML 便宜，也比較不會破壞版面。
4. **失敗分流**：格式問題只重做 B4，事實問題退回 B2，缺資料才回 A1，避免每次都從頭來。
5. **重試上限**：避免無限迴圈；超過上限交給人決定。每次重試都留紀錄，反思時才有數字。
6. **腳本與語意檢查並用**：腳本負責能明確判斷的事（連結、來源代碼、數字是否出現在 wiki），Claude Code 負責腳本判斷不了的事（是否被來源支持、初學者懂不懂）。語意檢查用固定評分表、輸出 JSON，才能統計。
7. **每個節點都寫 trace**：反思「哪個節點最常出錯」要靠數據，不靠印象。

### 7.6 從 v1 到 v2 的修改規則

v1 的檢查配置是常見的「先生成、後查證」：B3 只確認每條大綱「有標註」wiki 頁，內容是否真的被 wiki 支持，要到 B5（P4、P5）才查。第一次執行後依下列規則決定 v2：

1. 跑 `scripts/summarize_runs.py`，統計每個節點的失敗次數與失敗原因。
2. 對失敗最多的節點，逐筆問：「這個錯誤最早在哪一步就能被發現？」
3. 把對應的檢查搬到（或加到）那一步，寫成 v2，紀錄在 `workflow/CHANGELOG.md`。
4. 用同一份 wiki 與同一份問題清單跑 run-002，比較數字。

可能的 v2 修改（只是假設，以實際數據為準）：把「內容被 wiki 支持」從 B5 搬到 B3（新增 O6）；把「術語先定義」寫進 B2 的大綱模板，讓錯誤根本不會發生。如果 run-001 的數據指向別的節點，就照數據改。如果 run-001 幾乎沒有失敗，也照實寫，並說明 v2 只做了哪些小調整、為什麼。

## 8. 檢查規格

三個檢查點共 22 項檢查（v1），另有 1 項備用的 v2 候選。每項都標明由腳本還是語意判斷、通過標準、不通過時退回哪裡。

### 8.0 共同規則

- 每次檢查產生一個 JSON，放在 `runs/<run_id>/checks/<節點>-<目標>-a<第幾次>.json`。
- 語意檢查由**另一個子代理（subagent）**執行：它只看得到待檢查的檔案、被引用的 wiki 頁、評分表，看不到生成時的對話。這樣檢查者不會替自己的作品打分。
- 語意檢查的每個判定都要附證據位置（wiki 頁 + 段落）。沒有證據就判 UNSUPPORTED。
- 每支腳本要有 `--selftest`：用 `tests/fixtures/` 裡刻意放錯的小樣本，證明腳本抓得到錯。自我測試的結果不算進 `runs/`。

JSON 格式：

```json
{
  "run_id": "run-001-v1",
  "workflow_version": "v1",
  "node": "B3",
  "attempt": 2,
  "timestamp": "2026-11-21T15:42:10+08:00",
  "target": "runs/run-001-v1/outline-v2.md",
  "results": [
    {"id": "O2", "by": "script", "status": "FAIL",
     "details": [{"where": "slide-12 第 3 點", "problem": "缺 wiki 標註"}]},
    {"id": "O3", "by": "semantic", "status": "PASS", "details": []}
  ],
  "overall": "FAIL",
  "route_to": "B2"
}
```

### 8.1 A4：Wiki Lint（`scripts/lint_wiki.py` + 語意）

| ID | 檢查 | 方式 | 通過標準 |
| --- | --- | --- | --- |
| L1 | frontmatter 齊全 | 腳本 | 每頁都有 title、type、sources、updated、status |
| L2 | 有來源 | 腳本 | `sources` 的代碼都在 `raw/sources.yaml`；含數字或超過 40 字的段落、條列都有 `[Sx …]` 標記（比喻區塊除外） |
| L3 | 無斷連 | 腳本 | 所有相對連結指向存在的檔案 |
| L4 | 無孤兒頁 | 腳本 | 每頁都被 index.md 和至少一個其他頁連到 |
| L5 | index 完整 | 腳本 | `wiki/` 下每頁都列在 index.md，沒有多列不存在的頁 |
| L6 | log 正確 | 腳本 | 最新一筆符合 `## [日期 時間] 類型 \| 標題` 格式，且對應這次 ingest |
| L7 | 版本與時效 | 腳本 + 語意 | 含參數數字的頁 `spec_version` 不是 none；「尚未」「預計」「草案」等時效說法旁有「查核日期 YYYY-MM-DD」 |
| L8 | 跨頁一致 | 腳本 + 語意 | 同一個量（例：HQC-1 公鑰大小）在各頁數值一致，或明確標為不同版本；語意層面沒有互相矛盾的說法 |
| L9 | 先討論後生成 | 腳本 | 見 §6.4 |

不通過 → A3 修正出問題的頁，最多 3 次。

### 8.2 B3：大綱檢查（`scripts/check_outline.py` + 語意）

大綱格式先定好，腳本才能解析。每張投影片一個區塊：

```markdown
## slide-07 | type: concept | 目標: G3
標題：錯誤更正碼：多傳一點，就能修正錯誤
定義：錯誤更正碼, 漢明距離, 漢明重量
- 重點一…… [wiki: concepts/error-correcting-codes.md#白話解釋]
- 重點二…… [wiki: concepts/error-correcting-codes.md#重點]
圖示：……
講者備註：……
```

| ID | 檢查 | 方式 | 通過標準 |
| --- | --- | --- | --- |
| O1 | 覆蓋 | 腳本 | §9.2 每張都有對應區塊；5 個學習目標 G1–G5 各至少有一張負責 |
| O2 | 有標註 | 腳本 | 每個重點都有 `[wiki: …]`，而且檔案與章節存在 |
| O3 | 術語先定義後使用 | 腳本 + 語意 | glossary 的術語第一次出現的那張，不早於定義它的那張 |
| O4 | 教學結構 | 腳本 | type 順序符合 §9.1；含 objectives、example、misconception、quiz、summary 各至少一張 |
| O5 | 份量 | 腳本 | 全套 18–22 張；每張重點 ≤ 4 條、每條 ≤ 40 字 |
| O6（v2 候選） | 內容被 wiki 支持 | 語意 | 每個重點都被標註的 wiki 段落支持（規則同 P4）。v1 不跑 |

不通過 → B2 重寫大綱，最多 3 次。

### 8.3 B5：成品檢查（`scripts/check_slides.py` + 語意 + 截圖）

| ID | 檢查 | 方式 | 通過標準 | 不通過退回 |
| --- | --- | --- | --- | --- |
| P1 | HTML 合法、獨立 | 腳本 | 可解析；單一檔案；不載入外部 CSS、JS、字型（連到 wiki 的超連結可以） | B4 |
| P2 | 對應 | 腳本 | 每張 `<section>` 都有 `data-wiki`，路徑存在，且與大綱一致 | 大綱也缺 → B2；否則 → B4 |
| P3 | 數字一致 | 腳本 | 投影片上的每個數字（位元組、年份、機率）都出現在該張 `data-wiki` 的頁面中 | B2 |
| P4 | 內容被支持 | 語意 | 每個事實陳述判為 SUPPORTED；任一 UNSUPPORTED 就不通過，PARTIAL 超過 2 個也不通過 | B2 |
| P5 | 沒有混用版本 | 語意 | 不同版本的數字或名稱（hqc-128 與 HQC-1）不會沒說明就放在一起；提案中的修改不會寫成定案 | B2 |
| P6 | 渲染 | 腳本（playwright） | 1280×720 與 390×844 每張截圖；沒有文字溢出（元素 scrollWidth 不大於 clientWidth）；console 沒有錯誤 | B4 |
| P7 | 導覽與互動 | 腳本（playwright） | 左右鍵換頁、頁碼與進度條正確；小測驗點選後顯示對錯 | B4 |
| P8 | 初學者看得懂 | 語意 | 以「沒學過編碼理論的大學生」角色，依 §9.1 評分表逐張評 1–5 分；任一張低於 3 分就不通過 | B2 |

B5 的兩種退回合計最多 3 次。同一次檢查同時有格式錯與內容錯時，先退回 B2（內容改了，版面反正要重做）。

## 9. HTML 簡報規格

簡報共 21 張，照「為什麼 → 基礎 → 怎麼運作 → 好壞與現況 → 確認理解」的順序。每張都標註來源 wiki 頁，頁尾可以直接點過去。2026-11-20 起篇幅集中在 HQC 技術（基礎＋運作共 12 張），動機只留 2 張。

### 9.1 教學結構

| 段落 | 投影片 | type | 目的 |
| --- | --- | --- | --- |
| 開場 | 1–2 | cover、objectives | 告訴學習者會學到什麼 |
| 動機 | 3–4 | motivation、concept | 為什麼需要後量子密碼、HQC 在哪個位置（各一張，點到為止） |
| 基礎 | 5–9 | concept、example、compare | KEM、錯誤更正碼、編碼式密碼的核心點子、準循環 |
| 運作 | 10–16 | process、example、concept | 金鑰產生、加密、解密、小數字示例、公開碼、KEM、解碼失敗率 |
| 現況 | 17–18 | compare、concept | 和 ML-KEM 比較、為什麼被選中 |
| 驗收 | 19–21 | misconception、quiz、summary | 釐清誤解、小測驗、總結 |

每張內容投影片都要有：結論式標題（一句話講完重點）、最多 4 個重點、一個圖、例子或比喻、頁尾來源。

**P8 初學者評分表**（語意檢查用，逐張評分）：

| 分數 | 標準 |
| --- | --- |
| 1 | 用了沒定義的術語，沒有例子或圖，初學者無法說出這張在講什麼 |
| 3 | 術語都定義過，但缺例子、圖或比喻；要讀兩次才懂 |
| 5 | 標題就是結論；有例子或圖；術語都先定義；一分鐘內讀完並能用自己的話複述 |

### 9.2 逐張大綱與 wiki 對應

「要回答的問題」就是 B1 查詢 wiki 的問題清單，存成 `workflow/questions.yaml`。標題可以在 B2 改寫，但要保持結論式。

| # | type | 標題（草稿） | 要回答的問題 | wiki 頁 | 目標 |
| --- | --- | --- | --- | --- | --- |
| 1 | cover | HQC 是什麼？用「故意加入的錯誤」保護量子時代的金鑰 | — | overview/hqc-overview | — |
| 2 | objectives | 看完這份簡報，你會學會 5 件事 | 學習目標與路線圖 | overview/hqc-overview | G1–G5 |
| 3 | motivation | 量子電腦會解開今天的加密，而且資料現在就可能被偷存 | 量子電腦威脅哪一類密碼？為什麼？什麼是先收集後解密？為什麼現在就要換？ | concepts/quantum-threat | G1 |
| 4 | concept | HQC 是 NIST 選出的第五個演算法，當 ML-KEM 的備援 | PQC 是什麼？HQC 排在哪、扮演什麼角色？ | concepts/post-quantum-cryptography、overview/hqc-overview | G1, G5 |
| 5 | concept | KEM：在公開網路上安全地交換一把鑰匙 | KEM 做什麼？三個函式各做什麼？ | concepts/kem | G2 |
| 6 | example | 錯誤更正碼：多傳一點，就能修正錯誤 | 什麼是錯誤更正碼？漢明距離、漢明重量是什麼？ | concepts/error-correcting-codes | G3 |
| 7 | concept | 核心點子：故意加錯誤，只有懂結構的人修得回來 | 為什麼解碼隨機的碼很難？ | concepts/syndrome-decoding、concepts/code-based-cryptography | G3 |
| 8 | compare | McEliece 把結構藏起來，HQC 乾脆不藏 | HQC 和傳統編碼式密碼的設計差在哪？ | concepts/code-based-cryptography | G3 |
| 9 | concept | 準循環：用一個向量代表一整個矩陣 | 準循環結構為什麼讓金鑰變小？ | concepts/quasi-cyclic-codes | G3 |
| 10 | process | 步驟一：金鑰產生 | x、y、h、s 各是什麼？哪些公開、哪些秘密？ | concepts/hqc-pke | G4 |
| 11 | process | 步驟二：加密 | u、v 怎麼算？訊息藏在哪裡？ | concepts/hqc-pke | G4 |
| 12 | process | 步驟三：解密——剩下的錯誤小到修得回來 | v 減掉 u·y 之後剩下什麼？為什麼能解碼？ | concepts/hqc-pke | G4 |
| 13 | example | 用小數字走一遍 HQC：從金鑰到解密 | 用很小的參數實際算一次，金鑰、密文、解密結果各長什麼樣？ | concepts/hqc-toy-example | G3, G4 |
| 14 | concept | 公開碼：Reed-Muller 與 Reed-Solomon 串起來 | 解密用的是什麼碼？為什麼公開也沒關係？ | concepts/concatenated-rm-rs | G4 |
| 15 | concept | 從加密到 KEM：多一道「重新加密檢查」 | Fujisaki-Okamoto 轉換在做什麼？ | concepts/hqc-kem-fo-transform | G2, G4 |
| 16 | concept | 解碼失敗率：小到可以忽略 | 解碼失敗率是什麼？為什麼要小於 2^-128？ | concepts/decryption-failure-rate | G4 |
| 17 | compare | HQC vs ML-KEM：數學不同，HQC 比較大、比較吃資源 | HQC-1/3/5 的金鑰與密文多大？和 ML-KEM 的數學基礎與取捨差在哪？ | comparisons/hqc-vs-ml-kem、comparisons/hqc-parameter-sets | G5 |
| 18 | concept | NIST 為什麼選 HQC 當備援 | 為什麼要備援？為什麼是 HQC 而不是其他第四輪候選？標準化到哪了？ | entities/fips-207 | G5 |
| 19 | misconception | 四個常見誤解 | HQC 要取代 ML-KEM？應該等 HQC 再遷移？故意加錯誤會讓解密常常出錯？碼是公開的，不就不安全？ | concepts/common-misconceptions | G1–G5 |
| 20 | quiz | 小測驗 | 5 題選擇題，每題對應一個目標，答後顯示解釋 | 各題對應的頁 | G1–G5 |
| 21 | summary | 五句話記住 HQC | 五個重點＋延伸閱讀（S1、S2、S4、S5、S6） | overview/hqc-overview、sources/ | — |

註：G1–G5 對應 §2.1 的 5 個學習目標。第 6 張的例子（重複碼多數決、漢明距離計算）與第 13 張的小數字 HQC 示例屬於「教學示例」，必須由 `scripts/examples.py` 算出來並存進 `concepts/error-correcting-codes.md`、`concepts/hqc-toy-example.md`，標明「示例由腳本計算」，這樣 P4 才能驗證。

2026-11-20 調整（舊編號 → 新編號）：舊 3＋4 合併為新 3；舊 5 簡化為新 4（不列五個演算法）；舊 19「計時攻擊」刪除；新增 13「小數字示例」；誤解頁換掉「PQC 等於量子密碼學？」「HQC 已被攻破？」。

### 9.3 對應機制

- 每張投影片是一個 `<section data-slide="07" data-type="example" data-wiki="concepts/error-correcting-codes.md">`。多個頁面用空格分隔。
- 頁尾顯示「Wiki：錯誤更正碼 →」，連到該頁在 GitHub 上的網址。
- B6 時腳本產生 `reports/slide_wiki_map.md`：投影片編號、標題、wiki 頁、這些頁的來源代碼（從 frontmatter 讀出）。
- 同時在每個被用到的 wiki 頁 frontmatter 加上 `used_in_slides: [7]`，形成雙向對應。

### 9.4 技術與設計要求

1. 單一檔案 `slides/index.html`，小於 500 KB，不載入任何外部 CSS、JS、字型。
2. `<html lang="zh-Hant">`；字型用系統字型：`"PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif`。
3. 16:9 版面，手機寬度自動改為直式捲動。
4. 導覽：← → 空白鍵換頁；畫面上有上一頁／下一頁按鈕；「7 / 21」頁碼；頂部進度條；網址 `#7` 可直接跳到第 7 張。
5. 配色：一個主色加中性色；文字對比至少 4.5:1。公開值與秘密值全套用固定兩種顏色（例：公開藍、秘密橘），第 10–13 張特別重要。
6. 圖：用程式畫的內嵌 SVG。第 5 張 KEM 流程、第 10–12 張演算法流程、第 13 張小數字示例、第 17 張大小長條圖（數字來自 wiki）。
7. 公式用 HTML 的 `<sub>`、`<sup>` 與 `·` 寫，例如 s = x + h·y，不引用 LaTeX 函式庫。
8. 小測驗在頁面內作答，點選後顯示對錯與解釋。
9. 每張有隱藏的講者備註 `<aside class="notes">`，按 N 顯示。
10. `@media print` 每張一頁，可以用瀏覽器印成 PDF。
11. SVG 圖加 `role="img"` 與 `aria-label`。

### 9.5 部署

1. 建立 GitHub 公開 repo `hqc-llm-wiki`，在 Settings → Pages 選「Deploy from a branch」、`main` 分支、根目錄。
2. 簡報網址：`https://<帳號>.github.io/hqc-llm-wiki/slides/`；Wiki 入口：`https://github.com/<帳號>/hqc-llm-wiki/blob/main/wiki/index.md`。
3. 部署後用無痕視窗打開兩個連結，確認不用登入就看得到。這步是 H2 的一部分。
4. `README.md` 列出三個入口：簡報、wiki、REPORT.md。

## 10. 執行紀錄與檢查紀錄規格

至少要有三段完整紀錄：一段 ingest（5 份來源）、兩次完整的簡報生成（run-001 用 v1、run-002 用 v2）。紀錄由腳本產生，只能往後加，不能事後修改。

### 10.1 trace 格式

每執行完一個節點，用 `python scripts/trace.py` 在 `runs/<run_id>/trace.jsonl` 加一行：

```json
{"ts": "2026-11-21T15:42:10+08:00", "run_id": "run-001-v1", "workflow_version": "v1",
 "step": 7, "node": "B3", "attempt": 1,
 "inputs": ["runs/run-001-v1/outline-v1.md"],
 "outputs": ["runs/run-001-v1/checks/B3-outline-v1-a1.json"],
 "result": "FAIL", "route_to": "B2",
 "reason": "<失敗的檢查 ID 與一句話原因>",
 "duration_s": 42}
```

`result` 只能是 `DONE`（動作節點）、`PASS`、`FAIL`、`ESCALATED`、`HUMAN_APPROVED`、`HUMAN_REVISE`。

### 10.2 要跑哪幾次

| 紀錄 | 內容 | 位置 |
| --- | --- | --- |
| ingest | A1–A4 對 S1、S2、S4、S5、S6 各跑一次（含所有討論輪與 lint 重試） | `runs/ingest/` |
| run-001-v1 | v1 從 B1 跑到 B6 | `runs/run-001-v1/` |
| run-002-v2 | 依 §7.6 修改後，用同一份問題清單從 B1 跑到 B6；結果是最後發布的版本 | `runs/run-002-v2/` |

開始 run-001 前打 git tag `wiki-snapshot-1`。若 run-001 因為 B1→A1 補了來源，run-002 的 wiki 就會不同，比較時要註明。

### 10.3 彙整報告

`scripts/summarize_runs.py` 讀所有 trace 與 checks，產生 `reports/run_summary.md`：

1. **節點統計**：每個節點的執行次數、失敗次數、失敗率、最常失敗的檢查 ID。
2. **檢查統計**：每個檢查 ID（L1–L9、O1–O6、P1–P8）的失敗次數。
3. **run-001 與 run-002 比較**：總步數、各檢查點失敗次數、最後一版的 UNSUPPORTED 數、人工關卡要求修改的次數、總耗時。
4. **時間線**：按時間列出每一步。
5. **圖**：用腳本產生「各節點失敗次數」長條圖 SVG（v1、v2 並排），放進 REPORT.md。

### 10.4 代表性案例

從紀錄中挑 3 個真實的失敗案例寫進 REPORT.md，每個包含：哪個節點、哪項檢查、錯在哪（附修改前片段）、退回哪裡、修改後片段、第幾次通過。優先挑不同檢查點的案例。

### 10.5 誠實原則

1. trace 與 checks 只能由腳本寫入，不可事後編輯。每完成一個檢查點就 commit，git 歷史可以佐證。
2. 若發現是檢查腳本本身有 bug：保留舊結果、寫一筆 `issue`、修腳本後重跑；這類失敗歸類為 `checker_bug`，統計時分開列。
3. 不為了「有東西可以反思」而故意做出錯的大綱或簡報，也不為了好看而修改 v1 的輸出。

### 10.6 workflow 版本管理

修改 graph 前，先把目前的 `graph.yaml`、`graph.md` 複製到 `workflow/v1/`。`workflow/CHANGELOG.md` 每版一節：

```markdown
## v2（<日期>）
- 依據：<run-001 中哪個節點、哪項檢查失敗幾次，連到 run_summary.md>
- 錯誤最早可以在哪一步發現：<節點>，理由：<…>
- 修改：<新增或搬移了哪些檢查、改了哪些邊或模板>
- 預期效果：<…>
- 實際效果（run-002 後補上）：<數字比較>
```

改完在 `wiki/log.md` 加一筆 `workflow-change`，然後依新版重畫 `graph.md` 流程圖（修改處用重點色標出）。

## 11. 反思撰寫規格

反思要逐題回答作業的三個問題，而且每個答案都要引用 `reports/run_summary.md` 的數字。Claude Code 依紀錄寫初稿（400–700 字），你再改成自己的話定稿。

### 11.1 三題各自要寫到什麼

| 問題 | 必須包含 |
| --- | --- |
| 哪一個節點最常出錯？ | 節點名稱；失敗次數與佔全部失敗的比例；最常失敗的檢查 ID；一個具體案例；錯誤的根本原因屬於哪一類（例：生成時加入 wiki 沒有的內容、術語順序、版本混用、版面溢出） |
| 你發現問題後，把檢查往前移到了哪一個步驟？ | 從哪個節點移到哪個節點；為什麼那一步就能抓到；提前抓到省下了什麼（例：不用重做整份 HTML） |
| 你有沒有因此修改 workflow／graph？為什麼？ | v1 與 v2 流程圖並排；CHANGELOG 重點；修改前後的數字比較表；有沒有改善，沒改善的話下一步會怎麼改 |

另外用一小段寫限制：只跑了兩次、樣本小；語意檢查和生成使用同一個模型家族，可能有盲點；哪些問題是人工關卡才抓到、腳本抓不到的。

### 11.2 初稿模板

```markdown
## 6. 反思

### 哪一個節點最常出錯？
在 run-001（v1）中，<節點> 失敗 <N> 次，佔全部失敗的 <P>%。
主要是 <檢查 ID>：<一句話說明>。例如 <案例，連到 checks/…json>。
我認為原因是 <根本原因>。

### 把檢查往前移到哪一步？
把 <檢查> 從 <節點 X> 移到 <節點 Y>。因為 <在 Y 就能看到問題的理由>。
這樣 <省下了什麼>。

### 有沒有修改 workflow？為什麼？
有，v1 → v2 改了 <…>（見下圖與 CHANGELOG）。
| 指標 | run-001（v1） | run-002（v2） |
| --- | --- | --- |
| 總步數 | | |
| B5 失敗次數 | | |
| 最終 UNSUPPORTED 數 | | |
結果：<有沒有改善，為什麼>。

### 限制
<…>
```

### 11.3 寫作規則

- 用第一人稱，寫具體數字，不誇大。數字一律從 run_summary.md 複製，不自己估。
- 如果最常出錯的節點和 §7.6 的預測不同，直接寫出「原本預測……，實際是……」。這比預測全對更有說服力。
- 你自己在 H1、H2 提出的修改，可以當作「人工檢查抓到的錯誤」一起討論。

## 12. 繳交文件：REPORT.md

REPORT.md 的第 1–6 節一對一對應作業的 6 個繳交項目，助教照順序看就能逐項給分。繳交時依平台要求貼上內容，或用 `pandoc REPORT.md -o REPORT.pdf` 轉成 PDF 上傳。

### 12.1 標題格式

作業規定：學校 學號 系級 姓名 主題（學校、系級打簡稱）。

```
<學校簡稱> <學號> <系級簡稱> <姓名> HQC後量子密碼教學
```

這四個欄位由你自己填，Claude Code 保留角括號佔位即可。

### 12.2 結構

| 節 | 標題 | 內容 | 對應評分 |
| --- | --- | --- | --- |
| 0 | 標頭 | 標題、三個連結（簡報、Wiki、repo） | — |
| 1 | LLM Wiki 主題與簡介 | 150–250 字：主題、讀者、為什麼選這個主題；wiki 規模（頁數、來源數、討論紀錄數）；5 份來源列表（S1、S2、S4、S5、S6） | 至少 5 篇 |
| 2 | LLM Wiki 連結與成果 | wiki/index.md 連結；目錄結構；一頁概念頁截圖；一份討論紀錄截圖（含你的回覆）；log.md 節錄 | 先討論後生成 |
| 3 | 教學 HTML 簡報 | 簡報連結；3 張截圖（封面、演算法流程、小測驗）；教學結構表；投影片 ↔ wiki 對應表（可節錄並連到全表） | 教學結構、明確對應 |
| 4 | Loop / Graph 設計 | v1 流程圖；精簡節點表；依序回答「哪些步驟重複」「哪些地方檢查或重新生成」「為什麼這樣設計」；v2 流程圖 | 設計合理且說明清楚 |
| 5 | 實際執行與檢查紀錄 | run_summary 節錄表；各節點失敗次數長條圖；3 個代表案例；連到 `runs/` | 有實際執行與檢查紀錄 |
| 6 | 反思 | 依 §11 | 反思節點與提前檢查 |
| 附錄 | 如何重現 | 安裝、執行檢查、產生彙整的指令；檔案清單 | — |

### 12.3 繳交前的連結檢查

- 無痕視窗開啟簡報連結與 wiki 連結都能看到。
- REPORT.md 裡所有圖片、相對連結在 GitHub 上都能正常顯示。
- 轉成 PDF 時，連結要是完整網址（不是相對路徑）。

## 13. 時程、風險與驗收清單

截止是 11/23（一）23:59，遲交到 11/24 16:00。目標是 11/23 20:00 前繳交，保留 4 小時緩衝。

### 13.1 時程

1. **11/19（四）晚上**：建 repo 與 GitHub Pages、寫 CLAUDE.md、建腳本骨架並通過 `--selftest`、寫 graph.yaml v1、下載 S1–S8。
2. **11/20（五）**：ingest S1–S4。你要處理 4 次討論關卡，每次約 10–15 分鐘。
3. **11/21（六）**：ingest S5–S8、全域 lint、打 tag、開始 run-001-v1。
4. **11/22（日）**：run-001 完成（含 H2）、產生彙整、決定 v2、跑 run-002-v2、發布最後版。
5. **11/23（一）**：REPORT.md、反思定稿、連結檢查、填標題繳交。

時間不夠時的取捨：S3、S7、S8 已在 2026-11-20 依使用者要求拿掉，剩 5 份，不能再砍；只能把簡報縮到 18 張。run-002 不要砍，它是 9–10 分「調整檢查流程」的證據。（11/20–11/21 的 ingest 排程改為：S2、S4、S5、S6。）

### 13.2 已知風險

| 風險 | 對策 |
| --- | --- |
| 來源連結失效或下載被擋 | 你手動下載放進 `raw/`，log.md 記一筆 issue |
| 不同版本的數字混在一起（例：2,249 與 2,241） | L7、L8、P5 三道檢查；一律以 2025-08-22 版為準 |
| FIPS 207 在這幾天公布 | §5.3 的時效查核；公布就加 S9 |
| `playwright` 裝不起來 | P6、P7 改由你截圖與手動測試，紀錄為人工檢查 |
| 討論關卡變成只回「確認」 | 依 §6.3，每次至少做一個決定 |
| 語意檢查替自己打高分 | 由看不到生成對話的子代理檢查（§8.0） |
| GitHub Pages 部署延遲 | 11/19 就先部署一個空白頁測試 |
| 引用他人著作的版權 | §5.4：非 NIST PDF 不進公開 repo；摘要一律改寫 |

### 13.3 最終驗收清單

**Wiki**

- [ ] R1 `wiki/` 至少 15 頁概念、實體、比較頁，加上 index、log、glossary（2026-11-20 由 20 改為 15，預定頁見 §4.5）
- [ ] R2 每份來源都有討論紀錄，第 7 節是你的回覆原文，L9 通過
- [ ] R3 5 份來源（S1、S2、S4、S5、S6）完成 ingest，log.md 有對應紀錄
- [ ] 全域 lint L1–L9 全部通過

**簡報**

- [ ] R4 GitHub Pages 網址可用無痕視窗開啟
- [ ] R5 教學結構完整（學習目標、例子、誤解、小測驗、總結），P8 每張 ≥ 3 分
- [ ] 每張投影片有 `data-wiki` 與頁尾來源連結，`reports/slide_wiki_map.md` 已產生
- [ ] 最後一版 P1–P8 全部通過

**Loop / Graph**

- [ ] R6 `workflow/v1/`、`workflow/v2/` 各有 graph.yaml 與流程圖
- [ ] R7–R9 REPORT.md 第 4 節依序回答「哪些步驟重複」「哪些地方檢查或重新生成」「為什麼」

**紀錄與反思**

- [ ] R10 `runs/ingest/`、`runs/run-001-v1/`、`runs/run-002-v2/` 都有 trace 與 checks
- [ ] `reports/run_summary.md` 與失敗次數長條圖已產生
- [ ] R11–R13 反思三題都有數字、案例、v1/v2 比較
- [ ] 反思已由你改成自己的話

**繳交**

- [ ] REPORT.md 第 1–6 節齊全，所有連結可開
- [ ] 標題格式：學校 學號 系級 姓名 主題
- [ ] 11/23 23:59 前上傳

## 本規格參考的資料

查核日期：2026-11-19。S1–S8 的連結見 §5.1。

- [Karpathy：LLM Wiki（GitHub gist，2026-04）](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)：三層架構與 ingest、query、lint 操作。
- [HQC 官方規格書 2025-08-22](https://www.pqc-hqc.org/doc/hqc_specifications_2025_08_22.pdf)：參數命名 HQC-1/3/5 與大小。
- [Open Quantum Safe：HQC 頁面](https://openquantumsafe.org/liboqs/algorithms/kem/hqc)：2023 版參數（hqc-128 公鑰 2,249 位元組），用於確認版本差異。
- [IETF 草案：HQC-KEM Key Agreement for TLS 1.3（2026-10）](https://datatracker.ietf.org/doc/draft-preussmattsson-tls-hqckem/)：註明撰寫時 FIPS 207 尚未發布。
- [NIST：Status Report on the Fourth Round（IR 8545）更正請求回應](https://www.nist.gov/document/bernstein-2025-initial-response)：表 5 Classic McEliece 數字的爭議。
