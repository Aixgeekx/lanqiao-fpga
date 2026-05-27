# Project Reading Summary

## Scope
- Root: `X:\FPGA\LQBFPGA\simulated test\all_code`
- Official material: `title`
- User template RTL: `user`
- Device driver RTL: `driver`
- Extracted official docs index: `Aix_tools/title_docs_extract.md` (certificate ID is redacted in generated output)

## Official Requirements And Hardware Facts
- Platform: CT137X, Xilinx Spartan-7 `XC7S6-1FTGB196`, 50 MHz clock on `GCLK/G11`.
- Board `RESET/B6` is active-high. Current `user/top_board.v` correctly converts it to active-low `sys_rst_n`.
- S1-S4 are active-low keys on `M5/M4/P5/N4`.
- User LEDs are wired active-low. `driver/led_display.v` inverts `led_pattern`, matching the official constraint note.
- Seven-segment display uses common-anode codes. `driver/seg_driver.v` matches `SEG_TABLE.pdf` for 0-9, C, F, dash, and blank.
- I2C bus is shared by ADC081C021, DAC5571, and AT24C02 on `I2C_SCL/E11`, `I2C_SDA/M10`.
- UART through CH340C uses `UART_TX/F12`, `UART_RX/E12`.
- DS1302 uses `RTC_SCLK/A10`, `RTC_RST/A12`, `RTC_DATA/A13`; RTL names may use `ds1302_sclk`, `ds1302_ce`, `ds1302_data`.
- W25Q128 user flash uses `SPI_CS/D12`, `SPI_SCK/D13`, `SPI_IO0/G14`, `SPI_IO1/F14`, `SPI_IO2/F13`, `SPI_IO3/E13`.
- SRAM IS63WV1288 is 128K x 8 with 17 address lines and 8 data lines.

## Code Map
- `user/top_board.v`: board-level wrapper using official board signal names for the practice design.
- `user/top.v`: current core practice design. S1 increments a 4-digit BCD counter, S2 decrements, S3 changes LED mode, S4 changes buzzer mode, and the seven-segment display shows counter/modes.
- `user/seg_proc.v`: 1 kHz dynamic scan wrapper over `seg_driver`.
- `user/led_proc.v`: LED pattern generator, driven by a 1 Hz divider.
- `user/key_proc.v`: alternate key-mode wrapper; currently uses `down`, which is release pulse in the present `key_ctrl` implementation.
- `user/ds1302_test.v`: DS1302 time read/write wrapper that clears CH when needed.
- `user/uart_parser.v`: UART command parser for `A\r\n` and `W\r\n` style commands.
- `user/uart_string_sender.v`: UART string sender wrapper over `uart_tx`.
- `driver/iic_drive.v`: generic I2C transaction engine.
- `driver/adc_ctrl.v`, `driver/dac_ctrl.v`, `driver/eeprom_*_ctrl.v`: I2C device wrappers.
- `driver/ds1302_wr_drive.v`, `driver/ds1302_io_convert.v`, `driver/spi_master.v`: official DS1302 stack.
- `driver/key_ctrl.v`: 100 Hz sampled key edge detector.
- `driver/frequency_driver.v`: parameterized clock divider, module name `frequency_divider`.
- `driver/seg_driver.v`, `driver/led_display.v`: display polarity adapters.
- `driver/uart_rx.v`, `driver/uart_tx.v`: 8N1 UART modules.
- `driver/sram_ctrl.v`: simple SRAM read/write controller.
- `driver/w25q128_ctrl.v`: SPI flash controller with JEDEC ID, status, byte read/write, sector erase.

## Current Verification
- Syntax check command:
  `iverilog -g2005 -o Aix_tools\top_syntax.vvp user\*.v driver\*.v`
- Result: passed.
- Note: local Icarus Verilog does not accept `-g2012`; use `-g2005` or supported flags.

## Risks To Remember
- `driver/key_ctrl.v` signal names/comments are misleading for active-low keys: `up` pulses on key press, `down` pulses on release. `user/top.v` uses `up` as press and is consistent with actual behavior; `user/key_proc.v` uses `down`, so it triggers on release.
- The full PDF extraction of large Xilinx user guides can time out. Use `Aix_tools/extract_title_docs.py`, which fully extracts small docs and samples very large datasheets.
- Future competition implementation should follow `title` documents first, especially pin naming/polarity, then adapt `user/top_board.v` and `user/top.v` only as needed.
