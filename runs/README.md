# Run evidence

Use `runs/<run-id>/` for append-only evidence from actual builds, benchmarks, and experiments. Verify execution from the evidence recorded for each run.

The recommended run ID is `run-<UTC-timestamp>-<experiment-id>-a<two-digit-attempt>`.

For each substantive run, retain at least these records.

- `run-manifest.json` records the run ID, status, experiment plan version, code commit or patch, start and end timestamps, and any source run.
- `config/` contains the frozen configuration used for the run.
- `provenance/` records the environment, hardware, operating system, kernel, compiler, dependencies, and input and workload hashes.
- `logs/` contains build and execution commands, stdout, stderr, and small text logs.
- `metrics/` records raw metrics by repetition, units, and inputs to statistical analysis.
- `validation/` contains known-answer tests, boundary checks, and validation outputs.
- `decision/` records the claim verdict, quantified differences, limitations, and whether the run was accepted.

Every reported number must trace back to repository logs. Track small text logs, manifests, per-repetition metrics, raw outputs, and statistical scripts. Store large binary files in ignored `large-artifacts/` or `large-traces/` directories and record their sources, generation commands, byte counts, and SHA-256 hashes in the repository. Keep permissible small evidence such as text traces even when its filename ends in `.trace`.

Once a run succeeds, fails, becomes invalid, stops, or is cancelled, preserve it in place. Give a resumed run a new ID and cite the source using `resumed_from` or `supersedes_run_id`. Retain failures and unfavorable results.
