# Runtime impact of 32 B and 64 B ASan heap redzones

Campaign `exp-002-v0-2-20261118t170938z` ran under frozen protocol v0.2 on November 19, 2026 (UTC+08:00). All three batches completed. The published data contain 180 timed observations and 36 warmup observations. The ratio is 64 B divided by 32 B heap redzone wall-clock time. Each pair uses the same ASan-instrumented program binary.

The equal-weight six-program ratio was **1.079945x ± 0.003477x** across three batches. Each batch ratio was greater than 1, meeting the local `supported` criterion.

| Program | Mean runtime ratio | Sample SD across batches |
| --- | ---: | ---: |
| `bisort` | 1.066332x | 0.010808x |
| `em3d` | 0.991305x | 0.019238x |
| `mst` | 0.999294x | 0.011803x |
| `perimeter` | 1.105898x | 0.026029x |
| `treeadd` | 1.075118x | 0.031249x |
| `tsp` | 1.241720x | 0.003330x |

The geometric mean sensitivity result was 1.076756x ± 0.002996x. The preplanned arithmetic mean excluding `mst` was 1.096075x ± 0.005992x. The primary result includes all six programs.

The 64 B setting increased the six-program mean runtime by 7.99% in this setup. Two program-level mean ratios were slightly below 1. The experiment measures runtime. Memory consumption and detection effects remain outside its scope.

## Evidence

| Batch | Run | Suite runtime ratio |
| ---: | --- | ---: |
| 1 | [run-20261118t171710z-exp-002-a01](../arm64-formal-evidence/run-20261118t171710z-exp-002-a01.csv) | 1.077104x |
| 2 | [run-20261118t171927z-exp-002-a02](../arm64-formal-evidence/run-20261118t171927z-exp-002-a02.csv) | 1.078907x |
| 3 | [run-20261118t172144z-exp-002-a03](../arm64-formal-evidence/run-20261118t172144z-exp-002-a03.csv) | 1.083822x |

[Original campaign summary](summary.json) · [Original completion record](completion.json) · [CSV provenance](../arm64-formal-evidence/provenance.json) · [Method and offline verification](../../docs/arm64-formal-results.md)
