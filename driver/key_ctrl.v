module key_ctrl (
    input  wire       clk_100,  // 输入时钟信号(100Hz)
    input  wire       rst_n,    // 低电平复位信号
    input  wire [3:0] key_in,   // 4 个按键输入信号
    output reg  [3:0] down,     // 按键按下检测信号（下降沿触发）
    output reg  [3:0] up        // 按键释放检测信号（上升沿触发）
);

    reg [3:0] val;  // 当前按键状态
    reg [3:0] old;  // 上一个时钟周期的按键状态

    // 按键状态检测逻辑
    always @(posedge clk_100 or negedge rst_n) begin
        if (!rst_n) begin
            // 复位时将所有状态设为未按下
            val  <= 4'b1111;    // 假设按键为低电平有效，初始化为高电平未按下状态
            old <= 4'b1111;  // 上一个状态初始化为高电平
            down <= 4'b0000;  // 初始时没有按键按下
            up <= 4'b0000;  // 初始时没有按键释放
        end else begin
            old <= val;  // 保存当前状态到 old 以便下一个周期比较
            val <= key_in;  // 更新 val 为当前的按键状态

            // 检测按键按下：val 和 old 比较，下降沿检测
            down <= val & (val ^ old);  // val 为低且 val 与 old 不同，说明按键刚被按下

            // 检测按键释放：val 和 old 比较，上升沿检测
            up   <= ~val & (val ^ old); // val 为高且 val 与 old 不同，说明按键刚被释放
        end
    end
endmodule
