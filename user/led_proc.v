module led_proc (
    input  wire       clk,    // 50MHz 时钟输入
    input  wire       rst_n,  // 低电平复位信号
    input  wire [1:0] mode,   // 模式选择信号
    output wire [7:0] led     // LED 输出
);
    reg  [7:0] led_pattern;  // LED 控制模式寄存器
    wire       clk_1;  // 1Hz 分频时钟信号

    // 实例化 frequency_divider 模块，将 50MHz 时钟分频到 1Hz
    frequency_divider freq_div_inst (
        .clk    (clk),         // 原始时钟信号 50MHz
        .rst_n  (rst_n),       // 低电平复位信号
        .clkbase(50_000_000),  // 基准时钟频率为 50MHz
        .clkdiv (1),           // 期望输出频率为 1Hz
        .clkout (clk_1)        // 输出分频后的 1Hz 时钟信号
    );

    // 根据 mode 模式和 1Hz 慢时钟信号 clk_1 控制 LED 模式
    always @(posedge clk_1 or negedge rst_n) begin
        if (!rst_n) begin
            led_pattern <= 8'b0000_0001;  // 复位时默认模式（初始值）
        end else begin
            case (mode)
                2'b00:   led_pattern <= {led_pattern[6:0], led_pattern[7]};  // 左移模式
                2'b01:   led_pattern <= {led_pattern[0], led_pattern[7:1]};  // 右移模式
                2'b10:   led_pattern <= ~led_pattern;  // 闪烁模式
                2'b11:   led_pattern <= 8'b1010_1010;  // 固定模式
                default: led_pattern <= 8'b0000_0001;  // 默认模式为左移
            endcase
        end
    end

    // 实例化 LED 显示模块，将 led_pattern 映射到实际 LED 输出
    led_display led_display_inst (
        .led_pattern(led_pattern),  // 输入的 LED 控制模式
        .led        (led)           // 映射到实际 LED 显示
    );
endmodule
