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

## C-002：AddressSanitizer 的内存开销

- **主张**：AddressSanitizer 的平均内存开销约为 **3.4x**（Abstract／Introduction 记 3.4x，Table 1 实测总计 **3.37x**）。
- **论文出处**：
  - Abstract／Introduction："**3.4x** increased memory usage"。
  - Section 4 / Table 1："The average memory usage increase is **3.37x**"（总计 8171 → 24467 MB）。
- **复现方法**：
  - benchmark：LLVM test-suite 的 6 个程序（同 C-001，替代 SPEC CPU2006，教师授权）。
  - 指标：最大驻留内存（max RSS，KB），经 `/usr/bin/time -v` 的 `Maximum resident set size` 字段读取。
  - 编译与 ASan 设置：复用 C-001 的两套构建与 `quarantine_size_mb=0`、`malloc_context_size=0`。
  - 测量：每个程序各运行 3 次，报告 `mean ± std`。
- **结果**：

  | benchmark | native mean±std (KB) | ASan mean±std (KB) | ratio |
  | --- | --- | --- | --- |
  | Fhourstones | 6728±39 | 11707±155 | 1.74x |
  | cfrac | 3415±255 | 10003±23 | 2.93x |
  | espresso | 3533±122 | 12639±24 | 3.58x |
  | bh | 6368±136 | 15124±38 | 2.38x |
  | anagram | 3305±60 | 8236±114 | 2.49x |
  | nbench | 3504±205 | 8392±160 | 2.40x |

  **平均内存增长：2.58x**，范围 1.74x ~ 3.58x。
- **与论文对比**：论文 3.37x，本项目 2.58x。绝对差异 -0.79x；相对差异 -23%（以论文 3.37x 为基准，2.58/3.37 ≈ 0.77）。
- **裁决**：`partially_supported`。
  - 支持面：ASan 确带来显著内存开销（2.58x），方向正确、量级接近（均为「约 3 倍」）；malloc 密集程序（espresso 3.58x、cfrac 2.93x）开销更大，与论文规律一致。
  - 未完全支持面：平均 2.58x 低于论文的 3.37x。
- **偏离**：
  1. 指标：本项目用 max RSS（物理内存峰值）；论文用 VmPeak（虚拟内存峰值，含 shadow memory 的虚拟地址映射）。这是本项目比值偏低的一个重要原因。
  2. benchmark：LLVM test-suite 替代 SPEC CPU2006（教师授权）。
  3. 硬件与编译器：现代 CPU + Clang 18 替代论文的 Xeon E5620 + LLVM 3.x。
  4. 排除：MallocBench/perl 与 MallocBench/gawk。
- **可追溯性**：原始结果与测量脚本见 [`runs/bench-mem-20261115t033100z/`](../runs/bench-mem-20261115t033100z/README.md)（`memory_results.csv`、`memory_summary.json`、`memory_bench.py`）。

---

## 未决事项

- 功能检测主张（4 类内存错误）已有环境验收，但尚未提升为正式主张。
- 扩展实验（一次只改一个因素）尚未设计。
