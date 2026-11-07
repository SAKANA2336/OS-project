# OS-project 当前协议与复现索引

| 字段 | 当前值 |
| --- | --- |
| `controlled_object_id` | `project-protocol-index` |
| `exact_version` | `v0.1` |
| `status` | `draft_index` |
| `document_role` | `current_protocol_index` |
| `created_at` | `2026-11-07 (Asia/Shanghai)` |
| `last_verified_at` | `2026-11-07 (Asia/Shanghai)` |
| `approval_state` | 方向 8 选题已确认；本次授权补登记状态；实验方案仍待确认 |
| `freeze_state` | `not_frozen` |
| `supersedes` | `v0.0` |
| `next_allowed_version` | `v0.2` |
| `major_version_authorization` | `absent` |
| `archive_ref` | [`PROTOCOL_VERSION_ARCHIVE.md#v01`](PROTOCOL_VERSION_ARCHIVE.md#v01) |
| `source_of_authority` | 用户于 2026-10-30 确认方向 8，并于 2026-11-07 要求更新正确状态；`docs/DECISIONS.md` D-007；课程任务书 |

本文件是当前复现协议的唯一项目级入口。它索引已采纳的论文、主张和实验边界；不把课程清单、候选论文或目录模板冒充已选择方案。

## 当前复现对象

| 项目 | 当前值 | 状态 |
| --- | --- | --- |
| 所选论文 | 方向 8：AddressSanitizer: A Fast Address Sanity Checker | 用户已于 2026-10-30 确认 |
| 论文版本／发表时间 | USENIX ATC '12 会议发表版本，2012 年 6 月 | 官方书目信息已核对 |
| 主张及对应表／图 | 待定 | 未登记 |
| 起始代码仓库／commit | 待定 | 未登记 |
| 许可证 | 待定 | 未核实 |
| 复现尺度 | 待定 | 未决定 |
| 扩展实验问题 | 待定 | 未决定 |

## 已确认论文与来源

Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitry Vyukov. *AddressSanitizer: A Fast Address Sanity Checker*. USENIX Annual Technical Conference (ATC '12), 2012.

- 官方入口：[USENIX 论文页面](https://www.usenix.org/conference/atc12/addresssanitizer-fast-address-sanity-checker)。
- 正文入口：[USENIX 会议论文 PDF](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf)。
- 选题确认日期：2026-10-30；补登记日期：2026-11-07，见 [D-007](DECISIONS.md#d-007-方向-8-选题确认补登记)。
- 来源状态：已核对官方书目信息；本次只登记引用与公开入口，未将论文 PDF 作为仓库资产入库。资产获取记录、字节数、SHA-256 和使用／再分发许可在获取与入库前另行核实登记。

方向 8 是已采纳的复现主题。历史／现代工具链路线、具体主张、benchmark、测量指标、资源预算和扩展方案均未采纳；先前讨论的推荐选项不构成正式协议。

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

进入实现前应在后续连续版本中补齐：

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

论文主题及会议发表版本已登记。主张、代码、环境、硬件、内核、编译器、workload、输入、复现尺度、指标细节、成功阈值、统计方案、扩展条件、预算和运行入口仍未冻结。未知项保持“待定”，不得用默认值填充后称为已采纳协议。

本版本补登记已确认选题并保留实验待定项，不授权代码下载、构建、实验或发布，也不产生任何复现结论。
