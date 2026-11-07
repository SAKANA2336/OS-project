# project-protocol-index 版本档案

本文件追加保存 `docs/PROTOCOL.md` 的版本依据、差异、已知结果、影响和恢复信息。正文保存当前有效协议；历史条目不得覆盖或删除。

当前版本：[`project-protocol-index v0.1`](PROTOCOL.md)，`draft_index / not_frozen`。

## v0.0

- `controlled_object_id`: `project-protocol-index`
- `exact_version`: `v0.0`
- 日期：2026-10-30（Asia/Shanghai）
- 状态：`draft_index / not_frozen`
- 制定依据：用户要求参照 `rare-driver-panel-benchmark` 建立相同的项目规则；课程任务书规定的复现与 Git 评估要求。
- 内容：建立论文、主张、起始代码、环境、workload、评价、统计、安全和交付的待定索引；只固定课程任务书明确要求。
- 修改时已知结果：只有课程任务书与空的远端初始 README；未选择论文、未取得代码、未构建或运行实验。
- 影响：建立治理入口；不改变任何实验结果，不授权运行、commit、push 或标签。
- 受影响运行：`none`；重跑：`not_applicable — no runs exist`。
- 正文 SHA-256：`1b607217eb475910275320e08d9c2445e9dddf1c03c5d9164a92b0a4bf7114f3`
- 不可变快照：[`governance/snapshots/project-protocol-index-v0.0.md.snapshot`](governance/snapshots/project-protocol-index-v0.0.md.snapshot)
- Git 恢复：首次获准 commit 后补充 commit；在此之前以正文哈希和不可变快照恢复。

### v0.0 恢复信息补录（2026-11-07）

- 初始治理版本后来已提交于 `74bf5eb7cade99437630753166c38f76735fad1e`；该 commit 的 `docs/PROTOCOL.md` 与上述 v0.0 快照逐字节相同，可作为 Git 恢复来源。
- v0.0 中“未选择论文”仅保留为原始登记内容；用户于 2026-10-30 确认方向 8 的事实当时漏记，由 D-007 和 v0.1 纠正。旧快照与旧哈希保持不变。

## v0.1

- `controlled_object_id`: `project-protocol-index`
- `exact_version`: `v0.1`
- 修订日期：2026-11-07（Asia/Shanghai）；用户选题确认日期：2026-10-30。
- 状态：`draft_index / not_frozen`；取代：`v0.0`；下一合法版本：`v0.2`。
- 制定依据：用户已明确确认方向 8，并要求修正仓库中错误的待定状态；见 `docs/DECISIONS.md` D-007。
- 差异：登记 AddressSanitizer: A Fast Address Sanity Checker（USENIX ATC 2012）、作者、官方论文入口和确认时间；区分主题已选定与实验方案未冻结。
- 修正原因：首次治理发布遗漏选题决定；实验细节暂不确认不撤销已确认选题。本次是补登记，未将修订日期回填为选题日期。
- 备选与废弃内容：当前协议中的“所选论文待定／未选择”描述失效，保留在 v0.0 历史中；历史／现代工具链及其他候选实验建议未被采纳。
- 修改时已知结果：只有治理文件、工作区检查和此前发布记录；尚无论文实验运行或复现结论。
- 影响与迁移：同步 README、PROJECT_STATE、DECISIONS、HANDOFF 和当前协议入口；后续计划引用 v0.1 或其后续版本。主张、代码、环境、workload、指标、预算和扩展方案仍待定。
- 兼容性：不改变课程固定边界、双工作区制度或实验安全要求；仅修正登记与历史状态。
- 授权边界：本地状态更新；无新增代码获取、实验、commit、push 或标签授权；主版本升级授权仍为 `absent`。
- 受影响运行：`none`；重跑：`not_applicable — no runs exist`。
- 正文 SHA-256：`0fbc16f09648f724b8a4ac551e3afb3d9bddd877b9c29105cae736c6dae17a9f`
- 不可变快照：[`governance/snapshots/project-protocol-index-v0.1.md.snapshot`](governance/snapshots/project-protocol-index-v0.1.md.snapshot)
- Git 恢复：本次尚未创建 commit；以正文哈希和不可变快照恢复，后续获准提交后追加 commit 记录。

### v0.1 Git 恢复与发布授权补录（2026-11-07）

- Git 恢复：`fdedccb0e5df61109aa0e302f1567489dcc43997` 中的 `docs/PROTOCOL.md` 与 v0.1 快照一致，使用上述 SHA-256 核验。
- 后续授权：用户在本地修正完成后明确要求 push，见 `docs/DECISIONS.md` D-009；此前条目中的“本地状态更新”是修订当时的授权范围，本次发布已另获授权。
- 本补录只增加恢复依据与发布授权说明，不改变 v0.1 正文、快照、实验待定项或冻结状态。
