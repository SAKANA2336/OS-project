# OS-project 交接说明

最后核实：2026-11-08（Asia/Shanghai）

## 当前状态与入口

- 当前阶段：现代基础环境已建成，功能验收通过；正式实验方案准备。
- 当前协议：[`project-protocol-index v0.3`](PROTOCOL.md)，`draft_index / not_frozen`。
- 持续规则：[`AGENTS.md`](../AGENTS.md) 1.0。
- 文件治理：[`FILE_MANAGEMENT v0.0`](governance/FILE_MANAGEMENT.md)，草案、未冻结。
- 独立日常区已恢复且无 remote；PowerShell 角色核验通过，Bash 因 Win32 error 5 无法启动。本次用户已授权发布环境进度，补齐发布副本本机标记后使用 PowerShell 等价检查；范围见 D-013，完成以 Git 证据为准。
- 已选论文：方向 8，AddressSanitizer: A Fast Address Sanity Checker（USENIX ATC 2012）；用户于 2026-10-30 确认，2026-11-07 补登记，见 D-007。
- Ubuntu 24.04 / Linux x86_64 / Clang-LLVM 18 准备路线已采纳，见 D-010；主张、起始代码、workload、正式预算和实验计划仍待定。
- 已知成员：张瀚洋，学号 `1240036026`；首次治理基线已提交并发布，见 D-008。其余成员及贡献安排待补充。
- 用户运行 `env-20261108t013027z-6c0e488a` 已成功构建容器、通过七项真实功能验收；完整小型证据见 `runs/`。实际版本为 Ubuntu 24.04.5、Clang/LLVM/compiler-rt 18.1.3；镜像 ID 和复用方法见协议及交付包。
- 主机代理与用户 Docker 下载路径均已验证可通；助手仍无 named-pipe 权限，后续 Docker 命令仍需用户自己的 PowerShell。两次旧失败保留；尚无正式性能实验或论文主张裁决。

## 双工作区承接

1. 将带 `origin` 的仓库视为 GitHub 发布区，默认只读。
2. 日常区已按 D-002 的一次性 provisioning 建立；每轮仍须确认 `.git` 独立、`git remote -v` 为空，并运行 `scripts/check-workspace-zone.sh work`。
3. 需要发布时，用户明确授权 push；随后列出 commit／文件 allowlist，优先用 Git patch／提交迁移保留真实 author，执行检查后由各实际成员通过 Git CLI 完成其获准发布操作。
4. 冲突、远端前进、身份不符或验证失败时停止；禁止整树覆盖和 force push。

## 课程时间与 Git 边界

- 换题截止：2026-11-01。
- 展示日期：暂定 2026-12-01；详细要求见尚未取得的独立 `Presentation Instruction`。
- GitHub 周检：每周日 23:59；具体时区以课程通知为准。
- 每周至少一个有意义的已推送 commit；迟到只计入下一周，漏周不可补回。
- 每组四名学生；组员信息与复现仓库链接须通过 <https://v.wjx.cn/vm/rZCQLSE.aspx> 提交，当前状态须由实际回执核实。
- commit message 必须包含实际成员学号和全名。没有准确身份时不得创建代表成员的 commit。
- 周检要求不等于自动 push 授权；执行者应及时提醒用户安排发布。

## 下一步与承接条件

1. 补齐其余组员身份、完整贡献安排和表单提交回执；方向 8 已选定，无需再次确认主题。
2. 取得并核实独立 `Presentation Instruction`。
3. 切换到已核验的日常区。
4. 正常使用复用现有已验证镜像，不重复拉取；确需重建时每次产生新 run ID，保留旧证据。
5. 登记一至三个主张、对应表／图、起始 commit、许可、workload 和复现尺度。
6. 在下一连续协议版本（v0.4）或独立实验计划中冻结正式指标、三次以上运行、预算、隔离和停止条件，再执行正式实验。

规则、目录和候选方案不是实验完成证据。任何“已复现”声明必须能够追溯到冻结方案、有效运行、原始日志和统计输出。
