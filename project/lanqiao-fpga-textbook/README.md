# 蓝桥杯 FPGA 开发教程

本仓库用于发布《蓝桥杯 FPGA 开发教程》PDF 与配套 Markdown 文档，面向零基础读者学习 DP2026/CT137X 竞赛平台、Verilog 基础模块、常用外设驱动和竞赛题目实现思路。

## 下载

- [蓝桥杯FPGA开发教程_详细注释版.pdf](pdf/蓝桥杯FPGA开发教程_详细注释版.pdf)
- [教程 Markdown 摘要](docs/蓝桥杯FPGA开发教程.md)
- [项目阅读总结](docs/project_reading_summary.md)
- [硬件资料提取索引](docs/title_docs_extract.md)

## 内容范围

- CT137X / Spartan-7 竞赛平台硬件资源说明
- XDC 引脚约束、IO 电平和常用外设引脚映射
- I2C、UART、SPI、DS1302、W25Q128、SRAM、数码管、按键消抖等核心模块
- Driver 与 User Verilog 模块源码注释版阅读
- 蓝桥杯 FPGA 真题与模拟题实战章节

## 生成脚本

教材 PDF 由 `scripts/generate_textbook_v3.py` 生成。脚本依赖 Python 3 与 ReportLab，字体按本地 Windows 环境配置：

- 代码字体：`E:\素材\字体\font\MapleMono-NF-CN-Medium.ttf`
- 中文标题：`SimHei`
- 中文正文：`Microsoft YaHei`

## 当前状态

当前 PDF 已完成多轮内容增强：

- 页数：99 页
- 已加入 I2C、UART、SPI、状态机、按键消抖、亚稳态、数码管动态扫描、SRAM、DS1302、W25Q128 等零基础讲解
- 已嵌入 9 份扫描题面，共 46 页图片
- 已修复生成脚本中的附录调用、目录页码占位和代码章节排序问题

### 已嵌入题面

1. 第十六届蓝桥杯（电子类）FPGA设计与开发省赛真题
2. 第十七届蓝桥杯FPGA省赛真题（客观题）
3. 第十七届蓝桥杯FPGA省赛真题（设计题）
4. 十六届蓝桥杯FPGA模拟试题 I / II / III
5. 第十七届FPGA模拟考试 I / II / III

后续会继续迭代：

- 将扫描题面逐题文字化整理为 Markdown
- 增加错题解析和知识点索引
- 优化排版和美化细节，准备出版

## 说明

本仓库不包含原始竞赛资料包、原始 PDF 题面和开发板厂商工具，仅发布学习整理文档与生成脚本。若引用官方题目或资料，请遵守对应赛事与资料版权要求。
