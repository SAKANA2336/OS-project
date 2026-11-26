# Project status

Last verified on 2026-11-26 (Asia/Shanghai).

The project replicates the method of *AddressSanitizer: A Fast Address Sanity Checker* (USENIX ATC 2012) with a modern LLVM toolchain. Both formal ARM64 experiments completed under the frozen v0.2 plans. [The protocol](PROTOCOL.md) distinguishes the formal experiments from earlier results and pilot runs.

| Work | Verified outcome |
| --- | --- |
| x86_64 environment | Ubuntu 24.04.5 and Clang/LLVM 18.1.3 under Docker Desktop/WSL2 passed seven functional checks. The successful run and two earlier failed attempts remain under `runs/`. |
| ARM64 environment | Ubuntu 24.04.5, Linux 6.8.0-147-generic, and Clang/LLVM 18.1.3 passed seven checks and shut down normally. Local seal `run-20261114t185606z-env-arm64-001-a03` verified 111 host files. Two earlier attempts stopped or failed before the checks. |
| Olden pilot | Earlier x86_64 pilot had a slowdown geometric mean of 1.898806×. Independent ARM64 pilot `run-20261118t151453z-pilot-arm64-001-a02` had 60 valid measurements, 12 warmups, and a slowdown geometric mean of 2.086758×. Its 829-file host seal verified. Workload, platform, and collection scope limit comparisons across pilot and formal runs. |
| Formal main experiment, `exp-001` | Three batches and 180 valid measurements. ASan/baseline wall-clock ratio **2.270457× ± 0.015098×**. `supported` for the direction of overhead on ARM64 Olden. The comparison with Figure 2 is descriptive. |
| Formal extension, `exp-002` | Three batches and 180 valid measurements. 64 B/32 B heap redzone wall-clock ratio **1.079945× ± 0.003477×**. The predeclared directional criterion was met under the frozen settings. |

The six formal batches were independently rehashed and recomputed. See the [public results and per-batch evidence](arm64-formal-results.md). The original sealed run directories, failed attempts, and execution records remain in controlled local storage.

The historical x86_64 benchmark series registered C-001 (2.22× time), C-002 (2.58× peak RSS), and C-003 (seven functional checks). The first two ratios can be recovered from the published six-row summaries. Missing per-trial records prevent recomputing the original variability. The memory result uses a different metric from the paper's peak virtual memory. For C-003, the recorded compilation used `-O1` while the register says `-O2`. The checks establish the observed behavior for their specific test cases. [Earlier claims](CLAIMS.md)

Four members are documented in [the contribution record](CONTRIBUTIONS.md). The formal results are integrated into the [English report draft](../report/report.md). The final PDF and presentation, final contribution and AI-use statements, course registration receipt, and the separate Presentation Instruction are pending review. No final tag has been approved.

The independent daily and release repositories were verified. Publication decisions, evidence scope, and authorship are recorded in [DECISIONS.md](DECISIONS.md). The [handoff](HANDOFF.md) lists the remaining report and evidence work.


## Standalone reproduction handoff

The [source integration package v0.1](reproduction-package.md) provides a complete fresh-machine acquisition, preparation, collection and verification entry. The published archive has 47 members and a checked SHA-256/file manifest. It passed 37 packaged offline tests and clean-main acceptance on one M1 host: three new VMs, 180 timed observations, 36 warmups, 2.273131x ± 0.006420x. Complete original raw evidence remains local; small recomputable CSVs and provenance are inside the package. Another member's cross-machine verification remains pending. This handoff does not change the earlier formal results or create a final tag.


## Archived presentation modules

The [presentation archive](../presentation/README.md) contains module 3 (five current figures and five-page English notes, index v0.2) and module 4 (two current figures and two-page English notes, index v0.3), with retained earlier exports, bilingual sources, generators and review/version records. All 46 existing module files are byte-identical to the authorized local archives and listed by size/SHA-256 in the publication manifest. Historical local provenance and figure-generator dependencies are explained at the entry. The integrated deck and final presentation approval remain pending. Scientific results and protocols are unchanged. See D-034.
