module top (
    input  wire       sys_clk,
    input  wire       sys_rst_n,
    input  wire [3:0] key,
    output wire [7:0] led,
    output wire       buz,
    output wire [7:0] seg_sel,
    output wire [7:0] seg_data
);

    localparam BUZ_ACTIVE_LOW = 1'b1;

    // 50MHz -> 100Hz，给按键消抖
    wire clk_100;
    frequency_divider u_div_100 (
        .clk     (sys_clk),
        .rst_n   (sys_rst_n),
        .clkbase (32'd50_000_000),
        .clkdiv  (32'd100),
        .clkout  (clk_100)
    );

    // 按键消抖后，up 是按下脉冲
    wire [3:0] key_press;
    key_ctrl u_key (
        .clk_100 (clk_100),
        .rst_n   (sys_rst_n),
        .key_in  (key),
        .down    (),
        .up      (key_press)
    );

    // 基础练习状态
    // S1：加1
    // S2：减1
    // S3：切换 LED 模式
    // S4：切换蜂鸣器模式 0/1/2/3
    reg [3:0] ones;
    reg [3:0] tens;
    reg [3:0] hundreds;
    reg [3:0] thousands;
    reg [1:0] led_mode;
    reg [1:0] buz_mode;

    always @(posedge clk_100 or negedge sys_rst_n) begin
        if (!sys_rst_n) begin
            ones      <= 4'd0;
            tens      <= 4'd0;
            hundreds  <= 4'd0;
            thousands <= 4'd0;
            led_mode  <= 2'd0;
            buz_mode  <= 2'd0;
        end else begin
            if (key_press[0]) begin
                if (ones < 4'd9)
                    ones <= ones + 1'd1;
                else begin
                    ones <= 4'd0;
                    if (tens < 4'd9)
                        tens <= tens + 1'd1;
                    else begin
                        tens <= 4'd0;
                        if (hundreds < 4'd9)
                            hundreds <= hundreds + 1'd1;
                        else begin
                            hundreds <= 4'd0;
                            if (thousands < 4'd9)
                                thousands <= thousands + 1'd1;
                            else
                                thousands <= 4'd0;
                        end
                    end
                end
            end else if (key_press[1]) begin
                if (ones > 4'd0)
                    ones <= ones - 1'd1;
                else begin
                    ones <= 4'd9;
                    if (tens > 4'd0)
                        tens <= tens - 1'd1;
                    else begin
                        tens <= 4'd9;
                        if (hundreds > 4'd0)
                            hundreds <= hundreds - 1'd1;
                        else begin
                            hundreds <= 4'd9;
                            if (thousands > 4'd0)
                                thousands <= thousands - 1'd1;
                            else
                                thousands <= 4'd9;
                        end
                    end
                end
            end

            if (key_press[2])
                led_mode <= led_mode + 1'b1;

            if (key_press[3])
                buz_mode <= buz_mode + 1'b1;
        end
    end

    // LED 练习：S3 切换模式
    led_proc u_led_proc (
        .clk  (sys_clk),
        .rst_n(sys_rst_n),
        .mode (led_mode),
        .led  (led)
    );

    // 蜂鸣器练习：S4 切换模式
    // mode=0 静音，1/2/3 对应三种音调
    wire buz_clk_500;
    wire buz_clk_1k;
    wire buz_clk_2k;
    reg  buz_raw;

    frequency_divider u_div_buz_500 (
        .clk     (sys_clk),
        .rst_n   (sys_rst_n),
        .clkbase (32'd50_000_000),
        .clkdiv  (32'd500),
        .clkout  (buz_clk_500)
    );

    frequency_divider u_div_buz_1k (
        .clk     (sys_clk),
        .rst_n   (sys_rst_n),
        .clkbase (32'd50_000_000),
        .clkdiv  (32'd1000),
        .clkout  (buz_clk_1k)
    );

    frequency_divider u_div_buz_2k (
        .clk     (sys_clk),
        .rst_n   (sys_rst_n),
        .clkbase (32'd50_000_000),
        .clkdiv  (32'd2000),
        .clkout  (buz_clk_2k)
    );

    always @(*) begin
        case (buz_mode)
            2'd0: buz_raw = 1'b0;
            2'd1: buz_raw = buz_clk_500;
            2'd2: buz_raw = buz_clk_1k;
            default: buz_raw = buz_clk_2k;
        endcase
    end

    assign buz = BUZ_ACTIVE_LOW ? ~buz_raw : buz_raw;

    // 数码管练习显示：
    // COM1-COM4 显示计数值
    // COM5 显示 LED 模式
    // COM6 显示蜂鸣器模式
    // COM7-COM8 熄灭
    seg_proc u_seg_proc (
        .clk          (sys_clk),
        .rst_n        (sys_rst_n),
        .seg_number_in({ones, tens, hundreds, thousands, led_mode + 4'd0, buz_mode + 4'd0, 4'd10, 4'd10}),
        .dp           (8'b0000_0000),
        .dula         (seg_data),
        .wela         (seg_sel)
    );

endmodule
