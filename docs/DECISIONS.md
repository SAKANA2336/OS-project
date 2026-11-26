# Project decisions

This record summarizes effective decisions and their historical context. Dates use Asia/Shanghai. The original published wording of D-001 through D-015 is recoverable from `84606a8bf3d891bda612f31133e7c683fa664a16:docs/DECISIONS.md`. The original local records for D-016 through D-027 remain with the sealed ARM64 evidence.

## D-001 Establish the project and governance baseline

2026-10-30. Establish the CS340 repository rules and a source-grounded project record. The initial text left the paper selection pending. D-007 records the selection already made on that date.

## D-002 Separate development and release

2026-10-30. Use two independent repositories. The daily repository has no remote. The release repository tracks the canonical GitHub `main` branch and is used for authorized publication. Bootstrap provisioning was a one-time exception for the independent clone and role markers. Verify both repositories with the role script. Use Git CLI for GitHub operations and preserve contribution boundaries.

## D-003 Use the course brief as the source for requirements

2026-10-30. Follow *Research Paper Replication – CS340* for the report, Git review and registration requirements. Original brief SHA-256 is `d129642a953ab1ecd7c27bf67dc667887867ec4045b72917bedaf6b76cc2666c`. Obtain the separate Presentation Instruction before treating any presentation format as confirmed.

## D-004 Preserve authorship and authorize each release

2026-10-30. Each member contributes under their true account and uses the course-required student ID and full name in the commit message. An authorized release preserves original authorship, history and commit boundaries. Weekly checks do not grant standing authorization to publish.

## D-005 Adopt file governance and version records

2026-10-30. Maintain one active entry point per controlled object and a separate append-only version archive. Preserve immutable original inputs and run records. Promote only verified results. [File management](governance/FILE_MANAGEMENT.md)

## D-006 Bound operating-system experiments

2026-10-30. Run tests with crash, resource, or privilege risk in disposable isolated environments with recorded ceilings, timeouts, and recovery. Preserve failures and stop when the agreed isolation or budget fails.

## D-007 Record the paper selection

2026-11-07. Record the user's 2026-10-30 selection of topic 8, *AddressSanitizer: A Fast Address Sanity Checker*. Supersede the initial pending selection and retain its history. Protocol v0.1 recorded the decision. It carried no experiment approval.

## D-008 Record the first governance release

2026-11-07, recording the 2026-10-30 release. 张瀚洋, student ID `1240036026`, was the confirmed member for the first governance publication. Commit `74bf5eb7cade99437630753166c38f76735fad1e` used the verified repository-owner noreply address. Push and matching `ls-remote` were recorded.

## D-009 Publish the paper-selection correction

2026-11-07. Publish the README, status, protocol v0.1, decisions, handoff, protocol archive and its snapshot under the confirmed 张瀚洋 identity. Git commits `fdedccb0e5df61109aa0e302f1567489dcc43997` and `97829cba8257e0a30bcdbb3ea3a890b38b94da05` retain the original change and its recovery supplement.

## D-010 Adopt a modern environment

2026-11-08. Use Ubuntu 24.04 and the LLVM 18 x86_64 toolchain for a bounded functional validation before formal quantitative work. Record the initial image pull timeout in `env-20261108t005237z-5e6fe72f`. Explicitly include the C++ standard-library development dependency. This route studies the method with a modern toolchain.

## D-011 Restore the daily repository on Windows

2026-11-08. A Windows signal-pipe permission error blocked Bash and ordinary clone. Recover the independent repository through a Git bundle from `97829cb` and verify isolation with the PowerShell equivalent of the role check. Place the environment preparation bundle under `outputs/asan-environment/`.

## D-012 Accept the x86_64 environment

2026-11-08. User execution of `env-20261108t013027z-6c0e488a` built the image and passed seven functional checks on Ubuntu 24.04.5 and LLVM 18.1.3. Preserve the earlier pull and named-pipe failures. Reuse the verified image where practical. APT sources were not snapshot-pinned. The run is environment acceptance. [Run and package record](../runs/env-20261108t013027z-6c0e488a/README.md)

## D-013 Publish environment preparation progress

2026-11-08. Publish the environment package, three attempts' allowed evidence, governance entries and PowerShell role check. Verify CRLF and raw log hashes without normalizing the sealed files. Commit `2c4a89badee35dd8ae50442894c7a296d2e7eacf` carried the previously used 张瀚洋 metadata. D-014 and D-015 record the later attribution correction.

## D-014 Record the reported environment attribution

