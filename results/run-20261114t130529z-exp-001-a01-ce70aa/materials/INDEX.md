# Pilot Reproduction Handoff Index

This directory is the curated handoff package for:

- Run: `run-20261114t130529z-exp-001-a01-ce70aa`
- Experiment: `exp-001`
- Scope: LLVM Test Suite Olden workload-transfer pilot
- Run date: 2026-11-14 UTC
- Result: 72/72 records valid; pilot completed

This package is not a SPEC CPU2006 reproduction. It transfers the measurement
method to six public LLVM/Olden programs because no licensed SPEC CPU2006
package was available.

## Checklist

| Checklist item | Status | Evidence in this package |
| --- | --- | --- |
| Source, version, commit, license, directory mapping | complete | [sources-and-inputs.md](sources-and-inputs.md), `../../../workloads/llvm-suite-lock.json` |
| Arguments, generated inputs, hashes, reference validation | complete | [sources-and-inputs.md](sources-and-inputs.md), `reference-outputs/`, `../metrics/records.json` |
| Baseline and ASan configure/build/run/validation commands | complete | [commands-and-statistics.md](commands-and-statistics.md), `commands/` |
| CPU, architecture, memory, OS, kernel, Docker, Clang/LLVM/ASan | complete | [environment.md](environment.md), `provenance/` |
| 72 original records | complete | `../metrics/records.json`, `../metrics/samples.csv`, `raw-outputs/` |
| Report generation script and statistical formulas | complete | [commands-and-statistics.md](commands-and-statistics.md), `../../../scripts/llvm-asan.py` |
| Delivery index, limitations, old/new run relation | complete | this file, [missing-items.md](missing-items.md), `run-metadata.public.json` |

## Package map

| Path | Contents |
| --- | --- |
| `../README.md` | Human-readable result summary |
| `../metrics/samples.csv` | 72-row flat record table used by the report |
| `../metrics/summary.json` | Per-benchmark statistics and geometric mean |
| `../metrics/records.json` | Full raw record objects, including warmups and validity fields |
| `sources-and-inputs.md` | Source provenance, workload arguments, reference outputs and licenses |
| `environment.md` | Reproduction environment and isolation settings |
| `commands-and-statistics.md` | Exact command shapes, command evidence, validity rules and formulas |
| `missing-items.md` | Items that cannot be honestly reconstructed from the available materials |
| `run-metadata.public.json` | Machine-readable public run metadata without host mount arguments |
| `commands/` | Recorded configure, build, execution and reference-comparison command JSON files |
| `raw-outputs/` | Captured program stdout and timer summaries for all 72 records |
| `reference-outputs/` | Normalized copies of the six upstream reference outputs |
| `provenance/` | Effective config, isolation check, compiler, OS, package, build-cache, binary and project-source evidence |
| `SHA256SUMS.txt` | SHA-256 checksums for the published package files |

## How to audit

1. Read [sources-and-inputs.md](sources-and-inputs.md) and verify the upstream
   commit and the six benchmark arguments.
2. Read [environment.md](environment.md) and compare the image digest, compiler
   flags, ASan options and container limits.
3. Inspect `commands/logs/` for the exact configure, build and execution argv
   arrays. Inspect `commands/validation/` for the exact `fpcmp` comparisons.
4. Compare `../metrics/records.json` with `raw-outputs/` and the corresponding
   command records.
5. Recompute the report from the project runner:

   ```powershell
   python .\scripts\llvm-asan.py analyze `
     --output .\runs\run-20261114t130529z-exp-001-a01-ce70aa
   ```

   The local run is required for this command because the analyzer verifies the
   original run evidence hashes before writing a report.

## Publication boundary

The complete local run remains under:

`work/OS-project-local/runs/run-20261114t130529z-exp-001-a01-ce70aa/`

This handoff directory is a curated publication package. The local
`container-arguments.local.json` file is intentionally excluded because it
contains machine-specific host mount paths. The original run manifest hashes
that local file, so this package must not be described as a byte-for-byte
publication of the entire local run. The package has its own
`SHA256SUMS.txt` for the files actually delivered here.

