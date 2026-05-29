# 踩坑记录

### 2026-05-27 扫描题面 PDF 没有文字层
- **现象**：6 份扫描版真题/模拟题用 PyMuPDF 抽取文字时字符数为 0。
- **原因**：PDF 页面是图片，没有可复制文本；本机没有可直接使用的 Tesseract 或 Windows OCR 命令。
- **解决**：本轮先用 ReportLab 将 `真题模拟题/extracted_images` 下的 PNG 页面按题目顺序嵌入教材，确保题面完整进入 PDF。
- **教训**：后续若要逐题文字化解析，需要先安装可靠 OCR，或人工读取题面后整理成结构化 Markdown。

### 2026-05-27 代码章节目录与正文顺序不一致
- **现象**：目录显示 `4.1 key_ctrl.v`，但正文 4.1 实际输出为 `adc_ctrl.v`。
- **原因**：`read_verilog()` 按文件名字母序读取，目录使用人工教学顺序，二者没有统一排序来源。
- **解决**：新增 `MODULE_ORDER`，Driver/User 文件按教学顺序读取，目录和正文编号恢复一致。
- **教训**：生成类文档的目录、正文和页码必须共享同一份排序配置，不能一处硬编码一处自动排序。

### 2026-05-28 Windows PowerShell 读取 UTF-8 无 BOM 脚本乱码
- **现象**：`powershell -File Aix_tools\release_version.ps1` 解析中文异常消息时报 `Unexpected token`。
- **原因**：Windows PowerShell 5.1 默认按本地代码页读取无 BOM UTF-8，中文字符串被错误解码。
- **解决**：发布脚本内部异常消息改为 ASCII，保证 `powershell.exe` 和 `pwsh` 都能执行。
- **教训**：需要兼容 Windows PowerShell 5.1 的 `.ps1` 文件尽量使用 ASCII，或明确使用带 BOM 的 UTF-8。

### 2026-05-27 PDF文字层直接铺正文影响纸质阅读
- **现象**：第17届省赛客观题和程序设计题可抽取文字，但直接塞入正文后页面过密，不适合纸质手册和出版排版。
- **原因**：原PDF文字层是题面流式文本，缺少章节层级和表格结构，ReportLab按正文排版后可读性差。
- **解决**：改为“结构化摘要表 + FSM速查表 + 完整扫描题面图片”，既保留完整题面，又提升纸质阅读效率。
- **教训**：扫描题和原题文字不能机械堆入教材，出版稿应先做结构化整理，再保留原题作为附图或题面页。

### 2026-05-28 ReportLab嵌入大PNG导致MemoryError
- **现象**：生成教材第二遍构建 PDF 时，在 `asciiBase85Encode` 阶段触发 `MemoryError`。
- **原因**：46 张扫描题面 PNG 原图直接嵌入 ReportLab，两遍构建同时保留大量图片对象，内存占用过高。
- **解决**：新增 `compressed_exam_image()`，先把题面 PNG 压缩为 JPEG 缓存到 `Aix_tools/pdf_assets/exam_images`，再嵌入 PDF；第一遍构建后删除 `content_story`、`doc1` 并执行 `gc.collect()`。
- **教训**：教材生成包含大量扫描页时，必须先建立压缩缓存，再进入两遍页码生成流程，不能直接把原始大图塞进 story。

### 2026-05-29 Git MCP 提交触发 Git LFS hook PATH 问题
- **现象**：通过 Git MCP 提交时，`.git/hooks/post-commit` 报 `git-lfs was not found on your path`，但提交本身已经生成。
- **原因**：Git MCP 执行 hook 的环境 PATH 未包含本机 `git-lfs`，普通 PowerShell 中 `git lfs version` 正常。
- **解决**：确认提交已存在、`git lfs status` 正常后继续使用普通 PowerShell 执行后续推送和发布校验。
- **教训**：涉及 Git LFS 的仓库，若 Git MCP 提交报 hook 找不到 `git-lfs`，先检查提交是否已生成，再用当前 shell 验证 `git lfs status`，不要重复提交。
