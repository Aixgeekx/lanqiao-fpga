# 存储类驱动使用说明

## 1. 这次补了什么

- `code/driver/sram_ctrl.v`
- `code/driver/w25q128_ctrl.v`

这两个都是“够做题”的版本，接口故意做得简单，不追求最高吞吐率，先保证你容易接、容易看懂、容易调试。

## 2. 蜂鸣器要不要单独驱动

你这个阶段可以先不要。

这块板的蜂鸣器本质上就是一个数字输出脚 `BUZ`，最简单的做法是：

- 用分频器产生一个几百 Hz 到几 kHz 的方波
- 直接把方波送到 `BUZ`

所以普通题目里，蜂鸣器不一定要单独写一个 `buzzer_ctrl.v`。如果以后题目要求“播放音阶”或者“不同节拍蜂鸣”，再单独封装会更合适。

## 3. `sram_ctrl.v` 怎么用

### 接口含义

- `read_req`：发起一次读请求，高电平保持 1 个时钟周期即可
- `write_req`：发起一次写请求，高电平保持 1 个时钟周期即可
- `addr`：17 位地址
- `write_data`：写入的 8 位数据
- `read_data`：读出的 8 位数据
- `ready`：当前空闲，可以接收新请求
- `done`：本次读/写完成脉冲

### 最简单的使用顺序

1. 等 `ready == 1`
2. 给地址
3. 如果要写，给 `write_data` 并拉高 `write_req` 一个周期
4. 如果要读，拉高 `read_req` 一个周期
5. 等 `done == 1`
6. 读操作时，在 `done` 后读取 `read_data`

### 例化示意

```verilog
wire [7:0] sram_rdata;
wire sram_ready;
wire sram_done;

sram_ctrl u_sram (
    .clk       (sys_clk),
    .rst_n     (sys_rst_n),
    .read_req  (sram_read_req),
    .write_req (sram_write_req),
    .addr      (sram_addr_req),
    .write_data(sram_wdata),
    .read_data (sram_rdata),
    .ready     (sram_ready),
    .done      (sram_done),
    .sram_addr (sram_addr_bus),
    .sram_data (sram_data_bus),
    .sram_ce_n (SRAM_CE),
    .sram_oe_n (SRAM_OE),
    .sram_we_n (SRAM_WE)
);
```

注意：

- `SRAM_CE`、`SRAM_OE`、`SRAM_WE` 虽然板卡文件里名字没有 `_n`，但它们本质是低有效控制信号
- 这个驱动一次只处理一个字节，适合先做题，不适合高吞吐缓存设计

## 4. `w25q128_ctrl.v` 怎么用

### 支持的操作

- `OP_READ_JEDEC_ID = 3'd0`：读取 JEDEC ID
- `OP_READ_STATUS   = 3'd1`：读取状态寄存器 1
- `OP_READ_BYTE     = 3'd2`：读取 1 个字节
- `OP_WRITE_BYTE    = 3'd3`：写 1 个字节
- `OP_SECTOR_ERASE  = 3'd4`：擦除 4KB 扇区

### 接口含义

- `start`：启动脉冲，高 1 个时钟周期即可
- `op_code`：操作类型
- `flash_addr`：24 位地址
- `write_data`：写字节数据
- `jedec_id`：读 ID 结果
- `read_data`：读 1 字节结果
- `status_reg`：状态寄存器值
- `ready`：当前空闲
- `busy`：当前正在执行
- `done`：操作完成脉冲

### 最简单的使用顺序

#### 读 ID

1. `op_code = OP_READ_JEDEC_ID`
2. `start` 拉高 1 个周期
3. 等 `done`
4. 看 `jedec_id`

#### 读 1 字节

1. `op_code = OP_READ_BYTE`
2. `flash_addr = 目标地址`
3. `start` 拉高 1 个周期
4. 等 `done`
5. 看 `read_data`

#### 写 1 字节

1. 先擦除所在 4KB 扇区
2. 再执行 `OP_WRITE_BYTE`
3. 等 `done`
4. 再读回验证

### 最重要的 Flash 常识

- Flash 写入前通常要先擦除
- 不擦除时，位只能从 `1 -> 0`，不能直接从 `0 -> 1`
- 所以最稳妥的顺序是：
  先 `SECTOR_ERASE`，再 `WRITE_BYTE`，最后 `READ_BYTE` 验证

### 例化示意

```verilog
wire [23:0] jedec_id;
wire [7:0] flash_rdata;
wire [7:0] flash_status;
wire flash_ready;
wire flash_busy;
wire flash_done;

w25q128_ctrl u_flash (
    .clk       (sys_clk),
    .rst_n     (sys_rst_n),
    .start     (flash_start),
    .op_code   (flash_op),
    .flash_addr(flash_addr),
    .write_data(flash_wdata),
    .jedec_id  (jedec_id),
    .read_data (flash_rdata),
    .status_reg(flash_status),
    .ready     (flash_ready),
    .busy      (flash_busy),
    .done      (flash_done),
    .flash_cs_n(SPI_CS),
    .flash_sck (SPI_SCK),
    .flash_io0 (SPI_IO0_MOSI),
    .flash_io1 (SPI_IO1_MISO),
    .flash_io2 (SPI_IO2),
    .flash_io3 (SPI_IO3)
);
```

## 5. 你在 `top.v` 里该怎么写

推荐写一个小状态机，不要直接到处拉 `start`。

推荐结构：

1. `IDLE`：等待按键或串口命令
2. `LAUNCH`：给驱动一个单周期启动脉冲
3. `WAIT_DONE`：等待 `done`
4. `SHOW_RESULT`：把读到的数据显示到 LED 或数码管

不要在 `always` 里一直把 `start` 拉高。  
这些驱动都按“启动脉冲”工作，不是按电平一直工作。

## 6. 这两个驱动适合什么题

`sram_ctrl.v` 适合：

- 数据缓存
- 表查找
- 读写测试题
- 地址递增读写题

`w25q128_ctrl.v` 适合：

- 读 JEDEC ID
- 掉电保存少量参数
- 读写固定地址配置
- 简单的扇区擦除 / 单字节写入验证

如果你下一步要，我可以直接继续做两件事里的一个：

1. 给 `top.v` 接上 `SRAM` 做一个“按键写入 / 按键读取 / 数码管显示”的完整例子
2. 给 `top.v` 接上 `W25Q128` 做一个“读 ID 并显示”的完整例子
