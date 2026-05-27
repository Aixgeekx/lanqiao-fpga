# Aix_tools

本目录保存本项目的辅助阅读、记忆和验证资料。

- `project_reading_summary.md`：项目结构、官方板卡资料、RTL 模块地图和风险点。
- `title_docs_extract.md`：从 `title` 官方 PDF/XLSX 提取的资料索引，证件号已脱敏。
- `extract_title_docs.py`：生成 `title_docs_extract.md` 的辅助脚本。
- `template_memory_guide.md`：CT137X 模板记忆与赛场应用手册。
- `top_syntax.vvp`：`iverilog -g2005` 语法检查产物，可删除后重新生成。
- `generate_textbook_v3.py`：教材 PDF 主生成脚本。当前版本已修复附录调用，目录页码第一遍加入占位页，加入出版说明、赛场速查卡、第三章“核心原理与真题实战”、第16届国赛完整结构化整理、第17届省赛结构化整理，并自动嵌入 `真题模拟题/extracted_images` 下 9 组扫描题面图片。
- `pdf_check/`：新版 PDF 渲染抽检图片目录，用于检查目录页、协议讲解页、题面页和代码页是否排版正常。
