# Run evidence

`runs/<run-id>/` 保存实际构建、基准和实验的追加式证据。目录存在或本文件存在不代表已经运行实验。

推荐运行 ID：`run-<UTC时间>-<experiment-id>-a<两位尝试号>`。

每个实质运行至少保存：

- `run-manifest.json`：run ID、状态、实验计划版本、代码 commit／patch、开始结束时间和来源 run。
- `config/`：本次使用的冻结配置副本。
- `provenance/`：环境、硬件、OS、内核、编译器、依赖、输入和 workload 哈希。
- `logs/`：构建与运行命令、stdout／stderr 和小型文本日志。
- `metrics/`：每次重复的原始指标、单位和统计输入。
- `validation/`：已知答案测试、边界检查和验证输出。
- `decision/`：主张裁决、差异量化、限制和是否接受该 run。

课程要求报告数字可追溯到仓库日志，因此小型文本日志、manifest、逐次指标、原始输出和统计脚本应提交。大型二进制内容须显式放入被忽略的 `large-artifacts/` 或 `large-traces/`；仓库记录其来源、生成命令、字节数和 SHA-256。不得仅因扩展名为 `.trace` 就忽略可公开的小型关键证据。

运行进入成功、失败、无效、停止或取消终态后不得原位覆盖。续跑创建新 ID 并用 `resumed_from` 或 `supersedes_run_id` 引用来源。失败和不利结果不得删除。
