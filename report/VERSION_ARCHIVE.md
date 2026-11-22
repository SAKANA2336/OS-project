# Report version archive

| Field | Value |
| --- | --- |
| Controlled object | `report` |
| Document role | Append-only version archive |
| Current draft | [Report v0.1](report.md) |

## v0.0

- Date and status. 2026-11-15 (Asia/Shanghai), draft and unfrozen.
- Contribution. 陈卓康 prepared the initial draft with the introduction, setup, results, analysis, extension proposal, conclusion, references and statements.
- Scope at that time. The draft covered the published C-001, C-002 and C-003 records and discussed a proposed access-width extension. It recorded missing source and measurement evidence.
- Recovery. Git commit `6487b890de98470d07531c5d04e057320805f5fb`, file `report/report.md`, blob `901e4b2e880b6cd7efc733a64fe9a5cde7832434`.
- SHA-256. `d476226ab0ff3d09c1a1037a57af32aad3860b7715ff2ac8a0baee4337bf4c87`.

## v0.1

- Date and status. 2026-11-22 (Asia/Shanghai), draft and unfrozen.
- Publication scope. The 2026-11-22 instruction authorizes an English update for the first release of formal results. Official contributor names retain their original spelling. Report freeze, final PDF and submission remain outside this revision.
- Change. Updates the report to the completed ARM64 Olden main experiment and the single-factor heap-redzone extension. Retains earlier experiments with the limits of their source, raw measurement and comparability records. The earlier access-width proposal remains recoverable in v0.0.
- Evidence available at revision. Frozen exp-001 and exp-002 v0.2 each produced three accepted ARM64 batches. The results cover the registered timing claims. The paper's Figure 2 reference and the earlier project results remain separate observations.
- Scope and compatibility. Existing claim, run and campaign IDs remain stable. This revision changes presentation and references. Frozen plans, original observations, evidence hashes and run verdicts retain their existing values. The update requires no reruns and affects no existing run.
- Recovery. Current report at `report/report.md` in the Git commit containing this version entry.
- SHA-256. `25b1553a9fb4ab807c30558067466c92994fd05f1ec917963b07b043c5fb5c8c`.
