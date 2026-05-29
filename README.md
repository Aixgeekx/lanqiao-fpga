# 蓝桥杯国一工程模板及零基础教学

蓝桥杯 FPGA 设计与开发（AMD/Xilinx 平台）国一工程模板与零基础教学资源库，涵盖完整驱动库、真题解析、模拟赛代码和入门资料。

## 目录

- `driver/`：16 个可复用外设驱动模块（ADC/DAC/DS1302/EEPROM/IIC/LED/SEG/SPI/SRAM/UART/W25Q128 等）。
- `user/`：顶层应用逻辑与题目实现模块（top/key_proc/led_proc/seg_proc/uart_parser 等）。
- `study/`：零基础入门代码与参考资料（Verilog 入门、FPGA 大模板建立、竞赛规则等）。
- `title/`：CT137X 竞赛平台资料、引脚表、数据手册和官方工具。
- `真题模拟题/`：第十六/十七届省赛国赛真题、模拟题 PDF 及题目内容提取。
- `Aix_tools/`：PDF 提取、教材生成、自动同步等辅助工具。
- `project/lanqiao-fpga-textbook/`：教材发布副本（含生成的 PDF）。
- `results/`：最终生成结果和可提交文件。

## GitHub 同步

远程私密仓库：

```powershell
git remote -v
```

当前仓库已启用 Git LFS，`.exe` 大文件会通过 LFS 上传：

```powershell
git lfs ls-files
```

## 持续监视与自动推送

自动同步脚本位于：

```powershell
Aix_tools\watch_and_push.ps1
```

手动启动：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Aix_tools\watch_and_push.ps1 -IntervalSeconds 60
```

脚本每 60 秒检查一次项目变化，发现变更后执行 `git add -A`、自动提交、拉取远程最新状态并推送到 `origin/main`。日志写入 `Aix_tools/git_watch_push.log`，进程号写入 `Aix_tools/git_watch_push.pid`，二者已加入 `.gitignore`，不会反复触发提交。

停止监视：

```powershell
Stop-Process -Id (Get-Content .\Aix_tools\git_watch_push.pid)
```

## 版本管理

日常修改由自动监视脚本提交并推送；稳定节点必须更新版本号和更新日志。

版本文件：

```text
VERSION
CHANGELOG.md
```

发布新版本流程：

```powershell
# 1. 修改 VERSION，例如 0.1.1
# 2. 在 CHANGELOG.md 记录本版本变化
git add VERSION CHANGELOG.md
git commit -m "chore: release v0.1.1"
git push

# 3. 创建并推送 Git 标签
powershell -NoProfile -ExecutionPolicy Bypass -File .\Aix_tools\release_version.ps1 -Version 0.1.1
```

规则：

- 修 bug 或只改文档：递增修订版本，例如 `0.1.0` 到 `0.1.1`。
- 增加重要功能、章节或工具：递增次版本，例如 `0.1.0` 到 `0.2.0`。
- 结构大改或不兼容调整：递增主版本，例如 `1.0.0` 到 `2.0.0`。
