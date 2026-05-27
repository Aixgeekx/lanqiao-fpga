# ----------------------------------------------------------------------------
# 蓝桥杯 FPGA X系列 (XC7S6-1FTGB196) 综合约束文件
# 根据 CT137X_PIN.xlsx 更新，适配当前顶层模块 top.v 的端口名称
# ----------------------------------------------------------------------------
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]

# 系统时钟与复位
set_property -dict {PACKAGE_PIN G11 IOSTANDARD LVCMOS33} [get_ports sys_clk]
create_clock -period 20.000 -name sys_clk_pin -waveform {0.000 10.000} -add [get_ports sys_clk]
set_property -dict {PACKAGE_PIN B6  IOSTANDARD LVCMOS33} [get_ports sys_rst_n]

# 用户按键 (S1-S4)
set_property -dict {PACKAGE_PIN M5  IOSTANDARD LVCMOS33} [get_ports {key[0]}]
set_property -dict {PACKAGE_PIN M4  IOSTANDARD LVCMOS33} [get_ports {key[1]}]
set_property -dict {PACKAGE_PIN P5  IOSTANDARD LVCMOS33} [get_ports {key[2]}]
set_property -dict {PACKAGE_PIN N4  IOSTANDARD LVCMOS33} [get_ports {key[3]}]

# 数码管段选 (A~DP)
set_property -dict {PACKAGE_PIN D3  IOSTANDARD LVCMOS33} [get_ports {seg_data[0]}]
set_property -dict {PACKAGE_PIN C3  IOSTANDARD LVCMOS33} [get_ports {seg_data[1]}]
set_property -dict {PACKAGE_PIN A4  IOSTANDARD LVCMOS33} [get_ports {seg_data[2]}]
set_property -dict {PACKAGE_PIN A3  IOSTANDARD LVCMOS33} [get_ports {seg_data[3]}]
set_property -dict {PACKAGE_PIN B3  IOSTANDARD LVCMOS33} [get_ports {seg_data[4]}]
set_property -dict {PACKAGE_PIN A2  IOSTANDARD LVCMOS33} [get_ports {seg_data[5]}]
set_property -dict {PACKAGE_PIN B5  IOSTANDARD LVCMOS33} [get_ports {seg_data[6]}]
set_property -dict {PACKAGE_PIN A5  IOSTANDARD LVCMOS33} [get_ports {seg_data[7]}]

# 数码管位选 (COM1-COM8)
set_property -dict {PACKAGE_PIN B2  IOSTANDARD LVCMOS33} [get_ports {seg_sel[0]}]
set_property -dict {PACKAGE_PIN B1  IOSTANDARD LVCMOS33} [get_ports {seg_sel[1]}]
set_property -dict {PACKAGE_PIN C5  IOSTANDARD LVCMOS33} [get_ports {seg_sel[2]}]
set_property -dict {PACKAGE_PIN C4  IOSTANDARD LVCMOS33} [get_ports {seg_sel[3]}]
set_property -dict {PACKAGE_PIN E4  IOSTANDARD LVCMOS33} [get_ports {seg_sel[4]}]
set_property -dict {PACKAGE_PIN D4  IOSTANDARD LVCMOS33} [get_ports {seg_sel[5]}]
set_property -dict {PACKAGE_PIN F3  IOSTANDARD LVCMOS33} [get_ports {seg_sel[6]}]
set_property -dict {PACKAGE_PIN F2  IOSTANDARD LVCMOS33} [get_ports {seg_sel[7]}]

