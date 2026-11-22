# Project handoff

Last verified on 2026-11-22 (Asia/Shanghai).

Start with the [project status](PROJECT_STATE.md), [current protocol](PROTOCOL.md), and [workspace rules](../AGENTS.md). Use the independent daily repository with no remote for development. The release repository is reserved for authorized publication.

## Evidence already available

- The [x86_64 environment package](../outputs/asan-environment/README.md) and [accepted run](../runs/env-20261108t013027z-6c0e488a/README.md) document seven real functional checks. The ARM64 environment also passed seven checks in an independent VM, with its full evidence in local run `run-20261114t185606z-env-arm64-001-a03`.
- The [published x86_64 Olden pilot](../results/run-20261114t130529z-exp-001-a01-ce70aa/README.md) and the local ARM64 pilot used the same six program names. Their timing and provenance remain separate. ARM64 pilot `run-20261118t151453z-pilot-arm64-001-a02` resolved the source checkout line-ending mismatch and validated 222 locked source files.
- Both formal ARM64 experiments completed. The [English results and evidence index](arm64-formal-results.md) links the six independent batches and the offline analysis. The original runs, failed preparation attempts, and frozen plans remain sealed locally.
- The [original claim register](CLAIMS.md) covers a different benchmark series. The published summaries yield 2.22× time and 2.58× RSS, with gaps in the raw trial-level evidence. Preserve the original claim IDs and historical authorship.

## Remaining work

1. Review the [English report draft](../report/report.md) against the formal results. Complete the paper comparison, contributions, AI-use statement, and final PDF after team review. The completed extension varies the heap redzone from 32 B to 64 B.
2. Obtain the original trial records and source/input provenance for C-001 and C-002. Keep the RSS and VmPeak comparisons distinct. Document the limitations if the original records cannot be recovered.
3. Confirm the course registration receipt and separate Presentation Instruction, then complete the presentation. The final `v1.0` tag requires its own authorization.
4. Use a new run ID, an approved protocol, and a fresh evidence record if an experiment must be repeated. Publication of the existing results uses the evidence and scope in [D-028](DECISIONS.md#d-028-english-publication-of-formal-results-and-project-documents).
