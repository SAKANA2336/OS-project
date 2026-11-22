# OS-project operating rules

Rules version 1.0, established on 2026-10-30.

Applies to AI assistants and collaborators working on paper replication, system implementation, builds, tests, experiments, analysis, reports, or releases in OS-project.

Read this file before each substantive work session. Read it again after context compaction, a handoff, a change of experiment stage, or a new user instruction. These standing rules apply alongside the selected paper, experiment plans, resource budgets, and authorization for the current task. Limit conclusions to what the evidence supports.

“Must” and “must not” mark requirements. “Should” marks the default, and departures require a recorded reason. These rules apply to OS-project only.

## 0 Separation of work and release repositories

- `<workspace-parent>` denotes a machine-local parent directory. Keep it out of version control. Tracked files use logical paths and workspace roles. Exclude personal absolute paths, Codex project or chat identifiers, and transient Git state.
- Use `<workspace-parent>/OS-project-local` for routine development. By default, code, documents, configuration, builds, tests, experiments, analysis, and local commits belong in this independent Git repository. `git remote -v` must return no entries.
- Use `<workspace-parent>/OS-project` for GitHub releases. Both the fetch and push URLs for `origin` must be exactly `https://github.com/SAKANA2336/OS-project.git`. The release repository is read-only by default. Changes to its worktree, index, commits, branches, or remote state require an explicit user request to push, upload to GitHub, or carry out an equivalent release operation.
- Maintain two independent Git repositories. Branches and linked worktrees share Git metadata or remote configuration and may not serve as substitutes.
- Each repository must have an untracked `.local/workspace-role` marker containing `work` or `release`, as appropriate. The role check must also verify an independent `.git` directory, the canonical repository name, and that the release repository is on `main` and tracks `origin/main`.
- Treat the existing connected directory as the release repository when `origin` is configured. The initial drafting of these rules was a bootstrap exception. Once drafting is complete, routine implementation and experiments in that directory must stop until the independent work repository is established and verified.
- Requests to edit, complete, save, or commit do not authorize a push. The course's weekly requirement does not grant standing or automatic push authorization. Remind the user to decide when a check is approaching.
- At the start of each work session, run `git rev-parse --show-toplevel`, `git status --short --branch`, and `scripts/check-workspace-zone.sh <work|release>`. If the work repository has any remote, stop writes and report it. Leave the remote configured. Stop release operations if the release repository identity or `origin` does not match.
- After an explicit push authorization, fetch the latest remote state and verify both repository identities, branches, upstreams, and status. List the allowed files or commits for the release. Prefer reviewed `format-patch` and `git am` or an equivalent Git commit transfer that preserves the actual author. Use a file-by-file allowlist only for uncommitted bootstrap content. Inspect diffs for credentials, absolute paths, restricted inputs, build products, file size, and existing edits. Run applicable checks. Carry out release commits and pushes only in the release repository.
- Whole-tree mirroring, overwriting the work repository from the release repository, including unauthorized files or old changes, automatically resolving conflicts by overwriting, force-pushing, and rewriting remote history are prohibited. Stop and report remote advancement, conflicts, identity problems, or verification failures.
- Initial provisioning of the two repositories is a one-time exception. Within the user's authorization to set up the repositories, create an independent clone from the verified release repository, remove the temporary remote from the new clone, import uncommitted bootstrap content from an explicit governance-file allowlist, write the `work` marker, and verify the result. The exception permits only these provisioning steps.
- Use the local Git CLI for GitHub retrieval, inspection, comparison, commits, and pushes. If Git cannot complete an operation, report the limitation. Do not bypass this rule with the GitHub API, a browser, a connector, or `gh`.

## 1 Starting and continuing work

