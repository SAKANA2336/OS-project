# Missing Items and Run Relation

## Items that remain unavailable

The following items cannot be honestly reconstructed from the current files:

1. The licensed SPEC CPU2006 installation package and its official input sets.
2. A direct reproduction of the paper's original hardware, compiler, runtime
   library, allocator and operating-system configuration.
3. Official SPEC CPU2006 scores or a claim that the pilot confirms the paper's
   reported 73% result.
4. Physical-memory-overhead measurements and bug-detection-completeness
   measurements. They were outside this pilot's fixed scope.

These are limitations of the experiment, not omitted records. The package
therefore labels the result `exploratory-workload-transfer` and keeps the
formal claim verdict `inconclusive`.

## Failed earlier attempt

`run-20261114t120405z-exp-001-a01-b8c02c` was the earlier attempt on
2026-11-14 at 12:04:05 UTC. It used the same pinned image and upstream source
commit but ended as a failed/invalid pilot. Its evidence is preserved locally
and its timing data is not used in the successful report.

## Successful replacement run

`run-20261114t130529z-exp-001-a01-ce70aa` started at 13:05:32 UTC and
completed at 13:06:17 UTC. It is a new run ID, not an overwrite of the earlier
attempt. It produced 72 valid records and the published statistics.

## Local-only evidence

The full run directory contains host-specific Docker mount arguments and the
original evidence hash manifest. The local
`container-arguments.local.json` file is intentionally not copied here because
it embeds machine-specific paths. All public files in this package have their
own checksums in `SHA256SUMS.txt`.

