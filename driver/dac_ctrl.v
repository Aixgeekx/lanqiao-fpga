module dac_ctrl(
        input sys_clk,                    // 输入：系统时钟信号
        input rst_n,                      // 输入：低电平复位信号
        input da_write_start_flag,        // 输入：DAC 写入开始标志
        output da_write_end_flag,         // 输出：DAC 写入结束标志
        output scl,                       // 输出：I2C 时钟信号
        input [7:0]da_data,               // 输入：要写入 DAC 的数据
        inout sda                         // 双向：I2C 数据信号
    );
    // 参数定义
    parameter P_SYS_CLK = 28'd50_000_000;  // 系统时钟频率：50MHz
    parameter P_IIC_SCL = 28'd125_000;     // I2C SCL 时钟频率：125kHz
    parameter P_DEVICE_ADDR = 7'b100_1100; // I2C 从设备地址：DAC 器件地址
    parameter P_ADDR_BYTE_NUM = 8'd1;      // I2C 从设备地址字节数：1字节
    parameter P_DATA_BYTE_NUM = 8'd2;      // I2C 一次操作传输数据字节数：2字节

    // 内部信号定义
    wire [15:0]iic_w_data;                // I2C 写入的数据（16位）

    // DAC 数据处理：将8位数据扩展为16位，前后各补4个0
    assign iic_w_data = {4'b0000, da_data, 4'b0000};  // 数据格式转换

    // I2C 驱动模块实例化
    iic_drive #(
                  .P_SYS_CLK      (P_SYS_CLK),      // 系统时钟频率参数
                  .P_IIC_SCL      (P_IIC_SCL),      // I2C SCL 时钟频率参数
                  .P_DEVICE_ADDR  (P_DEVICE_ADDR),  // I2C 从设备地址参数
                  .P_ADDR_BYTE_NUM(P_ADDR_BYTE_NUM),// 地址字节数参数
                  .P_DATA_BYTE_NUM(P_DATA_BYTE_NUM) // 数据字节数参数
              ) inst_adc (
                  .iic_clk        (sys_clk),              // 输入：I2C 时钟信号
                  .iic_rst        (rst_n),                // 输入：I2C 复位信号
                  .iic_start      (da_write_start_flag),  // 输入：I2C 操作开始信号（0:空闲 1:开始）
                  .iic_ready      (da_write_end_flag),    // 输出：I2C 设备状态信号（0:繁忙 1:空闲）
                  .iic_rw_flag    (1'b0),                 // 输入：I2C 读写标志（0:写 1:读）
                  .iic_word_addr  (0),                    // 输入：I2C 读写地址（固定为0）
                  .iic_wdata      (iic_w_data),          // 输入：I2C 写数据（先写高字节数据的高位）
                  .iic_rdata      (),                     // 输出：I2C 读数据（先读高字节数据的高位）
                  .iic_rdata_valid(),                     // 输出：I2C 读数据有效信号（0:无效 1:有效）
                  .iic_scl        (scl),                  // 输出：I2C SCL 时钟信号
                  .iic_sda        (sda)                   // 双向：I2C SDA 数据信号
              );
endmodule
