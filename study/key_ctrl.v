module key_ctrl (
    input wire clk,
    input wire rst_n,
    input wire [3:0] key_in,
    output reg [3:0] up,
    output reg [3:0] down
);


//