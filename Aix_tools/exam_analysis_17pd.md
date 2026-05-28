# 第17届省赛程序设计题解析

## 题目来源
第十七届 蓝桥杯（电子类）FPGA设计与开发项目 省赛 - 第二部分 程序设计试题（85分）

---

## 一、题目概述

设计一个**串行工序控制器**，管理加载(LOAD)、加工(PROCESS)、检测(INSPECT)、卸载(UNLOAD)四个工序，支持循环执行，循环次数可控。

## 二、系统架构拆解

### 2.1 五层模块划分

| 层级 | 功能 | 对应模块 |
|------|------|---------|
| 输入采样层 | 按键消抖、ADC读取 | key_ctrl + adc_ctrl |
| 时序控制层 | 状态机、倒计时、分频 | fsm_ctrl + countdown |
| 数据存储层 | 循环次数N、ADC值、状态 | 寄存器组 |
| 算法层 | 1kHz PWM输出 | pwm_gen |
| 显示输出层 | 数码管、LED、信号输出 | seg_proc + led_proc |

### 2.2 状态机设计（6个状态）

```
IDLE → LOAD → PROCESS → INSPECT → UNLOAD → (N>1? LOAD : IDLE)
                ↓ (ADC<32)
              ERROR → (S4) → IDLE
```

状态编码建议：
```verilog
localparam S_IDLE    = 3'd0;
localparam S_LOAD    = 3'd1;
localparam S_PROCESS = 3'd2;
localparam S_INSPECT = 3'd3;
localparam S_UNLOAD  = 3'd4;
localparam S_ERROR   = 3'd5;
```

## 三、关键设计要点

### 3.1 状态跳转条件

| 当前状态 | 跳转条件 | 目标状态 |
|---------|---------|---------|
| IDLE | ADC≥128 且 S1按下 | LOAD |
| LOAD | 倒计时5秒结束 | PROCESS |
| PROCESS | 倒计时8秒结束 | INSPECT |
| INSPECT | ADC<32（立即跳转）| ERROR |
| INSPECT | 倒计时8秒结束 | UNLOAD |
| UNLOAD | 倒计时5秒结束且N>1 | LOAD（N减1）|
| UNLOAD | 倒计时5秒结束且N=1 | IDLE |
| ERROR | S4按下 | IDLE |

### 3.2 倒计时实现

50MHz时钟下：
- 5秒 = 50_000_000 × 5 = 250_000_000 个时钟周期
- 8秒 = 50_000_000 × 8 = 400_000_000 个时钟周期

```verilog
// 倒计时计数器（28位足够）
reg [27:0] cnt_down;
wire cnt_done = (cnt_down == 0);

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) cnt_down <= 0;
    else if (state != next_state) begin  // 状态切换时重载
        case (next_state)
            S_LOAD:    cnt_down <= 28'd250_000_000;
            S_PROCESS: cnt_down <= 28'd400_000_000;
            S_INSPECT: cnt_down <= 28'd400_000_000;
            S_UNLOAD:  cnt_down <= 28'd250_000_000;
            default:   cnt_down <= 0;
        endcase
    end else if (!pause && cnt_down > 0) begin
        cnt_down <= cnt_down - 1;
    end
end
```

### 3.3 按键有效性控制

题目要求按键在特定状态下才有效：

```verilog
// S1仅在IDLE且ADC≥128时有效
wire s1_valid = (state == S_IDLE) && (adc_value >= 8'd128) && s1_press;
// S2仅在IDLE时有效
wire s2_valid = (state == S_IDLE) && s2_press;
// S3仅在LOAD/PROCESS/INSPECT/UNLOAD时有效
wire s3_valid = (state == S_LOAD || state == S_PROCESS || 
                 state == S_INSPECT || state == S_UNLOAD) && s3_press;
// S4仅在ERROR时有效
wire s4_valid = (state == S_ERROR) && s4_press;
```

### 3.4 1kHz PWM输出

50MHz下1kHz的周期 = 50000个时钟周期。

```verilog
// PROCESS状态：90%占空比（高45000，低5000）
// INSPECT状态：10%占空比（高5000，低45000）
reg [15:0] pwm_cnt;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) pwm_cnt <= 0;
    else if (pwm_cnt >= 16'd49999) pwm_cnt <= 0;
    else pwm_cnt <= pwm_cnt + 1;
end

assign signal_out = (state == S_PROCESS && pwm_cnt < 16'd45000) ? 1'b1 :
                    (state == S_INSPECT && pwm_cnt < 16'd5000)  ? 1'b1 :
                    1'b0;
```

### 3.5 数码管显示格式

```
COM1: N（固定字符）
COM2: 循环次数（1-9）
COM3-4: 熄灭
COM5-7: ADC值（000-127）
COM8: 熄灭
```

IDLE状态下时间显示位（COM6-8）熄灭。
非IDLE状态下显示倒计时秒数。

### 3.6 LED指示灯

| LED | 条件 | 说明 |
|-----|------|------|
| LD1 | state == S_IDLE | 空闲指示 |
| LD2 | state == S_LOAD | 加载指示 |
| LD3 | state == S_PROCESS | 加工指示 |
| LD4 | state == S_INSPECT | 检测指示 |
| LD5 | state == S_UNLOAD | 卸载指示 |
| LD6 | state == S_ERROR, 0.2s闪烁 | 错误报警 |
| LD7-8 | 熄灭 | 未使用 |

LD6闪烁实现（0.2秒 = 10_000_000 时钟周期）：
```verilog
reg [23:0] blink_cnt;
reg blink;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin blink_cnt <= 0; blink <= 0; end
    else if (blink_cnt >= 24'd9_999_999) begin
        blink_cnt <= 0; blink <= ~blink;
    end else blink_cnt <= blink_cnt + 1;
end
assign led[5] = (state == S_ERROR) ? blink : 1'b1;  // 低有效
```

## 四、实现顺序建议（赛场策略）

1. **先建最小工程**：时钟、复位、LED1亮 → 验证工程能跑
2. **接按键**：S1-S4消抖，先用LED显示按下状态
3. **接ADC**：读取电位器值，显示到数码管
4. **实现状态机**：先只做IDLE→LOAD→PROCESS→INSPECT→UNLOAD→IDLE跳转
5. **加倒计时**：每个状态倒计时，数码管显示秒数
6. **加S2循环次数**：N从1到9循环
7. **加S3暂停/恢复**：pause标志控制倒计时
8. **加PWM输出**：PROCESS和INSPECT状态的1kHz信号
9. **加ERROR状态**：INSPECT中ADC<32跳转，LD6闪烁
10. **加S4重置**：ERROR状态下S4回IDLE

每一步都保留可观察输出（LED或数码管），不要一次写完所有功能再测试。

## 五、常见易错点

1. **按键消抖**：必须用10ms/20ms低频采样，不能直接用50MHz
2. **LED极性**：CT137X的LED低电平点亮，输出需要取反
3. **数码管重影**：切换位选前先关闭所有段选
4. **ADC读取**：I2C读取需要时间，不能每个时钟都读
5. **倒计时精度**：用状态切换边沿重载计数器，不要用组合逻辑
6. **暂停恢复**：暂停时保持计数器值，恢复后继续递减
7. **N减1时机**：在UNLOAD状态结束时减1，不是进入时
8. **RESET优先级**：复位必须优先于所有其他逻辑
