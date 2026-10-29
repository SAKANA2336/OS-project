# OS-project：CS340 操作系统论文复现

本仓库用于完成 CS340 2026–2027 学年 Research Paper Replication 项目。目标是选择一篇课程清单中的操作系统论文，复现一至三个可核查主张，以相同指标比较论文结果与本项目结果，量化并解释差异，再完成一个一次只改变一个因素的扩展实验。

当前阶段是治理与复现范围准备。**尚未登记所选论文、主张、起始代码、技术栈或正式实验；没有构建、运行、结果或复现结论。** 未决定事项必须保留为“待定”。

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
- 交接说明：[`docs/HANDOFF.md`](docs/HANDOFF.md)
- 文件治理：[`docs/governance/FILE_MANAGEMENT.md`](docs/governance/FILE_MANAGEMENT.md)
- 运行证据约定：[`runs/README.md`](runs/README.md)

## 双工作区制度

- 日常开发区：`<workspace-parent>/OS-project-local`，是独立 Git 仓库，不配置 remote；所有日常代码、构建、实验、文档和本地 commit 在此进行。
- GitHub 发布区：`<workspace-parent>/OS-project`，配置 `origin`，默认只读；只有用户明确授权 push 后，才按文件 allowlist 同步、验证、commit 和上传。

两个区域不能用分支或 `git worktree` 代替。每区还使用不跟踪的 `.local/workspace-role` 标记，并由 `scripts/check-workspace-zone.sh work` 或 `scripts/check-workspace-zone.sh release` 核验规范目录名、独立 `.git`、remote、分支与 upstream。当前已经连接 `origin` 的历史目录按发布区处理；独立日常区已于 2026-10-30 建立并通过检查。

## 下一步

1. 确认组员身份以及本项目选择的论文。
2. 后续日常工作切换到已核验的无 remote 开发区，不在发布区继续实现或实验。
3. 取得独立 `Presentation Instruction`，并核实组信息表单提交状态。
4. 在下一连续协议版本登记主张、起始代码 commit、许可证、环境、workload、比较指标、预算和安全边界。
5. 经确认后再开始代码获取、构建和有界可行性检查。
