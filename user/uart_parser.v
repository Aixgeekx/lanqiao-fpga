module uart_parser #(
    parameter MAX_LENGTH = 16,         // 最大字符串长度（可配置）
    parameter UART_BPS   = 115200,     // 串口波特率
    parameter CLK_FREQ   = 50_000_000  // 时钟频率
) (
    input  wire       clk,         // 时钟信号
    input  wire       rst_n,       // 复位信号（低电平有效）
    input  wire       rx,          // 串口接收数据信号
    output wire       parse_done,  // 数据解析完成信号
    output reg  [7:0] cmd_signal   // 解析出的命令信号
);

    // 串口接收模块输出信号
    wire [7:0] po_data;  // 串口接收的数据字节
    wire       po_flag;  // 串口接收数据完成标志

    // 状态机的状态定义
    localparam RECEIVE = 2'b00;  // 接收数据状态
    localparam PARSE = 2'b01;  // 解析数据状态

    // 状态机相关信号
    reg [1:0] state;  // 当前状态
    reg [1:0] next_state;  // 下一个状态

    // 数据缓冲区和计数器
    reg [7:0] data_buffer[MAX_LENGTH-1:0];  // 数据缓冲区，存储接收到的数据
    reg [4:0] data_count;  // 当前缓冲区中的数据计数

    // 解析相关信号
    reg parse_done_r;  // 数据解析完成标志寄存器
    reg state_CR;  // 检测 '\r' 的状态标志

    // ==================== 状态机时序逻辑 ====================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= RECEIVE;  // 复位时进入接收状态
        end else begin
            state <= next_state;  // 更新当前状态
        end
    end

    // 数据缓冲区的初始化和数据接收逻辑
    integer i;
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            data_count <= 0;  // 清空接收数据计数器
            state_CR   <= 0;  // 清除 '\r' 状态标志
            for (i = 0; i < MAX_LENGTH; i = i + 1) begin
                data_buffer[i] <= 8'h00;  // 将缓冲区初始化为 0
            end
        end else begin
            case (state)
                RECEIVE: begin
                    if (po_flag) begin  // 如果接收到新数据
                        if (po_data == 8'h0D) begin  // 检测 '\r' (回车符)
                            state_CR <= 1;  // 设置回车状态标志
                        end else if (state_CR) begin
                            if (po_data == 8'h0A) begin  // 检测 '\n' (换行符)
                                state_CR <= 0;  // 如果换行符跟在回车符后，结束本次接收
                            end else begin
                                state_CR   <= 0;  // 否则清除回车状态标志
                                data_count <= 0;  // 重置数据计数器
                            end
                        end else if (data_count < MAX_LENGTH) begin
                            data_buffer[data_count] <= po_data;  // 存储接收到的数据
                            data_count <= data_count + 1;  // 增加计数器
                        end
                    end
                end
                PARSE: begin
                    data_count <= 0;  // 清空数据计数器
                    state_CR   <= 0;  // 清除回车状态标志
                end
            endcase
        end
    end

    // 状态机的下一状态逻辑
    always @(*) begin
        next_state = state;  // 默认保持当前状态
        case (state)
            RECEIVE: begin
                if (po_flag && state_CR && po_data == 8'h0A) begin
                    next_state = PARSE;  // 如果检测到 '\r\n'，进入解析状态
                end
            end
            PARSE: begin
                if (parse_done_r) begin
                    next_state = RECEIVE;  // 如果解析完成，返回接收状态
                end
            end
        endcase
    end

    // 将解析完成信号输出
    assign parse_done = parse_done_r;

    // 数据解析逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            parse_done_r <= 0;  // 清除解析完成信号
            cmd_signal   <= 8'h00;  // 清空命令信号
        end else begin
            case (state)
                PARSE: begin
                    parse_done_r <= 1;  // 设置解析完成信号
                    case (data_buffer[0])  // 根据接收到的第一个字符判断命令
                        "A": cmd_signal <= 8'h01;  // 如果接收到 'A'，命令为 0x01
                        "W": cmd_signal <= 8'h00;  // 如果接收到 'W'，命令为 0x00
                        default: cmd_signal <= 8'h00;  // 其他字符默认为 0x00
                    endcase
                end
                default: begin
                    parse_done_r <= 0;  // 其他状态清除解析完成信号
                end
            endcase
        end
    end

    // 实例化串口接收模块
    uart_rx #(
        .UART_BPS(UART_BPS),  // 串口波特率参数
        .CLK_FREQ(CLK_FREQ)   // 时钟频率参数
    ) u_uart_rx (
        .clk    (clk),      // 输入：时钟信号
        .rst_n  (rst_n),    // 输入：复位信号
        .rx     (rx),       // 输入：串口接收数据
        .po_data(po_data),  // 输出：接收到的数据字节
        .po_flag(po_flag)   // 输出：接收完成标志
    );

endmodule
