# Replicating AddressSanitizer: A Fast Address Sanity Checker

| Field | Value |
| --- | --- |
| Controlled object | `report` |
| Version | `v0.1` |
| Status | Draft, pending member review |
| Freeze state | `not_frozen` |
| Updated | 2026-11-22 (Asia/Shanghai) |
| Course | CS340 Research Paper Replication, AY2026–2027 |
| Version archive | [Report revision history](VERSION_ARCHIVE.md) |

## 1. Introduction and claim

AddressSanitizer (ASan) uses compiler instrumentation and a runtime library to detect memory errors in C and C++ programs. The 2012 paper reports mean runtime overhead of 73% on SPEC CPU2006 in Section 4, Figure 2. We reproduce the method by comparing an instrumented build against a baseline build of the same workload. Our frozen claim, `claim-004`, asks whether enabling ASan increases the equally weighted mean wall-clock time ratio across six LLVM Olden programs in three independent ARM64 VM batches. The paper's 1.73× value provides a descriptive reference. [Paper, Section 4 and Figure 2](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf#page=6)

The project records confirmation from a group member that the instructor approved substituting the LLVM test suite for SPEC CPU2006. The formal measurement covers the specified Olden workloads and the deployment described below. Earlier project results for runtime, memory and detection are retained with their evidence limitations in Section 4. [Formal experiment records](../docs/arm64-formal-results.md)

## 2. Reproduction setup

| Setting | Formal measurement |
| --- | --- |
| Hardware and virtualization | Apple Silicon host and Apple Virtualization.framework. Each batch used a fresh native ARM64 VM from the same verified dependency base. |
| Guest | Ubuntu 24.04.5 LTS, Linux 6.8.0-147-generic, 2 vCPUs and 3 GiB RAM. Measurements ran serially on one logical vCPU. |
| Toolchain | Clang and compiler-rt 18.1.3, CMake 3.28.3 and Ninja 1.11.1. Both builds used the same sources, inputs and common compiler options, including `-O2`. The ASan build added address instrumentation at compile and link time. |
| Workload | LLVM Test Suite `llvmorg-18.1.3` at commit `72a946a42cbce06afef68b2326ff6c3869d09799`. Programs were bisort, em3d, mst, perimeter, treeadd and tsp. The 222-entry source lock binds source bytes and reference outputs. |
| ASan configuration | The minimum and maximum heap redzones were both 32 B. Global and thread-local quarantine were disabled. The runtime resolved the requested allocation stack context size of zero to its effective minimum of one. |
| Measurement | Wall-clock seconds from `timeit` include process startup, initialization and program output. Building and reference output validation were outside the timing window. |

Each batch had one warm-up and five measured runs per program and arm. The two arms ran in adjacent pairs with predetermined ordering and program rotation. We divided the mean ASan time by the mean baseline time for each program, averaged the six ratios with equal weights within each batch, and calculated the mean and sample standard deviation across the three batch values. Output comparison against locked references was part of the eligibility checks. [Formal setup, timing and evidence](../docs/arm64-formal-results.md)

## 3. Formal results

Three batches completed, with 180 valid measurements and 36 warm-ups. The main ratio was **2.270457× ± 0.015098×** (mean ± sample standard deviation across batches). The three batch ratios were 2.279290×, 2.279056× and 2.253024×. All exceeded 1.0, satisfying the frozen directional rule for a verdict of `supported`. [Main experiment summary](../results/exp-001-v0-2-20261118t170938z/summary.json)

| Program | ASan / baseline mean ratio | Sample SD across batches |
| --- | ---: | ---: |
| bisort | 1.542140× | 0.004036× |
| em3d | 1.335647× | 0.013812× |
| mst | 1.804131× | 0.038161× |
| perimeter | 2.561974× | 0.006956× |
| treeadd | 4.643152× | 0.063008× |
| tsp | 1.735697× | 0.007598× |

The prespecified geometric mean was 2.061309× ± 0.011018×. The arithmetic mean excluding the short-running mst workload was 2.363722× ± 0.015430×. The primary result includes all six programs. The batch identifiers, individual timing records and checksums are listed in the formal experiment records. [Formal results and batch evidence](../docs/arm64-formal-results.md)

## 4. Analysis of discrepancies

The mean ratio exceeded the paper's 1.73× reference by **0.540457×**, or **31.24%** relative to that reference. Expressed as overhead, the formal measurement was 127.05% and the paper reported 73%, a difference of **54.05 percentage points**. [Measured absolute and relative differences](../results/exp-001-v0-2-20261118t170938z/summary.json)

| Factor | Paper | Formal measurement | Implication |
| --- | --- | --- | --- |
| Workload | SPEC CPU2006 | Six LLVM Olden programs | Each suite gives different weight to program behavior. |
| Platform | 64-bit Linux on a dual Xeon E5620 HP Z600 | Linux in an ARM64 VM on Apple Silicon | Architecture, host resources and virtualization vary together. |
| Compiler and runtime | 2012 ASan implementation and its contemporary toolchain | Clang and compiler-rt 18.1.3 | Instrumentation and runtime behavior may differ between releases. |
| Timing and aggregation | Figure 2 gives an average. The publication leaves repetition, timing boundaries and aggregation detail unspecified. | Process wall time, fixed pairs and an equal-weight mean across program ratios | The published number is a descriptive reference for the new estimates. |

The run design controls the ASan treatment within the formal environment. Differences between the publication and the formal environment varied together, so the available evidence cannot assign the 0.540457× gap to a specific factor. The project did not measure Valgrind or Dr. Memory in these formal batches.

