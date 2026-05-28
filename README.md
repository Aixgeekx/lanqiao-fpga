# all_code

蓝桥杯 FPGA 学习与模拟测试项目仓库，包含 CT137X/AMD Xilinx 资料、Verilog 驱动与用户模块、真题模拟题、生成教材和提交结果。

## 目录

- `driver/`：可复用外设驱动模块。
- `user/`：顶层应用逻辑与题目实现模块。
- `study/`：学习和实验代码。
- `title/`：板卡资料、题目文件、数据手册和工具。
- `真题模拟题/`：真题、模拟题和提取图片。
- `Aix_tools/`：项目阅读、教材生成、验证和自动同步工具。
- `project/lanqiao-fpga-textbook/`：教材发布副本。
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
