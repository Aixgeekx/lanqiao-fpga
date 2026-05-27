### 2026-05-20 PDF full extraction timeout
- **现象**：对 `title` 下所有 PDF 逐页全文抽取时，命令 300 秒超时。
- **原因**：Xilinx 官方 user guide 和器件 datasheet 页数很多，全文逐页解析成本过高。
- **解决**：改用 `Aix_tools/extract_title_docs.py`，对小型官方资料全文抽取，对大型 datasheet 抽页数、首页/尾页和关键词摘要。
- **教训**：以后读取 FPGA 官方资料包时先按页数分级，赛题、引脚表、用户手册优先全文抽取，大型参考手册只建索引。

### 2026-05-20 Icarus Verilog generation flag mismatch
- **现象**：`iverilog -g2012` 报 `Unknown/Unsupported Language generation 2012`。
- **原因**：本机 Icarus Verilog 版本只列出 `1995/2001/2005/system-verilog` 等生成选项。
- **解决**：当前模板改用 `iverilog -g2005 -o Aix_tools\top_syntax.vvp user\*.v driver\*.v`，语法检查通过。
- **教训**：本项目做快速语法检查时优先用 `-g2005`，除非后续确认该环境支持 SystemVerilog 标志。
