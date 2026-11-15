# Reproduction Environment

## Image and host

| Field | Recorded value |
| --- | --- |
| Container image | `sha256:d79f3238f8d650516f45e8e4ae1072dfea32d5b9f4f7733fedd7a83ae10c3b77` |
| Container OS | Ubuntu 24.04.5 LTS |
| Target architecture | Linux `x86_64` |
| Docker engine | Docker Desktop Linux engine |
| Docker Server | `29.7.2` |
| Kernel | `6.18.33.2-microsoft-standard-WSL2` |
| Python | `3.12.3` |
| Clang | Ubuntu clang `18.1.3` |
| LLVM/ASan runtime | LLVM compiler-rt/AddressSanitizer from the Clang `18.1.3` toolchain |
| CMake | `3.28.3` |
| CPU affinity | logical CPU `0` inside the container |

The host engine reported 32 CPUs and 16,661,561,344 bytes of total engine
memory. The experiment itself used the stricter container limits below.
Captured command output and package versions are in `provenance/`.

## Container limits and isolation

| Setting | Value |
| --- | --- |
| CPU quota | 2 CPUs |
| Memory | `3g` |
| Swap | disabled (`memory-swap` equals memory) |
| PID limit | 128 |
| Temporary filesystem | 768 MiB, executable, `nosuid`, `nodev` |
| Network | disabled |
| Root filesystem | read-only |
| Project and source mounts | read-only |
| User | non-root UID/GID `65534:65534` |
| Linux capabilities | all dropped |
| New privileges | disabled |
| Core dumps | disabled |
| Build parallelism | 2 jobs |

The run checked these isolation properties inside the container before building
and saved the result in `provenance/isolation.json`.

The exact effective JSON configuration used by the successful run is
`provenance/effective-config.json`.

## Compiler and flags

Both arms used the same compiler family and optimization settings:

```text
C compiler:       clang-18
C++ compiler:     clang++-18
C flags:          -O2 -g -fno-omit-frame-pointer -std=gnu89
C++ flags:        -O2 -g -fno-omit-frame-pointer
```

The ASan arm added:

```text
-fsanitize=address
```

to both compile and link flags. CMake Release-specific flags were cleared so
that an implicit `-O3` was not appended. No LTO, PGO, source rewriting or
native CPU tuning was used.

## ASan runtime options

```text
detect_leaks=0:redzone=32:max_redzone=32:quarantine_size_mb=0:thread_local_quarantine_size_kb=0:malloc_context_size=0:detect_stack_use_after_return=0:halt_on_error=1:exitcode=86
```

These are explicit pilot settings. They approximate selected settings discussed
in the paper but are not a reconstruction of the historical allocator,
compiler or operating system.

## Run identity

| Field | Value |
| --- | --- |
| Run ID | `run-20261114t130529z-exp-001-a01-ce70aa` |
| Project commit recorded by runner | `efd70b62899dd633da2b117073d6b3c2b1f026c0` |
| Project state | dirty at run time; the relevant source files were snapshotted and hashed |
| Source commit | `72a946a42cbce06afef68b2326ff6c3869d09799` |
| Records | 72 total: 12 warmups and 60 measurements |
| Validity | 72/72 records valid |

The project commit was dirty because the experiment was being assembled in the
working tree. This is why the run also records hashes and copies of the
relevant project files under `provenance/project/`.

