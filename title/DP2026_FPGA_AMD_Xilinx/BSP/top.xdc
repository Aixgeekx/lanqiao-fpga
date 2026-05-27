# --------------------------------------------------------------------
# File: top.xdc
# Board: CT137X (Spartan-7 xc7s6ftgb196-1)
# Source: CT137X_PIN.xlsx
#
# 用法说明：
# 1. 默认只保留 clk / rst / 电压配置
# 2. 需要哪个外设，就把对应行取消注释
# 3. 没用到的端口一定保持注释，否则 Vivado 会报 get_ports 错误

# --------------------------------------------------------------------
# 基础配置
# --------------------------------------------------------------------
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]

# 如果后面要固化到配置 Flash，可按需取消下面三行注释
# set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
# set_property CONFIG_MODE SPIx4 [current_design]
# set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]


# --------------------------------------------------------------------
# 系统时钟与复位
# --------------------------------------------------------------------
set_property -dict {PACKAGE_PIN G11 IOSTANDARD LVCMOS33} [get_ports {clk}]
create_clock -period 20.000 -name clk [get_ports {clk}]

# 注意：板上的 RESET 按键是高有效
set_property -dict {PACKAGE_PIN B6 IOSTANDARD LVCMOS33} [get_ports {rst}]


# --------------------------------------------------------------------
# 用户按键 S1-S4
# 顶层建议写成 input wire [3:0] key;
# --------------------------------------------------------------------
set_property -dict {PACKAGE_PIN M5 IOSTANDARD LVCMOS33} [get_ports {key[0]}]
# set_property -dict {PACKAGE_PIN M4 IOSTANDARD LVCMOS33} [get_ports {key[1]}]
# set_property -dict {PACKAGE_PIN P5 IOSTANDARD LVCMOS33} [get_ports {key[2]}]
# set_property -dict {PACKAGE_PIN N4 IOSTANDARD LVCMOS33} [get_ports {key[3]}]


# --------------------------------------------------------------------
# LED LD1-LD8
# 顶层建议写成 output wire [7:0] ld;
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN N14 IOSTANDARD LVCMOS33} [get_ports {ld[0]}]
# set_property -dict {PACKAGE_PIN M14 IOSTANDARD LVCMOS33} [get_ports {ld[1]}]
# set_property -dict {PACKAGE_PIN P12 IOSTANDARD LVCMOS33} [get_ports {ld[2]}]
# set_property -dict {PACKAGE_PIN P13 IOSTANDARD LVCMOS33} [get_ports {ld[3]}]
# set_property -dict {PACKAGE_PIN N10 IOSTANDARD LVCMOS33} [get_ports {ld[4]}]
# set_property -dict {PACKAGE_PIN N11 IOSTANDARD LVCMOS33} [get_ports {ld[5]}]
# set_property -dict {PACKAGE_PIN P10 IOSTANDARD LVCMOS33} [get_ports {ld[6]}]
# set_property -dict {PACKAGE_PIN P11 IOSTANDARD LVCMOS33} [get_ports {ld[7]}]


# --------------------------------------------------------------------
# 数码管位选 COM1-COM8
# 顶层建议写成 output wire [7:0] sel;
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN B2 IOSTANDARD LVCMOS33} [get_ports {sel[0]}]
# set_property -dict {PACKAGE_PIN B1 IOSTANDARD LVCMOS33} [get_ports {sel[1]}]
# set_property -dict {PACKAGE_PIN C5 IOSTANDARD LVCMOS33} [get_ports {sel[2]}]
# set_property -dict {PACKAGE_PIN C4 IOSTANDARD LVCMOS33} [get_ports {sel[3]}]
# set_property -dict {PACKAGE_PIN E4 IOSTANDARD LVCMOS33} [get_ports {sel[4]}]
# set_property -dict {PACKAGE_PIN D4 IOSTANDARD LVCMOS33} [get_ports {sel[5]}]
# set_property -dict {PACKAGE_PIN F3 IOSTANDARD LVCMOS33} [get_ports {sel[6]}]
# set_property -dict {PACKAGE_PIN F2 IOSTANDARD LVCMOS33} [get_ports {sel[7]}]


