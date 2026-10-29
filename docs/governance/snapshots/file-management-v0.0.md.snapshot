# OS-project 文件管理规范

| 字段 | 当前值 |
| --- | --- |
| `controlled_object_id` | `FILE_MANAGEMENT` |
| `exact_version` | `v0.0` |
| `status` | `draft` |
| `document_role` | `current_policy` |
| `created_at` | `2026-10-30 (Asia/Shanghai)` |
| `last_verified_at` | `2026-10-30 (Asia/Shanghai)` |
| `applies_to` | 日常开发区内的项目文件、目录、生成物与运行记录，以及发布区同步边界 |
| `approval_state` | 已授权建立初始规则；尚未冻结为 v1.0 |
| `freeze_state` | `not_frozen` |
| `supersedes` | `none` |
| `next_allowed_version` | `v0.1` |
| `major_version_authorization` | `absent` |
| `governing_rule` | `AGENTS.md` 1.0 |
| `archive_ref` | [`FILE_MANAGEMENT_VERSION_ARCHIVE.md#v00`](FILE_MANAGEMENT_VERSION_ARCHIVE.md#v00) |
| `source_of_authority` | 用户于 2026-10-30 要求参照既有仓库规则建立本项目制度；`docs/DECISIONS.md` D-005 |

“正式规范”是文档职责，不表示本版已经冻结或验证为最终版本。本规范不授权下载、构建、实验、commit、push 或标签。

## 1 目的、范围与优先级

本规范确定文件的唯一职责、规范位置、命名、生命周期、版本、Git 跟踪、运行证据和双工作区发布边界。

优先级依次为：用户最新明确指令、`AGENTS.md`、有效协议与决策、本规范、具体实验计划、一般目录惯例。实质冲突时停止相关写入，记录冲突并请求决定。本规范不替代课程要求、实验协议、资源预算、许可证或安全边界。

## 2 单一事实来源

| 信息 | 唯一当前事实来源 | 其他文件的处理方式 |
| --- | --- | --- |
| 持续执行规则 | `AGENTS.md` | 只引用，不复制完整规则 |
| 当前阶段、产物、阻塞、下一步 | `docs/PROJECT_STATE.md` | README 只给摘要和链接 |
| 当前论文、主张和协议入口 | `docs/PROTOCOL.md` | 实验计划引用精确版本 |
| 有效决定与修订依据 | `docs/DECISIONS.md` | 新决定取代旧决定但不删除历史 |
| 文件治理 | 本文件 | `AGENTS.md` 只保留强制入口 |
| 跨会话承接 | `docs/HANDOFF.md` | 不把聊天记忆当事实来源 |
| 具体实验计划 | `experiments/<experiment-id>/PLAN.md` | 配置和 run 引用精确版本 |
| 实际运行证据 | `runs/<run-id>/` | 报告和汇总必须反向引用 run ID |

不得创建 `status-final.md`、`latest-protocol.md`、第二份运行事实表或其他影子来源。

## 3 顶层结构与职责

```text
docs/                         全局状态、协议、决策、交接与治理
experiments/<experiment-id>/  单项实验的方案、版本档案与说明
config/                       无凭据、可执行、版本化配置
src/                          本项目正式实现
scripts/                      构建、获取、运行、验证与报告入口
tests/                        单元、集成、边界与小型公开 fixture
workloads/                    workload 清单、获取脚本与小型公开输入
third_party/                  获许可且确需入库的第三方 notices 或 patch
runs/<run-id>/                追加式运行证据；只跟踪允许公开的小型内容
results/                      从已验证 run 提升的机器可读汇总
report/                       最终报告源文件、图表入口和允许发布的 PDF
presentation/                 展示源文件与允许发布的导出文件
archive/<retirement-id>/      已退役路线的只读历史包
scratch/                      本地临时内容；不得作为唯一证据
```

目录按真实需要创建，不批量制造空目录，不用 `.gitkeep` 假装实现存在。当前仓库只有治理阶段所需入口；结构示例不证明代码、实验或结果已经存在。

## 4 文件落位

| 文件类型 | 规范位置 | 约束 |
| --- | --- | --- |
| 治理与状态 | `docs/`、`docs/governance/` | 固定职责，不建同义副本 |
| 正式实验计划 | `experiments/<experiment-id>/` | `PLAN.md` 与 `VERSION_ARCHIVE.md` 物理分离 |
| 配置 | `config/` | 不含凭据、私密 URL 或个人绝对路径 |
| 正式代码 | `src/` | 清晰模块化，不把 notebook 当正式入口 |
| 自动化入口 | `scripts/` | 参数化、可重复、无硬编码个人路径 |
| 测试 | `tests/` | 使用合成或明确可公开的小型 fixture |
| workload 元数据 | `workloads/` | 来源、版本、许可、获取脚本与哈希 |
| 大型／受限输入 | 日常区本地受控位置 | 默认忽略，只在清单中记录逻辑路径和哈希 |
| 运行证据 | `runs/<run-id>/` | 追加式；小型日志和指标可跟踪，大型二进制忽略 |
| 机器结果 | `results/` | 只从已验证 run 提升，保留 run ID |
| 报告／展示 | `report/`、`presentation/` | 保存源文件和生成入口，导出物按交付需要跟踪 |
| 历史 | `archive/<retirement-id>/` | 清单完整后只读，不作为当前入口 |
| 临时文件 | `scratch/`、`tmp/` | 可清理，不得成为唯一证据 |

当前课程任务书的历史文件名含空格和 `(1)`。它是规则生效前的输入例外；不得静默重命名、移动、删除或自动发布。是否登记为公开资产应另行核对许可与用途。新文件必须遵守本规范命名。

## 5 命名与标识

- 新路径使用 ASCII，不使用空格、中文路径、尾随句点或仅大小写不同的名称。
- 人类可读目录和 ID 使用小写 kebab-case；代码标识按所选语言惯例。
- 固定治理文档使用既有大写文件名；第三方原始文件保留官方名称与版本。
- 主张 ID：`claim-<三位序号>`；实验 ID：`exp-<三位序号>`。
- 运行 ID：`run-<UTC时间>-<experiment-id>-a<两位尝试号>`。
- 退役包 ID：`YYYY-MM-DD-<kebab-case-scope>`。
- Git commit、外部版本、随机种子、run ID 和数据哈希保持自身标识，不用 `vN.x` 替代。
- 内部受控对象版本连续使用 `vN.0`、`vN.1`；`vN.9` 后是 `vN.10`。
- 禁止新文件名使用 `latest`、`final`、`new`、`old`、`copy`、`final2`、`最新版` 或系统自动后缀 `(1)`。

## 6 生命周期与冲突

| 类别 | 例子 | 写入规则 |
| --- | --- | --- |
| 不可变 | 原始来源、终态 run、冻结配置、历史快照 | 目标存在即失败；变化用新 ID／版本 |
| 受控更新 | 当前协议、正式计划、治理规范、正式代码 | 更新须有决定或版本依据并保留恢复路径 |
| 追加式 | 决策、版本档案、运行索引 | 不删除旧条目；错误用勘误修正 |
| 可再生 | 构建产物、派生指标、生成图表 | 由版本化代码和配置重建；不作为唯一来源 |
| 历史归档 | `archive/<retirement-id>/` | 清单后只读；恢复通过新决定和新提交 |
| 临时 | `scratch/`、`tmp/`、缓存、`.partial` | 可清理；不进入完成证据 |

创建前按大小写不敏感语义检查完整路径。目标存在时：哈希相同则复用；合法修订使用下一连续版本；不同来源使用新的来源版本；无法解释的碰撞立即停止，不自动加后缀。大文件先写 `.partial` 或临时路径，校验后再原子改名。

删除不可变或受控文件须有明确授权、精确目标和恢复方式。优先归档，不用 `git clean`、破坏性 reset 或清理命令掩盖失败和不利结果。归档内如保存旧规则，必须改名为 `AGENTS-<version>.md.snapshot`，不得留下会被误加载的活动 `AGENTS.md`。

## 7 受控对象与版本档案

- 正文与版本档案是两个文件，使用相同 `controlled_object_id` 和 `exact_version` 并双向链接。
- 正文只保存当前执行、验证和裁决所需内容；讨论、替代方案、历史差异和结果暴露进入档案。
- 档案按版本追加，记录依据、已知结果、影响、迁移、受影响运行、重跑和主版本授权。
- 档案条目保存正文 SHA-256，以及 Git commit、不可变快照或运行快照中的至少一种恢复路径。首次未提交版本可用正文哈希和不可变快照，获准提交后补充 commit。
- `.md.snapshot` 是正文在原路径语义下的逐字节恢复副本，其中的 `current_*` 角色名与相对链接仅用于还原原文，不是快照目录中的活动入口；读取快照前须遵守 `snapshots/README.md`。
- 一个对象升版不自动推动其他对象；没有用户明确许可，不得进入下一主版本。
- 状态与版本分离。`draft`、`frozen`、`complete` 或 `retired` 不由版本号推断。

## 8 来源、许可与大文件

- 每项第三方论文、代码、工具、数据、workload 或 trace 记录来源、官方版本／commit、获取日期、逻辑路径、字节数、SHA-256、许可、访问状态和用途。
- 原始输入只读，派生物由版本化代码和配置生成。网页入口不等于已经下载或可以再分发。
- 第三方代码须保留许可证与归属；修改以清晰 patch、fork commit 或修改文件清单追踪。
- 凭据、令牌、私钥、认证缓存、个人绝对路径和未获许可材料不得跟踪。
- 单个文件不得超过 50 MB。磁盘镜像、VM 镜像、core dump、大型 trace、构建产物和大型 benchmark 输入默认只保存在本地，通过哈希、来源和生成命令引用。

## 9 运行记录与报告数字

每个实质运行使用唯一 `runs/<run-id>/`，最低结构按需要采用：

```text
runs/<run-id>/
  run-manifest.json
  config/
  provenance/
  logs/
  raw-outputs/
  metrics/
  validation/
  decision/
```

运行终态后锁定；续跑创建新 ID 并记录 `resumed_from`。小型文本日志、manifest、逐次指标、原始输出和统计入口应跟踪，使报告每个数字可追溯。只有明确放入 `large-artifacts/` 或 `large-traces/` 的大型内容被忽略，并须跟踪其哈希和说明。报告和图表必须引用 run ID，不得手工修改原始 run 来迎合结论。

## 10 Git 跟踪边界

默认跟踪规则、状态、协议、决策、计划、代码、测试、无密配置、构建／运行脚本、锁文件、小型公开 fixture、来源清单、小型日志、逐次指标、统计脚本和允许公开的报告。

默认忽略缓存、虚拟环境、构建产物、临时文件、本机配置、凭据、磁盘／VM 镜像、core dump、大型 trace、下载内容和大型运行二进制。`.gitignore` 只是防护之一；发布前还须用 `git ls-files` 检查已跟踪内容。

commit message 必须包含实际成员学号和全名。未知身份时不创建 commit。构建产物、纯空白／拼写提交和伪造时间的提交不用于满足周检。

## 11 双工作区与公开边界

- 日常工作只在 `<workspace-parent>/OS-project-local`，该仓库不得配置 remote。
- `<workspace-parent>/OS-project` 是独立发布克隆，预期 `origin` 指向 `SAKANA2336/OS-project`，默认只读。
- 两区必须各自拥有独立 `.git` 目录和不跟踪的 `.local/workspace-role`；不得用 linked worktree。发布区 `main` 跟踪 `origin/main`，fetch／push URL 均使用规范 HTTPS `.git` 地址。
- 首次 provisioning 按 D-002 的一次性授权，从已核实发布区创建独立 clone，仅在新 clone 移除临时 remote，再按明确治理文件 allowlist 导入 bootstrap 内容并验证；该例外不延伸到后续同步。
- 用户明确授权 push 后，先建立本次发布 allowlist；只同步 allowlist，不镜像整树，不从发布区反向覆盖日常区。
- 普通已提交贡献优先使用经审阅的 `format-patch`／`git am` 或等价 Git 提交迁移保留真实 author；禁止由 AI 或单一成员改写、集中 squash 或重新提交来掩盖个人贡献。
- 发布前实时核对两区根目录、仓库身份、分支、状态、远端前进、diff、绝对路径、凭据、许可、50 MB 上限、禁止产物和适用测试。
- 远端更新需要导入日常区时，先只读审阅发布区的 commit／diff，再按明确 patch 或 allowlist 导入；不得用 pull 或整树复制让日常区重新获得 remote。
- 冲突、无关改动、远端前进或验证失败时停止。禁止 force push、历史重写和自动覆盖。

## 12 验证、例外与迁移

文件治理或发布最低检查：

1. `git rev-parse --show-toplevel` 与工作区角色正确；
2. `git status --short --branch` 和 `git diff` 仅包含获准范围；
3. `git diff --check` 无空白错误；
4. `git check-ignore -v --no-index` 对禁止路径命中、对规则和代码不命中；
5. `git ls-files` 中没有凭据、构建产物、镜像、大型 trace 或其他禁止内容；
6. `.gitattributes`、换行与二进制策略正确；
7. 不存在大小写不敏感重复路径或不合规新文件名；
8. 单文件不超过 50 MB；
9. 正文与版本档案的对象 ID、版本、链接和 SHA-256 一致；
10. 报告数字可从 run ID 追溯到逐次日志、指标和统计入口；
11. 发布区只含本次 allowlist，远端身份正确且没有强制推送；
12. `scripts/check-workspace-zone.sh` 对当前角色通过。

例外须在执行前记录原因、范围、期限、风险、恢复方式和授权来源。迁移优先新增与显式移动，路径移动和内容改写分开核查。当前草案下一合法版本为 `v0.1`。
