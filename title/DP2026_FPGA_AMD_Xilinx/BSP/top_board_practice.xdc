# ----------------------------------------------------------------------------
# CT137X practice constraints for code/user/top_board.v
# Target device: XC7S6-1FTGB196
# ----------------------------------------------------------------------------

set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]

# System clock and reset
# Board RESET is active-high. top_board.v converts it to active-low internally.
set_property -dict {PACKAGE_PIN G11 IOSTANDARD LVCMOS33} [get_ports GCLK]
create_clock -period 20.000 -name sys_clk_pin [get_ports GCLK]
set_property -dict {PACKAGE_PIN B6 IOSTANDARD LVCMOS33} [get_ports RESET]

# User keys (active-low when pressed)
set_property -dict {PACKAGE_PIN M5 IOSTANDARD LVCMOS33} [get_ports S1]
set_property -dict {PACKAGE_PIN M4 IOSTANDARD LVCMOS33} [get_ports S2]
set_property -dict {PACKAGE_PIN P5 IOSTANDARD LVCMOS33} [get_ports S3]
set_property -dict {PACKAGE_PIN N4 IOSTANDARD LVCMOS33} [get_ports S4]

# LEDs
set_property -dict {PACKAGE_PIN N14 IOSTANDARD LVCMOS33} [get_ports LD1]
set_property -dict {PACKAGE_PIN M14 IOSTANDARD LVCMOS33} [get_ports LD2]
set_property -dict {PACKAGE_PIN P12 IOSTANDARD LVCMOS33} [get_ports LD3]
set_property -dict {PACKAGE_PIN P13 IOSTANDARD LVCMOS33} [get_ports LD4]
set_property -dict {PACKAGE_PIN N10 IOSTANDARD LVCMOS33} [get_ports LD5]
set_property -dict {PACKAGE_PIN N11 IOSTANDARD LVCMOS33} [get_ports LD6]
set_property -dict {PACKAGE_PIN P10 IOSTANDARD LVCMOS33} [get_ports LD7]
set_property -dict {PACKAGE_PIN P11 IOSTANDARD LVCMOS33} [get_ports LD8]

# Buzzer
set_property -dict {PACKAGE_PIN L5 IOSTANDARD LVCMOS33} [get_ports BUZ]

# Seven-segment segment lines
set_property -dict {PACKAGE_PIN D3 IOSTANDARD LVCMOS33} [get_ports SEGA]
set_property -dict {PACKAGE_PIN C3 IOSTANDARD LVCMOS33} [get_ports SEGB]
set_property -dict {PACKAGE_PIN A4 IOSTANDARD LVCMOS33} [get_ports SEGC]
set_property -dict {PACKAGE_PIN A3 IOSTANDARD LVCMOS33} [get_ports SEGD]
set_property -dict {PACKAGE_PIN B3 IOSTANDARD LVCMOS33} [get_ports SEGE]
set_property -dict {PACKAGE_PIN A2 IOSTANDARD LVCMOS33} [get_ports SEGF]
set_property -dict {PACKAGE_PIN B5 IOSTANDARD LVCMOS33} [get_ports SEGG]
set_property -dict {PACKAGE_PIN A5 IOSTANDARD LVCMOS33} [get_ports SEGDP]

# Seven-segment digit select lines
set_property -dict {PACKAGE_PIN B2 IOSTANDARD LVCMOS33} [get_ports COM1]
set_property -dict {PACKAGE_PIN B1 IOSTANDARD LVCMOS33} [get_ports COM2]
set_property -dict {PACKAGE_PIN C5 IOSTANDARD LVCMOS33} [get_ports COM3]
set_property -dict {PACKAGE_PIN C4 IOSTANDARD LVCMOS33} [get_ports COM4]
set_property -dict {PACKAGE_PIN E4 IOSTANDARD LVCMOS33} [get_ports COM5]
set_property -dict {PACKAGE_PIN D4 IOSTANDARD LVCMOS33} [get_ports COM6]
set_property -dict {PACKAGE_PIN F3 IOSTANDARD LVCMOS33} [get_ports COM7]
set_property -dict {PACKAGE_PIN F2 IOSTANDARD LVCMOS33} [get_ports COM8]
