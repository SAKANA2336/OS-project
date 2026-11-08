# exp-001 确认性实验方案：ASan 的开销与内存放大复现

| 字段 | 当前值 |
| --- | --- |
| `controlled_object_id` | `exp-001-plan` |
| `exact_version` | `v0.0` |
| `status` | `draft` |
| `document_role` | `current_experiment_plan` |
| `created_at` | `2026-11-08 (Asia/Shanghai)` |
| `last_verified_at` | `2026-11-08 (Asia/Shanghai)` |
| `applies_to` | `claim-001`、`claim-002`、`claim-003` 的确认性实验 |
| `approval_state` | 未批准；主张与资源预算等待用户决定 |
| `freeze_state` | `not_frozen` |
| `supersedes` | `none` |
| `next_allowed_version` | `v0.1` |
| `major_version_authorization` | `absent` |
| `governing_rule` | `AGENTS.md` 1.0 |
| `archive_ref` | [`VERSION_ARCHIVE.md#v00`](VERSION_ARCHIVE.md#v00) |
| `source_of_authority` | 用户于 2026-11-08 授权“先只推方案和主张” |

本方案是草案，**不授权**运行确认性实验、创建 run、commit 或 push。第 2 节的主张尚未登记到 `docs/PROTOCOL.md`（v0.3 中仍为“待定”）；登记属于受控对象更新，需另立决定并保留版本档案，本方案不自行修改该文件。

## 1 目的与范围

在已通过功能验收的现代工具链环境中，复现论文的三项可核查主张，量化与论文数值的绝对差异和相对差异，并给出 `supported` / `partially_supported` / `not_supported` / `inconclusive` 裁决。

范围限定为**方法复现加定量比较**。原论文基于 2012 年的 LLVM 实现与 SPEC CPU2006，本项目不重建当年编译器，因此不声称复现当年的绝对值；可复现的是指标定义、测量方法和结论方向。

## 2 待检验主张

| ID | 主张 | 论文锚点 | 论文数值 |
| --- | --- | --- | --- |
| `claim-001` | ASan 使峰值内存增长约 3.4 倍 | Table 1「Memory usage with AddressSanitizer (MB)」 | 合计 8171 MB → 24467 MB，3.37x；单程序 1.40x（429.mcf）至 24.55x（453.povray） |
| `claim-002` | ASan 比同类动态工具快约一个数量级 | §4.1 Comparison | Valgrind 20x、Dr. Memory 10x slowdown；ASan 平均 73% |
| `claim-003` | SPEC CPU2006 上平均 slowdown 为 73% | Abstract、Figure 2、§6 | 平均 73%；最差 perlbench 2.60x、xalancbmk 2.67x |

### claim-001 指标与方向

- 指标：峰值虚拟内存 `VmPeak`，取自 `/proc/self/status`，同一输入下未插桩与插桩二进制的比值。
- 方向：插桩后应显著高于 1x，且主要来自堆 redzone 与 shadow 映射。
- 采用 `VmPeak` 而非 RSS 的理由：论文 Table 1 使用的就是虚拟内存峰值，同一指标才可比较。

### claim-002 指标与方向

- 指标：以未插桩 `-O2` 二进制为分母，分别得到 ASan 与 Valgrind Memcheck 的 slowdown，再取二者之比。
- 方向：ASan 应明显快于 Valgrind，量级为个位数倍数。

### claim-003 指标与方向

- 指标：插桩二进制与未插桩二进制的执行时间之比，在同一 workload 集合上聚合。
- **对照基准的选择需明示**：本项目 workload 刻意复刻论文自己点名的最坏情形（malloc 密集 + 1 至 2 字节访问），因此对照值取论文同一情形下的 2.60x–2.67x（perlbench、xalancbmk），而不是 18 个 benchmark 的均值 1.73x。用最坏情形去比平均值属于错配，必须避免。

## 3 论文设置与本项目设置

| 项 | 论文 | 本项目 | 差异理由与预期影响 |
| --- | --- | --- | --- |
| 硬件 | HP Z600，2×Xeon E5620（共 8 核），24 GB | 单台现代桌面 CPU（i9-14900HX，24 核 32 线程，约 32 GB） | 单核性能提升会降低相对开销；核数与内存带宽差异影响内存放大 |
| 操作系统 | 64-bit Linux | Ubuntu 24.04.5 LTS（容器） | 内核版本更高，`vm.mmap_rnd_bits` 默认值不同，见第 4 节 |
| 编译器 | `clang -O2`（2012 年 LLVM） | `clang 18.1.3 -O2` | 十余年插桩优化，预期降低 ASan 相对开销 |
| 堆 redzone | 32 B | 32 B | 一致 |
| quarantine | 0 | 0 | 一致 |
| malloc 栈回溯 | 禁用 | `malloc_context_size=0` | 一致 |
| workload | SPEC CPU2006（18 个） | 自写微基准，可选 PolyBench 对照 | SPEC CPU2006 已停售退役，无法取得授权副本，见第 5 节 |
| 计时口径 | 论文未明确区分 CPU 时间与墙钟 | CPU 时间（user+sys）为主，墙钟并列记录 | 容器宿主存在抢占，墙钟不稳定，见第 6 节 |

## 4 环境

优先复用 `outputs/asan-environment/` 已验证的镜像（Ubuntu 24.04.5、Clang/LLVM 18.1.3、镜像 ID `sha256:d79f3238f8d650516f45e8e4ae1072dfea32d5b9f4f7733fedd7a83ae10c3b77`），以保持与既有环境验收证据同一环境。

若必须重建，按 `AGENTS.md` §7 重新验收并保留新的 run ID，不复用旧 ID。

**已知运行时前置条件**：Linux ≥ 6.5 的 `vm.mmap_rnd_bits` 默认为 32，会与 ASan 固定 shadow 映射冲突，表现为同一二进制间歇性 `SIGSEGV`（退出码 139、无诊断）或静默漏检（退出码 0）。须设为 28 并在 run-manifest 中记录该值。容器共享宿主内核，因此该值在宿主设置。

## 5 workload

原论文使用 SPEC CPU2006，该套件已停售退役，本项目无法取得授权副本，故不能直接复用。

替代方案：自写微基准，刻意复刻论文在 §4 中点名的两个成本属性——「very malloc-intensive」与「a huge number of 1- and 2-byte memory accesses」。理由是这两点正是论文解释 perlbench（2.60x）与 xalancbmk（2.67x）的全部依据；复刻这两点比换一套无关 benchmark 更接近被检验的机制。

替代的代价必须写进报告：单一微基准不能代表 18 个程序的分布，因此 claim-003 只能与论文的同情形子集比较，不能与均值比较。

可选补强：引入 PolyBench 或 PARSEC 的 2 至 3 个程序作为第三方 workload，用于回应「只有自写基准」的质疑。是否纳入取决于第 8 节的资源上限。

## 6 测量与统计

- 每次比较至少 3 次独立重复；报告 `mean ± standard deviation`（`AGENTS.md` §8），中位数作为稳健性旁证并列给出。
- 保存逐次原始数据，不只保存聚合值；报告有效次数、失败次数与离群处理方式。
- 计时边界：以进程内 `clock_gettime(CLOCK_MONOTONIC)` 记录程序自计时区间，同时用 `/usr/bin/time` 记录 `%e %U %S %M`，两者并列。
- **墙钟有效性判据**：若单次运行的 `wall − cpu` 超过 `cpu` 的 10% 且绝对值超过 0.5 s，判该次运行被宿主抢占，不进入统计，并在 run 记录中保留该次数据与判定理由。
- 不使用 CPU 绑核：在容器或 WSL 中绑核会加剧宿主调度饥饿，实测曾出现墙钟 10.39 s 对 CPU 时间 1.37 s 的偏差。

## 7 裁决判据

裁决只使用以下四值（`AGENTS.md` §9）。

| 裁决 | 判据 |
| --- | --- |
| `supported` | 测量值与论文值同方向，且相对差 `\|测量−论文\| / 论文 ≤ 50%` |
| `partially_supported` | 同方向，相对差在 50% 至 200% 之间 |
| `not_supported` | 方向相反，或相对差超过 200% |
| `inconclusive` | 有效重复不足 3 次；或存在无法解释的离群；或环境未通过验收 |

claim-002 的「论文值」取论文隐含比值 `20 / 1.73 ≈ 11.6`（Valgrind slowdown 与 ASan slowdown 之比）。

## 8 资源上限与停止条件

- 单次 run 不超过 10 分钟；本实验总时长不超过 2 小时。
- 仅在容器内运行，不使用特权容器，不修改宿主内核参数以外的系统配置。
- 仓库内单文件不超过 50 MB；构建产物与二进制不入库。
- 出现以下情形立即停止并报告：连续 3 次运行被判无效；环境验收不通过；资源用量超出上限；出现无法归因的崩溃或结果反转。

## 9 无效运行条件

- `wall − cpu` 超过第 6 节阈值（宿主抢占）。
- ASan 二进制以 139 退出且无诊断（`vm.mmap_rnd_bits` 冲突）。
- `/proc/self/status` 不可读，无法取得 `VmPeak`。
- 容器 OOM 或退出码与预期不符。
- 运行中变更了 workload 参数、编译选项或环境变量。

无效运行不原位覆盖，保留原样并新建 run ID 重跑。

## 10 探索阶段的既有观察（不作为裁决依据）

以下数值来自方案拟定前的探索性运行，**环境为 WSL2 + Ubuntu 22.04 + clang 14**，与第 4 节规定的环境不同，因此不构成 claim-001 至 claim-003 的确认性证据，也不得写入报告作为复现结果。列出目的仅为说明方案可行性与预期量级。

| 观测项 | 探索值 | 论文值 |
| --- | --- | --- |
| 峰值内存放大 | 4.36x | 3.37x |
| ASan slowdown | 4.60x | 2.60x–2.67x（同情形） |
| Valgrind slowdown | 32.27x | 20x |
| ASan 相对 Valgrind 快 | 7.0x | 隐含 11.6x |

确认性实验必须在第 4 节环境中重跑，不得直接沿用上表。

## 11 时序说明与事后合理化风险

`AGENTS.md` §4 要求不得把探索后形成的假设倒写为预先主张。本节如实记录时序：

- 探索性运行发生在 2026-11-08，早于本方案与第 7 节判据的拟定。
- 因此第 7 节的容差（50% / 200%）是在已知探索值的情况下选定的，存在事后合理化的风险。
- 处置方式：冻结本方案前，判据须由用户明确确认，或由未参与探索的成员独立复核。若复核认为容差不合理，按 `v0.1` 修订并记录理由，不静默调整。

## 12 非目标

- 不验证 Chromium 十个月发现 300 余个缺陷的部署结论（§4.2）——需要历史代码库与长期模糊测试。
- 不验证 shadow 编码在 Scale 1 至 7 上的泛化（§3.1）——需要重建 LLVM。
- 不给出假阳性率的统计结论（§3.6）——仅在本项目 workload 上做对照检查。
- 不重建 2012 年编译器，不声称复现论文的绝对值。

## 13 待决定事项

1. 是否采纳 `claim-001` 至 `claim-003`，并登记到 `docs/PROTOCOL.md`（需升版至 v0.4 并保留版本档案）。
2. 是否把 PolyBench 或 PARSEC 纳入 workload 集合。
3. 第 7 节容差是否认可，或由独立成员复核。
4. 本轮资源上限（第 8 节）是否批准。
