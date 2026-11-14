# LLVM / ASan exploratory pilot

This is workload-transfer evidence, not a reproduction of SPEC CPU2006 values.
Wall time includes process startup and program output; units are seconds.
Standard deviation is the sample standard deviation (n-1).
Runtime ratio = mean(ASan) / mean(baseline). No failed sample is a speedup.

| Benchmark | Baseline mean +/- SD | ASan mean +/- SD | Ratio | Status |
| --- | --- | --- | --- | --- |
| bisort | 0.2068 +/- 0.0064 | 0.3722 +/- 0.0310 | 1.800x | valid_pilot |
| em3d | 0.8863 +/- 0.0169 | 1.3316 +/- 0.0287 | 1.503x | valid_pilot |
| mst | 0.0285 +/- 0.0029 | 0.0444 +/- 0.0044 | 1.558x | valid_pilot; short run |
| perimeter | 0.0804 +/- 0.0066 | 0.1595 +/- 0.0090 | 1.983x | valid_pilot |
| treeadd | 0.0937 +/- 0.0055 | 0.3457 +/- 0.0100 | 3.689x | valid_pilot |
| tsp | 0.2317 +/- 0.0229 | 0.3524 +/- 0.0160 | 1.521x | valid_pilot |

Failed, missing, very short or sanitizer-reporting runs require investigation.
No benchmark replacement or outlier removal was applied.
