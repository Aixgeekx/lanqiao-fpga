# CT137X 模板记忆与赛场应用手册

## 1. 先记整体骨架

这套模板分三层：

1. `top_board.v`：板卡适配层，负责把官方引脚名接到你的逻辑端口。
2. `top.v`：赛题业务层，按题目写状态机、计数器、显示内容、外设流程。
3. `driver/*.v`：器件驱动层，负责 I2C、UART、RTC、SRAM、Flash、数码管、按键等底层时序。

考场上不要背整套代码，按这个顺序搭：

```text
官方引脚 -> top_board -> top -> 驱动模块 -> 显示/存储/通信结果
```

最重要的板卡事实：

```text
GCLK = 50MHz
RESET = 高有效
S1-S4 = 低有效
LED = 低电平点亮
数码管 = 共阳段码，低电平点亮段
I2C = ADC + DAC + EEPROM 共用 SCL/SDA
```

## 2. 必背最小系统

每道题都先写这个思路：

```verilog
module top (
    input  wire       sys_clk,
    input  wire       sys_rst_n,
    input  wire [3:0] key,
    output wire [7:0] led,
    output wire       buz,
    output wire [7:0] seg_sel,
    output wire [7:0] seg_data
);
```

然后固定三件事：

```text
分频 -> 按键 -> 状态/数据显示
```

## 3. 分频器记忆

模块名是 `frequency_divider`，文件名是 `frequency_driver.v`。

```verilog
frequency_divider u_div (
    .clk    (sys_clk),
    .rst_n  (sys_rst_n),
    .clkbase(32'd50_000_000),
    .clkdiv (32'd1000),
    .clkout (clk_1k)
);
```

记忆点：

```text
clkbase 写 50_000_000
clkdiv 写目标频率
100Hz 给按键
1kHz 给数码管扫描
1Hz 给慢速显示或计时
```

## 4. 按键记忆

CT137X 按键低有效。当前 `key_ctrl` 的实际行为：

```text
up   = 按下脉冲
down = 松开脉冲
```

所以业务逻辑里优先这样接：

```verilog
wire [3:0] key_press;

key_ctrl u_key (
    .clk_100(clk_100),
    .rst_n  (sys_rst_n),
    .key_in (key),
    .down   (),
    .up     (key_press)
);
```

常用写法：

```verilog
always @(posedge clk_100 or negedge sys_rst_n) begin
    if (!sys_rst_n) begin
        mode <= 2'd0;
    end else if (key_press[0]) begin
        mode <= mode + 1'b1;
    end
end
```

## 5. LED 记忆

板上 LED 低电平亮，模板里 `led_display` 已经取反：

```verilog
led_display u_led (
    .led_pattern(led_pattern),
    .led        (led)
);
```

你只要记：

```text
led_pattern 里 1 表示想让灯亮
真正输出给板子的 led 会自动取反
```

## 6. 数码管记忆

最推荐直接用 `seg_proc`，输入 8 个 4-bit 数字：

```verilog
seg_proc u_seg (
    .clk          (sys_clk),
    .rst_n        (sys_rst_n),
    .seg_number_in({d7, d6, d5, d4, d3, d2, d1, d0}),
    .dp           (8'b0000_0000),
    .dula         (seg_data),
    .wela         (seg_sel)
);
```

注意当前 `seg_proc` 取数方式是：

```text
bits=0 显示 seg_number_in[31:28]
bits=7 显示 seg_number_in[3:0]
```

特殊数字：

```text
0-9 = 正常数字
10  = 灭
11  = -
12  = C
15  = F
```

## 7. 蜂鸣器记忆

蜂鸣器可以先按 `top.v` 的简单方案：

```text
mode=0 静音
mode=1 500Hz
mode=2 1kHz
mode=3 2kHz
```

如果题目只要求响/不响，直接：

```verilog
assign buz = enable ? buz_clk : 1'b1;
```

当前模板假设蜂鸣器低有效，所以静音时输出 1。

## 8. UART 记忆

底层两个模块：

```text
uart_rx: rx -> po_data + po_flag
uart_tx: pi_data + pi_flag -> tx + tx_done
```

接收核心：

```verilog
uart_rx u_rx (
    .clk    (sys_clk),
    .rst_n  (sys_rst_n),
    .rx     (rx),
    .po_data(rx_data),
    .po_flag(rx_flag)
);
```

发送核心：

