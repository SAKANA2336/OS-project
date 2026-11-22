# ASan runtime overhead on ARM64 Olden

Campaign `exp-001-v0-2-20261118t170938z` ran under frozen protocol v0.2 on November 19, 2026 (UTC+08:00). All three batches completed. The published data contain 180 timed observations and 36 warmup observations. The ratio is ASan-instrumented wall-clock time divided by baseline wall-clock time.

The equal-weight six-program ratio was **2.270457x ± 0.015098x** across three batches. Each batch ratio was greater than 1, meeting the local `supported` criterion.

| Program | Mean runtime ratio | Sample SD across batches |
| --- | ---: | ---: |
| `bisort` | 1.542140x | 0.004036x |
| `em3d` | 1.335647x | 0.013812x |
| `mst` | 1.804131x | 0.038161x |
| `perimeter` | 2.561974x | 0.006956x |
| `treeadd` | 4.643152x | 0.063008x |
| `tsp` | 1.735697x | 0.007598x |

The geometric mean sensitivity result was 2.061309x ± 0.011018x. The preplanned arithmetic mean excluding `mst` was 2.363722x ± 0.015430x. The primary result includes all six programs.

Figure 2 reports a 1.73x runtime ratio. The observed difference is +0.540457x, or +31.24% relative to the paper's ratio (+54.05 percentage points of runtime overhead). The workload, CPU, virtualization and toolchain differ. The measurements do not identify the effect of any one of those differences.

## Evidence

| Batch | Run | Suite runtime ratio |
| ---: | --- | ---: |
| 1 | [run-20261118t170939z-exp-001-a01](../arm64-formal-evidence/run-20261118t170939z-exp-001-a01.csv) | 2.279290x |
| 2 | [run-20261118t171144z-exp-001-a02](../arm64-formal-evidence/run-20261118t171144z-exp-001-a02.csv) | 2.279056x |
| 3 | [run-20261118t171349z-exp-001-a03](../arm64-formal-evidence/run-20261118t171349z-exp-001-a03.csv) | 2.253024x |

[Original campaign summary](summary.json) · [Original completion record](completion.json) · [CSV provenance](../arm64-formal-evidence/provenance.json) · [Method and offline verification](../../docs/arm64-formal-results.md)
