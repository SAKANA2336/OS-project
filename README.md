# OS-project：CS340 操作系统论文复现

本仓库用于完成 CS340 2026–2027 学年 Research Paper Replication 项目。目标是选择一篇课程清单中的操作系统论文，复现一至三个可核查主张，以相同指标比较论文结果与本项目结果，量化并解释差异，再完成一个一次只改变一个因素的扩展实验。

复现主题已确定为课程方向 8：**AddressSanitizer: A Fast Address Sanity Checker（USENIX ATC 2012）**。用户于 2026-10-30 确认选题，本次于 2026-11-07 补登记；论文引用与来源见 [`docs/PROTOCOL.md`](docs/PROTOCOL.md)。

现代基础环境已建成并通过七项真实功能验收：Ubuntu 24.04.5、Linux x86_64、Clang/LLVM 18.1.3，C/C++ 编译、越界与释放后使用检测均通过。协议 v0.3 未冻结，正式主张、benchmark、预算和扩展方案仍待定；尚无论文性能复现结论。

## 环境搭建进度

2026-11-08 完成 Docker Desktop / WSL2 下的现代 ASan 基础环境构建与验收。

本阶段提交成员：**张瀚洋（1240036026），GitHub 账号 `wbw374`**。贡献范围、历史署名说明及教师检查入口见[贡献记录](docs/CONTRIBUTIONS.md)。

| 已完成内容 | 可检查入口 |
| --- | --- |
| Ubuntu 24.04 + Clang/LLVM 18 容器配置 | [Dockerfile](outputs/asan-environment/Dockerfile) |
| 一键下载、构建、版本记录与功能检查 | [setup.ps1](outputs/asan-environment/setup.ps1) |
| 3 项正常程序检查 + 4 类内存错误检测，7/7 通过 | [原始验收结果](runs/env-20261108t013027z-6c0e488a/validation/summary.json) |
| 实际编译器版本、软件包、资源限制与逐项输出 | [运行证据与说明](runs/env-20261108t013027z-6c0e488a/README.md) |
| 网络及执行权限失败后的恢复过程 | [环境说明与尝试记录](outputs/asan-environment/README.md) |

在已安装并启动 Docker Desktop、可使用 Linux 容器的 Windows PowerShell 中，从仓库根目录执行：

```powershell
& .\outputs\asan-environment\setup.ps1
```

成功时显示 `PASS: 7/7 functional checks`，并输出镜像 ID 和证据目录。首次运行需要下载镜像及依赖；执行策略处理、资源要求和完整步骤见[环境使用说明](outputs/asan-environment/README.md)。仓库保存搭建材料和小型日志，镜像由脚本在本机生成。

当前完成的是复现基础环境；论文性能主张、三次以上独立实验与扩展实验仍待开展。

## 课程硬性要求摘要

- 最终报告使用英文并提交 PDF。
- 每组应有四名学生，并通过课程表单提交组员信息与复现仓库链接；提交状态以实际回执为准。
- 每个主张关联论文中的具体表格、图或数值。
- 论文结果与本项目结果使用相同指标和可比设置；偏离项逐条记录。
- 主结果至少运行三次，报告 `mean ± standard deviation`，且每个数字可追溯到仓库日志。
- 差异同时报告绝对值和相对值，并通过受控检查或重跑解释。
- 扩展实验一次只改变一个因素，并尽量保持硬件与 workload 不变。
- GitHub 每周日 23:59 检查；每周至少一个有意义的已推送 commit。
- 每条 commit message 包含实际贡献成员的学号和全名；不得伪造署名。
- 仓库不得提交构建产物、磁盘镜像、大型 trace、凭据或超过 50 MB 的文件。
- 最终交付在用户确认后标记 `v1.0`。

课程任务书给出的组信息表单为 <https://v.wjx.cn/vm/rZCQLSE.aspx>。任务书还列出：组队截止 2026-10-25、换题截止 2026-11-01、展示暂定 2026-12-01。周检和里程碑的具体时区应以课程通知为准；最终展示的详细要求来自尚未取得的独立 `Presentation Instruction`。

## 项目入口

- 持续执行规则：[`AGENTS.md`](AGENTS.md)
- 当前状态：[`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md)
- 当前协议与待定项：[`docs/PROTOCOL.md`](docs/PROTOCOL.md)
- 决策记录：[`docs/DECISIONS.md`](docs/DECISIONS.md)
- 成员与贡献记录：[`docs/CONTRIBUTIONS.md`](docs/CONTRIBUTIONS.md)
- 交接说明：[`docs/HANDOFF.md`](docs/HANDOFF.md)
- 文件治理：[`docs/governance/FILE_MANAGEMENT.md`](docs/governance/FILE_MANAGEMENT.md)
- 运行证据约定：[`runs/README.md`](runs/README.md)

## 双工作区制度

- 日常开发区：`<workspace-parent>/OS-project-local`，是独立 Git 仓库，不配置 remote；所有日常代码、构建、实验、文档和本地 commit 在此进行。
- GitHub 发布区：`<workspace-parent>/OS-project`，配置 `origin`，默认只读；只有用户明确授权 push 后，才按文件 allowlist 同步、验证、commit 和上传。

两个区域不能用分支或 `git worktree` 代替。每区还使用不跟踪的 `.local/workspace-role` 标记，并由 `scripts/check-workspace-zone.sh work` 或 `scripts/check-workspace-zone.sh release` 核验规范目录名、独立 `.git`、remote、分支与 upstream。Windows 下 Bash 无法启动时，本次采用 [PowerShell 等价检查](scripts/check-workspace-zone.ps1)，依据见决策 D-011、D-013。本机角色标记不随公开仓库发布。

## 下一步

1. 补齐其余组员身份与贡献安排；已知成员张瀚洋（1240036026），见决策记录。
2. 后续日常工作切换到已核验的无 remote 开发区，不在发布区继续实现或实验。
3. 取得独立 `Presentation Instruction`，并核实组信息表单提交状态。
4. 按协议 v0.3 复用已验证的现代环境；重建时使用新 run ID 并重新验收，尚不执行正式 benchmark。
5. 登记主张、起始代码 commit、许可证、workload、比较指标、正式预算和安全边界，冻结定量方案后运行正式实验。
