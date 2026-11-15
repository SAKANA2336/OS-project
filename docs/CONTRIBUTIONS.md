# 成员与贡献记录

核实日期：2026-11-08（Asia/Shanghai）。

## 已确认身份

| 姓名 | 学号 | GitHub 账号 | 确认依据 |
| --- | --- | --- | --- |
| 张瀚洋 | 1240036026 | 待核实 | 已有成员登记见 D-008 |
| 王博文 | 1240026080 | `wbw374` | 用户直接提供姓名与学号，并明确指定该账号；在原有成员基础上追加 |
| 成昊扬 | 1240026250 | `chenghaoyang733-ctrl` | 用户直接提供姓名与学号，并明确指定该账号；在原有成员基础上追加 |
| 陈卓康 | 1240026110 | `chenzhuokang0429` | 用户于 2026-11-08 确认姓名、学号与该账号的对应关系 |

四名组员身份均已登记。张瀚洋的 GitHub 账号仍待核实；各成员的完整分工安排尚未登记。本文件只说明已确认的贡献，不代替课程组信息表单回执。

## 环境准备贡献

本阶段由上述成员确认现代 ASan 路线，在自己的 PowerShell 中执行容器构建和七项功能验收，并提交环境准备材料及证据供教师检查。脚本、文档整理与日志核对使用了 AI 辅助。

| 可检查内容 | 证据入口 |
| --- | --- |
| Ubuntu 24.04 / Clang-LLVM 18 环境与开发依赖 | [Dockerfile](../outputs/asan-environment/Dockerfile) |
| 下载、构建、隔离配置及运行记录生成 | [setup.ps1](../outputs/asan-environment/setup.ps1) |
| 验收规则与失败路径检查 | [verify.py](../outputs/asan-environment/verify.py)、[单元测试](../outputs/asan-environment/tests/test_verify.py) |
| 三项正常程序检查、四类内存错误诊断，7/7 通过 | [原始汇总](../runs/env-20261108t013027z-6c0e488a/validation/summary.json) |
| 完整包版本、编译输出和逐项诊断 | [成功运行说明](../runs/env-20261108t013027z-6c0e488a/README.md) |
| 首次镜像下载失败与助手引擎访问失败 | [下载失败记录](../runs/env-20261108t005237z-5e6fe72f/README.md)、[权限失败记录](../runs/env-20261108t012755z-7026d8b6/README.md) |
| 重建步骤、限制与本地镜像复用 | [环境使用说明](../outputs/asan-environment/README.md) |

原始环境材料发布于提交 `2c4a89badee35dd8ae50442894c7a296d2e7eacf`。本阶段完成的是环境搭建与功能验收，尚无论文性能测量或正式主张裁决。

## 成昊扬的环境重建贡献

成昊扬（1240026250）于 2026-11-08 在本机完成 Docker Desktop 与 WSL2 安装、国内镜像加速配置，排查了主机加速器代理干扰问题，并重新完成环境构建与七项功能验收（run ID `env-20261108t125852z-c0c3afe7`，`PASS: 7/7 functional checks`）。本次为独立本机复验，原始环境材料与验收证据仍以既有发布内容为准。

## 成昊扬的性能与内存实验贡献

成昊扬（1240026250）于 2026-11-15 完成性能主张 C-001 与内存主张 C-002 的正式实验：用 LLVM test-suite 的 6 个 benchmark（经教师邮件授权替代 SPEC CPU2006）测量 ASan 的运行时间开销（平均 slowdown 2.22x）与内存开销（平均内存增长 2.58x），裁决均为 `partially_supported`。主张记录见 [CLAIMS.md](CLAIMS.md)，原始证据见 [runs/bench-20261114t171000z/](../runs/bench-20261114t171000z/README.md) 与 [runs/bench-mem-20261115t033100z/](../runs/bench-mem-20261115t033100z/README.md)。

## 提交身份更正

上述原始提交的作者与提交者姓名为张瀚洋，但邮箱使用了仓库所有者 `SAKANA2336` 的 noreply 地址；实际推送使用的是本机已登录的 `wbw374` 账号。提交元数据与推送登录账号需要分别核对，不能以仓库所属账号判断成员贡献。

用户指定以 `wbw374` 为提交身份。提交采用本机已有 Git 配置中的 `wbw374` 姓名及邮箱，作者和提交者均使用该身份；标题包含本次提交成员的学号和全名。王博文的成员登记追加在张瀚洋原有记录之后，不替换张瀚洋的记录、原始验收记录或已发布提交。

Git 配置邮箱在 GitHub 的绑定状态未通过本轮 Git CLI 检查核实；本文件不将登录成功当作邮箱关联已验证的证据。

## 陈卓康的实验方案贡献

陈卓康（1240026110）于 2026-11-08 提出 `claim-001` 至 `claim-003` 三项候选主张与 `exp-001`、`exp-002` 两份实验方案草案，覆盖指标定义、论文与本项目设置逐项对照、workload 替代理由、计时与统计口径、四值裁决判据、资源上限与停止条件。

| 可检查内容 | 证据入口 |
| --- | --- |
| 三项候选主张及论文锚点、设置对照、裁决判据 | [exp-001 方案](../experiments/exp-001/PLAN.md) |
| 扩展实验问题与两模式对照设计 | [exp-002 方案](../experiments/exp-002/PLAN.md) |
| 两份方案的版本档案与正文哈希 | [exp-001 档案](../experiments/exp-001/VERSION_ARCHIVE.md)、[exp-002 档案](../experiments/exp-002/VERSION_ARCHIVE.md) |

本阶段只提交方案与主张提案，**没有运行确认性实验，没有产生 run ID，没有报告数字**。方案第 10 节与 exp-002 第 9 节列出的探索性观察环境为 WSL2 + Ubuntu 22.04 + clang 14，与方案规定的已验证镜像环境不同，不构成任何主张裁决的依据。

主张尚未登记到 `docs/PROTOCOL.md`（v0.3 中仍为“待定”），登记需另立决定并升版；本阶段未修改该受控对象。

## 陈卓康的报告起草贡献

陈卓康（1240026110）于 2026-11-15 起草最终报告正文 `report/report.md`（v0.0 draft），按课程要求组织为 Introduction and Claims、Reproduction Setup、Results、Analysis of Discrepancies、Extension、Conclusion 六节，并附 References、contribution statement 与 AI usage statement。

| 可检查内容 | 证据入口 |
| --- | --- |
| 报告正文（六节 + 参考文献 + 两处声明） | [report.md](../report/report.md) |
| 三个主张与论文表／图锚点 | 报告 Table 1；[CLAIMS.md](CLAIMS.md) |
| 完整偏离表（11 项，含未显式固定的 redzone 与 RSS／VmPeak 指标差异） | 报告 Table 4 |
| 每个报告数字对应的 run 目录 | 报告 Table 8 |
| 尚未完成项（起始代码 commit、基准机 CPU、图表生成、两项受控重跑） | 报告第 10 节 |

报告中的全部数值取自已提交的 `runs/bench-20261114t171000z/`、`runs/bench-mem-20261115t033100z/` 与 `runs/env-20261108t013027z-6c0e488a/`，未手工录入终端数字。第 10 节明确列出待补证据，这些尚未完成，报告不声称已取得。

本阶段未修改任何受控对象（`docs/PROTOCOL.md`、`docs/CLAIMS.md`、`docs/PROJECT_STATE.md`），未运行新实验，未新增 run ID。
