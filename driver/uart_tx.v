/* UART发送模块
    一.模块功能：
    1.支持可配置的波特率
    2.支持8位数据位，1位起始位，1位停止位
    3.支持无校验位
    4.支持数据发送完成标志输出

    二.模块说明：
    1.使用状态机实现UART发送时序
    2.波特率通过参数配置，默认115200
    3.系统时钟频率通过参数配置，默认50MHz
*/

module uart_tx #(
    parameter UART_BPS = 115200,  // 串口波特率（默认115200）
    parameter CLK_FREQ = 50_000_000  // 系统时钟频率（默认50MHz）
) (
    input  wire       clk,      // 输入：系统时钟信号（50MHz）
    input  wire       rst_n,    // 输入：全局复位信号（低电平有效）
    input  wire [7:0] pi_data,  // 输入：8位并行数据
    input  wire       pi_flag,  // 输入：并行数据有效标志信号（高电平有效）
    output reg        tx,       // 输出：串行数据输出
    output reg        tx_done   // 输出：数据发送完成标志（高电平有效）
);

    // 定义参数和内部信号
    localparam BAUD_CNT_MAX = CLK_FREQ / UART_BPS;  // 计算波特率计数器最大值

    // 定义状态机的状态（独热码）
    localparam IDLE = 3'b000;  // 空闲状态：等待数据发送请求
    localparam START = 3'b001;  // 起始位状态：发送起始位（低电平）
    localparam DATA = 3'b010;  // 数据位状态：发送8位数据
    localparam STOP = 3'b011;  // 停止位状态：发送停止位（高电平）

    reg [2:0] state, next_state;  // 状态寄存器：当前状态和下一状态
    reg [12:0] baud_cnt;  // 波特率计数器：用于生成正确的波特率
    reg [ 3:0] bit_cnt;  // 数据位计数器：用于计数已发送的数据位

    // 状态机：状态转移逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) state <= IDLE;  // 复位时进入空闲状态
        else state <= next_state;  // 正常工作时状态转移
    end

    // 状态机：下一状态逻辑
    always @(*) begin
        case (state)
            IDLE:
            if (pi_flag) next_state = START;  // 收到数据有效标志，进入起始位状态
            else next_state = IDLE;  // 无数据发送请求，保持空闲状态
            START:
            if (baud_cnt == BAUD_CNT_MAX - 1)
                next_state = DATA;  // 起始位发送完成，进入数据位状态
            else next_state = START;  // 起始位未发送完成，保持起始位状态
            DATA:
            if ((bit_cnt == 4'd7) && (baud_cnt == BAUD_CNT_MAX - 1))
                next_state = STOP;  // 所有数据位发送完成，进入停止位状态
            else next_state = DATA;  // 数据位未发送完成，保持数据位状态
            STOP:
            if (baud_cnt == BAUD_CNT_MAX - 1)
                next_state = IDLE;  // 停止位发送完成，进入空闲状态
            else next_state = STOP;  // 停止位未发送完成，保持停止位状态
            default: next_state = IDLE;  // 默认状态为空闲状态
        endcase
    end

    // 波特率计数器逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) baud_cnt <= 13'b0;  // 复位时清零
        else if (state == IDLE || baud_cnt == BAUD_CNT_MAX - 1) 
            baud_cnt <= 13'b0;  // 空闲状态或计数到最大值时清零
        else baud_cnt <= baud_cnt + 1'b1;  // 正常计数
    end

    // 数据位计数器逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) bit_cnt <= 4'b0;  // 复位时清零
        else if (state == DATA && baud_cnt == BAUD_CNT_MAX - 1) 
            bit_cnt <= bit_cnt + 1'b1;  // 数据位状态且波特率计数到最大值时加1
        else if (state != DATA) bit_cnt <= 4'b0;  // 非数据位状态时清零
    end

    // 串行输出数据逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) tx <= 1'b1;  // 复位时输出高电平
        else begin
            case (state)
                IDLE: tx <= 1'b1;  // 空闲状态输出高电平
                START: tx <= 1'b0;  // 起始位输出低电平
                DATA: tx <= pi_data[bit_cnt];  // 数据位按位输出
                STOP: tx <= 1'b1;  // 停止位输出高电平
                default: tx <= 1'b1;  // 默认输出高电平
            endcase
        end
    end

    // 数据发送完成标志逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) tx_done <= 1'b0;  // 复位时清零
        else if (state == STOP && baud_cnt == BAUD_CNT_MAX - 1)
            tx_done <= 1'b1;  // 停止位发送完成，标志置高
        else if (state == IDLE) tx_done <= 1'b0;  // 空闲状态时清零
    end

endmodule
