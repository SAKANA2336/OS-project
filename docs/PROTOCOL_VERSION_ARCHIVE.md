# Protocol version archive

Controlled object `project-protocol-index`. The [current protocol](PROTOCOL.md) holds the active index. This archive records decisions, changes, results known at the time, and recovery information for the original versions.

## v0.0

2026-10-30. Initial unfrozen governance index. Established the project requirements and left experiment details pending. The chosen paper was omitted from the initial record and entered during v0.1. The known material at this point was the course brief and repository baseline. No run was affected.

## v0.1

2026-11-07. Recorded the user's 2026-10-30 AddressSanitizer selection, the publication and official source. The experiment design, claims, inputs, toolchain and budget remained pending. This corrected the written record and affected no run. D-009 later authorized publication and recovery notation.

## v0.2

2026-11-08. Adopted the Ubuntu 24.04 and Clang/LLVM 18 preparation route under D-010. Specified functional checks, isolation, preparation limits, and source constraints. An initial pull timed out. Static checks passed and container acceptance was still pending. Future attempts needed new IDs. Formal quantitative plans remained unfrozen.

## v0.3

2026-11-08. Recorded actual x86_64 Ubuntu 24.04.5 and LLVM 18.1.3 acceptance under D-012. Seven checks passed in `env-20261108t013027z-6c0e488a`; two earlier failed attempts were retained. No quantitative result was added and no previous run required repetition.

### Recovery of published v0.0 through v0.3

Use `git show <commit>:docs/governance/snapshots/project-protocol-index-<version>.md.snapshot` and compare the original SHA-256.

| Version | Commit containing the snapshot | SHA-256 |
| --- | --- | --- |
| v0.0 | `74bf5eb7cade99437630753166c38f76735fad1e` | `1b607217eb475910275320e08d9c2445e9dddf1c03c5d9164a92b0a4bf7114f3` |
| v0.1 | `fdedccb0e5df61109aa0e302f1567489dcc43997` | `0fbc16f09648f724b8a4ac551e3afb3d9bddd877b9c29105cae736c6dae17a9f` |
| v0.2 | `2c4a89badee35dd8ae50442894c7a296d2e7eacf` | `5e7e0a9a90bdfb22538eafacf1321313067e0896d3fca2e43b518e621660c722` |
| v0.3 | `2c4a89badee35dd8ae50442894c7a296d2e7eacf` | `984c4c29a21b8a347257518d9cf087d426e148d7b0772b8b7bcb91837fb52381` |

The original published archive is at `84606a8bf3d891bda612f31133e7c683fa664a16:docs/PROTOCOL_VERSION_ARCHIVE.md`. The authority and dates above reflect the decisions at the time. Git recovery records publication of the old bytes independently from those earlier drafting states.

## v0.4

The project briefly had two separate v0.4 texts. The 2026-11-15 daily edition indexed the proposed native ARM64 environment, isolation and budgets under D-016. The separate published edition registered C-001, C-002 and C-003 with their recorded decisions and measurements. D-021 preserved their independent histories. The published text is at `84606a8bf3d891bda612f31133e7c683fa664a16:docs/PROTOCOL.md`, Git blob `7c9b2f486c910f3f1545e2a2c94bfeb12a3302e4`, SHA-256 `c48004aa83f2195a6a86b1d996100f3fa2228257b5770aeb8a61eac1c5d1e9ff`. The published archive stopped at v0.3.

## v0.5

2026-11-15. Updated the ARM64 host launcher after a stopped Swift/SDK attempt. Adopted system Clang and Objective-C with explicit SDK and ad-hoc signature. The same guest checks, isolation and bounds applied. The stopped attempt was retained and the next attempt got a new ID.

## v0.6

2026-11-15. Recorded ARM64 environment acceptance. Kept the earlier setup failures and the successful guest clock correction under D-017 and D-018. Verified seven checks and shutdown in the new run. Retained its execution-time v0.5 references and recorded the results separately.

## v0.7

2026-11-18. Recorded the user-approved reconciliation under D-021. Preserved both v0.4 lineages and imported the original six upstream commits with their authors. Indexed the upstream claim register and pilot. The older aggregate ratios could be recomputed with limits on the raw evidence, and the independent ARM64 environment acceptance remained valid.

## v0.8

2026-11-18. Added the ARM64 Olden pilot proposal and runner adaptation under D-022. The old x86_64 pilot's 357 evidence entries and 72 records had been checked, and the ARM64 environment had passed. The pilot proposal still required separate execution authority.

## v0.9

2026-11-19. Recorded the approved ARM64 pilot attempt under D-023. A first checkout failed the source line-ending check. The retry verified 222 files and accepted 72 sample records, including warmups, with a slowdown geometric mean of 2.086758×. No formal run was changed.

## v0.10

2026-11-19. Corrected a v0.9 sentence that still said no new run had been added. The pilot evidence, its scope and authority remained as recorded in D-023. The correction required no run changes.

## v0.11

2026-11-19. Indexed formal adoption under D-025 and freezing under D-026, before collection. Retained known pilot results and recorded the exact v0.2 experiments, checked dependency base, and the scope of claim-004. Older evidence and verdicts kept their original scopes.

### Recovery of daily v0.4 through v0.11

The daily repository retains the original snapshots at `docs/governance/snapshots/project-protocol-index-<version>.md.snapshot`. The November 22 release includes this English index and the published measurements. The daily snapshots and full local execution record are available from the project custodians.

| Daily version | Original SHA-256 |
| --- | --- |
| v0.4 | `ed569d85ae3f672af77501fc019765cc78bf1f91f2accb6c07d892094316e9a3` |
| v0.5 | `7c98caca9523a7c18f2a530ebbfa069101d3d4e583a2ee977712d0d77984b0eb` |
| v0.6 | `546fa0d72101bfd2b65c6f72f6b5434d5bbc8d8e2d55e7715a883874a95d2dd7` |
| v0.7 | `eb1822014efedc25d984af5214a190cb1bce65911bd86713c41f9fc78e8a63fd` |
| v0.8 | `cef4c7d163957a778129781d5dd41449d79d24479d46e39d0b1bfbfb0c6ab6c8` |
| v0.9 | `c612cb899551a2104ff17be8b10594d274df767a0239d46e50991818c4de9b36` |
| v0.10 | `f1deac626b18f40b47b414695ea85a268cbf571f6a0de57cda5d856f57a00a30` |
| v0.11 | `b6e7f586f83725be77a3e7eabc1b37427e767a1325320f916c6754ba4f3721cf` |

## v0.12

2026-11-22. English active index authorized under D-028. Records the completed formal campaigns under D-027 and links their public offline-reproducible results. Distinguishes the earlier published benchmark series and pilots. Retires current-tree Chinese protocol snapshots in favor of the exact historical recovery records above. This documentation update keeps the original inputs, frozen v0.2 experiment plans and criteria, existing verdicts and run seals. No run is affected or needs repetition.

- Recovery. `docs/PROTOCOL.md` in the Git revision containing this entry.
- Body SHA-256. `2412bce62e1e0a40eba64b764aad818bdc72262583359ff518d509f60c4fbcb9`.
