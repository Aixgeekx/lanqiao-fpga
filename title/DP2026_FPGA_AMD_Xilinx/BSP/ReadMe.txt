驱动使用说明

1. 编码规范
	所有驱动代码注释采用UTF-8编码，推荐使用VSCODE查看详细注释。

2. 驱动接口
	通过iic_drive模块操作IIC设备，已提供相关端口信号及协议时序。
	通过ds1302_wr_drive模块操作RTC设备，已提供相关端口信号及协议时序

3. IIC驱动调用方式
	Verilog：在目标模块中直接例化iic_drive驱动模块，实现IIC读写控制。
	VHDL：需将iic_drive.v（Verilog源码）与iic_drive_wrapper.vhd（VHDL封装层）共同加入工程，例化iic_drive_wrapper模块，实现IIC读写控制。
3.RTC驱动调用方式
	Verilog：需将spi_master.v、ds1302_io_convert.v与ds1302_wr_drive.v共同加入工程，例化ds1302_wr_drive模块，实现RTC读写控制。
	VHDL：需将spi_master.v（Verilog源码）、ds1302_io_convert.v（Verilog源码）、ds1302_wr_drive.v（Verilog源码）与ds1302_wr_drive_wrapper.vhd（VHDL封装层）共同加入工程，例化ds1302_wr_drive_wrapper模块，实现RTC读写控制。

本驱动实现方案仅供参考，选手可以根据硬件平台、开发环境、器件特性等因素进行灵活调整。