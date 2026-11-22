# ARM64 Olden timing results

These two campaigns test the runtime behavior of AddressSanitizer (ASan) on six LLVM Olden programs. Both were collected under frozen protocol v0.2 on November 19, 2026 (UTC+08:00). Each experiment completed three independent VM batches of 60 timed and 12 warmup observations.

| Experiment | Comparison | Mean ratio ± sample SD | Evidence |
| --- | --- | ---: | --- |
| Main timing experiment | ASan / baseline | 2.270457x ± 0.015098x | [exp-001](../results/exp-001-v0-2-20261118t170938z/README.md) |
| Heap redzone extension | 64 B / 32 B | 1.079945x ± 0.003477x | [exp-002](../results/exp-002-v0-2-20261118t170938z/README.md) |

All three batch ratios exceeded 1 in each experiment, satisfying the preregistered directional criterion for `supported`. Figure 2 of the original paper reports a 1.73x slowdown. Our main result exceeds that reference by 0.540457x, or 31.24% relative to 1.73x. The paper uses SPEC CPU2006 on x86-64 Xeon hardware with its period compiler and ASan implementation. Our study uses LLVM Olden in an ARM64 VM with a modern toolchain. The paper does not specify the timing boundaries, repetition design, or aggregation formula in comparable detail. The comparison therefore describes the observed difference across the two settings. [USENIX ATC 2012 paper](https://www.usenix.org/conference/atc12/addresssanitizer-fast-address-sanity-checker)

## Method

- Each batch ran in a fresh aarch64 VM on Apple Silicon using Apple Virtualization.framework and the same verified dependency base. The guest used Ubuntu 24.04.5 LTS, Linux 6.8.0-147-generic, and Clang/LLVM and compiler-rt 18.1.3. Each VM had 2 vCPUs and 3 GiB of RAM. Measurement processes were pinned to one guest vCPU and ran serially.
- The six programs are `bisort` (`700000`), `em3d` (`1024 1000 125`), `mst` (`1000`), `perimeter` (`10`), `treeadd` (`22`), and `tsp` (`1024000`). The workload release is LLVM Test Suite `llvmorg-18.1.3`, commit `72a946a42cbce06afef68b2326ff6c3869d09799`. The local source inventory validated 222 files before use. [LLVM Test Suite source](https://github.com/llvm/llvm-test-suite/tree/72a946a42cbce06afef68b2326ff6c3869d09799)
- The main comparison used the same source, inputs, toolchain, and common optimization flags (`-O2`) in both arms. The ASan arm added `-fsanitize=address` during compile and link, used 32 B heap redzones, and disabled quarantine and leak detection. The extension fixed the ASan-instrumented binary per program and batch. The only varied configuration factor was heap redzone size, with `redzone` and `max_redzone` set together to 32 B or 64 B. The extension collected its own 32 B observations.
- For each program and batch, execution included one warmup and five timed repetitions per arm. Program order and which arm ran first varied by a fixed rotation. The wall-clock metric `timeit real` includes program startup, execution, and output. Building and reference-output comparison occurred outside the timed interval. Warmups are excluded from the result.
- For each program and batch, divide the arithmetic mean time of the five numerator observations by that of the five denominator observations. Average the six program ratios equally within each batch. Report the mean and sample standard deviation of the three batch ratios. The geometric mean over all six programs and the arithmetic mean with `mst` excluded are secondary summaries. The short-run flag marks a program with a mean below 0.050 seconds in either arm.

The extension measures the runtime effect of the redzone setting in this environment. Memory use and error-detection effects were outside the measurement scope. The ASan 18.1.3 runtime reports an effective `malloc_context_size` of 1 when the requested value is 0. The same effective value applies to all ASan arms.

## Verify the published results offline

Run this command from the repository root with Python 3.8 or later. It uses the standard library and typically runs in under a second. It checks each published CSV SHA-256, validates the expected observations, and recomputes per-program, per-batch, and campaign statistics against the published summaries.

```sh
python3 scripts/verify-arm64-formal-results.py
```

Expected output:

```text
exp-001: 2.270457x +/- 0.015098x; 3 batches, 180 timed observations, 36 warmups
exp-002: 1.079945x +/- 0.003477x; 3 batches, 180 timed observations, 36 warmups
```

The six CSVs are byte-exact copies of the exported measurement tables. The provenance index maps each copy to its local run ID, original repository-relative path, and SHA-256. The two original `summary.json` and `completion.json` pairs preserve the campaign results and hashes. Their plan, configuration, records, and outer-seal digests identify files in the complete local archive. The public bundle supports recalculation from the published measurements. Full run replay and validation against raw console logs, VM artifacts, reference stdout, and the original frozen plans require the local archive. [CSV provenance](../results/arm64-formal-evidence/provenance.json)
