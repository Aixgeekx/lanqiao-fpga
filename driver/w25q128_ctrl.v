module w25q128_ctrl #(
    parameter P_SYS_CLK = 50_000_000,
    parameter P_SPI_CLK = 2_000_000
) (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        start,
    input  wire [ 2:0] op_code,
    input  wire [23:0] flash_addr,
    input  wire [ 7:0] write_data,
    output reg  [23:0] jedec_id,
    output reg  [ 7:0] read_data,
    output reg  [ 7:0] status_reg,
    output wire        ready,
    output wire        busy,
    output reg         done,
    output wire        flash_cs_n,
    output wire        flash_sck,
    inout  wire        flash_io0,
    inout  wire        flash_io1,
    inout  wire        flash_io2,
    inout  wire        flash_io3
);

    localparam [2:0] OP_READ_JEDEC_ID = 3'd0;
    localparam [2:0] OP_READ_STATUS   = 3'd1;
    localparam [2:0] OP_READ_BYTE     = 3'd2;
    localparam [2:0] OP_WRITE_BYTE    = 3'd3;
    localparam [2:0] OP_SECTOR_ERASE  = 3'd4;

    localparam [2:0] S_IDLE        = 3'd0;
    localparam [2:0] S_LAUNCH_WREN = 3'd1;
    localparam [2:0] S_WAIT_WREN   = 3'd2;
    localparam [2:0] S_LAUNCH_MAIN = 3'd3;
    localparam [2:0] S_WAIT_MAIN   = 3'd4;
    localparam [2:0] S_LAUNCH_POLL = 3'd5;
    localparam [2:0] S_WAIT_POLL   = 3'd6;
    localparam [2:0] S_DONE        = 3'd7;

    localparam [1:0] SPI_IDLE      = 2'd0;
    localparam [1:0] SPI_TRANSFER  = 2'd1;
    localparam [1:0] SPI_FINISH    = 2'd2;

    localparam integer SPI_DIV = ((P_SYS_CLK / (P_SPI_CLK * 2)) < 1) ? 1 : (P_SYS_CLK / (P_SPI_CLK * 2));

    reg [2:0] state;
    reg [2:0] op_code_reg;
    reg [23:0] flash_addr_reg;
    reg [7:0] write_data_reg;

    reg        spi_start;
    reg [39:0] spi_tx_word;
    reg [ 5:0] spi_total_bits;
    reg [ 5:0] spi_capture_bits;

    reg [ 1:0] spi_state;
    reg [39:0] spi_shift_reg;
    reg [31:0] spi_rx_shift;
    reg [31:0] spi_rx_data;
    reg        spi_done;
    reg [ 5:0] spi_bit_index;
    reg [ 5:0] spi_rx_start;
    reg [ 5:0] spi_total_bits_reg;
    reg [15:0] spi_div_cnt;
    reg        flash_cs_n_reg;
    reg        flash_sck_reg;
    reg        flash_io0_out;

    wire flash_miso;

    assign ready = (state == S_IDLE);
    assign busy  = (state != S_IDLE);

    assign flash_cs_n = flash_cs_n_reg;
    assign flash_sck  = flash_sck_reg;

    assign flash_io0 = flash_io0_out;
    assign flash_io1 = 1'bz;
    assign flash_io2 = 1'bz;
    assign flash_io3 = 1'bz;
    assign flash_miso = flash_io1;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state          <= S_IDLE;
            op_code_reg    <= OP_READ_JEDEC_ID;
            flash_addr_reg <= 24'd0;
            write_data_reg <= 8'd0;
            jedec_id       <= 24'd0;
            read_data      <= 8'd0;
            status_reg     <= 8'd0;
            done           <= 1'b0;
            spi_start      <= 1'b0;
            spi_tx_word    <= 40'd0;
            spi_total_bits <= 6'd0;
            spi_capture_bits <= 6'd0;
        end else begin
            done      <= 1'b0;
            spi_start <= 1'b0;

            case (state)
                S_IDLE: begin
                    if (start) begin
                        op_code_reg    <= op_code;
                        flash_addr_reg <= flash_addr;
                        write_data_reg <= write_data;

                        if (op_code == OP_WRITE_BYTE || op_code == OP_SECTOR_ERASE)
                            state <= S_LAUNCH_WREN;
                        else
                            state <= S_LAUNCH_MAIN;
                    end
                end

                S_LAUNCH_WREN: begin
                    spi_tx_word      <= {8'h06, 32'h0000_0000};
                    spi_total_bits   <= 6'd8;
                    spi_capture_bits <= 6'd0;
                    spi_start        <= 1'b1;
                    state            <= S_WAIT_WREN;
                end

                S_WAIT_WREN: begin
                    if (spi_done)
                        state <= S_LAUNCH_MAIN;
                end

                S_LAUNCH_MAIN: begin
                    case (op_code_reg)
                        OP_READ_JEDEC_ID: begin
                            spi_tx_word      <= {8'h9F, 24'h00_0000, 8'h00};
                            spi_total_bits   <= 6'd32;
                            spi_capture_bits <= 6'd24;
                        end

                        OP_READ_STATUS: begin
                            spi_tx_word      <= {8'h05, 8'h00, 24'h00_0000};
                            spi_total_bits   <= 6'd16;
                            spi_capture_bits <= 6'd8;
                        end

                        OP_READ_BYTE: begin
                            spi_tx_word      <= {8'h03, flash_addr_reg, 8'h00};
                            spi_total_bits   <= 6'd40;
                            spi_capture_bits <= 6'd8;
                        end

                        OP_WRITE_BYTE: begin
                            spi_tx_word      <= {8'h02, flash_addr_reg, write_data_reg};
                            spi_total_bits   <= 6'd40;
                            spi_capture_bits <= 6'd0;
                        end

                        OP_SECTOR_ERASE: begin
                            spi_tx_word      <= {8'h20, flash_addr_reg, 8'h00};
                            spi_total_bits   <= 6'd32;
                            spi_capture_bits <= 6'd0;
                        end

                        default: begin
                            spi_tx_word      <= {8'h05, 8'h00, 24'h00_0000};
                            spi_total_bits   <= 6'd16;
                            spi_capture_bits <= 6'd8;
                        end
                    endcase

                    spi_start <= 1'b1;
                    state     <= S_WAIT_MAIN;
                end

                S_WAIT_MAIN: begin
                    if (spi_done) begin
                        case (op_code_reg)
                            OP_READ_JEDEC_ID: begin
                                jedec_id <= spi_rx_data[23:0];
                                state    <= S_DONE;
                            end

                            OP_READ_STATUS: begin
                                status_reg <= spi_rx_data[7:0];
                                state      <= S_DONE;
                            end

                            OP_READ_BYTE: begin
                                read_data <= spi_rx_data[7:0];
                                state     <= S_DONE;
                            end

                            OP_WRITE_BYTE,
                            OP_SECTOR_ERASE: begin
                                state <= S_LAUNCH_POLL;
                            end

                            default: begin
                                state <= S_DONE;
                            end
                        endcase
                    end
                end

                S_LAUNCH_POLL: begin
                    spi_tx_word      <= {8'h05, 8'h00, 24'h00_0000};
                    spi_total_bits   <= 6'd16;
                    spi_capture_bits <= 6'd8;
                    spi_start        <= 1'b1;
                    state            <= S_WAIT_POLL;
                end

                S_WAIT_POLL: begin
                    if (spi_done) begin
                        status_reg <= spi_rx_data[7:0];

                        if (spi_rx_data[0])
                            state <= S_LAUNCH_POLL;
                        else
                            state <= S_DONE;
                    end
                end

                S_DONE: begin
                    done  <= 1'b1;
                    state <= S_IDLE;
                end

                default: begin
                    state <= S_IDLE;
                end
            endcase
        end
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            spi_state          <= SPI_IDLE;
            spi_shift_reg      <= 40'd0;
            spi_rx_shift       <= 32'd0;
            spi_rx_data        <= 32'd0;
            spi_done           <= 1'b0;
            spi_bit_index      <= 6'd0;
            spi_rx_start       <= 6'd0;
            spi_total_bits_reg <= 6'd0;
            spi_div_cnt        <= 16'd0;
            flash_cs_n_reg     <= 1'b1;
            flash_sck_reg      <= 1'b0;
            flash_io0_out      <= 1'b0;
        end else begin
            spi_done <= 1'b0;

            case (spi_state)
                SPI_IDLE: begin
                    flash_cs_n_reg <= 1'b1;
                    flash_sck_reg  <= 1'b0;
                    spi_div_cnt    <= 16'd0;
                    spi_bit_index  <= 6'd0;

                    if (spi_start) begin
                        flash_cs_n_reg     <= 1'b0;
                        flash_sck_reg      <= 1'b0;
                        spi_shift_reg      <= spi_tx_word;
                        spi_rx_shift       <= 32'd0;
                        spi_rx_start       <= spi_total_bits - spi_capture_bits;
                        spi_total_bits_reg <= spi_total_bits;
                        flash_io0_out      <= spi_tx_word[39];
                        spi_state          <= SPI_TRANSFER;
                    end
                end

                SPI_TRANSFER: begin
                    if (spi_div_cnt == SPI_DIV - 1) begin
                        spi_div_cnt <= 16'd0;

                        if (!flash_sck_reg) begin
                            flash_sck_reg <= 1'b1;

                            if (spi_bit_index >= spi_rx_start && spi_capture_bits != 0)
                                spi_rx_shift <= {spi_rx_shift[30:0], flash_miso};
                        end else begin
                            flash_sck_reg <= 1'b0;

                            if (spi_bit_index == spi_total_bits_reg - 1) begin
                                spi_rx_data <= spi_rx_shift;
                                spi_state   <= SPI_FINISH;
                            end else begin
                                spi_bit_index <= spi_bit_index + 1'b1;
                                spi_shift_reg <= {spi_shift_reg[38:0], 1'b0};
                                flash_io0_out <= spi_shift_reg[38];
                            end
                        end
                    end else begin
                        spi_div_cnt <= spi_div_cnt + 1'b1;
                    end
                end

                SPI_FINISH: begin
                    flash_cs_n_reg <= 1'b1;
                    flash_sck_reg  <= 1'b0;
                    spi_done       <= 1'b1;
                    spi_state      <= SPI_IDLE;
                end

                default: begin
                    spi_state <= SPI_IDLE;
                end
            endcase
        end
    end

endmodule