```verilog
uart_tx u_tx (
    .clk    (sys_clk),
    .rst_n  (sys_rst_n),
    .pi_data(tx_data),
    .pi_flag(tx_flag),
    .tx_done(tx_done),
    .tx     (tx)
);
```

记忆点：

```text
rx_flag 来一个周期，表示收到一个字节
tx_flag 拉高一个周期，开始发一个字节
tx_done 来一个周期，表示一个字节发完
```

## 9. I2C 外设记忆

I2C 底层 `iic_drive` 很长，不建议赛场完整手搓。优先记三个封装：

```text
adc_ctrl           读 ADC，输出 ad_data
dac_ctrl           写 DAC，输入 da_data
eeprom_read_ctrl   读 EEPROM
eeprom_write_ctrl  写 EEPROM
```

统一规律：

```text
start_flag 拉高启动
end_flag/ready 表示完成或空闲
scl/sda 接官方 I2C 引脚
```

ADC：

```verilog
adc_ctrl u_adc (
    .sys_clk           (sys_clk),
    .rst_n             (sys_rst_n),
    .ad_read_start_flag(adc_start),
    .ad_read_end_flag  (adc_done),
    .scl               (scl),
    .ad_data           (adc_data),
    .sda               (sda)
);
```

DAC：

```verilog
dac_ctrl u_dac (
    .sys_clk            (sys_clk),
    .rst_n              (sys_rst_n),
    .da_write_start_flag(dac_start),
    .da_write_end_flag  (dac_done),
    .scl                (scl),
    .da_data            (dac_data),
    .sda                (sda)
);
```

EEPROM：

```text
写：addr + data + write_start
读：addr + read_start -> read_data
```

## 10. RTC DS1302 记忆

DS1302 不建议完整默写底层，优先记 `ds1302_test` 封装：

```text
write_second/minute/hour/date/month/week/year
write_time_req
read_second/minute/hour/date/month/week/year
ds1302_ce / ds1302_sclk / ds1302_io
```

注意：

```text
DS1302 数据通常是 BCD
秒寄存器 bit7 是 CH，模板会尝试清除 CH
```

## 11. SRAM 和 Flash 记忆

SRAM：

```text
read_req / write_req
addr[16:0]
write_data
read_data
ready / done
sram_addr / sram_data / sram_ce_n / sram_oe_n / sram_we_n
```

W25Q128：

```text
op_code=0 读 JEDEC ID
op_code=1 读状态寄存器
op_code=2 读单字节
op_code=3 写单字节
op_code=4 擦除扇区
```

这两个属于低中频考点，能看懂调用即可，不作为第一优先级默写。

## 12. 赛场应用流程

拿到题目后按 6 步走：

1. 圈出输入：按键、ADC、UART、RTC、EEPROM、SRAM、Flash。
2. 圈出输出：LED、数码管、蜂鸣器、DAC、UART。
3. 先写 `top` 端口，只保留题目用到的外设。
4. 写按键/计时/状态机，把题目流程跑通。
5. 接显示，把内部变量显示到数码管或 LED。
6. 最后接复杂外设，用 `start/done` 状态机包住驱动。

通用状态机套路：

```text
IDLE -> START -> WAIT_DONE -> SAVE_RESULT -> DISPLAY
```

## 13. 背诵优先级

第一优先级，必须能默写：

```text
top 骨架
frequency_divider 例化
key_ctrl 例化
seg_proc 例化
LED 低有效取反概念
BCD 加减计数
简单状态机
```

第二优先级，必须能套：

```text
uart_rx / uart_tx
adc_ctrl
dac_ctrl
eeprom_read_ctrl / eeprom_write_ctrl
ds1302_test
```

第三优先级，理解接口：

```text
iic_drive
ds1302 底层三件套
sram_ctrl
w25q128_ctrl
```

## 14. 练习安排

每天 30-45 分钟，按这个顺序练：

1. 不看代码写 `top + 分频 + 按键 + LED`。
2. 不看代码写 `top + 数码管显示 12345678`。
3. 写 S1 加一、S2 减一、数码管显示 0000-9999。
4. 写 S3 切 LED 模式，S4 切蜂鸣器模式。
5. 接 UART，收到 `A` 切模式，收到 `W` 清零。
6. 接 ADC 显示采样值，或接 DAC 输出按键调节值。
7. 接 EEPROM 保存/读取一个配置值。

最终目标不是背下所有源码，而是看到题目能在 10 分钟内搭出：

```text
时钟 + 复位 + 按键 + 状态机 + 显示
```

复杂外设再按题目选择性补上。
