module ds1302_test (
    input wire rst,  // 复位信号，高电平有效
    input wire clk,  // 时钟信号，用于同步逻辑操作

    output wire ds1302_ce,    // DS1302 芯片使能信号
    output wire ds1302_sclk,  // DS1302 串行时钟信号
    inout  wire ds1302_io,    // DS1302 数据线（双向）

    input wire [7:0] write_second,  // 写入的秒值
    input wire [7:0] write_minute,  // 写入的分值
    input wire [7:0] write_hour,    // 写入的小时值
    input wire [7:0] write_date,    // 写入的日期值
    input wire [7:0] write_month,   // 写入的月份值
    input wire [7:0] write_week,    // 写入的星期值
    input wire [7:0] write_year,    // 写入的年份值

    input  wire       write_time_req,  // 写入时间请求信号
    output wire [7:0] read_second,     // 读取到的秒值
    output wire [7:0] read_minute,     // 读取到的分值
    output wire [7:0] read_hour,       // 读取到的小时值
    output wire [7:0] read_date,       // 读取到的日期值
    output wire [7:0] read_month,      // 读取到的月份值
    output wire [7:0] read_week,       // 读取到的星期值
    output wire [7:0] read_year        // 读取到的年份值
);

    // 状态机变量定义
    reg [2:0] state, next_state;  // 当前状态和下一状态
    reg        write_time_flag;  // 写时间触发信号
    reg        clear_ch_flag;  // 清除 CH 位的触发信号
    reg  [7:0] write_second_reg;  // 写入秒值寄存器
    reg  [7:0] write_minute_reg;  // 写入分钟值寄存器
    reg  [7:0] write_hour_reg;  // 写入小时值寄存器
    reg  [7:0] write_date_reg;  // 写入日期值寄存器
    reg  [7:0] write_month_reg;  // 写入月份值寄存器
    reg  [7:0] write_week_reg;  // 写入星期值寄存器
    reg  [7:0] write_year_reg;  // 写入年份值寄存器
    wire       write_time_ack;  // 写时间完成信号
    wire       read_time_ack;  // 读时间完成信号
    wire       CH;  // 秒值的最高位，用于判断是否暂停

    // 状态定义
    localparam S_IDLE = 0;  // 空闲状态
    localparam S_READ_CH = 1;  // 读取 CH 状态
    localparam S_CLEAR_CH = 2;  // 清除 CH 状态
    localparam S_WRITE = 3;  // 写时间状态
    localparam S_WAIT = 4;  // 等待状态
    localparam S_READ_TIME = 5;  // 读取时间状态

    // CH 位的分配
    assign CH = read_second[7];

    // 写时间触发逻辑
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            write_time_flag <= 1'b0;  // 复位时清除写时间标志
        end else if (write_time_req) begin
            write_time_flag <= 1'b1;  // 收到写时间请求时设置标志
        end else if (write_time_ack) begin
            write_time_flag <= 1'b0;  // 写完成后清除写时间标志
        end
    end

    // 清除 CH 触发逻辑
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            clear_ch_flag <= 1'b0;  // 复位时清除清除 CH 标志
        end else if (state == S_CLEAR_CH && write_time_ack) begin
            clear_ch_flag <= 1'b0;  // 清除 CH 完成后清零标志
        end else if (state == S_READ_CH && read_time_ack && CH) begin
            clear_ch_flag <= 1'b1;  // 如果 CH 位为 1，则触发清除
        end
    end

    // 写入时间寄存器赋值逻辑
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            write_second_reg <= 8'h00;  // 复位时清零
            write_minute_reg <= 8'h00;
            write_hour_reg   <= 8'h00;
            write_date_reg   <= 8'h00;
            write_month_reg  <= 8'h00;
            write_week_reg   <= 8'h00;
            write_year_reg   <= 8'h00;
        end else if (write_time_req) begin
            write_second_reg <= write_second;  // 写入预设的时间数据
            write_minute_reg <= write_minute;
            write_hour_reg   <= write_hour;
            write_date_reg   <= write_date;
            write_month_reg  <= write_month;
            write_week_reg   <= write_week;
            write_year_reg   <= write_year;
        end else if (clear_ch_flag) begin
            write_second_reg <= {1'b0, read_second[6:0]};  // 清除 CH 位
        end
    end

    // 状态机控制逻辑
    always @(posedge clk or posedge rst) begin
        if (rst) state <= S_IDLE;  // 复位时进入空闲状态
        else state <= next_state;  // 否则进入下一状态
    end

    // 状态机状态转移逻辑
    always @(*) begin
        case (state)
            S_IDLE: begin
                if (write_time_flag) next_state <= S_WRITE;  // 写时间触发时进入写状态
                else next_state <= S_READ_CH;  // 否则进入读 CH 状态
            end
            S_READ_CH: begin
                if (read_time_ack)
                    next_state <= (CH ? S_CLEAR_CH : S_READ_TIME);  // CH 为 1 进入清除 CH，否则直接读时间
                else next_state <= S_READ_CH;
            end
            S_CLEAR_CH: begin
                if (write_time_ack) next_state <= S_WAIT;  // 清除 CH 完成后进入等待状态
                else next_state <= S_CLEAR_CH;
            end
            S_WRITE: begin
                if (write_time_ack) next_state <= S_WAIT;  // 写完成后进入等待状态
                else next_state <= S_WRITE;
            end
            S_WAIT: begin
                next_state <= S_READ_TIME;  // 等待完成后进入读时间状态
            end
            S_READ_TIME: begin
                if (read_time_ack) next_state <= S_IDLE;  // 读完成后返回空闲状态
                else next_state <= S_READ_TIME;
            end
            default: next_state <= S_IDLE;  // 默认返回空闲状态
        endcase
    end

    // 实例化 DS1302 控制模块
    ds1302_wr_drive ds1302_ctrl_m0 (
        .ds1302_clk(clk),  // 时钟信号
        .ds1302_rst(rst),  // 复位信号
        .write_second(write_second_reg),  // 写入的秒值
        .write_minute(write_minute_reg),  // 写入的分钟值
        .write_hour(write_hour_reg),  // 写入的小时值
        .write_date(write_date_reg),  // 写入的日期值
        .write_month(write_month_reg),  // 写入的月份值
        .write_week(write_week_reg),  // 写入的星期值
        .write_year(write_year_reg),  // 写入的年份值
        .write_time_req(clear_ch_flag || write_time_flag),  // 写时间或清除 CH 触发信号
        .write_time_ack(write_time_ack),  // 写时间完成信号
        .read_second(read_second),  // 读取的秒值
        .read_minute(read_minute),  // 读取的分钟值
        .read_hour(read_hour),  // 读取的小时值
        .read_date(read_date),  // 读取的日期值
        .read_month(read_month),  // 读取的月份值
        .read_week(read_week),  // 读取的星期值
        .read_year(read_year),  // 读取的年份值
        .read_time_req(state == S_READ_CH || state == S_READ_TIME),  // 读时间请求信号
        .read_time_ack(read_time_ack),  // 读时间完成信号
        .ds1302_ce(ds1302_ce),  // DS1302 芯片使能信号
        .ds1302_sclk(ds1302_sclk),  // DS1302 串行时钟信号
        .ds1302_data(ds1302_io)  // DS1302 数据线
    );

endmodule
