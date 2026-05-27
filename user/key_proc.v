module key_proc (
    input  wire       clk,         // 系统时钟信号
    input  wire       rst_n,       // 低电平复位信号
    input  wire [3:0] key_in,      // 4 个按键输入信号
    output reg  [1:0] mode,        // 模式输出，用于切换 LED 显示模式
    output reg        write_pulse  // 写入数据的单周期脉冲信号
);

    wire [3:0] down;  // 每个按键的按下检测信号
    wire [3:0] up;  // 每个按键的松开检测信号
    wire       clk_100;  // 100Hz 时钟，用于按键消抖

    // 频率分频器生成 100Hz 时钟
    frequency_divider u_frequency_divider (
        .clk    (clk),
        .rst_n  (rst_n),
        .clkbase(50_000_000),
        .clkdiv (100),
        .clkout (clk_100)
    );

    // 按键消抖模块
    key_ctrl key_ctrl_inst (
        .clk_100(clk_100),  // 系统时钟输入
        .rst_n  (rst_n),    // 低电平复位信号
        .key_in (key_in),   // 按键输入信号
        .down   (down),     // 按下检测输出
        .up     (up)        // 松开检测输出
    );

    // 模式切换逻辑
    always @(posedge clk_100 or negedge rst_n) begin
        if (!rst_n) begin
            mode <= 2'b00;  // 复位时模式设为初始模式 0
        end else begin
            if (down[0]) mode <= 2'b00;  // 按键0：切换到模式 0
            else if (down[1]) mode <= 2'b01;  // 按键1：切换到模式 1
            else if (down[2]) mode <= 2'b10;  // 按键2：切换到模式 2
            else if (down[3]) mode <= 2'b11;  // 按键3：切换到模式 3
        end
    end

    // 写入脉冲生成逻辑
    always @(posedge clk_100 or negedge rst_n) begin
        if (!rst_n) begin
            write_pulse <= 1'b0;  // 复位时清零
        end else if (down[0]) begin
            write_pulse <= 1'b1;  // 按下按键0时产生写入脉冲
        end else begin
            write_pulse <= 1'b0;  // 脉冲保持一个周期后清零
        end
    end
endmodule
