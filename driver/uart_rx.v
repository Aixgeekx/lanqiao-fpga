/* UART接收模块
    一.模块功能：
    1.支持可配置的波特率
    2.支持8位数据位，1位起始位，1位停止位
    3.支持无校验位
    4.支持数据接收完成标志输出
    5.支持数据同步和亚稳态处理

    二.模块说明：
    1.使用状态机实现UART接收时序
    2.波特率通过参数配置，默认115200
    3.系统时钟频率通过参数配置，默认50MHz
    4.使用两级寄存器同步输入数据，消除亚稳态
*/

module uart_rx #(
    parameter UART_BPS = 115200,     // 串口波特率（默认115200）
    parameter CLK_FREQ = 50_000_000  // 系统时钟频率（默认50MHz）
) (
    input  wire       clk,      // 输入：系统时钟信号（50MHz）
    input  wire       rst_n,    // 输入：全局复位信号（低电平有效）
    input  wire       rx,       // 输入：串行数据输入
    output reg  [7:0] po_data,  // 输出：8位并行数据
    output reg        po_flag   // 输出：数据有效标志信号（高电平有效）
);

    // 定义参数和内部信号
    localparam BAUD_CNT_MAX = CLK_FREQ / UART_BPS;  // 计算波特率计数器最大值

    // 定义状态机的状态（独热码）
    localparam IDLE = 3'b000;  // 空闲状态：等待起始位
    localparam START = 3'b001;  // 起始位检测状态：检测起始位下降沿
    localparam RECEIVE = 3'b010;  // 数据接收状态：接收8位数据
    localparam STOP = 3'b011;  // 停止位检测状态：检测停止位

    // 定义寄存器
    reg [ 2:0] state;  // 状态寄存器：当前状态
    reg [ 2:0] next_state;  // 状态寄存器：下一状态
    reg [12:0] baud_cnt;  // 波特率计数器：用于生成正确的波特率
    reg [ 3:0] bit_cnt;  // 位计数器：用于计数已接收的数据位
    reg [ 7:0] rx_data;  // 数据寄存器：暂存接收的数据
    reg rx_reg1, rx_reg2;  // 同步寄存器：用于消除亚稳态

    // 数据同步，消除亚稳态
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rx_reg1 <= 1'b1;  // 复位时置高电平
            rx_reg2 <= 1'b1;  // 复位时置高电平
        end else begin
            rx_reg1 <= rx;  // 第一级同步：采样输入数据
            rx_reg2 <= rx_reg1;  // 第二级同步：进一步稳定数据
        end
    end

    // 波特率计数器逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) baud_cnt <= 13'b0;  // 复位时清零
        else if (state == IDLE || baud_cnt == BAUD_CNT_MAX - 1)
            baud_cnt <= 13'b0;  // 空闲状态或计数到最大值时清零
        else baud_cnt <= baud_cnt + 1'b1;  // 正常计数
    end

    // 状态机：状态转移逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= IDLE;  // 复位时进入空闲状态
        else state <= next_state;  // 正常工作时状态转移
    end

    // 状态机：下一状态逻辑
    always @(*) begin
        case (state)
            IDLE: begin
                if (!rx_reg2)  // 检测到起始位的下降沿
                    next_state = START;  // 进入起始位检测状态
                else next_state = IDLE;  // 保持空闲状态
            end
            START: begin
                if (baud_cnt == BAUD_CNT_MAX / 2 - 1)  // 到达起始位采样中点
                    next_state = RECEIVE;  // 进入数据接收状态
                else next_state = START;  // 保持起始位检测状态
            end
            RECEIVE: begin
                if (bit_cnt == 4'd8 && baud_cnt == BAUD_CNT_MAX - 1)  // 8位数据接收完成
                    next_state = STOP;  // 进入停止位检测状态
                else next_state = RECEIVE;  // 保持数据接收状态
            end
            STOP: begin
                if (baud_cnt == BAUD_CNT_MAX - 1)  // 停止位采样完成
                    next_state = IDLE;  // 进入空闲状态
                else next_state = STOP;  // 保持停止位检测状态
            end
            default: next_state = IDLE;  // 默认进入空闲状态
        endcase
    end

    // 位计数器逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) bit_cnt <= 4'b0;  // 复位时清零
        else if (state == RECEIVE && baud_cnt == BAUD_CNT_MAX - 1)
            bit_cnt <= bit_cnt + 1'b1;  // 数据位接收完成时加1
        else if (state != RECEIVE) bit_cnt <= 4'b0;  // 非数据接收状态时清零
    end

    // 数据接收逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) rx_data <= 8'b0;  // 复位时清零
        else if (state == RECEIVE && baud_cnt == BAUD_CNT_MAX / 2 - 1)  // 在数据位中点采样
            rx_data <= {rx_reg2, rx_data[7:1]};  // 右移并保存接收到的位
    end

    // 数据输出逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            po_data <= 8'b0;  // 复位时输出数据清零
            po_flag <= 1'b0;  // 复位时标志信号清零
        end else if (state == STOP && baud_cnt == BAUD_CNT_MAX - 1) begin
            po_data <= rx_data;  // 停止位接收完成时输出数据
            po_flag <= 1'b1;  // 停止位接收完成时标志信号置高
        end else po_flag <= 1'b0;  // 其他状态标志信号清零
    end

endmodule