# --------------------------------------------------------------------
# 数码管段选 SEGA-SEGDP
# 顶层建议写成 output wire [7:0] seg;
# seg[0]=A, seg[1]=B, ... seg[6]=G, seg[7]=DP
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN D3 IOSTANDARD LVCMOS33} [get_ports {seg[0]}]
# set_property -dict {PACKAGE_PIN C3 IOSTANDARD LVCMOS33} [get_ports {seg[1]}]
# set_property -dict {PACKAGE_PIN A4 IOSTANDARD LVCMOS33} [get_ports {seg[2]}]
# set_property -dict {PACKAGE_PIN A3 IOSTANDARD LVCMOS33} [get_ports {seg[3]}]
# set_property -dict {PACKAGE_PIN B3 IOSTANDARD LVCMOS33} [get_ports {seg[4]}]
# set_property -dict {PACKAGE_PIN A2 IOSTANDARD LVCMOS33} [get_ports {seg[5]}]
# set_property -dict {PACKAGE_PIN B5 IOSTANDARD LVCMOS33} [get_ports {seg[6]}]
# set_property -dict {PACKAGE_PIN A5 IOSTANDARD LVCMOS33} [get_ports {seg[7]}]


# --------------------------------------------------------------------
# 蜂鸣器
# 顶层建议写成 output wire buz;
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN L5 IOSTANDARD LVCMOS33} [get_ports {buz}]


# --------------------------------------------------------------------
# UART
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN F12 IOSTANDARD LVCMOS33} [get_ports {uart_tx}]
# set_property -dict {PACKAGE_PIN E12 IOSTANDARD LVCMOS33} [get_ports {uart_rx}]


# --------------------------------------------------------------------
# I2C 接口（ADC / DAC / EEPROM 共用）
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN E11 IOSTANDARD LVCMOS33} [get_ports {scl}]
# set_property -dict {PACKAGE_PIN M10 IOSTANDARD LVCMOS33} [get_ports {sda}]


# --------------------------------------------------------------------
# RTC（DS1302）
# A12 在资料表中写的是 RTC_RST
# 如果你的代码习惯写 rtc_ce，也可以把下面那一行换成 rtc_ce
# 两行不要同时取消注释
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN A10 IOSTANDARD LVCMOS33} [get_ports {rtc_sclk}]
# set_property -dict {PACKAGE_PIN A12 IOSTANDARD LVCMOS33} [get_ports {rtc_rst}]
# set_property -dict {PACKAGE_PIN A13 IOSTANDARD LVCMOS33} [get_ports {rtc_data}]

# 备选命名
# set_property -dict {PACKAGE_PIN A12 IOSTANDARD LVCMOS33} [get_ports {rtc_ce}]


# --------------------------------------------------------------------
# SPI Flash（用户 Flash）
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN D12 IOSTANDARD LVCMOS33} [get_ports {spi_cs_n}]
# set_property -dict {PACKAGE_PIN D13 IOSTANDARD LVCMOS33} [get_ports {spi_sck}]
# set_property -dict {PACKAGE_PIN G14 IOSTANDARD LVCMOS33} [get_ports {spi_io0}]
# set_property -dict {PACKAGE_PIN F14 IOSTANDARD LVCMOS33} [get_ports {spi_io1}]
# set_property -dict {PACKAGE_PIN F13 IOSTANDARD LVCMOS33} [get_ports {spi_io2}]
# set_property -dict {PACKAGE_PIN E13 IOSTANDARD LVCMOS33} [get_ports {spi_io3}]


