# OS-project 当前状态

最后核实：2026-10-30（Asia/Shanghai）

本文件只记录由当前仓库文件和已观察命令支持的持久事实。工作树是否干净、是否领先远端等瞬时 Git 状态必须在操作时实时核验，不在此缓存。

## 当前阶段

- 阶段：治理 bootstrap 与复现范围准备。
- 所选论文：待定。
- 待复现主张：待定。
- 协议：`project-protocol-index v0.0 / draft_index / not_frozen`。
- 实验状态：未开始。
- 科学／性能结论：无。

## 已核实入口与产物

- 根目录持续规则 `AGENTS.md` 1.0。
- 当前协议 `docs/PROTOCOL.md` v0.0 及版本档案。
- 决策、交接和文件治理入口。
- 双工作区角色检查脚本 `scripts/check-workspace-zone.sh`。
- 课程任务书本地证据，SHA-256 为 `d129642a953ab1ecd7c27bf67dc667887867ec4045b72917bedaf6b76cc2666c`。
- GitHub 仓库预期身份：`SAKANA2336/OS-project`；发布操作时须用本机 Git 实时核验。

上述治理文件存在不代表论文已选择、代码已取得、环境已建立或实验已运行。

## 双工作区状态

- 制度已在 `AGENTS.md`、`docs/DECISIONS.md` 和文件治理中建立。
- 当前已配置 `origin` 的历史目录按发布区处理，本轮规则编写是制度生效前的 bootstrap。
- 独立日常开发区 `<workspace-parent>/OS-project-local` 已于 2026-10-30 通过一次性 provisioning 建立：拥有独立 `.git`，`git remote -v` 为空，角色标记为 `work`，`scripts/check-workspace-zone.sh work` 通过。
- 发布区角色标记为 `release`，`main` 跟踪 `origin/main`，规范 fetch／push URL 和发布角色检查通过；现有目录名是规则生效前的 legacy bootstrap 例外，脚本会明确警告。
- 当前聊天仍附着在发布区；后续日常实现、实验和本地 commit 必须在日常区进行。
- 不静默移除现有 remote，不用分支或 `git worktree` 冒充双区。

## 当前缺口与阻塞

- 组员学号、全名、GitHub 账户和贡献安排未登记。
- 课程要求四名组员；组信息与仓库表单的提交回执未登记。
- 独立 `Presentation Instruction` 尚未取得或核实。
- 所选论文、论文版本、目标表／图／主张尚未决定。
- 起始代码、精确 commit、许可证、修改范围尚未登记。
- 技术栈、构建命令、环境、硬件、内核、workload 和输入尚未确定。
- 比较指标、运行次数之外的统计细节、成功判据、资源预算、安全隔离和停止条件尚未冻结。
- 当前没有本轮 commit、push 或 `v1.0` 标签授权；日常区中的治理变更仍未提交。

## 下一步

1. 由用户确认论文和真实组员身份。
2. 后续任务切换到已核验的日常区，并在每轮开始重新运行角色检查。
3. 取得并核实独立 `Presentation Instruction` 和组信息表单回执。
4. 将论文、主张、来源代码和实验边界写入下一连续协议版本及其版本档案。
5. 先做来源／许可／成本审计，再请求并执行有界构建与可行性检查。
6. 临近每周日 23:59 检查时，明确提醒用户决定是否授权本周有意义变更的发布；不得自动 push。
