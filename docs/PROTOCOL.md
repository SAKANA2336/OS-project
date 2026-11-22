# Replication protocol index

| Field | Value |
| --- | --- |
| Controlled object | `project-protocol-index` |
| Version | `v0.12` |
| Status | `active_index` |
| Updated | 2026-11-22 (Asia/Shanghai) |
| Supersedes | Daily protocol `v0.11` |
| Next allowed version | `v0.13` |
| Freeze scope | `exp-001 v0.2` and `exp-002 v0.2`, frozen before collection under D-026 |
| Authority | D-007 for the paper, D-025 and D-026 for formal collection, D-028 for this publication |
| Version history | [Protocol version archive](PROTOCOL_VERSION_ARCHIVE.md) |

## Paper and reproduction scope

Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitry Vyukov. *AddressSanitizer: A Fast Address Sanity Checker*. USENIX Annual Technical Conference, June 2012. [Publication record](https://www.usenix.org/conference/atc12/addresssanitizer-fast-address-sanity-checker) and [paper PDF](https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf).

The paper was selected on 2026-10-30 (course topic 8). The work reproduces the measurement method and checks the direction of the runtime overhead using modern LLVM and six Olden workloads on ARM64. The paper used SPEC CPU2006, different hardware, and a different toolchain. D-023 records the user's confirmation that the instructor approved the LLVM benchmark substitution.

## Frozen formal experiments

| ID | Question and comparison | Endpoint |
| --- | --- | --- |
| `exp-001 v0.2`, `claim-004` | Does ASan increase wall-clock time on the six Olden workloads in the frozen ARM64 environment? Compare ASan and baseline. | Per-program ratio of arm means, equal-weight arithmetic mean across programs, then mean and sample standard deviation across three independent batches. |
| `exp-002 v0.2` | How does increasing the heap redzone from 32 B to 64 B affect wall-clock time? Change only the redzone setting with the same ASan binary and fixed workloads and environment. | 64 B/32 B ratio using the same aggregation and three-batch design. |

Each batch used one warmup and five measured executions per program and arm. Output validation, completion checks, timeout, and isolation requirements were frozen before sampling. The [formal results index](arm64-formal-results.md) records the environment, results, evidence coverage, and exact source plan hashes. The original frozen v0.2 plan bytes remain in sealed local provenance. The English public index describes their executed scope.

The published data support a local directional comparison and a controlled local redzone timing result. The Figure 2 comparison reports the absolute and relative difference as a descriptive comparison. The work did not measure VmPeak in the formal ARM64 campaign.

## Environment checks and pilot evidence

- x86_64 used Ubuntu 24.04.5 and Clang/LLVM/compiler-rt 18.1.3 in Docker Desktop/WSL2. See the [environment package](../outputs/asan-environment/README.md) and [run](../runs/env-20261108t013027z-6c0e488a/README.md).
- ARM64 used an Apple Virtualization guest with Ubuntu 24.04.5, Linux 6.8.0-147-generic, and Clang 18.1.3. The environment run passed the same seven checks, with a separate bounded VM and private validation service. Its evidence and failed predecessors are indexed in [the project status](PROJECT_STATE.md).
- The [earlier x86_64 Olden pilot](../results/run-20261114t130529z-exp-001-a01-ce70aa/README.md) and the ARM64 pilot are exploratory. The frozen campaign uses independent measurements.

## Earlier published claims

| Claim | As recorded upstream | Current evidence limitation |
| --- | --- | --- |
| C-001, Figure 2 | 2.22×, `partially_supported` | The six-row timing summary can be recomputed. The underlying repetitions and complete setup are pending. |
| C-002, Table 1 | 2.58×, `partially_supported` | The six-row ratio can be recomputed. Max RSS and VmPeak measure different quantities, and underlying repetitions are pending. |
| C-003, Abstract and Section 3.6 | `supported` for four error classes | Seven observed checks passed. The measured build used `-O1`, while the original method description says `-O2`. The tests provide evidence for their covered cases. |

See the [historical claim register](CLAIMS.md). These IDs retain their own source, evidence, and scope.

## Course and evidence requirements

The project uses one to three paper-grounded claims, at least three independent runs for each main result, and a single-factor extension. Report mean and standard deviation, absolute and relative deviations, setup differences, and analysis supported by evidence. Each report number must trace to a run record. The final deliverables include an English PDF report, a contribution statement, an AI-use statement, and a presentation governed by the separate course instructions. Course registration needs an actual receipt. The final `v1.0` tag is subject to explicit final-release authorization.
