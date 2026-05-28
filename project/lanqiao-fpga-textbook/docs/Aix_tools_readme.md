# Aix_tools

本目录保存本项目的辅助阅读、记忆和验证资料。

- `project_reading_summary.md`：项目结构、官方板卡资料、RTL 模块地图和风险点。
- `title_docs_extract.md`：从 `title` 官方 PDF/XLSX 提取的资料索引，证件号已脱敏。
- `extract_title_docs.py`：生成 `title_docs_extract.md` 的辅助脚本。
- `template_memory_guide.md`：CT137X 模板记忆与赛场应用手册。
- `top_syntax.vvp`：`iverilog -g2005` 语法检查产物，可删除后重新生成。
- `generate_textbook_v3.py`：教材 PDF 主生成脚本。当前版本已修复附录调用，目录页码第一遍加入占位页，加入出版说明、纸质使用建议、零基础14天学习路线、赛场速查卡、Vivado工程创建流程、第三章“核心原理与真题实战”、第16届国赛完整结构化整理、第17届省赛结构化整理、真题训练索引与错题复盘表，并自动嵌入 `真题模拟题/extracted_images` 下 9 组扫描题面图片。
- `pdf_assets/exam_images/`：题面图片 JPEG 压缩缓存目录。脚本会把 46 张扫描 PNG 压缩后再嵌入 PDF，避免 ReportLab 两遍生成时占用过多内存。
- `pdf_check/`：新版 PDF 渲染抽检图片目录，用于检查目录页、协议讲解页、题面页和代码页是否排版正常。
- `watch_and_push.ps1`：持续监视项目变更并自动提交、拉取、推送到 `origin/main`，日志和 PID 分别写入 `git_watch_push.log`、`git_watch_push.pid`。
- `release_version.ps1`：读取 `VERSION` 或指定版本号，创建 `vX.Y.Z` Git 标签并推送到远程仓库。
- `patch_table_numbers.py`：一次性补丁工具，用于给教材生成脚本增加图表编号相关函数和样式。
- `patch_exam_analysis.py`：一次性补丁工具，用于把真题结构化解析段落插入教材生成脚本。

## 当前 PDF 状态

- 输出文件：`results/蓝桥杯FPGA开发教程_详细注释版.pdf`
- 当前规模：113 页，约 6.9 MB，正文可抽取字符 130162 个。
- 题面素材：已嵌入 9 组真题/模拟题，共 46 页图片，均经过 JPEG 缓存压缩。
- 最近验证：`python -m py_compile Aix_tools/generate_textbook_v3.py` 与 `python Aix_tools/generate_textbook_v3.py` 均通过；关键字命中“零基础14天学习路线”“Vivado工程创建流程”“真题训练索引与错题复盘表”“错题复盘模板”“官方资料依据速查”。

## 真题分析辅助文件

- `extracted_16national.txt`：第16届 FPGA 国赛题面文字抽取结果。
- `exam_analysis_16national.md`：第16届 FPGA 国赛题目架构拆解、算法模块和实现要点解析。
- `extracted_17ps.txt`：第17届 FPGA 省赛客观题文字抽取结果。
- `extracted_17pd.txt`：第17届 FPGA 省赛程序设计题文字抽取结果。
- `exam_analysis_17ps.md`：第17届 FPGA 省赛客观题答案解析和知识点索引。
- `exam_analysis_17pd.md`：第17届 FPGA 省赛程序设计题架构拆解、模块设计和评分点解析。
