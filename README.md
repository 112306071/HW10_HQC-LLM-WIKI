# HQC LLM Wiki 與教學簡報

主題：**HQC 是什麼？用「故意加入的錯誤」保護量子時代的金鑰**

| 入口 | 連結 |
| --- | --- |
| 教學 HTML 簡報 | https://112306071.github.io/HW10_HQC-LLM-WIKI/slides/ （原始檔 [slides/index.html](slides/index.html)） |
| LLM Wiki | [wiki/index.md](wiki/index.md) |
| 繳交報告 | [REPORT.md](REPORT.md)（完成後補上） |
| 規格書 | [SPEC.md](SPEC.md) |
| 流程圖 | [workflow/graph.md](workflow/graph.md) |

## 怎麼重現

```bash
python3 -m venv .venv && .venv/bin/pip install pyyaml beautifulsoup4 playwright
.venv/bin/python -m playwright install chromium

# 檢查腳本的自我測試
.venv/bin/python scripts/lint_wiki.py --selftest
.venv/bin/python scripts/check_outline.py --selftest
.venv/bin/python scripts/check_slides.py --selftest
.venv/bin/python scripts/examples.py --selftest
```
