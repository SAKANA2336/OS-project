# OS-project 当前协议与复现索引

| 字段 | 当前值 |
| --- | --- |
| `controlled_object_id` | `project-protocol-index` |
| `exact_version` | `v0.3` |
| `status` | `draft_index` |
| `document_role` | `current_protocol_index` |
| `created_at` | `2026-11-07 (Asia/Shanghai)` |
| `last_verified_at` | `2026-11-08 (Asia/Shanghai)` |
| `approval_state` | 现代准备环境已通过功能验收；正式定量实验方案未冻结 |
| `freeze_state` | `not_frozen` |
| `supersedes` | `v0.2` |
| `next_allowed_version` | `v0.4` |
| `major_version_authorization` | `absent` |
| `archive_ref` | [`PROTOCOL_VERSION_ARCHIVE.md#v03`](PROTOCOL_VERSION_ARCHIVE.md#v03) |
| `source_of_authority` | 方向 8 选题见 D-007；用户于 2026-11-08 以“按照你的来”接受现代环境准备建议，见 D-010；课程任务书 |

本文件是当前复现协议的唯一项目级入口。它索引已采纳的论文、主张和实验边界；不把课程清单、候选论文或目录模板冒充已选择方案。

## 当前复现对象

| 项目 | 当前值 | 状态 |
| --- | --- | --- |
| 所选论文 | 方向 8：AddressSanitizer: A Fast Address Sanity Checker | 用户已于 2026-10-30 确认 |
| 论文版本／发表时间 | USENIX ATC '12 会议发表版本，2012 年 6 月 | 官方书目信息已核对 |
| 主张及对应表／图 | 待定 | 未登记 |
| 起始代码仓库／commit | 待定 | 未登记 |
| 许可证 | 待定 | 未核实 |
| 复现尺度 | 现代工具链方法复现，先做环境功能检查 | 路线已采纳；主张与定量方案待定 |
| 扩展实验问题 | 待定 | 未决定 |

## 已确认论文与来源

Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitry Vyukov. *AddressSanitizer: A Fast Address Sanity Checker*. USENIX Annual Technical Conference (ATC '12), 2012.

- 官方入口：[USENIX 论文页面](https://www.usenix.org/conference/atc12/addresssanitizer-fast-address-sanity-checker)。
- 正文入口：[USENIX 会议论文 PDF](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)。
- 选题确认日期：2026-10-30；补登记日期：2026-11-07，见 [D-007](DECISIONS.md#d-007-方向-8-选题确认补登记)。
- 来源状态：已核对官方书目信息；本次只登记引用与公开入口，未将论文 PDF 作为仓库资产入库。资产获取记录、字节数、SHA-256 和使用／再分发许可在获取与入库前另行核实登记。

方向 8 是已采纳的复现主题。现代环境准备路线已采纳；具体主张、benchmark、定量测量方案和扩展实验仍未冻结。

## 已采纳的环境准备路线

- 平台：现有 Windows 主机、Docker Desktop Linux 引擎、Linux x86_64；容器用户空间采用 Ubuntu 24.04。
- 工具链：已验证 Ubuntu 24.04.5 LTS、Clang/LLVM/compiler-rt 18.1.3、对应 symbolizer、C/C++ 标准库开发文件、Make/CMake/Ninja、Git、Python 和 GNU time。完整包版本保存在验收运行的 `validation/packages.json`。
- 范围：验证正常 C/C++ 程序，以及堆、栈、全局越界和释放后使用的诊断，共七项检查；这是环境验收，不产生论文主张裁决。
- 验收：七项真实检查全部通过；错误用例必须有预期退出码、ASan 错误类别及源码位置。仅语法检查、Python 单元测试或镜像构建不满足验收。
- 运行隔离：功能检查容器非 root、只读根目录、无网络、无 capabilities、2 CPU quota、2 GiB 内存、无 swap、128 PID、256 MiB tmpfs、关闭 core dump；单程序 10 秒，编译 60 秒，验证阶段 300 秒。
- 准备界限：pull 300 秒、build 900 秒、apt 600 秒；构建资源使用 Docker Desktop 的现有配置，不能把功能检查配额写成构建配额。预计至少需要 4 GiB 可用磁盘；不购买资源，不执行长时间 benchmark。
- 当前入口：本地准备包 `outputs/asan-environment/README.md` 与 `setup.ps1`。这是从此前独立交付包接入日常区的准备产物，暂不作为正式实验代码布局；正式实验入口和运行证据仍须按文件治理登记。
- 证据位置：准备包默认在相邻 `work/asan-environment/` 创建唯一运行目录；旧失败证据保留在外层工作区。正式实验将使用 `runs/<run-id>/`，不得将准备检查提升为正式主结果。
- 偏离：WSL2/Docker 内核、现代 CPU、Ubuntu 和 LLVM 版本均不同于论文环境；不将本路线写成 2012 年工具链复刻或 SPEC CPU2006 数值复现。
- 可重复性限制：基础镜像 digest 和包版本可记录，但 apt 尚未采用快照源；正式定量实验前需固定镜像与完整依赖来源，并确定 benchmark、许可、指标和主张。

环境功能验收已于 2026-11-08 09:34:51（Asia/Shanghai）通过。用户运行 `env-20261108t013027z-6c0e488a` 成功构建镜像，七项真实功能检查全部通过；完整小型证据见 `runs/env-20261108t013027z-6c0e488a/`。基础镜像 digest 为 `ubuntu@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852`，已验证镜像 ID 为 `sha256:d79f3238f8d650516f45e8e4ae1072dfea32d5b9f4f7733fedd7a83ae10c3b77`。这些是环境验收结果，不是论文性能复现结果。

## 课程级固定边界

- 选择课程清单中的一篇论文，测试一至三个与具体表格、图或数值关联的主张。
- 每组四名学生，并通过课程表单提交组员信息和复现仓库链接；提交事实必须由实际回执支持。
- 使用相同指标和尽可能相同的设置比较论文结果与本项目结果；所有偏离逐项记录。
- 主结果至少三次有效运行，报告 `mean ± standard deviation`，且每个报告数字可追溯到仓库日志。
- 每个主张使用 `supported`、`partially_supported`、`not_supported` 或 `inconclusive` 裁决。
- 量化绝对和相对差异；解释必须由受控检查或重跑支持。
- 扩展实验一次只改变一个因素，并尽量固定硬件和 workload。
- 最终报告为英文 PDF，包含贡献声明和 AI 使用声明。
- 最终展示还受独立 `Presentation Instruction` 约束；取得并核实前，其细节保持待定。
- 最终版本标签为 `v1.0`，创建与推送仍需用户明确授权。

## 进入实现前必须建立

进入正式主张实现和确认性实验前，应在后续连续版本中补齐；有界环境准备依上节执行：

1. 已登记论文的资产获取信息与许可；
2. 一至三个主张及论文表／图／数值定位；
3. 起始代码、精确 commit、许可证和修改文件清单；
4. 硬件、OS、内核、编译器、依赖、构建设置和隔离方式；
5. workload／输入／trace 的来源、版本、获取方式、校验值和许可；
6. 原论文设置、本项目设置、偏离表和复现尺度；
7. 主指标、辅助指标、至少三次运行的统计方法和裁决标准；
8. 资源预算、超时、停止条件、运行无效条件和恢复方案；
9. 配置、代码、运行入口、日志、预期产物和报告生成入口；
10. OS 高风险操作是否涉及特权、内核、磁盘、fuzzer、崩溃或网络暴露。

## 当前未冻结事项

论文主题、现代准备路线、实际工具链、包版本、镜像 ID 和七项环境验收已登记。主张、起始代码 commit、workload、输入、定量指标、成功阈值、统计方案、扩展条件、正式资源预算和运行入口仍未冻结。未知项保持“待定”。

本版本登记已授权的依赖准备、容器构建和有界功能检查，不授权正式性能实验、系统代理或 DNS 修改、commit、push 或标签，不产生任何复现结论。
