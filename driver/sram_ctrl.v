module sram_ctrl #(
    parameter READ_WAIT_CYCLES  = 2,
    parameter WRITE_PULSE_CYCLES = 2
) (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        read_req,
    input  wire        write_req,
    input  wire [16:0] addr,
    input  wire [ 7:0] write_data,
    output reg  [ 7:0] read_data,
    output wire        ready,
    output reg         done,
    output wire [16:0] sram_addr,
    inout  wire [ 7:0] sram_data,
    output wire        sram_ce_n,
    output wire        sram_oe_n,
    output wire        sram_we_n
);

    localparam [1:0] S_IDLE  = 2'd0;
    localparam [1:0] S_READ  = 2'd1;
    localparam [1:0] S_WRITE = 2'd2;
    localparam [1:0] S_DONE  = 2'd3;

    reg [1:0]  state;
    reg [16:0] addr_reg;
    reg [ 7:0] write_data_reg;
    reg [ 7:0] wait_cnt;

    wire [7:0] sram_data_in;
    reg  [7:0] sram_data_out;
    reg        sram_data_oe;

    assign ready       = (state == S_IDLE);
    assign sram_addr   = addr_reg;
    assign sram_data   = sram_data_oe ? sram_data_out : 8'bz;
    assign sram_data_in = sram_data;

    assign sram_ce_n = (state == S_READ || state == S_WRITE) ? 1'b0 : 1'b1;
    assign sram_oe_n = (state == S_READ)  ? 1'b0 : 1'b1;
    assign sram_we_n = (state == S_WRITE) ? 1'b0 : 1'b1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state          <= S_IDLE;
            addr_reg       <= 17'd0;
            write_data_reg <= 8'd0;
            read_data      <= 8'd0;
            wait_cnt       <= 8'd0;
            done           <= 1'b0;
            sram_data_out  <= 8'd0;
            sram_data_oe   <= 1'b0;
        end else begin
            done <= 1'b0;

            case (state)
                S_IDLE: begin
                    wait_cnt     <= 8'd0;
                    sram_data_oe <= 1'b0;

                    if (write_req) begin
                        addr_reg       <= addr;
                        write_data_reg <= write_data;
                        sram_data_out  <= write_data;
                        sram_data_oe   <= 1'b1;
                        state          <= S_WRITE;
                    end else if (read_req) begin
                        addr_reg       <= addr;
                        sram_data_oe   <= 1'b0;
                        state          <= S_READ;
                    end
                end

                S_READ: begin
                    if (wait_cnt == READ_WAIT_CYCLES - 1) begin
                        read_data <= sram_data_in;
                        wait_cnt  <= 8'd0;
                        state     <= S_DONE;
                    end else begin
                        wait_cnt <= wait_cnt + 1'b1;
                    end
                end

                S_WRITE: begin
                    sram_data_oe  <= 1'b1;
                    sram_data_out <= write_data_reg;

                    if (wait_cnt == WRITE_PULSE_CYCLES - 1) begin
                        wait_cnt <= 8'd0;
                        state    <= S_DONE;
                    end else begin
                        wait_cnt <= wait_cnt + 1'b1;
                    end
                end

                S_DONE: begin
                    sram_data_oe <= 1'b0;
                    done         <= 1'b1;
                    state        <= S_IDLE;
                end

                default: begin
                    state <= S_IDLE;
                end
            endcase
        end
    end

endmodule
