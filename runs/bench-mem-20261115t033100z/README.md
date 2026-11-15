# Run: bench-mem-20261115t033100z — ASan 内存开销测量

- 运行 ID：`bench-mem-20261115t033100z`
- 时间：2026-11-15 11:31（Asia/Shanghai，UTC 2026-11-15 03:31）
- 类型：正式定量实验（内存主张 C-002）
- 执行者：成昊扬（1240026250）
- 环境：Docker Desktop + WSL2，Ubuntu 24.04.5 LTS，Clang/LLVM 18.1.3，Linux x86_64

## 目的

测量 AddressSanitizer 的内存开销，复现论文 Table 1 的「平均 3.37x 内存增长」主张（见 `docs/CLAIMS.md` 的 C-002）。

## 方法

- benchmark：LLVM test-suite 的 6 个程序（与性能主张 C-001 相同，替代 SPEC CPU2006，经课程教师邮件授权）。
- 指标：**最大驻留内存（max RSS，KB）**，通过 `/usr/bin/time -v` 的 `Maximum resident set size` 字段读取。
- 编译：复用 C-001 的 native（`clang-18 -O2`）与 ASan（`clang-18 -O2 -fsanitize=address`）两套构建。
- ASan 运行时：`quarantine_size_mb=0`、`malloc_context_size=0`。
- 测量：每个 benchmark 各运行 3 次，报告 `mean ± std`。

## 结果

| benchmark | native mean±std (KB) | ASan mean±std (KB) | ratio |
| --- | --- | --- | --- |
| Fhourstones | 6728±39 | 11707±155 | 1.74x |
| cfrac | 3415±255 | 10003±23 | 2.93x |
| espresso | 3533±122 | 12639±24 | 3.58x |
| bh | 6368±136 | 15124±38 | 2.38x |
| anagram | 3305±60 | 8236±114 | 2.49x |
| nbench | 3504±205 | 8392±160 | 2.40x |

**平均内存增长：2.58x**，范围 1.74x ~ 3.58x。

## 文件清单

| 文件 | 内容 |
| --- | --- |
| `memory_results.csv` | 每个 benchmark 的 mean±std 和 ratio |
| `memory_summary.json` | 汇总（含原生结果供报告引用） |
| `memory_bench.py` | 内存测量脚本 |

## 偏离说明

1. 指标：本项目用 max RSS（物理内存峰值），论文用 VmPeak（虚拟内存峰值，含 shadow memory 的虚拟地址映射）。这解释了本项目比值（2.58x）低于论文（3.37x）的一部分。
2. benchmark：LLVM test-suite 替代 SPEC CPU2006（教师授权）。
3. 硬件与编译器：现代 CPU + Clang 18 替代论文的 Xeon E5620 + LLVM 3.x。
4. 排除：MallocBench/perl、gawk 因旧代码不兼容而排除。
