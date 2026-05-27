module frequency_divider (
    input  wire        clk,      // 输入时钟
    input  wire        rst_n,    // 低电平复位
    input  wire [31:0] clkbase,  // 基准时钟频率（单位：Hz），例如50MHz
    input  wire [31:0] clkdiv,   // 期望输出频率（单位：Hz），如1000代表1kHz
    output reg         clkout    // 输出时钟
);
    reg [31:0] counter;  // 计数器
    reg [31:0] limit;  // 计数限制值

    // 计算每个分频周期的计数限制
    always @* begin
        if (clkdiv > 0) begin
            limit = clkbase / (2 * clkdiv);  // 计算分频周期
        end else begin
            limit = 0;  // 防止除以零
        end
    end

    // 计数逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter <= 0;  // 复位计数器
            clkout  <= 0;  // 复位输出时钟
        end else begin
            if (limit > 0) begin
                if (counter >= limit - 1) begin
                    clkout  <= ~clkout;  // 翻转输出时钟
                    counter <= 0;  // 计数器归零
                end else begin
                    counter <= counter + 1;  // 计数器加一
                end
            end
        end
    end
endmodule
