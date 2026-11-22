# OS-project file management policy

| Field | Current value |
| --- | --- |
| `controlled_object_id` | `FILE_MANAGEMENT` |
| `exact_version` | `v0.1` |
| `status` | `draft` |
| `document_role` | `current_policy` |
| `created_at` | `2026-10-30 (Asia/Shanghai)` |
| `last_verified_at` | `2026-11-22 (Asia/Shanghai)` |
| `applies_to` | Project files, directories, generated artifacts, and run records in the work repository, plus the boundary for transfer to the release repository |
| `approval_state` | Initial rules authorized. English revision authorized. Major version freeze pending. |
| `freeze_state` | `not_frozen` |
| `supersedes` | `v0.0` |
| `next_allowed_version` | `v0.2` |
| `major_version_authorization` | `absent` |
| `governing_rule` | `AGENTS.md` 1.0 |
| `archive_ref` | [`FILE_MANAGEMENT_VERSION_ARCHIVE.md#v01`](FILE_MANAGEMENT_VERSION_ARCHIVE.md#v01) |
| `source_of_authority` | The user's initial governance request on 2026-10-30 and `docs/DECISIONS.md` D-005. The user authorized English revisions on 2026-11-22. |

This document defines the file management policy. Its current status is draft. Downloads, builds, experiments, commits, pushes, and tags each require applicable authorization.

## 1 Purpose, scope, and precedence

This policy defines the responsibilities, standard locations, naming, lifecycle, versioning, and tracking of files and run evidence. It also defines the transfer boundary between the work and release repositories.

Apply these sources in order of precedence.

1. The most recent explicit user instruction
2. `AGENTS.md`
3. Active protocols and decisions
4. This policy
5. The applicable experiment plan
6. General directory conventions

For a substantive conflict, stop the affected writes, document the conflict, and request a decision. Course requirements, experiment protocols, resource budgets, licenses, and safety boundaries continue to apply.

## 2 Sources of record

| Information | Current source of record | Treatment elsewhere |
| --- | --- | --- |
| Standing operating rules | `AGENTS.md` | Reference the rules without copying them in full |
| Current stage, artifacts, blockers, and next steps | `docs/PROJECT_STATE.md` | Summarize the state and link to it in the README |
| Active paper, claims, and protocol entry point | `docs/PROTOCOL.md` | Cite the exact protocol version in experiment plans |
| Active decisions and reasons for revisions | `docs/DECISIONS.md` | Preserve decisions superseded by later entries |
| File management policy | This document | Keep the required entry point in `AGENTS.md` |
| Handoff between sessions | `docs/HANDOFF.md` | Verify remembered chat context against recorded evidence |
| Specific experiment plan | `experiments/<experiment-id>/PLAN.md` | Cite the exact plan version in configurations and runs |
| Evidence from actual runs | `runs/<run-id>/` | Cite run IDs in reports and summaries |

Avoid parallel sources such as `status-final.md`, `latest-protocol.md`, or a duplicate table of canonical run facts.

## 3 Top-level structure and responsibilities

```text
docs/                         Project state, protocol, decisions, handoff, and governance
experiments/<experiment-id>/  Plans, version archives, and notes for an experiment
config/                       Credential-free, executable, versioned configuration
src/                          Main project implementation
scripts/                      Build, retrieval, execution, validation, and report entry points
tests/                        Unit, integration, and boundary tests, plus small public fixtures
workloads/                    Workload manifests, retrieval scripts, and small public inputs
third_party/                  Required, licensed third-party notices or patches
runs/<run-id>/                Append-only run evidence, with small publishable items tracked
results/                      Machine-readable summaries promoted from verified runs
report/                       Report source, figure-generation entry points, and publishable PDFs
presentation/                 Presentation source and publishable exports
archive/<retirement-id>/      Read-only history for retired lines of work
scratch/                      Local temporary files, never the sole copy of evidence
```

Create directories as needed. Avoid empty scaffolding and `.gitkeep` placeholders. This layout describes where to put actual artifacts. Verify each implementation, experiment, and result against its corresponding evidence.

## 4 File locations

| File type | Standard location | Constraints |
| --- | --- | --- |
| Governance and state | `docs/`, `docs/governance/` | One location per responsibility |
| Formal experiment plans | `experiments/<experiment-id>/` | Separate `PLAN.md` from `VERSION_ARCHIVE.md` |
| Configuration | `config/` | Exclude credentials, private URLs, and personal absolute paths |
| Main code | `src/` | Keep modules clear and use a reproducible entry point outside any notebook |
| Automation entry points | `scripts/` | Parameterized, repeatable, and free of hardcoded personal paths |
| Tests | `tests/` | Use small synthetic fixtures or fixtures explicitly cleared for publication |
| Workload metadata | `workloads/` | Record sources, versions, licenses, retrieval scripts, and hashes |
| Large or restricted inputs | Controlled local storage in the work repository | Ignore by default and record logical paths and hashes in manifests |
| Run evidence | `runs/<run-id>/` | Append-only. Track small logs and metrics. Ignore large binaries. |
| Machine-readable results | `results/` | Promote from verified runs and retain their run IDs |
| Report and presentation | `report/`, `presentation/` | Preserve source and generation instructions. Track exports needed for delivery. |
| History | `archive/<retirement-id>/` | Read-only once the manifest is complete. Use the corresponding current document as the active entry point. |
| Temporary files | `scratch/`, `tmp/` | Disposable. Preserve any evidence elsewhere before cleanup. |

The existing course brief filename includes spaces and `(1)`. Keep this pre-policy input in place unless a change is expressly authorized. Verify license and intended use before registering it as a public asset. New files must follow this policy.

## 5 Names and identifiers

- Use ASCII for new paths. Exclude spaces, Chinese characters, and trailing periods. Paths that differ only in letter case are prohibited.
- Use lowercase kebab-case for human-readable directories and IDs. Follow the language's conventions for code identifiers.
- Keep established uppercase filenames for fixed governance documents. Preserve official names and versions for original third-party files.
- Use `claim-<three-digit-sequence>` for claims and `exp-<three-digit-sequence>` for experiments.
- Use `run-<UTC-timestamp>-<experiment-id>-a<two-digit-attempt>` for runs.
- Use `YYYY-MM-DD-<kebab-case-scope>` for retirement packages.
- Preserve the original identifiers for Git commits, external versions, random seeds, run IDs, and data hashes. Use `vN.x` for internal controlled-object versions only.
- Increment internal versions in sequence from `vN.0` to `vN.1` and onward. Follow `vN.9` with `vN.10`.
- Exclude `latest`, `final`, `new`, `old`, `copy`, `final2`, non-English forms of “latest version,” and automatic suffixes like `(1)` from new filenames.

## 6 Lifecycle and conflicts

| Category | Examples | Write rule |
| --- | --- | --- |
| Immutable | Original sources, terminal runs, frozen configurations, historical snapshots | Stop if the target exists. Use a new ID or version for changes. |
| Controlled update | Current protocol, formal plans, governance policy, main code | Document the decision or version basis and preserve a recovery path. |
| Append-only | Decisions, version archives, run indexes | Preserve earlier entries. Correct errors with an erratum. |
| Regenerable | Build products, derived metrics, generated figures | Rebuild from versioned code and configuration. Retain the source separately. |
| Historical archive | `archive/<retirement-id>/` | Make read-only once the manifest is complete. Restore through a new decision and commit. |
| Temporary | `scratch/`, `tmp/`, caches, `.partial` files | May be deleted. Keep any completion evidence elsewhere. |

Check the full path on case-insensitive semantics before creating a file. If the same bytes already exist, reuse the file. Use the next sequential version for an authorized revision or a new source version for different source material. Stop on unexplained collisions. Automatic suffixes are prohibited. Write large files to a `.partial` or temporary path, verify them, and rename them atomically.

Deleting an immutable or controlled file requires explicit authorization, an exact target, and a recovery method. Prefer archiving. Do not use `git clean`, destructive resets, or cleanup commands to conceal failures or unfavorable results. Use `AGENTS-<version>.md.snapshot` when archiving former operating rules to prevent automatic loading.

## 7 Controlled objects and version archives

- Keep the current document and archive in separate files. Cross-link both with the same `controlled_object_id` and `exact_version`.
- The current document contains operative execution, verification, and adjudication requirements. The archive records discussions, alternatives, historical differences, and results known before each revision.
- Append one entry per version. Record the rationale, known results, scope, migration, affected runs, rerun decision, and authorization for any major version change.
- Archive entries record the current document's SHA-256 and at least one recovery reference. Use a Git commit, an immutable snapshot, or a run snapshot. Before the first commit, record the document hash and an immutable snapshot. Add the commit after an authorized commit exists.
- A `.md.snapshot` file is a byte-for-byte recovery copy of a document in its original path context. Its `current_*` role and relative links apply only when restoring the original. Follow the [snapshot instructions](snapshots/README.md).
- A version increase in one object does not carry over to others. An increase in a major version requires explicit user approval.
- Record status separately as `draft`, `frozen`, `complete`, or `retired`. Verify status independently of version numbering.

## 8 Sources, licenses, and large files

- For each third-party paper, source repository, tool, dataset, workload, or trace, record its source, official version or commit, retrieval date, logical path, byte count, SHA-256, license, access status, and intended use.
- Preserve original inputs as read-only. Generate derived material from versioned code and configuration. Verify acquisition and redistribution rights separately from a website's availability.
- Preserve licenses and attribution for third-party code. Track changes with a patch, fork commit, or explicit changed-file list.
- Exclude credentials, tokens, private keys, authentication caches, personal absolute paths, and unlicensed materials from tracked files.
- The per-file limit is 50 MB. Keep disk images, VM images, core dumps, large traces, build products, and large benchmark inputs local by default. Record their hashes, sources, and generation commands in the repository.

## 9 Run records and report figures

Give every substantive run a unique `runs/<run-id>/`. Use the following minimum structure as applicable.

```text
runs/<run-id>/
  run-manifest.json
  config/
  provenance/
  logs/
  raw-outputs/
  metrics/
  validation/
  decision/
```

Lock each run after it reaches a terminal status. For a resumed run, create a new ID and record `resumed_from`. Track small text logs, manifests, per-iteration metrics, raw outputs, and statistical entry points so every reported number is traceable. Store large run content explicitly in ignored `large-artifacts/` or `large-traces/` directories and track its hashes and descriptions. Reports and charts must cite run IDs. Raw run evidence must remain as recorded.

## 10 Git tracking boundaries

Track rules, state, protocols, decisions, plans, code, tests, credential-free configuration, build and run scripts, lockfiles, small public fixtures, source manifests, small logs, per-iteration metrics, statistical scripts, and publishable reports by default.

Ignore caches, virtual environments, build products, temporary files, machine-local configuration, credentials, disk and VM images, core dumps, large traces, downloads, and large run binaries by default. Before release, use `git ls-files` to check for prohibited tracked content even when `.gitignore` covers the path.

Commit messages must include the actual member's student ID and full name. Confirm identity before committing. Do not use build outputs, whitespace-only or spelling-only changes, or backdated commits to satisfy weekly checks.

## 11 Work and release repositories

- Use `<workspace-parent>/OS-project-local` for routine work. This repository must have no remotes.
- Use the independent release clone `<workspace-parent>/OS-project` with `origin` set to `SAKANA2336/OS-project`. The clone is read-only by default.
- Each repository must have its own independent `.git` directory and an untracked `.local/workspace-role` marker. Linked worktrees are prohibited. The release repository's `main` tracks `origin/main`. Both remote URLs use the canonical HTTPS `.git` address.
- Follow the one-time authorization in D-002 for initial provisioning. Clone the verified release repository, remove the temporary remote in the new clone only, then import bootstrap content from an explicit governance-file allowlist and verify it. Later transfers follow the normal release procedure.
- Establish a release allowlist after the user authorizes a push. Transfer only the listed content. Whole-tree mirroring and overwriting the work repository from the release repository are prohibited.
- Prefer reviewed `format-patch` and `git am` or an equivalent Git commit transfer for committed contributions. Preserve the actual author. AI or a single member may not rewrite, squash, or recommit other members' work to obscure attribution.
- Before release, verify both repositories' roots, identities, branches, and status. Check for remote advancement, inspect diffs for absolute paths, credentials, and prohibited artifacts, confirm licensing and the 50 MB limit, and run applicable tests.
- For importing remote changes into the work repository, first inspect the release commits and diffs in read-only mode. Import through an explicit patch or allowlist. Keep the work repository remote-free and avoid whole-tree copying.
- Stop on conflicts, unrelated changes, remote advancement, or failed checks. Force pushes, history rewrites, and automatic overwrites are prohibited.

## 12 Checks, exceptions, and migration

Run at least these checks for file management or release work.

1. `git rev-parse --show-toplevel` and the workspace role match the intended repository.
2. `git status --short --branch` and `git diff` show only authorized changes.
3. `git diff --check` reports no whitespace errors.
4. `git check-ignore -v --no-index` matches prohibited paths and excludes rules and code.
5. `git ls-files` lists no credentials, build products, images, large traces, or other prohibited content.
6. `.gitattributes`, line endings, and binary handling follow repository policy.
7. Paths are unique on a case-insensitive comparison, and new filenames follow the policy.
8. Each file is at most 50 MB.
9. The current document and archive agree on object ID, version, links, and the SHA-256.
10. Report figures trace back through run IDs to individual logs, metrics, and statistical entry points.
11. The release repository contains only allowed changes, the remote identity matches, and the push is a normal fast-forward.
12. `scripts/check-workspace-zone.sh` passes for the current role.

Record the reason, scope, duration, risk, recovery process, and authority before using an exception. Prefer adding files or explicitly moving them during migrations. Review path moves separately from content changes. The next allowable version for this draft is `v0.2`.
