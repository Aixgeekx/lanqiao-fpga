# FPGA 新手上手指南

## 1. 先按层次读这套代码

- `code/driver/`：通用驱动层。先学这一层，除非确认有 bug，否则不要一开始就重写。
- `code/user/`：用户逻辑和示例层。比赛做题时，主要改这一层。
- `title/DP2026_FPGA_AMD_Xilinx/BSP/`：官方参考驱动、约束文件和板卡资料。

最重要的两个文件是：

- `top_board.v`：板级包装层。上板综合时建议把它设为顶层。
- `top.v`：核心逻辑层。比赛做题时优先改这个文件。

`top_board.v` 已经帮你处理了两件事：

- 把开发板的高有效 `RESET` 转成核心逻辑使用的低有效 `sys_rst_n`
- 把板上的 `S1..S4`、`COM1..COM8`、`SEGA..SEGDP` 映射到 `top.v` 使用的总线端口

## 2. 这些驱动可以直接用

- `frequency_divider.v`：分频器，可生成 `100Hz`、`1kHz`、`1Hz` 等慢时钟
- `key_ctrl.v`：按键消抖，并输出按下/松开脉冲
- `seg_driver.v`：驱动单个扫描位的数码管
- `seg_proc.v`：如果你想直接驱动 8 位数码管，可以直接用它
- `uart_rx.v` / `uart_tx.v`：字节级 UART 收发
- `uart_parser.v`：解析简单串口命令，如 `A\r\n`
- `uart_string_sender.v`：通过 UART 发送短字符串
- `adc_ctrl.v`：通过 I2C 读取 ADC
- `dac_ctrl.v`：通过 I2C 写 DAC
- `eeprom_read_ctrl.v` / `eeprom_write_ctrl.v`：EEPROM 单字节读写
- `ds1302_wr_drive.v`：DS1302 实时时钟读写

## 3. 两个必须记住的坑

- 板卡的 `RESET` 是高有效，但这里大多数用户代码使用的是低有效 `rst_n`
- 在 `key_ctrl.v` 里，`up` 才是“按下脉冲”，`down` 是“松开脉冲”，名字很容易看反

## 4. 一道常见比赛题应该怎么做

1. 从 `top.v` 开始，不要先改板级包装层。
2. 把“你的逻辑”集中放在一个区域里，例如计数器、状态机、判断逻辑、协议控制。
3. 能复用驱动就复用，不要一上来自己手搓底层时序。
4. 对 I2C、RTC 这类驱动，把它们当成“事务模块”：
   给一个单周期启动脉冲，然后等待 `*_end_flag` 或 `*_ack`
5. 逻辑先跑通，再把结果接到 LED、数码管、UART 或外设上。

推荐的结构是：

- 按键或 UART 产生命令
- 你的状态机更新内部状态
- 显示模块把状态显示出来
- 外设驱动只做单一职责

## 5. 三天学习安排

### 第一天

- 读 `top.v`、`top_board.v`、`frequency_divider.v`、`key_ctrl.v`、`seg_driver.v`
- 跑一次 `top_board` 的语法和展开检查
- 修改 `top.v`，做到按 S1/S2/S3/S4 时，数码管能明显变化

### 第二天

- 读 `uart_rx.v`、`uart_tx.v`、`uart_parser.v`、`uart_string_sender.v`
- 做一个 UART 小例子：接收一个命令字节，修改计数值或模式，再回发一个字符串
- 再读 `adc_ctrl.v`、`dac_ctrl.v`、`eeprom_read_ctrl.v`、`eeprom_write_ctrl.v`
- I2C 外设先只练一个，优先练 ADC 或 EEPROM

### 第三天

- 读 `ds1302_wr_drive.v` 和 `ds1302_test.v`
- 做一个 RTC 小例子：写入固定时间，再把读回来的时间显示出来
- 给自己整理一份比赛模板：按键输入 + 显示输出 + 一个状态机 + 一个可选外设

## 6. 本地常用命令

PowerShell 语法检查：

```powershell
$files = (Get-ChildItem code\driver\*.v),(Get-ChildItem code\user\*.v) | ForEach-Object { $_.FullName }
xvlog $files
```

展开当前示例：

```powershell
xelab top
xelab top_board
xelab ds1302_test
```

## 7. 先改哪里

如果题目只是计数、定时、按键扫描、数码管显示：

- 直接改 `top.v`

如果题目涉及外设：

- 在 `top.v` 里例化对应驱动
- 协议细节留在驱动层
- 你自己只写一个小状态机控制外设什么时候启动、什么时候取结果

如果你拿到真实比赛题，我最快的处理方式是直接帮你拆成：

- 需要哪些输入
- 需要哪些输出
- 要用哪些驱动
- `top.v` 里该加什么状态机
