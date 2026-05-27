# CT137X full board-level constraint template
# Target FPGA: XC7S6-1FTGB196
#
# Usage:
# 1. Use the board signal names below as your top-level ports, or rename the
#    get_ports targets to match your design.
# 2. Each constraint is guarded with get_ports -quiet, so unused peripherals do
#    not need to be commented out.
# 3. All user-facing I/O banks on this board are powered at 3.3V.

proc ct137x_get_port {args} {
    foreach port_name $args {
        set port_obj [get_ports -quiet $port_name]
        if {[llength $port_obj]} {
            return $port_obj
        }
    }
    return {}
}

proc ct137x_bind_lvcmos33 {pin args} {
    set port_obj [ct137x_get_port {*}$args]
    if {[llength $port_obj]} {
        set_property PACKAGE_PIN $pin $port_obj
        set_property IOSTANDARD LVCMOS33 $port_obj
    }
    return $port_obj
}

# Bitstream / configuration settings
set_property CFGBVS VCCO                     [current_design]
set_property CONFIG_VOLTAGE 3.3              [current_design]
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property CONFIG_MODE SPIx4               [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 50  [current_design]

# 50 MHz system clock
set ct137x_clk_port [ct137x_bind_lvcmos33 G11 GCLK sys_clk clk]
if {[llength $ct137x_clk_port]} {
    create_clock -name CT137X_SYS_CLK -period 20.000 $ct137x_clk_port
}

# Reset and user keys
# RESET is active-high. S1-S4 are active-low.
# Do not bind the board reset button directly to an active-low logical reset port
# such as rst_n unless you invert it in RTL.
ct137x_bind_lvcmos33 B6 RESET sys_rst reset rst
ct137x_bind_lvcmos33 M5 S1 {key[0]} {key_in[0]}
ct137x_bind_lvcmos33 M4 S2 {key[1]} {key_in[1]}
ct137x_bind_lvcmos33 P5 S3 {key[2]} {key_in[2]}
ct137x_bind_lvcmos33 N4 S4 {key[3]} {key_in[3]}

# User LEDs
# The LED bank is wired to 3.3V through resistors, so drive low to light.
ct137x_bind_lvcmos33 N14 LD1 {led[0]} {led_out[0]}
ct137x_bind_lvcmos33 M14 LD2 {led[1]} {led_out[1]}
ct137x_bind_lvcmos33 P12 LD3 {led[2]} {led_out[2]}
ct137x_bind_lvcmos33 P13 LD4 {led[3]} {led_out[3]}
ct137x_bind_lvcmos33 N10 LD5 {led[4]} {led_out[4]}
ct137x_bind_lvcmos33 N11 LD6 {led[5]} {led_out[5]}
ct137x_bind_lvcmos33 P10 LD7 {led[6]} {led_out[6]}
ct137x_bind_lvcmos33 P11 LD8 {led[7]} {led_out[7]}

# Shared I2C bus: ADC081C021 + DAC5571 + AT24C02
ct137x_bind_lvcmos33 E11 I2C_SCL scl i2c_scl
ct137x_bind_lvcmos33 M10 I2C_SDA sda i2c_sda

# User SPI flash (U10)
ct137x_bind_lvcmos33 D12 SPI_CS spi_cs flash_cs_n
ct137x_bind_lvcmos33 D13 SPI_SCK spi_sck flash_sck
ct137x_bind_lvcmos33 G14 SPI_IO0_MOSI spi_io0 flash_io0
ct137x_bind_lvcmos33 F14 SPI_IO1_MISO spi_io1 flash_io1
ct137x_bind_lvcmos33 F13 SPI_IO2 spi_io2 flash_io2
ct137x_bind_lvcmos33 E13 SPI_IO3 spi_io3 flash_io3

# Seven-segment display
# SEG_TABLE.pdf uses common-anode segment codes.
ct137x_bind_lvcmos33 D3 SEGA {segment_control[0]} {seg_data[0]} {dula[0]}
ct137x_bind_lvcmos33 C3 SEGB {segment_control[1]} {seg_data[1]} {dula[1]}
ct137x_bind_lvcmos33 A4 SEGC {segment_control[2]} {seg_data[2]} {dula[2]}
ct137x_bind_lvcmos33 A3 SEGD {segment_control[3]} {seg_data[3]} {dula[3]}
ct137x_bind_lvcmos33 B3 SEGE {segment_control[4]} {seg_data[4]} {dula[4]}
ct137x_bind_lvcmos33 A2 SEGF {segment_control[5]} {seg_data[5]} {dula[5]}
ct137x_bind_lvcmos33 B5 SEGG {segment_control[6]} {seg_data[6]} {dula[6]}
ct137x_bind_lvcmos33 A5 SEGDP {segment_control[7]} {seg_data[7]} {dula[7]}
ct137x_bind_lvcmos33 B2 COM1 {digit_select[0]} {seg_sel[0]} {wela[0]}
ct137x_bind_lvcmos33 B1 COM2 {digit_select[1]} {seg_sel[1]} {wela[1]}
ct137x_bind_lvcmos33 C5 COM3 {digit_select[2]} {seg_sel[2]} {wela[2]}
ct137x_bind_lvcmos33 C4 COM4 {digit_select[3]} {seg_sel[3]} {wela[3]}
ct137x_bind_lvcmos33 E4 COM5 {digit_select[4]} {seg_sel[4]} {wela[4]}
ct137x_bind_lvcmos33 D4 COM6 {digit_select[5]} {seg_sel[5]} {wela[5]}
ct137x_bind_lvcmos33 F3 COM7 {digit_select[6]} {seg_sel[6]} {wela[6]}
ct137x_bind_lvcmos33 F2 COM8 {digit_select[7]} {seg_sel[7]} {wela[7]}

# UART via CH340C
ct137x_bind_lvcmos33 F12 UART_TX USB_UART_TX uart_tx tx
ct137x_bind_lvcmos33 E12 UART_RX USB_UART_RX uart_rx rx

# Buzzer
ct137x_bind_lvcmos33 L5 BUZ buz buz_out

# External SRAM: IS63WV1288, 128K x 8
ct137x_bind_lvcmos33 J3 SRAM_D0 {sram_data[0]}
ct137x_bind_lvcmos33 M1 SRAM_D1 {sram_data[1]}
ct137x_bind_lvcmos33 L1 SRAM_D2 {sram_data[2]}
ct137x_bind_lvcmos33 M3 SRAM_D3 {sram_data[3]}
ct137x_bind_lvcmos33 M2 SRAM_D4 {sram_data[4]}
ct137x_bind_lvcmos33 P2 SRAM_D5 {sram_data[5]}
ct137x_bind_lvcmos33 N1 SRAM_D6 {sram_data[6]}
ct137x_bind_lvcmos33 P4 SRAM_D7 {sram_data[7]}

ct137x_bind_lvcmos33 G1 SRAM_A0 {sram_addr[0]}
ct137x_bind_lvcmos33 F1 SRAM_A1 {sram_addr[1]}
ct137x_bind_lvcmos33 E2 SRAM_A2 {sram_addr[2]}
ct137x_bind_lvcmos33 D2 SRAM_A3 {sram_addr[3]}
ct137x_bind_lvcmos33 D1 SRAM_A4 {sram_addr[4]}
ct137x_bind_lvcmos33 C1 SRAM_A5 {sram_addr[5]}
ct137x_bind_lvcmos33 G4 SRAM_A6 {sram_addr[6]}
ct137x_bind_lvcmos33 F4 SRAM_A7 {sram_addr[7]}
ct137x_bind_lvcmos33 H4 SRAM_A8 {sram_addr[8]}
ct137x_bind_lvcmos33 H3 SRAM_A9 {sram_addr[9]}
ct137x_bind_lvcmos33 H2 SRAM_A10 {sram_addr[10]}
ct137x_bind_lvcmos33 H1 SRAM_A11 {sram_addr[11]}
ct137x_bind_lvcmos33 J2 SRAM_A12 {sram_addr[12]}
ct137x_bind_lvcmos33 J1 SRAM_A13 {sram_addr[13]}
ct137x_bind_lvcmos33 K4 SRAM_A14 {sram_addr[14]}
ct137x_bind_lvcmos33 K3 SRAM_A15 {sram_addr[15]}
ct137x_bind_lvcmos33 J4 SRAM_A16 {sram_addr[16]}

ct137x_bind_lvcmos33 L3 SRAM_OE sram_oe_n sram_oe
ct137x_bind_lvcmos33 P3 SRAM_WE sram_we_n sram_we
ct137x_bind_lvcmos33 L2 SRAM_CE sram_ce_n sram_ce

# RTC: DS1302
ct137x_bind_lvcmos33 A10 RTC_SCLK rtc_sclk ds1302_sclk
ct137x_bind_lvcmos33 A12 RTC_RST rtc_ce rtc_rst ds1302_ce
ct137x_bind_lvcmos33 A13 RTC_DATA rtc_data ds1302_data

# J5 expansion header
# PIN3..PIN18 map to EXT_IO0..EXT_IO15 in order.
ct137x_bind_lvcmos33 H11 EXT_IO0 {ext_io[0]}
ct137x_bind_lvcmos33 H12 EXT_IO1 {ext_io[1]}
ct137x_bind_lvcmos33 H13 EXT_IO2 {ext_io[2]}
ct137x_bind_lvcmos33 H14 EXT_IO3 {ext_io[3]}
ct137x_bind_lvcmos33 M13 EXT_IO4 {ext_io[4]}
ct137x_bind_lvcmos33 L14 EXT_IO5 {ext_io[5]}
ct137x_bind_lvcmos33 L12 EXT_IO6 {ext_io[6]}
ct137x_bind_lvcmos33 L13 EXT_IO7 {ext_io[7]}
ct137x_bind_lvcmos33 J11 EXT_IO8 {ext_io[8]}
ct137x_bind_lvcmos33 J12 EXT_IO9 {ext_io[9]}
ct137x_bind_lvcmos33 J13 EXT_IO10 {ext_io[10]}
ct137x_bind_lvcmos33 J14 EXT_IO11 {ext_io[11]}
ct137x_bind_lvcmos33 K11 EXT_IO12 {ext_io[12]}
ct137x_bind_lvcmos33 K12 EXT_IO13 {ext_io[13]}
ct137x_bind_lvcmos33 M11 EXT_IO14 {ext_io[14]}
ct137x_bind_lvcmos33 M12 EXT_IO15 {ext_io[15]}

# J1 expansion header
# The provided docs list pin positions but no canonical net names.
# Suggested top-level names are J1_PIN1..J1_PIN6.
ct137x_bind_lvcmos33 B13 J1_PIN1
ct137x_bind_lvcmos33 B14 J1_PIN2
ct137x_bind_lvcmos33 D14 J1_PIN3
ct137x_bind_lvcmos33 C14 J1_PIN4
ct137x_bind_lvcmos33 C12 J1_PIN5
ct137x_bind_lvcmos33 F11 J1_PIN6