2026-11-08. Record the use of the authenticated GitHub account `wbw374` for the environment publication. The follow-up used the account's Git author metadata and incorrectly retained 张瀚洋's name and student ID in the summary. Preserve the evidence and original commit `7ddc1b083991f02a5bd2fd72de5d55c46e0a96fd`. Its identity mapping was corrected under D-015.

## D-015 Correct the separate member identity

2026-11-08. The user confirmed that `wbw374` belongs to 王博文, student ID `1240026080`. Keep 王博文 and 张瀚洋, student ID `1240036026`, as distinct members. The correction used ordinary commits and retained the original records. [Contribution register](CONTRIBUTIONS.md)

## D-016 Authorize independent ARM64 environment acceptance

2026-11-15. Authorize a bounded native ARM64 VM and seven functional checks. The budget for this acceptance was 90 minutes of cumulative activity and 6 GiB of downloads. Guest resources were capped at two vCPUs, 3 GiB RAM and a 30 GiB sparse disk. Validation used a separate constrained, private service.

## D-017 Repair the ARM64 host launcher

2026-11-15. After the Swift/SDK attempt stopped before VM start, adopt the existing Apple Virtualization backend with the system Clang and Objective-C launcher, explicit SDK, and local ad-hoc signing. Record the failure and use a new attempt. Preserve the environment scope and remaining budget.

## D-018 Correct the guest clock and retry

2026-11-15. The second attempt failed before checks because APT Release metadata was newer than the guest clock. Seed the new guest clock from the host while retaining APT and TLS verification. Use a new attempt and count earlier attempts against the same budget.

## D-019 Record ARM64 environment acceptance

2026-11-15. Run `run-20261114t185606z-env-arm64-001-a03` passed the three normal-program checks and four diagnostic checks and powered off normally. Register the result without changing the plan or protocol used during execution.

## D-020 Verify the sealed ARM64 environment evidence

2026-11-15. Independently check 111 host files, 67 guest evidence entries, and 86 archive-to-file comparisons. The source was recorded with hash verification. The detached signature and APT snapshot limitations remain. Subsequent checks covered the host, receiver, and initialization scripts without changing the completed run.

## D-021 Reconcile upstream history and the daily protocol

2026-11-18. The user approved the merged documents and allowlisted import of six original commits up to `84606a8bf3d891bda612f31133e7c683fa664a16`. Preserve the authors and both v0.4 protocol lineages. Recompute the published Olden pilot and the earlier C-001/C-002 aggregate ratios. Record evidence gaps and keep the two sets of six programs distinct. No experiment authorization followed from the import.

## D-022 Prepare the ARM64 Olden pilot

2026-11-18. Restore agreed workload and runner entries from the archived upstream materials through an explicit allowlist. Prepare an independent ARM64 proposal and keep the execution gate closed pending authorization. Preserve the old handoff and its exact hash chain.

## D-023 Complete one ARM64 Olden pilot

2026-11-18. The user confirmed instructor acceptance of LLVM in place of SPEC CPU2006 and authorized one bounded exploratory run. The first source checkout failed its locked line-endings check. The next attempt verified 222 source files, matched outputs and recorded 60 valid timings and 12 warmups. Pilot `run-20261118t151453z-pilot-arm64-001-a02` returned a 2.086758× geometric mean and powered off normally. Its 2,400-second cumulative and 1,800-second VM caps applied to that pilot.

## D-024 Submit the formal experiment plans for review

2026-11-19. Propose a Figure 2 method study on ARM64 Olden and a same-binary 32 B/64 B redzone extension. Preserve the older access-width proposal as historical. The plan submission was a review step. Existing pilot results were known.

## D-025 Adopt the formal plans and prepare validation

2026-11-19. The user approved proceeding with both proposed experiments. Each campaign had 3,600 seconds of cumulative machine activity and at most four batch attempts. Start the extension after three complete main batches are checked. Preserve the failed dependency-install attempt and use a separately verified dependency base. This approval concerned collection and local verification.

## D-026 Freeze formal collection

2026-11-19, before formal measurement. Freeze exp-001 and exp-002 at v0.2 with exact inputs, fixed environments, timing, workload selection, two arms, sample sizes, verdict rules, and budget. Record the dependency base and its offline preflight. Preserve the execution-time plans and hashes. See the [formal evidence index](arm64-formal-results.md).

## D-027 Seal and audit formal collection

2026-11-19. Both experiments completed three batches, with 180 valid measurements each. The main ratio is 2.270457× and the extension ratio is 1.079945×. The frozen conditions support both directional verdicts. The six original run seals and the report statistics were checked. Retain earlier results and failed attempts as prior evidence.

## D-028 English publication of formal results and project documents

