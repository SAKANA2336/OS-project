# OS-project 交接说明

最后核实：2026-11-07（Asia/Shanghai）

## 当前状态与入口

- 当前阶段：选题已确定，复现方案准备。
- 当前协议：[`project-protocol-index v0.1`](PROTOCOL.md)，`draft_index / not_frozen`。
- 持续规则：[`AGENTS.md`](../AGENTS.md) 1.0。
- 文件治理：[`FILE_MANAGEMENT v0.0`](governance/FILE_MANAGEMENT.md)，草案、未冻结。
- 已建立并核验两个独立 Git 仓库：日常区无 remote，发布区使用规范 `origin` 并跟踪 `origin/main`。日常文档和实现工作在日常区进行。
- 已选论文：方向 8，AddressSanitizer: A Fast Address Sanity Checker（USENIX ATC 2012）；用户于 2026-10-30 确认，2026-11-07 补登记，见 D-007。
- 主张、起始代码、工具链、环境、workload、预算和正式实验计划仍待定。
- 已知成员：张瀚洋，学号 `1240036026`；首次治理基线已提交并发布，见 D-008。其余成员及贡献安排待补充。
- 尚无论文实现的构建、测试、实验 run、结果、报告或复现结论；已有验证仅涉及治理文档和工作区角色。

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
4. 阅读论文及其 artifact，登记一至三个主张、对应表／图、起始 commit、许可和复现尺度。
5. 待用户确认后，将环境、workload、指标、三次以上运行、预算、隔离和停止条件写入下一连续协议版本（v0.2）或独立实验计划。
6. 经用户确认后再开始代码获取、依赖安装和有界可行性检查。

规则、目录和候选方案不是实验完成证据。任何“已复现”声明必须能够追溯到冻结方案、有效运行、原始日志和统计输出。
