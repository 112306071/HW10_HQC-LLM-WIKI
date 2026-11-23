# run-001-v1 執行中的問題紀錄

trace 與 checks 只能往後加，不能改；執行中發現的流程問題記在這裡。

## [2026-11-23 13:31] issue | trace #12 比實際修改早幾秒

- 經過：B3 第 4 次（outline-v4）不通過後，我用一個指令同時做三件事：複製出 outline-v5.md、套用修改、寫 trace #12（B2 DONE）。套用修改那段因為工作目錄不對，找不到 `.venv/bin/python`，沒有執行；但後面的 trace 指令照樣跑了。
- 結果：trace #12 寫入時，outline-v5.md 還是 v4 的原樣複本。13:31 發現後補上修改（第 7 張第 4 點改白話），之後才送 B3 第 5 次檢查，所以檢查的是修改後的版本。
- 影響：trace #12 的 ts 比實際完成時間早約 1 分鐘，其他內容正確。
- 以後的做法：產出檔案與寫 trace 分成兩個指令，確認產出無誤再寫 trace。

## [2026-11-23 13:25] issue | B3 重試上限怎麼算，規格沒寫清楚

- 經過：B3 前三次（outline-v1～v3）第 3 次通過。之後 B5 以內容問題退回 B2，產生 outline-v4，又要再過 B3。check_outline.py 自動把它編成第 4 次。
- 解讀：graph.yaml 的 `max_attempts_per_check_node: 3` 是為了擋「同一個迴圈連續失敗」。前一輪已經通過，這是新的一輪，所以從 1 重新計算，沒有 ESCALATED。
- 待辦：v2 在 graph.yaml 寫明計算方式。
