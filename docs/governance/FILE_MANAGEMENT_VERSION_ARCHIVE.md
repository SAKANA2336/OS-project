# FILE_MANAGEMENT 版本档案

本文件追加保存 `FILE_MANAGEMENT` 的版本依据、差异、已知结果、影响和恢复信息。当前正文位于 [`FILE_MANAGEMENT.md`](FILE_MANAGEMENT.md)。

## v0.0

- `controlled_object_id`: `FILE_MANAGEMENT`
- `exact_version`: `v0.0`
- 日期：2026-10-30（Asia/Shanghai）
- 状态：`draft / not_frozen`
- 制定依据：用户要求参照 `rare-driver-panel-benchmark` 建立同等规则；`docs/DECISIONS.md` D-005。
- 内容：建立单一事实来源、规范目录、命名、生命周期、受控版本、来源许可、50 MB 上限、追加式 run、小型日志跟踪和双工作区发布边界。
- 修改时已知结果：项目只有远端初始 README、课程任务书和本轮治理文件；无代码、构建、run 或结果。
- 影响：只改变治理与文件边界；不授权外部获取、实验、commit、push 或标签。
- 受影响运行：`none`；重跑：`not_applicable — no runs exist`。
- 正文 SHA-256：`7a15db9beca4abd79488ba4256f4c99d6345f8f1aa9b8c91c6705b299cd6376e`
- 不可变快照：[`snapshots/file-management-v0.0.md.snapshot`](snapshots/file-management-v0.0.md.snapshot)
- Git 恢复：首次获准 commit 后补充 commit；在此之前以正文哈希和不可变快照恢复。
