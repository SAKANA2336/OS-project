# ASan Functional Environment

Status: the user built the container and all seven real functional checks
passed on 2026-11-08 at 09:34:51 Asia/Shanghai. The assistant inspected the
shared evidence. Run ID: `env-20261108t013027z-6c0e488a`.

Validated stack: Ubuntu 24.04.5 LTS, Linux x86_64 under WSL2,
Clang/LLVM/compiler-rt 18.1.3, and working C/C++ development libraries.
See `validated-run.json` and `validation-summary.json` in this delivery.

Run Docker commands from a Windows PowerShell session that can access the
Docker Desktop Linux engine. The kit does not change daemon permissions,
install a proxy, or alter system security settings.

Local checks on 2026-11-08: 14 Python unit tests passed, PowerShell syntax parsed,
and six Windows argument-quoting roundtrips passed. These checks cover the
validator and launcher logic only. Target package installation, C/C++
compilation, and ASan diagnostics were subsequently verified in the successful
container run above.

## Scope

- Selected preparatory environment: Ubuntu 24.04, Linux x86_64, Clang/LLVM 18.
- This is NOT the 2012 toolchain, not a frozen research protocol, and not a
  reproduction of SPEC CPU2006 performance or memory results.
- The user accepted the modern route on 2026-11-08. No SPEC assets are downloaded;
  benchmark selection and formal quantitative claims remain undecided.
- The repository contains setup sources and small validation records. Container
  images, personal configuration and authentication material remain local.
- This progress publication is authorized on 2026-11-08; it does not designate
  a final report or `v1.0` release.

## Rebuild From A Fresh Checkout

Requirements: Windows PowerShell 5.1 or newer, Docker Desktop running with
Linux x86_64 containers, the `desktop-linux` context, at least 2 CPUs and
3 GiB engine memory, and at least 4 GiB free space for preparation.
The tested host used WSL2; no host Clang installation is required.

From the repository root:

```powershell
& .\outputs\asan-environment\setup.ps1
```

If PowerShell reports that scripts are disabled, the previously used temporary
setting is:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

It applies only to that PowerShell window. Then rerun the setup command.
The script itself never changes execution policy.

Expected terminal result: `PASS: 7/7 functional checks`, an immutable image ID,
and a new evidence directory under `work/asan-environment/`. The first build
downloads Ubuntu and development packages. The validated run took about
4 minutes 24 seconds; network and machine differences affect build time.

The committed `validated-run.json` and `validation-summary.json` describe
the recorded run. A new machine must build its own image. The recorded
image ID is not a publicly downloadable image.

## Reuse The Validated Local Image

On the machine where the recorded run succeeded, the validated image is
already available locally. To open a bounded, offline scratch shell:

```powershell
$imageId = "sha256:d79f3238f8d650516f45e8e4ae1072dfea32d5b9f4f7733fedd7a83ae10c3b77"
$dockerArgs = @(
    "--context", "desktop-linux", "run", "--rm", "-it", "--pull=never",
    "--platform", "linux/amd64", "--network", "none", "--read-only",
    "--user", "65534:65534", "--cap-drop", "ALL",
    "--security-opt", "no-new-privileges", "--cpus", "2",
    "--memory", "2g", "--memory-swap", "2g", "--pids-limit", "128",
    "--ulimit", "core=0",
    "--tmpfs", "/tmp:rw,exec,nosuid,nodev,size=256m,mode=1777",
    "--workdir", "/tmp", "--entrypoint", "/bin/bash", $imageId
)
docker @dockerArgs
```

Scratch files under `/tmp` disappear when this container exits. The shell
command reuses the tested image and isolation flags; the interactive shell
itself has not been executed by the assistant. The included normal C++ case
can be compiled inside it:

```sh
clang++-18 -O1 -g -fno-omit-frame-pointer -fsanitize=address \
    /opt/asan-check/normal.cpp -o /tmp/normal-cpp
ASAN_OPTIONS=detect_leaks=0 /tmp/normal-cpp
```

Expected output: `OK 7`. Use `exit` to return to PowerShell.
For a fresh build and a new complete validation record, execute from the
repository root:

```powershell
& .\outputs\asan-environment\setup.ps1
```

Use `-CheckOnly` for a daemon preflight with no download/build. The script uses
only the existing `desktop-linux` context and verifies its local named-pipe
endpoint. It refuses TCP endpoints and never changes daemon permissions.
The user previously authorized `RemoteSigned` at Process scope for their own
PowerShell window. That setting expires when the window closes. This script
does not change execution policy.

Repository sources live under `outputs/asan-environment/`. During development
they are edited only in the independent, no-remote daily checkout. Publication
uses the separate release checkout under the project's Git rules.

The script pulls Ubuntu, resolves its immutable digest, installs the compiler
and build tools, records the built image ID, and runs seven functional checks:
C baseline, instrumented C, instrumented C++, heap overflow, use-after-free,
stack overflow, and global overflow. Invalid cases run only under ASan.
Success requires the expected exit status, error category, and source location,
not merely a crash or any nonzero exit code.

