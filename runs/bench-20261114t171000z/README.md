# Run: bench-20261114t171000z — ASan 运行时间开销测量

- 运行 ID：`bench-20261114t171000z`
- 时间：2026-11-15 01:10（Asia/Shanghai，UTC 2026-11-14 17:10）
- 类型：正式定量实验（性能主张 C-001）
- 执行者：成昊扬（1240026250）
- 环境：Docker Desktop + WSL2，Ubuntu 24.04.5 LTS，Clang/LLVM 18.1.3，Linux x86_64（镜像 `os-project-asan`）

## 目的

测量 AddressSanitizer 在基准程序上的运行时间开销，复现论文「平均 73% slowdown」主张（见 `docs/CLAIMS.md` 的 C-001）。

## 方法

- benchmark：LLVM test-suite 的 6 个程序（替代 SPEC CPU2006，经课程教师邮件授权，见偏离）。
- 编译：
  - native 基线：`clang-18 -O2`
  - ASan：`clang-18 -O2 -fsanitize=address -fno-omit-frame-pointer -Wno-implicit-function-declaration`
- ASan 运行时设置：`quarantine_size_mb=0`、`malloc_context_size=0`（对齐论文）。
- 测量：每个 benchmark 各运行 3 次，记录 `exec_time`，报告 `mean ± standard deviation`。
- 工具：llvm-test-suite 的 lit 框架 + `timeit-target` 计时 + `fpcmp-target` 校验输出。

## 结果

| benchmark | native mean±std (s) | ASan mean±std (s) | slowdown |
| --- | --- | --- | --- |
| Fhourstones | 0.3151±0.0047 | 0.4650±0.0168 | 1.48x |
| cfrac | 0.2545±0.0005 | 1.0656±0.0491 | 4.19x |
| espresso | 0.1463±0.0032 | 0.3338±0.0035 | 2.28x |
| bh | 0.7207±0.0085 | 1.5310±0.0089 | 2.12x |
| anagram | 0.3726±0.0202 | 0.6550±0.0545 | 1.76x |
| nbench | 0.5413±0.0078 | 0.7932±0.0039 | 1.47x |

**平均 slowdown：2.22x（平均开销 122%）**，范围 1.47x ~ 4.19x。

## 文件清单

| 文件 | 内容 |
| --- | --- |
| `slowdown_results.csv` | 每个 benchmark 的 mean±std 和 slowdown |
| `slowdown_summary.json` | 汇总（含原生结果供报告引用） |
| `run_bench.sh` | 复现脚本（编译 + 运行 + 分析） |
| `analyze.py` | 结果分析脚本 |

## 偏离说明

1. benchmark：LLVM test-suite 替代 SPEC CPU2006（教师邮件授权，2026-11-14）。
2. 硬件：现代多核 CPU 替代论文的 HP Z600（Xeon E5620）。
3. 编译器：Clang 18.1.3 替代论文的 LLVM 3.x。
4. 排除：MallocBench/perl、MallocBench/gawk 因 1990 年代旧代码（隐式函数声明）与现代 clang 不兼容而排除。
