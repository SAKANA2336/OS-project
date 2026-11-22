#!/usr/bin/env python3
"""Verify the public measurement files and recompute the frozen runtime summaries."""

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import geometric_mean, mean, stdev


BENCHMARKS = ('bisort', 'em3d', 'mst', 'perimeter', 'treeadd', 'tsp')
ARMS = {'exp-001': ('baseline', 'asan'), 'exp-002': ('rz32', 'rz64')}
METRICS = ('arithmetic_mean_runtime_ratio', 'geometric_mean_runtime_ratio',
           'arithmetic_mean_runtime_ratio_without_mst')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_statistics(actual, expected, label):
    for name, value in actual.items():
        if isinstance(value, dict):
            verify_statistics(value, expected[name], f'{label}/{name}')
        elif isinstance(value, list):
            require(len(value) == len(expected[name]), f'{label}/{name}: list length differs')
            for index, (left, right) in enumerate(zip(value, expected[name])):
                require(math.isclose(left, right, rel_tol=1e-12), f'{label}/{name}/{index}: value differs')
        elif isinstance(value, float):
            require(math.isclose(value, expected[name], rel_tol=1e-12, abs_tol=1e-15),
                    f'{label}/{name}: value differs')
        else:
            require(value == expected[name], f'{label}/{name}: value differs')


def summarize_batch(path, slot, experiment):
    with path.open(encoding='ascii', newline='') as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 72, f'{path.name}: expected 72 observations')
    timings = defaultdict(list)
    binaries = defaultdict(set)
    seen = set()
    arms = ARMS[experiment]
    for sequence, row in enumerate(rows, 1):
        label = f'{path.name} row {sequence}'
        require(row['experiment_id'] == experiment and int(row['batch_slot']) == slot
                and int(row['sequence']) == sequence, f'{label}: inconsistent identifiers')
        require(row['valid'] == row['reference_match'] == 'True' and
                row['timed_out'] == row['sanitizer_report'] == 'False' and
                row['exit_code'] == row['program_exit_code'] == '0', f'{label}: unsuccessful observation')
        benchmark, arm, phase = row['benchmark'], row['arm'], row['phase']
        iteration, seconds = int(row['iteration']), float(row['real_seconds'])
        require(benchmark in BENCHMARKS and arm in arms and
                (phase == 'warmup' and iteration == 1 or phase == 'measure' and 1 <= iteration <= 5),
                f'{label}: unexpected observation')
        key = (benchmark, arm, phase, iteration)
        require(key not in seen and math.isfinite(seconds) and seconds > 0, f'{label}: invalid sample')
        seen.add(key)
        binaries[benchmark].add(row['binary_sha256'])
        if phase == 'measure':
            timings[benchmark, arm].append(seconds)

    benchmarks = {}
    for benchmark in BENCHMARKS:
        stats = {}
        for arm in arms:
            values = timings[benchmark, arm]
            require(len(values) == 5, f'{path.name}: incomplete measurements for {benchmark}/{arm}')
            stats[arm] = {'mean_seconds': mean(values), 'sample_sd_seconds': stdev(values), 'n': len(values)}
        if experiment == 'exp-002':
            require(len(binaries[benchmark]) == 1, f'{path.name}: redzone arms disagree on binary for {benchmark}')
        benchmarks[benchmark] = {
            'arms': stats,
            'runtime_ratio': stats[arms[1]]['mean_seconds'] / stats[arms[0]]['mean_seconds'],
            'short_run_warning': min(arm['mean_seconds'] for arm in stats.values()) < 0.050,
        }
    ratios = [result['runtime_ratio'] for result in benchmarks.values()]
    return {
        'benchmarks': benchmarks,
        METRICS[0]: mean(ratios),
        METRICS[1]: geometric_mean(ratios),
        METRICS[2]: mean(result['runtime_ratio'] for name, result in benchmarks.items() if name != 'mst'),
    }


def across_batches(values):
    return {'batch_values': values, 'mean': mean(values), 'sample_sd': stdev(values), 'n': len(values)}


def verify_campaign(campaign, evidence):
    campaign_id, experiment = campaign['id'], campaign['experiment_id']
    directory = evidence.parent / campaign_id
    summary_path = directory / 'summary.json'
    summary = json.loads(summary_path.read_text(encoding='utf-8'))
    completion = json.loads((directory / 'completion.json').read_text(encoding='utf-8'))
    require(sha256(summary_path) == campaign['summary_sha256'] == completion['summary_sha256'],
            f'{campaign_id}: summary SHA-256 differs')
    require(summary['campaign_id'] == completion['campaign_id'] == campaign_id and
            summary['experiment_id'] == completion['experiment_id'] == experiment and
            completion['status'] == 'complete' and completion['audit_exit'] == 0,
            f'{campaign_id}: inconsistent completion record')

    runs = campaign['runs']
    require([run['batch_slot'] for run in runs] == [0, 1, 2] == summary['included_batch_slots'] and
            [run['run_id'] for run in runs] == completion['run_ids'], f'{campaign_id}: unexpected batches')
    attempts = {attempt['run_id']: attempt for attempt in summary['attempts']}
    batches = []
    for run in runs:
        csv_path = evidence / run['csv']
        require(csv_path.name == f"{run['run_id']}.csv" and csv_path.parent == evidence and
                sha256(csv_path) == run['sha256'], f'{csv_path.name}: CSV SHA-256 differs')
        attempt = attempts[run['run_id']]
        require(attempt['included'] and attempt['batch_slot'] == run['batch_slot'] and
                attempt['outer_seal_sha256'] == run['original_run_seal_sha256'],
                f'{csv_path.name}: published provenance and campaign summary disagree')
        batch = summarize_batch(csv_path, run['batch_slot'], experiment)
        verify_statistics(batch, attempt['batch'], csv_path.name)
        batches.append(batch)

    aggregate = {metric: across_batches([batch[metric] for batch in batches]) for metric in METRICS}
    aggregate['benchmarks'] = {
        name: across_batches([batch['benchmarks'][name]['runtime_ratio'] for batch in batches])
        for name in BENCHMARKS
    }
    verify_statistics(aggregate, summary['aggregate'], campaign_id)
    primary = aggregate[METRICS[0]]
    require(summary['verdict'] == 'supported' and all(value > 1 for value in primary['batch_values']),
            f'{campaign_id}: primary ratios do not support the recorded verdict')
    print(f"{experiment}: {primary['mean']:.6f}x +/- {primary['sample_sd']:.6f}x; "
          f"{primary['n']} batches, 180 timed observations, 36 warmups")


def main():
    evidence = Path(__file__).resolve().parents[1] / 'results' / 'arm64-formal-evidence'
    index = json.loads((evidence / 'provenance.json').read_text(encoding='utf-8'))
    require([campaign['experiment_id'] for campaign in index['campaigns']] == list(ARMS),
            'The evidence index must contain both formal campaigns in order')
    for campaign in index['campaigns']:
        verify_campaign(campaign, evidence)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit(f'Verification failed: {error}') from None
