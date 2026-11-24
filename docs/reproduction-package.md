# Standalone ASan reproduction package v0.1

[Download the source integration package](../packages/asan-reproduction-source-v0.1.tar.gz) · [SHA-256](../packages/asan-reproduction-source-v0.1.sha256) · [File manifest](../packages/asan-reproduction-source-v0.1.manifest.json)

This source-only handoff contains the English fresh-machine guide, portable configuration template, acquisition and VM preparation scripts, the fixed six-Olden-workload measurement and analysis code, LLVM/Olden notices, frozen plan context, 37 offline tests and small validation records. It has 47 regular archive members (46 manifest entries plus the manifest), is 156224 bytes, and contains no downloaded images, compiled launchers, private local state or credentials.

The target is an Apple Silicon Mac with Python 3.9 or later and Xcode Command Line Tools. The guest uses Ubuntu 24.04.5 LTS/aarch64, Linux 6.8.0-147-generic and Clang/compiler-rt 18.1.3. Full prerequisites, fixed package pins, resource limits, expected output and failure recovery are in the extracted README. Other host platforms are outside this entry point.

## Obtain and inspect

From a checked-out copy of this GitHub repository, verify and extract to a new parent directory. The new temporary parent prevents overwriting an existing work repository.

```sh
(cd packages && shasum -a 256 -c asan-reproduction-source-v0.1.sha256)
replay_parent="$(mktemp -d)"
tar -xzf packages/asan-reproduction-source-v0.1.tar.gz -C "$replay_parent"
cd "$replay_parent/OS-project-local"
```

Read the extracted `README.md`, then initialize its independent, remote-free work zone:

```sh
git init
mkdir -p .local
printf '%s\n' work > .local/workspace-role
bash scripts/check-workspace-zone.sh work
python3 -B -m unittest discover -s tests
python3 -B scripts/asan-reproduce.py --root . check
```

The expected offline test count is 37. The host check does not download inputs or start a VM. It requires normal host memory pressure and at least 20 GiB free storage. An Intel Mac, unsupported framework, missing development tools or unsafe resources causes an explicit stop.

## Prepare and run

Use the extracted README for the exact staged commands: `fetch`, `prepare`, `freeze`, `run` and `verify`. Choose a new session/campaign ID and an explicit resource allowance for your own run. The completed project's earlier approval is not a new operator's permission. The documented main-route example sets a 7200-second cumulative activity ceiling, fetch at most 1800 seconds, preparation at most 900 seconds and main collection at most 3600 seconds. VM limits are two vCPUs, 3 GiB RAM and a 30 GiB per-disk ceiling; measurement has its own tighter process limits. Failed activity remains charged.

Acquisition verifies the pinned Ubuntu inputs and the exact LLVM commit and 222 source-lock entries. Git honors an existing OS/environment proxy only for the child process; it changes no global proxy setting and records no proxy values. `fetch --resume` keeps the same ledger and total budget and rechecks completed inputs. Provisioning builds and signs the local launcher, verifies dependencies and creates a newly hashed base. Freezing binds the actual new assets and source hashes. Never edit the historical configuration snapshot to borrow its activation.

The main campaign creates three new VMs, each with one warmup and five measurements per workload/arm. Successful acceptance has 180 timed observations, 36 warmups, output/reference checks, source/config/environment evidence, normal shutdown and a successful independent `verify`. Source trees, images and binary artifacts remain local. Network-dependent setup time varies; limits are stop conditions, not a promise of completion time.

## Acceptance evidence and scope

The package route was exercised from a new exported work repository and fresh official inputs on an M1 MacBookAir10,1 with 8 GiB RAM on November 25, 2026 (Asia/Shanghai). Three independent new VM batches completed with **2.273131x ± 0.006420x** ASan/baseline wall-clock ratio (sample SD across batches, n=3). The package includes byte-exact per-batch CSVs, statistics, provenance, the activity ledger and an inert configuration snapshot under `results/clean-main-20261125-a02/`. Two-layer raw evidence and CSV statistics were independently rechecked. Original complete raw logs, source snapshots and VM artifacts remain in controlled local storage.

The session ledger used 671.707313 seconds, including failed attempts; acquisition used 135.228419 seconds. Additional independent audit computation is recorded separately. This demonstrates a clean-repository/new-VM route on one host. Another member's cross-machine replay remains pending. It is a modern-toolchain method/direction replication on six Olden workloads, not numerical reproduction of the original SPEC CPU2006 result. Earlier formal results remain separate and unchanged.

The extension workflow is included as code and instructions, but it was not rerun in this clean-main authorization. Any new extension collection needs its own operator-approved scope and remaining budget. This package publication is an incremental handoff; it does not create the final `v1.0` tag.
