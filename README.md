# 蓝桥杯国一工程模板及零基础教学

> 蓝桥杯 FPGA 设计与开发（AMD/Xilinx 平台）**国一工程模板**与**零基础教学**资源库。从零基础到国赛一等奖，一套工程模板、16 个驱动模块、真题全覆盖。

**适用平台**：CT137X 竞赛平台（AMD/Xilinx FPGA）　　**当前版本**：v0.2.2

---

## 为什么选择这套模板

| 亮点 | 说明 |
|:---|:---|
| **国一工程模板** | 经过第十六、十七届蓝桥杯省赛和国赛实战验证的工程结构，拿到手就能用 |
| **16 个驱动模块** | ADC / DAC / DS1302 / EEPROM / IIC / LED / SEG / SPI / SRAM / UART / W25Q128 等，全部可复用 |
| **真题全覆盖** | 第十六届省赛真题 + 国赛真题、第十七届省赛真题 + 3 套模拟题，含题目内容提取 |
| **零基础入门** | Verilog 入门、大模板建立教程、FPGA 课程安排、竞赛规则说明，从零开始也能上手 |
| **竞赛平台资料** | CT137X 引脚表、数据手册、比赛手册、SEG 编码表，备赛所需一应俱全 |
| **自动化工具链** | PDF 提取、自动同步、版本发布脚本，省去重复劳动 |

---

## 教材与发行包

- 最新 PDF：`results/蓝桥杯FPGA开发教程_详细注释版.pdf`
- 轻量发布包：`releases/lanqiao-fpga-textbook-pdf-v0.2.2.zip`
- 完整发布包：`releases/lanqiao-fpga-textbook-v0.2.2.zip`

当前 PDF 为 118 页，约 7.0 MB，正文可抽取字符 136364 个；35 个表格全部带“表 N”编号，46 个题面页全部带“图 N”编号。本轮新增“考场时间分配建议”和“ZIP压缩包检查单”，用于赛场纸质手册和发布包交付检查。

---

## 项目结构

```
all_code/
├── driver/                 # 16 个可复用外设驱动模块
│   ├── adc_ctrl.v          # ADC 采样控制
│   ├── dac_ctrl.v          # DAC 输出控制
│   ├── ds1302_*.v          # DS1302 实时时钟驱动
│   ├── eeprom_*.v          # EEPROM 读写控制
│   ├── frequency_driver.v  # 频率测量
│   ├── iic_drive.v         # IIC 总线驱动
│   ├── key_ctrl.v          # 按键消抖与状态机
│   ├── led_display.v       # LED 显示控制
│   ├── seg_driver.v        # 数码管驱动（含编码表）
│   ├── spi_master.v        # SPI 主机驱动
│   ├── sram_ctrl.v         # SRAM 读写控制
│   ├── uart_rx/tx.v        # UART 收发
│   └── w25q128_ctrl.v      # W25Q128 Flash 控制
│
├── user/                   # 顶层应用逻辑与题目实现
│   ├── top.v               # 顶层模块（板级封装）
│   ├── top_board.v         # 板级顶层
│   ├── key_proc.v          # 按键处理逻辑
│   ├── led_proc.v          # LED 处理逻辑
│   ├── seg_proc.v          # 数码管处理逻辑
│   ├── uart_parser.v       # UART 协议解析
│   └── uart_string_sender.v
│
├── study/                  # 零基础入门与学习资料
│   ├── FPGA_BEGINNER_GUIDE.md      # FPGA 零基础入门指南
│   ├── STORAGE_DRIVER_USAGE.md     # 存储驱动使用说明
│   ├── key_ctrl.v / top.v          # 入门示例代码
│   └── 参考资料/                    # PDF 教程（Verilog 入门、大模板建立等）
│
├── title/                  # 竞赛平台资料与数据手册
│   ├── DP2026_FPGA_AMD_Xilinx/     # CT137X 平台引脚表与数据手册
│   └── 比赛手册.pdf
│
├── 真题模拟题/              # 第十六、十七届真题与模拟题
│   ├── 第十六届 省赛真题.pdf
│   ├── 16届FPGA国赛题.pdf
│   ├── FPGA_17PD.pdf / FPGA_17PS.pdf  # 第十七届省赛真题
│   ├── 模拟题 I / II / III.pdf         # 第十七届模拟题
│   └── 题目内容提取.txt                # 题目文本提取（方便检索）
│
├── Aix_tools/              # 辅助工具（PDF 提取、自动同步、版本发布）
├── project/                # 教材发布副本（含生成的 PDF）
└── results/                # 最终生成结果和可提交文件
```

