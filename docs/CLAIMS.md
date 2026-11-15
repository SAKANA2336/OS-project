# 主张记录（Claims）

本文件登记已采纳、已执行并已有实验数据支撑的论文复现主张。每个主张须关联论文中的具体表／图／数值，报告 `mean ± standard deviation`，并给出裁决与偏离说明。

最后核实：2026-11-15（Asia/Shanghai）。

---

## C-001：AddressSanitizer 的平均运行时间开销

- **主张**：AddressSanitizer 在基准程序上的平均运行时间开销约为 **73%**（平均 slowdown 1.73x），远低于 Valgrind（20x）与 Dr. Memory（10x），是低开销的内存错误检测器。
- **论文出处**：
  - Abstract："Its average slowdown is just **73%** yet it accurately detects bugs at the point of occurrence."
  - Section 4（Evaluation）："Figure 2 shows that the average slowdown on CPU2006 is **73%**."
- **复现方法**：
  - benchmark：LLVM test-suite 的 6 个程序（Fhourstones、cfrac、espresso、bh、anagram、nbench），替代 SPEC CPU2006（经课程教师谢轩教授邮件授权，见偏离 1）。
  - 编译：native 基线 `clang-18 -O2`；ASan `clang-18 -O2 -fsanitize=address -fno-omit-frame-pointer`。
  - ASan 运行时：`quarantine_size_mb=0`、`malloc_context_size=0`（对齐论文 Section 4 的设置）。
  - 测量：每个程序各运行 3 次，记录 `exec_time`，报告 `mean ± std`。
- **结果**：

  | benchmark | native mean±std (s) | ASan mean±std (s) | slowdown |
  | --- | --- | --- | --- |
  | Fhourstones | 0.3151±0.0047 | 0.4650±0.0168 | 1.48x |
  | cfrac | 0.2545±0.0005 | 1.0656±0.0491 | 4.19x |
  | espresso | 0.1463±0.0032 | 0.3338±0.0035 | 2.28x |
  | bh | 0.7207±0.0085 | 1.5310±0.0089 | 2.12x |
  | anagram | 0.3726±0.0202 | 0.6550±0.0545 | 1.76x |
  | nbench | 0.5413±0.0078 | 0.7932±0.0039 | 1.47x |

  **平均 slowdown：2.22x（平均开销 122%）**，范围 1.47x ~ 4.19x。
- **与论文对比**：论文 1.73x（73%），本项目 2.22x（122%）。绝对差异 +0.49x；相对差异 +28%（以论文 1.73x 为基准，2.22/1.73 ≈ 1.28）。
- **裁决**：`partially_supported`。
  - 支持面：ASan 确为低开销检测器（本项目 2.22x 远低于 Valgrind 的 20x、Dr. Memory 的 10x）；且内存/分配密集程序开销更大、纯计算程序开销更小，这一规律与论文一致（论文中 perlbench、xalancbmk 最慢）。
  - 未完全支持面：平均数值 2.22x 高于论文的 1.73x。
- **偏离**：
  1. benchmark：LLVM test-suite 替代 SPEC CPU2006（教师邮件授权，须在 GitHub/展示/报告中说明）。
  2. 硬件：现代多核 CPU + Docker/WSL2 替代论文的 HP Z600（2×Intel Xeon E5620，24GB RAM，原生 Linux）。
  3. 编译器：Clang 18.1.3 替代论文的 LLVM 3.x。
  4. 排除：MallocBench/perl 与 MallocBench/gawk 因 1990 年代旧代码（隐式函数声明）与现代 clang 不兼容而排除。
- **可追溯性**：原始结果与复现脚本见 [`runs/bench-20261114t171000z/`](../runs/bench-20261114t171000z/README.md)（`slowdown_results.csv`、`slowdown_summary.json`、`run_bench.sh`、`analyze.py`）。

---

## 未决事项

- 内存开销主张（论文 Table 1，平均 3.37x）尚未开展测量。
- 功能检测主张（4 类内存错误）已有环境验收，但尚未提升为正式主张。
- 扩展实验（一次只改一个因素）尚未设计。