2026-11-22. The user authorized two sequential publications to GitHub main under 张瀚洋, student ID `1240036026`. First publish the English formal results, public per-batch evidence, offline verification and updated draft report. Then update the user's previously published project and governance prose to English. Use English prose in future publications and preserve members' official names as recorded. Retire the standalone Chinese governance and protocol snapshots from the current public tree using exact historical Git recovery references and registered hashes.

The initial review knew of the six completed batches and their local sealed evidence. This decision changes publication and documentation. Frozen methods, original run bytes, recorded verdicts and past attribution are preserved. Public copies carry their own provenance and expose the evidence scope. No new workload run or final release tag is part of this decision.


## D-029 Public reproduction entry and clean-main validation

2026-11-25. The user requested the public reproduction implementation and approved a new main-only clean validation with 7200 seconds total activity, fetch at most 1800 seconds, two vCPUs, 3 GiB RAM and a 30 GiB per-disk ceiling. Preserve the old frozen experiments. The source-only package rebuilds its launcher/base, binds new assets and collects independent new records. Git transport failures, a pre-launch memory-pressure stop and a pre-batch directory initialization repair were retained. Three new VM batches then passed output/environment/two-layer evidence audits and independent CSV recomputation: 2.273130839663948x ± 0.006420217102247743x (sample SD, n=3), 180 timed observations and 36 warmups. The ledger used 671.707312582 seconds, acquisition 135.228418666 seconds; extra independent checks are recorded separately. Source, method, old results and author boundaries are preserved. This acceptance is on one host; another member's cross-machine replay remains pending. No extension was collected.

## D-030 Publish the standalone reproduction package

2026-11-25. The user explicitly requested uploading the required reproduction integration package to GitHub. This authorizes the focused local commit, preserving commit transfer, release integration and ordinary push. Use the latest confirmed submitting member, 张瀚洋, student ID 1240036026, with the previously verified SAKANA2336 noreply identity and cached matching Git credential. Preserve existing members' history.

The publication allowlist is three source-package artifacts under `packages/`, `docs/reproduction-package.md`, and targeted README/status/handoff/decision updates. The small `packages/` location is a scoped handoff-artifact exception to the default layout: source-only archives and integrity metadata, not compiled outputs, VM images or downloaded inputs. It applies to this package and later reviewed revisions; artifacts keep distinct versions and hashes. No whole-tree synchronization or unrelated uncommitted work is included. Complete local VM/raw archives, credentials and original course PDFs remain excluded.

The archive SHA-256 is 11e4321bf3dfc8996e2d2645eb63dcb7dd81436836c2f5532f9e4d72c0aa5af5. The archive carries its own source/file manifest and inert historical context; past activation records grant no new execution authority. Stage this focused commit against the reviewed release baseline using an isolated Git index, leaving the work branch and its existing edits untouched, then transfer the same commit by Git bundle and fast-forward the release repository. This records the integration method, not a new experiment or final-delivery approval. No `v1.0` tag is authorized.


## D-034 Publish archived presentation images and documents

2026-11-26 (Asia/Shanghai). The user explicitly requested uploading the already archived images and documents to GitHub. This authorizes a focused local publication commit, exact commit transfer and ordinary push under the latest confirmed submitting member, 张瀚洋 (1240036026), using the verified SAKANA2336 noreply identity. Preserve other members' contributions and all existing work.

The allowlist is the 46 existing files under `presentation/modules/module-03/` and `presentation/modules/module-04/`, an English presentation README and SHA-256 publication manifest, a byte-preservation attribute, and targeted README/status/handoff/decision updates. Module 3 contains five current PNGs and five-page English notes; module 4 contains two current PNGs and two-page English notes, with already archived earlier table exports and supporting sources/data/reviews/version records retained. Original asset and document bytes are unchanged.

The archive excludes duplicate shared images, unapproved previews, original course/paper PDFs, the private paper translation, local authentication and VM state, and unrelated sensitivity/mst diagnostic work. Historical logical provenance paths and creation-time local-only status remain in immutable records; the public README explains their boundary and the full-local-evidence dependencies of figure generators. Existing scientific protocols, original results and verdicts are unchanged; no experiment or final tag is authorized by this publication.

Stage against the verified release baseline in the independent remote-free work repository using an isolated Git index, preserving its active branch/index and unrelated edits. Transfer the same reviewed commit through a Git bundle and fast-forward release main. Validate archive hashes, module/version records, images/PDFs, existing formal-result recomputation, links, file sizes and tracked-tree privacy before the ordinary push; verify the remote commit afterward.

Publication preflight retained the archived CSV files' original CRLF bytes. Scope `whitespace=cr-at-eol` to the module 4 data CSVs so the whitespace check accepts those recorded line endings while continuing to check other whitespace. No CSV, figure, document or source hash changed.
