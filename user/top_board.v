module top_board (
    input  wire       GCLK,
    input  wire       RESET,
    input  wire       S1,
    input  wire       S2,
    input  wire       S3,
    input  wire       S4,
    output wire       LD1,
    output wire       LD2,
    output wire       LD3,
    output wire       LD4,
    output wire       LD5,
    output wire       LD6,
    output wire       LD7,
    output wire       LD8,
    output wire       BUZ,
    output wire       COM1,
    output wire       COM2,
    output wire       COM3,
    output wire       COM4,
    output wire       COM5,
    output wire       COM6,
    output wire       COM7,
    output wire       COM8,
    output wire       SEGA,
    output wire       SEGB,
    output wire       SEGC,
    output wire       SEGD,
    output wire       SEGE,
    output wire       SEGF,
    output wire       SEGG,
    output wire       SEGDP
);

    wire       sys_rst_n;
    wire [3:0] key;
    wire [7:0] led;
    wire       buz;
    wire [7:0] seg_sel;
    wire [7:0] seg_data;

    // Board RESET is active-high, while the core uses active-low reset.
    assign sys_rst_n = ~RESET;
    assign key = {S4, S3, S2, S1};

    assign LD1 = led[0];
    assign LD2 = led[1];
    assign LD3 = led[2];
    assign LD4 = led[3];
    assign LD5 = led[4];
    assign LD6 = led[5];
    assign LD7 = led[6];
    assign LD8 = led[7];
    assign BUZ = buz;

    assign COM1 = seg_sel[0];
    assign COM2 = seg_sel[1];
    assign COM3 = seg_sel[2];
    assign COM4 = seg_sel[3];
    assign COM5 = seg_sel[4];
    assign COM6 = seg_sel[5];
    assign COM7 = seg_sel[6];
    assign COM8 = seg_sel[7];

    assign SEGA  = seg_data[0];
    assign SEGB  = seg_data[1];
    assign SEGC  = seg_data[2];
    assign SEGD  = seg_data[3];
    assign SEGE  = seg_data[4];
    assign SEGF  = seg_data[5];
    assign SEGG  = seg_data[6];
    assign SEGDP = seg_data[7];

    top u_top (
        .sys_clk (GCLK),
        .sys_rst_n(sys_rst_n),
        .key     (key),
        .led     (led),
        .buz     (buz),
        .seg_sel (seg_sel),
        .seg_data(seg_data)
    );

endmodule