# --------------------------------------------------------------------
# SRAM
# 顶层建议：
# output wire [16:0] sram_a
# inout  wire [7:0]  sram_d
# output wire        sram_oe_n, sram_we_n, sram_ce_n
# --------------------------------------------------------------------
# set_property -dict {PACKAGE_PIN J3 IOSTANDARD LVCMOS33} [get_ports {sram_d[0]}]
# set_property -dict {PACKAGE_PIN M1 IOSTANDARD LVCMOS33} [get_ports {sram_d[1]}]
# set_property -dict {PACKAGE_PIN L1 IOSTANDARD LVCMOS33} [get_ports {sram_d[2]}]
# set_property -dict {PACKAGE_PIN M3 IOSTANDARD LVCMOS33} [get_ports {sram_d[3]}]
# set_property -dict {PACKAGE_PIN M2 IOSTANDARD LVCMOS33} [get_ports {sram_d[4]}]
# set_property -dict {PACKAGE_PIN P2 IOSTANDARD LVCMOS33} [get_ports {sram_d[5]}]
# set_property -dict {PACKAGE_PIN N1 IOSTANDARD LVCMOS33} [get_ports {sram_d[6]}]
# set_property -dict {PACKAGE_PIN P4 IOSTANDARD LVCMOS33} [get_ports {sram_d[7]}]

# set_property -dict {PACKAGE_PIN G1 IOSTANDARD LVCMOS33} [get_ports {sram_a[0]}]
# set_property -dict {PACKAGE_PIN F1 IOSTANDARD LVCMOS33} [get_ports {sram_a[1]}]
# set_property -dict {PACKAGE_PIN E2 IOSTANDARD LVCMOS33} [get_ports {sram_a[2]}]
# set_property -dict {PACKAGE_PIN D2 IOSTANDARD LVCMOS33} [get_ports {sram_a[3]}]
# set_property -dict {PACKAGE_PIN D1 IOSTANDARD LVCMOS33} [get_ports {sram_a[4]}]
# set_property -dict {PACKAGE_PIN C1 IOSTANDARD LVCMOS33} [get_ports {sram_a[5]}]
# set_property -dict {PACKAGE_PIN G4 IOSTANDARD LVCMOS33} [get_ports {sram_a[6]}]
# set_property -dict {PACKAGE_PIN F4 IOSTANDARD LVCMOS33} [get_ports {sram_a[7]}]
# set_property -dict {PACKAGE_PIN H4 IOSTANDARD LVCMOS33} [get_ports {sram_a[8]}]
# set_property -dict {PACKAGE_PIN H3 IOSTANDARD LVCMOS33} [get_ports {sram_a[9]}]
# set_property -dict {PACKAGE_PIN H2 IOSTANDARD LVCMOS33} [get_ports {sram_a[10]}]
# set_property -dict {PACKAGE_PIN H1 IOSTANDARD LVCMOS33} [get_ports {sram_a[11]}]
# set_property -dict {PACKAGE_PIN J2 IOSTANDARD LVCMOS33} [get_ports {sram_a[12]}]
# set_property -dict {PACKAGE_PIN J1 IOSTANDARD LVCMOS33} [get_ports {sram_a[13]}]
# set_property -dict {PACKAGE_PIN K4 IOSTANDARD LVCMOS33} [get_ports {sram_a[14]}]
# set_property -dict {PACKAGE_PIN K3 IOSTANDARD LVCMOS33} [get_ports {sram_a[15]}]
# set_property -dict {PACKAGE_PIN J4 IOSTANDARD LVCMOS33} [get_ports {sram_a[16]}]

# set_property -dict {PACKAGE_PIN L3 IOSTANDARD LVCMOS33} [get_ports {sram_oe_n}]
# set_property -dict {PACKAGE_PIN P3 IOSTANDARD LVCMOS33} [get_ports {sram_we_n}]
# set_property -dict {PACKAGE_PIN L2 IOSTANDARD LVCMOS33} [get_ports {sram_ce_n}]
