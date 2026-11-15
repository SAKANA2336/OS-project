# Sources and Inputs

## Upstream source

| Field | Value |
| --- | --- |
| Repository | `https://github.com/llvm/llvm-test-suite.git` |
| Tag | `llvmorg-18.1.3` |
| Commit | `72a946a42cbce06afef68b2326ff6c3869d09799` |
| Acquired material | 222 locked files |
| Selected source root | `MultiSource/Benchmarks/Olden` |
| Source changes | none |

The complete file inventory, byte sizes and SHA-256 values are in
`../../../workloads/llvm-suite-lock.json`. The checkout is sparse and
contains only the build helpers and selected Olden directories needed for this
pilot.

## Workload mapping

| Program | Source directory | Input arguments | Input generation | Reference output |
| --- | --- | --- | --- | --- |
| `bisort` | `MultiSource/Benchmarks/Olden/bisort` | `700000` | generated internally by the program | `bisort.reference_output` |
| `em3d` | `MultiSource/Benchmarks/Olden/em3d` | `1024 1000 125` | generated internally by the program | `em3d.reference_output` |
| `mst` | `MultiSource/Benchmarks/Olden/mst` | `1000` | generated internally by the program | `mst.reference_output` |
| `perimeter` | `MultiSource/Benchmarks/Olden/perimeter` | `10` | generated internally by the program | `perimeter.reference_output` |
| `treeadd` | `MultiSource/Benchmarks/Olden/treeadd` | `22` | generated internally by the program | `treeadd.reference_output` |
| `tsp` | `MultiSource/Benchmarks/Olden/tsp` | `1024000` | generated internally by the program | `tsp.reference_output` |

No external dataset, SPEC input file or generated input file was downloaded.
The programs receive the arguments above and create their working data in
process memory.

The CMake provenance records `TEST_SUITE_RUN_TYPE=train`. The harness invokes
each selected executable directly with the fixed arguments above and compares
its captured output against the corresponding upstream reference output.

## Reference-output hashes

The comparison copy normalizes CRLF to LF only. The original upstream files are
not modified. The hashes below are the normalized reference hashes used by the
run and are also recorded in every record object.

| Program | Normalized reference SHA-256 |
| --- | --- |
| `bisort` | `9dd770c691f91cf76f1612eb1f2b3c2e84bb112cb7e5b047c7c5e8f7303b9531` |
| `em3d` | `0cc3baac5ad11946785dd9eb174e02e4081ce41554b1a47a4c595de2cfe7ca0c` |
| `mst` | `e1ec306bc51c83d5c42d5ee3e6d7d589890f6bb90757a4236b9d95d5dc4b2b39` |
| `perimeter` | `08f3e4915c6ad518dd6bc0bcf02934fc72ee51ffdbc89e354bb04de40b2eee9c` |
| `treeadd` | `02d65395247dc9402770389a761be13e3ef16531abb125d0b2881b7762bfa739` |
| `tsp` | `4a81dfd5f72936284c8bcc87854a6de39b0642d4591da331acfb907ad6e3870b` |

The six normalized reference files are included in `reference-outputs/`.

## License and attribution

The project does not vendor the upstream source. Local acquisition is
documented by:

- `../../../third_party/llvm-test-suite/README.md`
- `../../../third_party/llvm-test-suite/LICENSE.TXT`
- `../../../third_party/llvm-test-suite/OLDEN-LICENSE.TXT`

The additional Olden conditions remain applicable. Public visibility of this
handoff package does not place the upstream source in the public domain.

