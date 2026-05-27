# 进度记录

## 当前目标

持续迭代《蓝桥杯 FPGA 开发教程》PDF 与 Markdown 发布仓库，面向零基础读者补全协议原理、外设时序、真题模拟题题面和生成验证流程。

## 已完成

- 创建公开 GitHub 仓库：`https://github.com/Aixgeekx/lanqiao-fpga-textbook`
- 本地发布仓库：`project/lanqiao-fpga-textbook`
- 修复 `Aix_tools/generate_textbook_v3.py` 附录调用错误：改为直接 `build_appendix(st)`
- 修复第一遍页码计算未包含目录页的问题：第一遍加入 `build_toc(st)` 作为占位
- 修复 Driver/User 章节排序与目录不一致的问题：增加 `MODULE_ORDER`
- 第三章重构为”核心原理与真题实战”
- 已补充教育性内容：
  - 状态机、Moore vs Mealy、三段式状态机
  - 按键消抖、亚稳态、两级同步器
  - I2C 起始条件、地址帧、ACK、采样规则
  - UART 8N1 帧格式、波特率计算
  - SPI 主从模式、CPOL/CPHA、全双工、DS1302 类 SPI
  - 数码管动态扫描、SRAM 时序、DS1302 RTC、W25Q128 Flash
- 已嵌入 9 份扫描题面，共 46 页图片：
  - 第十六届 蓝桥杯（电子类）FPGA设计与开发省赛真题
  - 第十七届蓝桥杯FPGA省赛真题（客观题 + 设计题）
  - 十六届蓝桥杯FPGA模拟试题I / II / III
  - 第十七届FPGA模拟考试I / II / III
- 新版 PDF 已生成：
  - 路径：`results/蓝桥杯FPGA开发教程_详细注释版.pdf`
  - 页数：99
  - 图片页：46 页

## 验证结果

- `python -m py_compile Aix_tools/generate_textbook_v3.py` 通过
- `python Aix_tools/generate_textbook_v3.py` 通过
- PyMuPDF 检查命中关键字：全部 9 份题名
- 已同步到 `project/lanqiao-fpga-textbook` 并更新 Markdown

## 待完成

- 对扫描题逐页人工文字化整理，增加错题解析和对应知识点索引
- 优化排版美化，准备出版
- 持续迭代并上传 GitHub
