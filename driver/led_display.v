module led_display (
    input  wire [7:0] led_pattern,
    output reg  [7:0] led
);
    always @(*) begin
        led = ~led_pattern;
    end
endmodule
