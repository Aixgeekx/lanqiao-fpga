module seg_driver (
    input  wire [3:0] digit,        // 输入的十进制数字（0-9）
    input  wire       rst_n,        // 复位信号（低电平有效）
    input  wire       current_dp,   // 小数点使能信号
    input  wire [2:0] position,     // 当前显示的位
    output reg  [7:0] digit_sel,    // 位选信号
    output reg  [7:0] segment_data  // 段选信号
);

    // 段码定义（每个数字对应的七段显示编码）
    localparam [7:0] SEG_0 = 8'b1100_0000;  //0
    localparam [7:0] SEG_1 = 8'b1111_1001;  //1
    localparam [7:0] SEG_2 = 8'b1010_0100;  //2
    localparam [7:0] SEG_3 = 8'b1011_0000;  //3
    localparam [7:0] SEG_4 = 8'b1001_1001;  //4
    localparam [7:0] SEG_5 = 8'b1001_0010;  //5
    localparam [7:0] SEG_6 = 8'b1000_0010;  //6
    localparam [7:0] SEG_7 = 8'b1111_1000;  //7
    localparam [7:0] SEG_8 = 8'b1000_0000;  //8
    localparam [7:0] SEG_9 = 8'b1001_0000;  //9
    localparam [7:0] SEG_C = 8'b1100_0110;  //C
    localparam [7:0] SEG_F = 8'b1000_1110;  //F
    localparam [7:0] SEG_DASH = 8'b1011_1111; // -
    localparam [7:0] SEG_NULL = 8'b1111_1111;  //灭

    // 根据输入的数字和小数点状态生成段码
    always @(*) begin
        if (!rst_n) begin
            segment_data = 8'b1111_1111;  // 复位时熄灭所有段码
            digit_sel = 8'b1111_1111;  // 复位时关闭所有位选
        end else begin
            // 根据输入的数字选择对应的段码
            case (digit)
                4'd0: segment_data = SEG_0;
                4'd1: segment_data = SEG_1;
                4'd2: segment_data = SEG_2;
                4'd3: segment_data = SEG_3;
                4'd4: segment_data = SEG_4;
                4'd5: segment_data = SEG_5;
                4'd6: segment_data = SEG_6;
                4'd7: segment_data = SEG_7;
                4'd8: segment_data = SEG_8;
                4'd9: segment_data = SEG_9;
                4'd10: segment_data = SEG_NULL;  // 灭
                4'd11: segment_data = SEG_DASH;  // -
                4'd12: segment_data = SEG_C;     // C
                4'd15: segment_data = SEG_F;     // F
                default: segment_data = SEG_NULL;  // 无效输入时熄灭所有段码
            endcase

            // 如果 decimal_en 为 1，则激活小数点（最高位为小数点位）
            if (current_dp) segment_data[7] = 1'b0;

            // 根据当前位位置 `position` 控制位选信号
            digit_sel = ~(8'b0000_0001 << position);  // 按位激活
        end
    end

endmodule
