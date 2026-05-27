module uart_string_sender #(
    parameter MAX_LENGTH = 16,         // 最大字符串长度（可配置）
    parameter UART_BPS   = 115200,     // 串口波特率
    parameter CLK_FREQ   = 50_000_000  // 时钟频率
) (
    input  wire                    clk,           // 时钟信号
    input  wire                    rst_n,         // 复位信号（低电平有效）
    input  wire [8*MAX_LENGTH-1:0] string_data,   // 输入的字符串数据（宽总线）
    input  wire [             3:0] data_length,   // 实际需要发送的长度（动态指定）
    input  wire                    send_trigger,  // 发送触发信号
    output wire                    tx,            // 串口发送引脚
    output reg                     busy           // 模块忙碌信号（正在发送数据）
);

    // ==================== 状态定义 ====================
    localparam IDLE = 2'b00;  // 空闲状态
    localparam LOAD = 2'b01;  // 装载数据状态
    localparam SEND = 2'b10;  // 发送数据状态
    localparam DONE = 2'b11;  // 完成状态

    // 状态变量
    reg [1:0] current_state, next_state;  // 当前状态和下一状态

    // ==================== 内部信号 ====================
    reg  [3:0] cnt;  // 字符计数器，用于指示发送到第几个字符
    reg  [7:0] pi_data;  // 当前发送的单字节数据
    reg        pi_flag;  // 当前发送触发信号
    wire       tx_done;  // 串口发送完成信号

    // ==================== 状态机：状态转移逻辑 ====================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            current_state <= IDLE;  // 复位时进入空闲状态
        end else begin
            current_state <= next_state;  // 状态更新
        end
    end

    // ==================== 状态机：下一状态逻辑 ====================
    always @(*) begin
        next_state = current_state;  // 默认保持当前状态
        case (current_state)
            IDLE: begin
                if (send_trigger) begin
                    next_state = LOAD;  // 接收到发送触发信号后，进入装载状态
                end
            end
            LOAD: begin
                next_state = SEND;  // 装载完成后，进入发送状态
            end
            SEND: begin
                if (tx_done) begin
                    if (cnt + 1 == data_length) begin
                        next_state = DONE;  // 所有字符发送完成后，进入完成状态
                    end else begin
                        next_state = LOAD;  // 否则继续装载下一个字符
                    end
                end
            end
            DONE: begin
                next_state = IDLE;  // 完成状态结束后，返回空闲状态
            end
        endcase
    end

    // ==================== 状态机：状态行为逻辑 ====================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt     <= 0;  // 字符计数器复位
            pi_flag <= 0;  // 发送触发标志复位
            pi_data <= 8'h00;  // 当前发送数据复位
            busy    <= 0;  // 空闲标志复位
        end else begin
            case (current_state)
                IDLE: begin
                    cnt <= 0;     // 计数器清零
                    pi_flag <= 0; // 清除发送标记
                    pi_data <= 8'h00; // 清空发送数据
                    busy <= 0;    // 标记为空闲
                end
                LOAD: begin
                    pi_data <= string_data[(data_length-1-cnt)*8+:8]; // 提取当前要发送的字符
                    pi_flag <= 1;  // 发送触发标志有效
                    busy <= 1;  // 标记为忙碌
                end
                SEND: begin
                    pi_flag <= 0;  // 清除发送触发标志
                    if (tx_done) begin
                        cnt <= cnt + 1;  // 如果发送完成，计数器加1
                    end
                end
                DONE: begin
                    busy <= 0;  // 标记为空闲，发送结束
                end
            endcase
        end
    end

    // ==================== 串口发送模块实例化 ====================
    uart_tx #(
        .UART_BPS(UART_BPS),  // 波特率配置
        .CLK_FREQ(CLK_FREQ)   // 时钟频率配置
    ) uart_tx_inst (
        .clk    (clk),      // 时钟信号
        .rst_n  (rst_n),    // 复位信号
        .pi_data(pi_data),  // 输入：当前发送的单字节数据
        .pi_flag(pi_flag),  // 输入：发送触发信号
        .tx_done(tx_done),  // 输出：发送完成标志
        .tx     (tx)        // 输出：串口发送信号
    );

endmodule
