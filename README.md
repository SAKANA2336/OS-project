# OS-project

This CS340 research paper replication studies *AddressSanitizer: A Fast Address Sanity Checker* (USENIX ATC 2012). The project checks memory-error diagnostics with a modern toolchain, measures the direction of the runtime overhead reported in Figure 2, and evaluates one change to the ASan heap redzone setting.

## Results

| Experiment | Result |
| --- | --- |
| x86_64 and ARM64 environment acceptance | Seven functional checks passed on each platform. The x86_64 container evidence is in the [validation run](runs/env-20261108t013027z-6c0e488a/README.md). |
| ARM64 Olden runtime overhead | ASan took **2.270457× ± 0.015098×** the baseline wall-clock time. The paper reports 1.73× on a different benchmark suite and platform. |
| ARM64 Olden heap redzone extension | A 64-byte redzone took **1.079945× ± 0.003477×** the wall-clock time of a 32-byte redzone. |

Each formal ARM64 experiment used three independent batches, with 180 valid measurements and 36 warmups. Ratios are reported as the mean and sample standard deviation across batches. See the [methods, results, and evidence index](docs/arm64-formal-results.md) and the [draft report](report/report.md).

From the repository root, verify and recompute the formal results with Python 3:

```sh
python3 scripts/verify-arm64-formal-results.py
```

## Replay the main experiment from a clean environment

The [standalone reproduction package v0.1](docs/reproduction-package.md) contains the full source workflow, fixed-input metadata, licenses, tests and a fresh-machine guide for Apple Silicon/ARM64 Linux VMs. [Download the archive](packages/asan-reproduction-source-v0.1.tar.gz) and verify its [SHA-256](packages/asan-reproduction-source-v0.1.sha256) before extracting into a new work directory.

The clean-main acceptance completed three new VM batches with 180 timed observations and 36 warmups; its independent validation result was 2.273131x ± 0.006420x (batch sample SD, n=3). This is a separate workflow validation; the formal results above are unchanged. Follow the package guide for setup, resource allowances, collection and verification.

## Rebuild the x86_64 functional-check environment

On Windows, start Docker Desktop with Linux containers enabled, then run this in PowerShell from the repository root:

```powershell
& .\outputs\asan-environment\setup.ps1
```

A successful run prints `PASS: 7/7 functional checks`, the image ID, and the evidence directory. Initial setup downloads the base image and dependencies. The [environment guide](outputs/asan-environment/README.md) lists requirements, time limits, and failure recovery. The [validation run](runs/env-20261108t013027z-6c0e488a/README.md) records the verified image, package versions, and output.

## Presentation materials

The [archived module materials](presentation/README.md) provide the reviewed methodology and main-result figures, paired English speaker-note PDFs, sources and integrity records. The integrated deck remains in progress.

## Project records

- [Current status](docs/PROJECT_STATE.md) and [handoff](docs/HANDOFF.md)
- [Protocol](docs/PROTOCOL.md), [decisions](docs/DECISIONS.md), and [earlier claim register](docs/CLAIMS.md)
- [Member contributions](docs/CONTRIBUTIONS.md)
- [Workspace rules](AGENTS.md), [file management](docs/governance/FILE_MANAGEMENT.md), and [run conventions](runs/README.md)

Development takes place in the independent `<workspace-parent>/OS-project-local` repository, which has no remote. The independent release repository tracks GitHub and is used for explicitly authorized publication. Use `scripts/check-workspace-zone.sh` to verify the active repository's role.

The course requires four members, a [group and repository registration](https://v.wjx.cn/vm/rZCQLSE.aspx), and an English final report in PDF. The GitHub review is scheduled for Sundays at 23:59, subject to the course's time-zone guidance. The tentative presentation date is December 1, 2026. The separate presentation instructions and form receipt still need verification. The final release uses the `v1.0` tag after the final deliverables are reviewed and approved.
