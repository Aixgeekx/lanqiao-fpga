module adc_ctrl (
        input        sys_clk,              // 输入：系统时钟信号
        input        rst_n,                // 输入：低电平复位信号
        input        ad_read_start_flag,   // 输入：ADC 读取开始标志
        output       ad_read_end_flag,     // 输出：ADC 读取结束标志
        output       scl,                  // 输出：I2C 时钟信号
        output [7:0] ad_data,              // 输出：ADC 转换后的数据
        inout        sda                   // 双向：I2C 数据信号
    );
    // 参数定义
    parameter P_SYS_CLK = 28'd50_000_000;  // 系统时钟频率：50MHz
    parameter P_IIC_SCL = 28'd125_000;     // I2C SCL 时钟频率：125kHz
    parameter P_DEVICE_ADDR = 7'b1010_100; // I2C 从设备地址：ADC 器件地址
    parameter P_ADDR_BYTE_NUM = 8'd1;      // I2C 从设备地址字节数：1字节
    parameter P_DATA_BYTE_NUM = 8'd2;      // I2C 一次操作传输数据字节数：2字节

    // 内部信号定义
    wire [15:0]iic_r_data;                // I2C 读取的原始数据（16位）

    // I2C 驱动模块实例化
    iic_drive #(
                  .P_SYS_CLK      (P_SYS_CLK),      // 系统时钟频率参数
                  .P_IIC_SCL      (P_IIC_SCL),      // I2C SCL 时钟频率参数
                  .P_DEVICE_ADDR  (P_DEVICE_ADDR),  // I2C 从设备地址参数
                  .P_ADDR_BYTE_NUM(P_ADDR_BYTE_NUM),// 地址字节数参数
                  .P_DATA_BYTE_NUM(P_DATA_BYTE_NUM) // 数据字节数参数
              ) inst_dac (
                  .iic_clk        (sys_clk),              // 输入：I2C 时钟信号
                  .iic_rst        (rst_n),                // 输入：I2C 复位信号
                  .iic_start      (ad_read_start_flag),   // 输入：I2C 操作开始信号（0:空闲 1:开始）
                  .iic_ready      (ad_read_end_flag),     // 输出：I2C 设备状态信号（0:繁忙 1:空闲）
                  .iic_rw_flag    (1'b1),                 // 输入：I2C 读写标志（0:写 1:读）
                  .iic_word_addr  (0),                    // 输入：I2C 读写地址（固定为0）
                  .iic_wdata      (),                     // 输入：I2C 写数据（先写高字节数据的高位）
                  .iic_rdata      (iic_r_data),          // 输出：I2C 读数据（先读高字节数据的高位）
                  .iic_rdata_valid(),                    // 输出：I2C 读数据有效信号（0:无效 1:有效）
                  .iic_scl        (scl),                 // 输出：I2C SCL 时钟信号
                  .iic_sda        (sda)                  // 双向：I2C SDA 数据信号
              );

    // ADC 数据处理：从16位原始数据中提取有效的8位数据
    assign ad_data = iic_r_data[11:4];    // 取中间8位作为有效数据输出

endmodule
