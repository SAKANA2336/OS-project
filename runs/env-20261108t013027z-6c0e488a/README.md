# Environment Functional Acceptance

This is one environment preparation run, not a confirmatory paper experiment.
The user executed the reviewed setup script in their own PowerShell session.
The assistant verified the shared logs and reports.

- Run ID: `env-20261108t013027z-6c0e488a`.
- Started: `2026-11-08T01:30:27.8662037Z`.
- Finished: `2026-11-08T01:34:51.6810035Z`.
- Outcome: build succeeded and all seven real functional checks passed.
- Environment: Ubuntu 24.04.5 LTS, x86_64, WSL2 kernel
  `6.18.33.2-microsoft-standard-WSL2`, Clang/LLVM 18.1.3.
- Immutable image:
  `sha256:d79f3238f8d650516f45e8e4ae1072dfea32d5b9f4f7733fedd7a83ae10c3b77`.
- Base digest:
  `ubuntu@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852`.

`run-manifest.json` is an unmodified copy of the setup run's `run.json`,
SHA-256 `589c45741c4189d86b80a832fcdce94c6d628ed3ded642f6e84d74a63deeaa08`.
`validation/` preserves the raw compiler, package, resource, compilation and
execution records byte for byte. The five top-level logs are also unmodified.
Host commands containing personal absolute paths remain only in the outer
workspace's original `work/asan-environment/<run-id>/`; they are not promoted.

The entry point and source snapshot are the daily repository's
`outputs/asan-environment/`. Their hashes match the manifest. To rebuild,
run `setup.ps1` in the user's PowerShell; this creates a new run and image.
For repeated use, prefer the existing immutable image ID.

The three valid programs returned `OK 7` with exit 0 and empty stderr. The
four invalid programs returned 86 and the expected ASan category plus source
location. CPU quota, memory limit and PID limit were checked in cgroup v2.
There is no baseline execution of deliberately invalid programs.

The build emitted `InvalidDefaultArgInFrom` because `BASE_IMAGE` has no
default; the setup command supplied the recorded digest and the build
succeeded. This warning did not invalidate compilation or functional checks.

Limits: this is a modern toolchain, apt repositories were not snapshot-pinned,
the kernel is shared with WSL2, and leak/use-after-return checks were disabled
for the smoke tests. No SPEC asset, formal performance measurement, statistical
comparison or paper-claim verdict is included.