## Limits And Evidence

Validation: 2 CPU quota, 2 GiB memory, no swap, 128 PIDs, 256 MiB temporary
storage, non-root, read-only root filesystem, no network, no added capabilities,
no published ports, and only this run's evidence directory mounted writable.
The verifier requires and checks cgroup-v2 memory/CPU/PID limits. Core dumps are
disabled. Leak detection is outside this smoke check and is disabled; no ptrace
or privileged container is needed.

Timeouts: pull 5 minutes, build 15 minutes, validation 5 minutes, individual
programs 10 seconds. Package installation has a 10-minute in-container timeout.
Build CPU/memory usage is governed by Docker Desktop settings, NOT by the
validation limits. Allow about 4 GiB of free storage for initial preparation;
the script checks the evidence drive, not Docker's separate virtual disk.
Review Docker Desktop's available storage before starting.

Every attempt gets a new directory under `../../work/asan-environment/`,
including failures. Override it with `-WorkRoot <directory>`. `run.json`
records image IDs and the final state. `validation/` contains compiler/package
versions, source hashes, raw command outputs, and `summary.json`.

The Ubuntu base digest and installed package versions are recorded, but apt
repositories are NOT snapshot-pinned. Rebuilding later is not guaranteed to be
byte-for-byte identical. Preserve the recorded image ID for repeat use; freeze
the complete dependency sources before any formal quantitative experiment.

The script never runs an unbounded benchmark or starts a persistent service.
It removes only its own temporary validation container. The uniquely tagged
image and run evidence remain. On build timeout, the client is terminated;
inspect Docker Desktop for any remaining build before retrying. No global
`docker system prune` or unrelated cleanup is performed.

## Verified Result And Earlier Attempts (2026-11-08)

The user's run `env-20261108t005237z-5e6fe72f` passed the engine checks, then
failed while pulling `ubuntu:24.04` from Docker Hub.

After the user started v2rayN, the system proxy was enabled at
`127.0.0.1:10808`. Python HTTPS checks through this proxy, with certificate
verification enabled, reached the registry (HTTP 401) and authentication
host (HTTP 404 at its root). This establishes a working host proxy route,
not a successful Docker engine pull. Windows curl could establish the
proxy tunnel but its Schannel TLS backend failed to acquire credentials.

The assistant retried the setup: `env-20261108t012755z-7026d8b6` failed at the
engine stage with named-pipe permission denied, before attempting a pull.
The user then ran the script in their own PowerShell window, where engine
access previously succeeded. Docker Desktop was in system proxy mode; its
actual download path was verified by the successful user run.
The two failed run records are preserved in
[`../../runs/env-20261108t005237z-5e6fe72f/`](../../runs/env-20261108t005237z-5e6fe72f/)
and
[`../../runs/env-20261108t012755z-7026d8b6/`](../../runs/env-20261108t012755z-7026d8b6/).
Their host command files remain local because they contain personal paths.

Successful run `env-20261108t013027z-6c0e488a`:

| Check | Result |
| --- | --- |
| Normal C baseline | Passed, exit 0 and `OK 7` |
| Normal C with ASan | Passed, exit 0 and `OK 7` |
| Normal C++ with ASan | Passed, exit 0 and `OK 7` |
| Heap buffer overflow | Passed, exit 86 and expected diagnostic/source |
| Heap use after free | Passed, exit 86 and expected diagnostic/source |
| Stack buffer overflow | Passed, exit 86 and expected diagnostic/source |
| Global buffer overflow | Passed, exit 86 and expected diagnostic/source |

Base: `ubuntu@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852`.
Image: `sha256:d79f3238f8d650516f45e8e4ae1072dfea32d5b9f4f7733fedd7a83ae10c3b77`.
Tag: `os-project-asan:env-20261108t013027z-6c0e488a`.

Measured cgroup-v2 configuration: `memory.max=2147483648`,
`cpu.max=200000 100000`, `pids.max=128`. Reviewed raw logs and JSON reports are
in `../../runs/env-20261108t013027z-6c0e488a/`. The full original local directory
is `../../work/asan-environment/env-20261108t013027z-6c0e488a`.

If an existing proxy is available, start it and use its actual HTTP or mixed
proxy address in Docker Desktop's proxy settings, then retry `setup.ps1`.
An environment variable in a terminal alone does not establish the Desktop
engine's proxy configuration. Do not guess a port or enter a SOCKS-only
address as an HTTP proxy. The script does not change proxy or DNS settings.

The functional acceptance rule has been met. No formal benchmark or paper
claim has been tested; there are no runtime-overhead or memory-overhead results.

## Sources

- LLVM 18 ASan documentation:
  https://releases.llvm.org/18.1.8/tools/clang/docs/AddressSanitizer.html
- Ubuntu Clang 18 package:
  https://packages.ubuntu.com/noble/clang-18
- Docker resource constraints:
  https://docs.docker.com/engine/containers/resource_constraints/
- Docker daemon security:
  https://docs.docker.com/engine/security/
