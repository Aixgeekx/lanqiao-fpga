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
- 出版与纸质手册定位增强：
  - 加入出版说明页、纸质使用建议、赛场速查卡
  - 封面改为“赛场手册与开发教程”，署名为“Aix，极道工作室”
  - 第17届省赛客观题和程序设计题改为结构化整理，并保留完整题面图片
  - 附录新增 `title` 官方资料依据速查表和 CT137X 关键硬件事实表
  - 第16届国赛补充完整结构化题目摘要，覆盖硬件资源、性能、数据录入、算法、显示、按键功能、串口上报和推荐顶层状态划分
- 新版 PDF 已生成：
  - 路径：`results/蓝桥杯FPGA开发教程_详细注释版.pdf`
  - 页数：111
  - 图片页：46 页
  - 表格编号：21个表格全部带"表 N"编号
  - 图片编号：46个题面页全部带"图 N"编号
  - 参考文献：12条，含Xilinx官方文档、四梯科技手册和芯片数据手册

## 验证结果

- `python -m py_compile Aix_tools/generate_textbook_v3.py` 通过
- `python Aix_tools/generate_textbook_v3.py` 通过
- PyMuPDF 检查命中关键字：出版说明、赛场速查卡、第16届国赛题目完整结构、录入界面、按键功能、串口上报格式、推荐顶层状态划分、第17届省赛题目摘要、程序设计题FSM速查、全部 9 份题名、官方资料依据速查、CT137X关键硬件事实
- 已渲染抽检封面、出版说明、速查卡、目录、题面页、代码页和附录页到 `Aix_tools/pdf_check/`

## 待完成

- 对扫描题逐页人工文字化整理，增加错题解析和对应知识点索引
- 优化排版美化，准备出版
- 同步本轮 98 页新版 PDF、脚本和 Markdown 到 GitHub
- 持续迭代并上传 GitHub