1. Verify the workspace role, repository identity, current branch, and existing edits. Keep other projects' files, rules, and uncommitted changes out of this repository.
2. Read this file, `README.md`, `docs/PROJECT_STATE.md`, `docs/PROTOCOL.md`, and `docs/DECISIONS.md` in that order. Also read `docs/governance/FILE_MANAGEMENT.md` before creating, moving, overwriting, archiving, or deleting files. For experiment work, read the applicable plan, configuration, run records, and source manifest.
3. Check the skills available in the current session. For a matching task, explain which skill applies and read the minimum required skill instructions in full, including explicitly required resources. The user's instructions, these rules, the active protocol, resource limits, and evidence boundaries take precedence.
4. Verify the paper, claims, current stage, approved scope, evaluation criteria, resource limits, risk boundaries, and completion conditions for this task. Record missing or undecided items as pending. Common defaults require an actual decision before adoption.
5. Check the artifacts and validation evidence behind earlier completion claims. Plans, example directory structures, expected file names, README descriptions, and unchecked tasks are insufficient evidence of implementation or a passing result.
6. Briefly state the intended action and key assumptions, then proceed. Ask only about missing information that materially affects correctness, authorization, member attribution, or a core experimental choice. Continue independent work while awaiting a decision.
7. Complete implementation, verification, documentation, and delivery within the authorized scope and budget. Avoid adding approval gates or expanding the task.
8. Recheck these rules and the active records before inspecting key results, revising the protocol, drawing conclusions, or preparing a release. Use repository evidence to verify chat recollections.

## 2 Project goals, course requirements, and authorization

Select an operating systems paper from the course list and replicate one to three verifiable claims. Compare the paper's results with project results using the same metrics and settings as closely as possible. Explain differences and complete an extension that changes one factor at a time. Use `docs/PROTOCOL.md` for the active paper, claims, starting code, and experimental design. Items remain pending until recorded there.

The course requires a final report, a presentation, and a Git history check. Submit the final report as an English PDF. The final release requires a `v1.0` tag. Create or push it only when the user explicitly confirms the final delivery and grants the corresponding authorization.

