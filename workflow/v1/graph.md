# Workflow v1 流程圖

12 個節點：8 個動作、3 個自動檢查點（菱形）、2 個人工關卡（紅框）。
機器可讀定義見 [graph.yaml](graph.yaml)，規格見 [SPEC.md §7](../SPEC.md#7-loop--graph-設計)。

```mermaid
flowchart TB
    subgraph PA["階段一：建立 Wiki（每份來源跑一次）"]
        A1["A1 取得來源<br/>raw/ + sources.yaml"]
        A2["A2 寫討論備忘錄<br/>discussions/NN-*.md"]
        H1{{"H1 使用者確認<br/>【人工關卡】"}}
        A3["A3 寫入 Wiki<br/>頁面 + index + log + glossary"]
        A4{"A4 Wiki lint<br/>L1–L9"}
        A1 --> A2 --> H1
        H1 -- 確認 --> A3
        H1 -- 要修改 --> A2
        A3 --> A4
        A4 -- 不通過<br/>最多 3 次 --> A3
        A4 -- 通過，還有來源 --> A1
    end

    subgraph PB["階段二：產生簡報（每次執行跑一次）"]
        B1["B1 查詢 Wiki<br/>queries/q-*.md"]
        B2["B2 整理大綱<br/>outline-vN.md"]
        B3{"B3 大綱檢查<br/>O1–O5"}
        B4["B4 產生 HTML<br/>slides-vN.html"]
        B5{"B5 成品檢查<br/>P1–P8 + 截圖"}
        H2{{"H2 使用者預覽<br/>【人工關卡】"}}
        B6["B6 發布<br/>slides/index.html → GitHub Pages"]
        B1 -- 有答案 --> B2 --> B3
        B3 -- 不通過<br/>最多 3 次 --> B2
        B3 -- 通過 --> B4 --> B5
        B5 -- 格式錯 --> B4
        B5 -- 內容錯 --> B2
        B5 -- 通過 --> H2
        H2 -- 內容問題 --> B2
        H2 -- 版面問題 --> B4
        H2 -- 通過 --> B6
    end

    A4 -- 通過，來源都完成 --> B1
    B1 -. wiki 缺資料<br/>每次最多補 2 份 .-> A1

    classDef human fill:#fde8e8,stroke:#c0392b,stroke-width:2px,color:#000
    classDef check fill:#fff4d6,stroke:#b7791f,color:#000
    class H1,H2 human
    class A4,B3,B5 check
```

## 重試上限

| 檢查點 | 退回 | 上限 | 超過時 |
| --- | --- | --- | --- |
| A4 | A3 | 3 次 | `ESCALATED`，交給使用者決定 |
| B3 | B2 | 3 次 | 同上 |
| B5 | B4（格式）或 B2（內容） | 兩種合計 3 次 | 同上 |
| B1 → A1 | 補來源 | 每次執行 2 份 | 同上 |
| 階段二總步數 | — | 15 步 | 同上 |
