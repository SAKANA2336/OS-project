# Recorded Command Files

The JSON files in this directory are copied from the successful local run.

- `logs/`: configure, build, warmup and measurement commands.
- `validation/`: reference-output comparison commands.
- `preflight/`: Docker context, engine and image checks.

Each file contains the exact argv array, timeout, exit code, timeout state and
elapsed time captured by the harness. Host mount arguments are not included;
the machine-specific container argument file remains local-only.