Each group must have four members and submit its member details and repository link through the [course form](https://v.wjx.cn/vm/rZCQLSE.aspx). Verify submission with an actual receipt. The separate `Presentation Instruction` defines the presentation structure and grading. Obtain and verify it before recording its requirements.

- The user decides the paper, claims, resource limits, major direction, formal plans, commit identity, and releases. Clear natural-language decisions are valid. Experimental and validation evidence is still required.
- Authorization for the initial governance task covered drafting the rules. Downloading paper code, installing dependencies, changing kernels, running benchmarks or fuzzing, and creating commits, pushes, or tags require applicable authorization.
- Existing authorization remains valid within its stated scope. Proceed without renewed approval for read-only checks, reversible actions within the plan, and necessary verification.
- Without a resource budget, limit work to documentation review, static checks, minimum-cost estimates, and safe design. Purchases, unbounded downloads, long stress tests, large parameter searches, and experiments that might damage the host require defined limits and authorization.
- At a plan stop point, over budget, when elevated privileges are needed, or when claims or evaluation standards would change, explain the impact and ask the user to decide. Isolate anomalous results and diagnose them within scope before changing evaluation criteria.
- Rules, templates, and candidate configurations provide no authorization for formal experiments. Building successfully is one verification step. Replicating a paper result requires separate evidence.

## 3 Paper, claims, and replication scope

Record the following before formal replication begins.

- Complete citation, public source, version or publication date, and applicable code and data licenses.
- One to three claims, each anchored to a specific table, figure, value, or observable behavior in the paper.
- Replication scale, explicit exclusions, original settings, and project settings.
- Starting repository, exact commit, license, list of changed files, and patch sources.
- Hardware, operating system, kernel, compiler, dependencies, build options, and any other settings that can affect results.
- Workload, input, trace, or benchmark sources, versions, acquisition scripts, checksums, and use permissions.
- Matched metrics, units, statistical methods, and directions of comparison for paper and project results.

Document any reduction in replication scale. Assess numerical replication, methodological replication, and build or integration checks separately. A successful example run is evidence only for the behavior it exercised.

## 4 Exploration, confirmation, and protocol revisions

Exploration may include bounded feasibility checks, small benchmarks, prototypes, and debugging runs. Exploration can guide next steps. Keep records of attempts, failures, resource use, and any results already seen. Date hypotheses when they are formed and identify those derived after exploration.

Before confirmatory experiments, freeze the paper version, claims, starting code, environment, workloads, varied factor, fixed conditions, repetitions, metrics, statistical methods, criteria for the four claim verdicts, resource limits, invalid-run conditions, and stop conditions.

After viewing confirmation results, record proposed changes to metrics, workloads, inputs, code versions, environments, samples, run counts, or success criteria. Preserve the earlier protocol version and record the reason, date, results known at the time, affected scope, and rerun decision. Record implementation fixes and protocol changes separately. Mark affected runs after a fix and preserve the prior evidence.

## 5 Formal plans, version archives, and numbering

Maintain two separate, cross-linked files for each important plan or controlled object.

- The current document contains the operative instructions for execution, verification, and adjudication, along with its exact version, status, and archive link.
- The append-only version archive records changes, reasons, alternatives and rejected material, results known at revision time, scope, compatibility or migration, affected runs, rerun decisions, and authorization for major versions.

Maintain a separate version chain for each project-controlled object. Within a major version, increment sequentially from `vN.0` through `vN.1`, `vN.2`, and onward. Continue from `vN.9` to `vN.10`. Version numbers may not be skipped, reused, or overwritten. Moving from `vN.x` to `v(N+1).0` requires explicit user approval. Record draft, frozen, complete, and paused status separately. Verify each status independently of the version number.

Preserve official versions for external papers, code, tools, data, and workloads. Give project wrappers and configurations their own internal versions.

## 6 Sources, dependencies, and traceability

- Preserve original papers, course instructions, third-party code, workloads, and traces as read-only inputs. Derived materials must be reproducible from versioned code and configuration.
- For each external asset, record its source URL, official version or commit, retrieval date, logical path, byte count, SHA-256, license, access status, and intended use. Verify retrieval independently of the existence of a web page.
- Use stable IDs or hashes to associate inputs, configuration, code, runs, and results. Avoid fuzzy matching by display name or directory order.
- Verify licenses, attribution, and the scope of changes to original code. Cite the paper, code, and tools correctly in the report.
- Exclude credentials, personal tokens, private keys, machine authentication state, and unlicensed material from the repository.
- Before releasing, inspect `git ls-files`, file sizes, contents, and diffs, including files already tracked despite `.gitignore`.

## 7 Builds, environment, and reproducibility

- The README must let a reader prepare the environment, build, and run the main experiments on a clean machine, VM, or container. Include expected outputs and approximate runtime.
- Pin and record the hardware, operating system, kernel, compiler, dependencies, tools, and settings that affect conclusions. Include the CPU governor, core affinity, virtualization, filesystem, and cache warmup as applicable.
- Where practical, acquire and verify workloads and inputs with scripts. Use configuration or environment variables for machine differences. Personal absolute paths must never be hardcoded.
- Provide a Makefile or equivalent build script. Document any unavoidable manual steps precisely and verify repeatability.
- Before formal experiments, run small known-answer tests and cover boundary cases and failure paths. Each test must check actual behavior. Placeholders that always pass are prohibited.
- Retain diagnostics for dependency, build, and run failures, including failed attempts before eventual success.

## 8 Fair comparison, repetitions, and statistics

- Compare paper and project results using the same metrics, units, and comparable settings. For each unavoidable difference, record the original setting, project setting, reason, and expected effect.
- Run each main result independently at least three times and report `mean ± standard deviation`, unless the course changes that requirement in writing. Repeating a fixed deterministic output can check repeatability. Independent evidence requires independent observations.
- Vary only the protocol-specified factor in each main comparison. Keep hardware, workloads, code paths, warmup, measurement windows, and statistics fixed where required. Disclose any differences.
- Preserve raw results for every run. Report valid and failed run counts, outlier handling, sources of randomness, and timing boundaries.
- Check units, direction, denominators, time bases, and aggregation. Define performance ratios, throughput, latency, defect counts, and coverage before comparing or combining them.
- Use suitable, reasonably tuned baselines. Control or disclose differences in tuning opportunities, budgets, preprocessing, and postprocessing.

## 9 Discrepancies and extension experiments

Assign one of `supported`, `partially_supported`, `not_supported`, or `inconclusive` to each claim. Cite run evidence and calculate absolute and relative differences from the paper.

Support explanations with controlled reruns, configuration checks, version comparisons, or other observable evidence. When several factors changed together, report the association and its limitations. Attribution to one factor requires evidence that isolates it.

State the extension question, motivation, and what it adds to the paper. Change one factor at a time and keep hardware and workload fixed as far as possible. Keep the main replication success criteria independent of exploratory extension results.

## 10 Operating systems experiment safety

- Use a disposable VM, container, or dedicated test machine by default for experiments that might crash a kernel, corrupt a filesystem, generate malicious inputs, trigger races, exhaust CPU, memory, or storage, require root, change boot settings, or expose a network service. Keep these experiments off the daily host and real user data.
- Before using disk images, snapshots, kernel modules, fuzzers, crash injectors, or privileged containers, document isolation boundaries, resource limits, timeouts, stop procedures, and recovery steps. Obtain applicable authorization.
- Scanning, stress testing, fuzzing, and exploitation of non-project systems, third-party services, or unauthorized targets are prohibited.
- Exclude raw disk images, large traces, core dumps, build products, and files over 50 MB from commits. Keep necessary evidence in controlled local storage, with hashes, generation commands, small logs, and authorized summaries in the repository.
- Stop affected runs immediately if isolation fails, host risk increases, or resource use exceeds the plan. Preserve logs and report the incident.

## 11 Acceptance and unsuccessful outcomes

| Stage | Minimum acceptance evidence |
| --- | --- |
| Source feasibility | Verified paper and code versions, licenses, asset manifest, checksums, and acquisition method |
| Implementation readiness | Clean environment build and passing minimal, boundary, and failure-path tests |
| Confirmatory experiment | Frozen plan, exact configuration, at least three valid runs, complete raw logs, and analysis scripts |
| Findings and delivery | Paper comparison, claim verdicts, evidence for discrepancies, extension, limitations, and reproduction instructions |

Distinguish pending prerequisites, insufficient evidence, unsupported claims, invalid runs or withdrawn verdicts, and a user decision to stop a line of work. Resource exhaustion, a single failure, or an empty result is insufficient evidence against the paper. Report unfinished experimental arms, failures, and counterexamples.

## 12 Run records and promotion of results

Use a unique, append-only `runs/<run-id>/` directory for every substantive run. The recommended ID is `run-<UTC-timestamp>-<experiment-id>-a<two-digit-attempt>`. Preserve successful, failed, invalid, stopped, and cancelled runs as recorded. A resumed run receives a new ID and cites the original.

At minimum, record the following for each run.

- Plan in effect before execution, effective configuration, and input and workload hashes.
- Code commit, plus relevant patches or a source snapshot when there are uncommitted edits.
- Environment manifest, build and run commands, randomness settings, and timing boundaries.
- Raw per-run outputs, logs, resource consumption, anomalies, and deviations from the protocol.
- Derived metrics, validation results, figure-generation entry points, and claim verdicts.

Every reported number must be traceable to repository logs. Track small text logs, manifests, metric tables, and generation scripts as appropriate. Store large traces, binary outputs, and machine images locally, and track hashes and retrieval or generation instructions. Keep raw outputs, derived results, and interpretation in separate records. Raw run output must remain as recorded.

## 13 Git history, attribution, and releases

- The course checks GitHub at 23:59 every Sunday. Each week requires at least one pushed commit with a substantive change. Whitespace and spelling changes alone do not count. Late commits count toward the next week. Missed weeks cannot be recovered.
- Every commit message must include the actual submitting member's student ID and full name. The suggested format is `<student-id> <full-name>: <imperative summary>`. Obtain accurate identity details from the user before committing when they are missing. Fabricated or substituted identities are prohibited.
- Each member must make substantive contributions from their own GitHub account. The final contribution statement must agree with the record. AI assistance is allowed. Fabricated authorship, contribution, or attribution is prohibited.
- Preserve actual authors and verifiable commit boundaries when transferring contributions from the work repository. Rewriting authorship, squash merges, or recommitting to conceal individual contributions is prohibited. Each member should use their own GitHub account for the release operations they are authorized to perform.
- Local commits, release commits, pushes, and tags are distinct operations, each requiring explicit user authorization. Push only from the release repository using the Git CLI.
- Keep commits focused on one purpose, describe the actual change, and pass applicable checks. Empty changes, backdating, and rewriting another contributor's history to satisfy the weekly check are prohibited.
- Create and push the final `v1.0` tag only after verifying the final report, README, build and run instructions, result evidence, and contribution record, and receiving explicit user authorization.

## 14 Project records, handoff, and maintenance

Assign one source of record to each responsibility.

| Record | Responsibility |
| --- | --- |
| `docs/PROJECT_STATE.md` | Current stage, verified artifacts, blockers, next steps, and last verification |
| `docs/PROTOCOL.md` | Active paper, claims, protocol entry point, freeze status, and version |
| `docs/DECISIONS.md` | Active decisions, revision rationale, authorization, and impacts |
| `docs/governance/FILE_MANAGEMENT.md` | File locations, lifecycle, tracking, and release boundaries |
| Formal plans and version archives | Current operative content and append-only history in separate files |
| `runs/<run-id>/` | Actual commands, raw evidence, validation, and verdicts |
| `docs/HANDOFF.md` | Entry point for a new session, next steps, and outstanding user decisions |

Update `PROJECT_STATE.md` after each completed milestone. Reflect protocol changes in both `PROTOCOL.md` and `DECISIONS.md`. Keep the status record concise and task-focused. Support completion claims with actual files or command output.

For changes to these rules or a core protocol, record the date, previous and revised requirements, reason, observed results at the time, scope, affected runs, and rerun decisions. Archive superseded clauses so only the active requirements apply.

Suggested start for a new session

> Read and follow the repository's AGENTS.md. Verify the workspace role, current state, protocol, decisions, and plan for this task. Work within the authorized scope and budget. Verify deliverables and update the project records when finished. Current task: [describe the task].

Saving this file does not start monitoring, automatic commits or pushes, scheduled tasks, or experiments.

## 15 Sources and revision history

- On 2026-10-30 the user asked for project rules based on `SAKANA2336/rare-driver-panel-benchmark`, especially the two-repository separation. The reviewed reference commit was `f6901842ac5ffb44a8dd34b2e65b2325f4962596`.
- Course brief: *Research Paper Replication – CS340*. SHA-256: `d129642a953ab1ecd7c27bf67dc667887867ec4045b72917bedaf6b76cc2666c`.
- Initial version 1.0, 2026-10-30. Established and verified the independent work and release repositories. Set requirements for evidence, experiment planning, version archives, reproducibility, operating system safety, run records, Git attribution, and releases. At the time of this bootstrap the paper was pending, the protocol was unfrozen, and no starting code or runs existed. The bootstrap authorization did not include committing, pushing, or tagging.
- English edition, 2026-11-22. Translated the operating rules for publication. The original 1.0 text remains available at commit `74bf5eb7cade99437630753166c38f76735fad1e` in `AGENTS.md`. No experimental requirements or run evidence changed. No reruns were required.