---

## 驱动模块速查

| 模块 | 文件 | 功能 |
|:---|:---|:---|
| ADC | `adc_ctrl.v` | ADC 采样控制，支持多通道 |
| DAC | `dac_ctrl.v` | DAC 输出控制 |
| DS1302 | `ds1302_io_convert.v` / `ds1302_wr_drive.v` | 实时时钟读写驱动 |
| EEPROM | `eeprom_read_ctrl.v` / `eeprom_write_ctrl.v` | IIC EEPROM 读写 |
| 频率测量 | `frequency_driver.v` | 信号频率测量 |
| IIC | `iic_drive.v` | IIC 总线时序驱动 |
| 按键 | `key_ctrl.v` | 按键消抖 + 短按/长按状态机 |
| LED | `led_display.v` | LED 显示控制 |
| 数码管 | `seg_driver.v` | 数码管动态扫描驱动 |
| SPI | `spi_master.v` | SPI 主机时序驱动 |
| SRAM | `sram_ctrl.v` | SRAM 读写控制 |
| UART | `uart_rx.v` / `uart_tx.v` | UART 收发，可配置波特率 |
| W25Q128 | `w25q128_ctrl.v` | SPI Flash 读写控制 |

---

## 零基础入门路线

1. **Verilog 基础** → `study/参考资料/快速掌握veirlog.pdf`
2. **建立工程模板** → `study/参考资料/蓝桥杯FPGA大模板建立（数码管，按键，LED）.pdf`
3. **了解竞赛规则** → `study/参考资料/第十六届蓝桥杯大赛电子赛竞赛规则及说明.pdf`
4. **学习驱动模块** → `driver/` 目录下逐个阅读，每个模块独立可复用
5. **刷真题** → `真题模拟题/` 目录下第十六、十七届真题 + 模拟题
6. **查看题目提取** → `真题模拟题/题目内容提取.txt`，快速检索题目要求

---

## 真题与模拟题列表

| 届次 | 类型 | 文件 |
|:---|:---|:---|
| 第十六届 | 省赛真题 | `第十六届 蓝桥杯（电子类）FPGA设计与开发省赛真题.pdf` |
| 第十六届 | 国赛真题 | `16届FPGA国赛题.pdf` |
| 第十七届 | 省赛真题 | `FPGA_17PD.pdf` / `FPGA_17PS.pdf` |
| 第十七届 | 模拟题 I | `第十七届FPGA模拟考试I.pdf` |
| 第十七届 | 模拟题 II | `第十七届FPGA模拟考试II.pdf` |
| 第十七届 | 模拟题 III | `第十七届FPGA模拟考试III.pdf` |
| 第十六届 | 模拟题 I / II / III | `十六届蓝桥杯FPGA模拟试题I/II/III.pdf` |

---

## GitHub 同步

远程仓库：

```powershell
git remote -v
```

已启用 Git LFS，`.exe` 大文件通过 LFS 上传：

```powershell
git lfs ls-files
```

## 持续监视与自动推送

```powershell
# 启动（每 60 秒自动检查、提交、推送）
powershell -NoProfile -ExecutionPolicy Bypass -File .\Aix_tools\watch_and_push.ps1 -IntervalSeconds 60

# 停止
Stop-Process -Id (Get-Content .\Aix_tools\git_watch_push.pid)
```

## 版本管理

版本文件：`VERSION` / `CHANGELOG.md`

```powershell
# 发布新版本
# 1. 修改 VERSION 和 CHANGELOG.md
# 2. 提交并推送
git add VERSION CHANGELOG.md
git commit -m "chore: release v0.2.2"
git push

# 3. 创建 Git 标签
powershell -NoProfile -ExecutionPolicy Bypass -File .\Aix_tools\release_version.ps1 -Version 0.2.2
```

规则：修 bug / 改文档 → 修订版本（0.2.0 → 0.2.1）；增加功能 / 章节 → 次版本（0.2.0 → 0.3.0）；结构大改 → 主版本（1.0.0 → 2.0.0）。

---

## 许可

本项目仅供学习交流使用。真题版权归蓝桥杯大赛组委会所有。
