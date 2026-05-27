module seg_proc (
    input wire clk,  // 50MHz 时钟信号
    input wire rst_n,  // 低电平复位信号
    input wire [31:0] seg_number_in,  // 输入的数字内容
    input wire [7:0] dp,  // 每个位的小数点状态（1: 显示小数点，0: 不显示）
    output wire [7:0] dula,  // 段选信号
    output wire [7:0] wela  // 位选信号
);

    wire       clk_1k;  // 1kHz 时钟信号
    reg  [2:0] bits;  // 当前显示的数码管位索引（0 到 7）
    reg  [3:0] current_num;  // 当前显示位的数字内容
    reg        current_dp;  // 当前显示位的小数点状态

    // 分频器实例化，将 50MHz 时钟分频至 1kHz
    frequency_divider u_frequency_divider (
        .clk    (clk),
        .rst_n  (rst_n),
        .clkbase(50_000_000),
        .clkdiv (1_000),
        .clkout (clk_1k)
    );

    // 根据当前的位选择信号 bits，选择对应的数码管输入数据和小数点状态
    always @(*) begin
        current_num = seg_number_in[(7-bits)*4+:4];  // 选择相应的数字
        current_dp  = dp[7-bits];  // 获取小数点状态
    end

    // 数码管驱动模块实例化
    seg_driver u_seg_driver (
        .digit       (current_num),
        .rst_n       (rst_n),
        .current_dp  (current_dp),
        .position    (bits),
        .digit_sel   (wela),
        .segment_data(dula)
    );

    // 动态扫描逻辑，每 1ms 切换一个显示位
    always @(posedge clk_1k or negedge rst_n) begin
        if (!rst_n) bits <= 3'd0;  // 复位时从第 0 位开始显示
        else bits <= (bits == 3'd7) ? 3'd0 : bits + 3'd1;  // 切换到下一个显示位
    end
endmodule