### Earlier results

| Record | Observed result | Evidence limit |
| --- | --- | --- |
| [x86_64 Olden pilot](../results/run-20261114t130529z-exp-001-a01-ce70aa/README.md) | 1.898806× geometric mean ratio | Exploratory result from one x86_64 pilot. The statistic differs from the formal primary arithmetic mean. |
| ARM64 Olden pilot | 2.086758× geometric mean ratio | Exploratory result from one ARM64 pilot. The formal analysis uses fresh batches. |
| [C-001 runtime benchmark](../runs/bench-20261114t171000z/README.md) | 2.22× mean slowdown across six other programs, registered as `partially_supported` | The six published program ratios give a mean of 2.215215×. Individual timings and exact workload revision remain unavailable in the repository, so the reported per-program statistics cannot be independently recomputed. |
| [C-002 memory benchmark](../runs/bench-mem-20261115t033100z/README.md) | 2.58× mean maximum RSS ratio, registered as `partially_supported` | The six published program ratios give a mean of 2.584668×. Individual observations remain unavailable in the repository. Maximum RSS and the paper's peak virtual memory are different quantities, so the two ratios do not support a like-for-like verdict. |
| [C-003 x86_64 functionality](../runs/env-20261108t013027z-6c0e488a/validation/summary.json) | Seven checks passed, including four memory error classes, registered as `supported` | The original build record uses `-O1`, while the earlier method description lists `-O2`. These finite checks support detection on the tested cases. |

The ARM64 environment separately passed seven functional checks. The two environment checks establish behavior on their tested inputs and platforms. The claim that false positives never occur remains beyond the scope of these checks. [ARM64 validation record](../docs/arm64-formal-results.md)

## 5. Extension

The extension asked whether a 64 B heap redzone increases wall-clock time relative to a 32 B heap redzone. Each pair ran the same ASan-instrumented binary and changed the configured minimum and maximum redzone together as one factor. Input, compiler, remaining runtime options and VM settings were held fixed. The three extension batches used fresh VMs and new measurements for both sizes. The primary statistic used the same per-program and per-batch aggregation as the main experiment. [Extension setup and evidence](../docs/arm64-formal-results.md)

Three batches completed, with 180 valid measurements and 36 warm-ups. The mean 64 B / 32 B ratio was **1.079945× ± 0.003477×**, or approximately **7.99%** higher wall-clock time across the six programs. The batch ratios were 1.077104×, 1.078907× and 1.083822×. All exceeded 1.0, satisfying the frozen directional rule for a verdict of `supported`. [Extension summary](../results/exp-002-v0-2-20261118t170938z/summary.json)

| Program | 64 B / 32 B mean ratio | Sample SD across batches |
| --- | ---: | ---: |
| bisort | 1.066332× | 0.010808× |
| em3d | 0.991305× | 0.019238× |
| mst | 0.999294× | 0.011803× |
| perimeter | 1.105898× | 0.026029× |
| treeadd | 1.075118× | 0.031249× |
| tsp | 1.241720× | 0.003330× |

The change varied by workload. Tsp showed the highest mean ratio and two program means were below 1.0. The primary extension result applies to wall-clock time at the two tested settings. Memory consumption and detection behavior were outside the measurements.

## 6. Conclusion

The formal runs reproduce the direction of Figure 2 on the specified Olden workloads with a newer compiler and an ARM64 VM. Enabling ASan increased the mean wall-clock ratio in every batch. The measured 2.270457× and the paper's 1.73× describe different experimental settings. In the extension, increasing the configured heap redzone from 32 B to 64 B raised the equally weighted mean runtime by about 7.99% on the same workload. Both results can be recomputed from their individual timing records.

## References

1. Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitry Vyukov. *AddressSanitizer: A Fast Address Sanity Checker.* USENIX Annual Technical Conference, 2012. [Publication and paper](https://www.usenix.org/conference/atc12/addresssanitizer-fast-address-sanity-checker)
2. LLVM Project. *AddressSanitizer*, Clang 18.1.3. [Documentation at the tagged revision](https://github.com/llvm/llvm-project/blob/llvmorg-18.1.3/clang/docs/AddressSanitizer.rst)
3. LLVM Project. *LLVM Test Suite*, `llvmorg-18.1.3`. [Pinned source revision](https://github.com/llvm/llvm-test-suite/tree/72a946a42cbce06afef68b2326ff6c3869d09799)

## Contributions

| Member | Student ID | Recorded contributions |
| --- | --- | --- |
| 张瀚洋 | 1240036026 | Project governance, dual-workspace setup and validated container environment. |
| 王博文 | 1240026080 | x86_64 LLVM Olden pilot, source and evidence handoff, and member records. |
| 成昊扬 | 1240026250 | Independent environment rebuilding, earlier runtime, memory and functional measurements, and claim registration. |
| 陈卓康 | 1240026110 | Candidate claims, early experiment plans and the original report draft. |

The final contribution statement will record the allocation of work on the ARM64 experiments after member review. [Contribution record](../docs/CONTRIBUTIONS.md)

## AI usage

AI assistance was used in planning, scripts, drafting and evidence analysis. The formal headline statistics were independently recomputed from the six per-batch CSV files during preparation of this draft. Member review and the final AI usage statement are pending.

## Items for final review

- Add figures generated from the formal per-batch data with a reproducible plotting entry point.
- Confirm the contribution and AI usage statements and review the final English PDF before submission.
