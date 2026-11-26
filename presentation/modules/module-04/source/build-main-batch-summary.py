#!/usr/bin/env python3
"""Render the formal exp-001 batch summary from immutable run evidence.

Usage: python3 build-main-batch-summary.py --root . --out /tmp/new-output
Dependencies: ReportLab; pdftoppm on PATH for the PNG preview.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, stdev
from xml.sax.saxutils import escape

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

CAMPAIGN = 'exp-001-v0-2-20261118t170938z'
BENCHMARKS = ('bisort', 'em3d', 'mst', 'perimeter', 'treeadd', 'tsp')
STEM = 'module-04-main-batch-summary-v0.0'
os.environ.setdefault('SOURCE_DATE_EPOCH', str(int(datetime(2026, 11, 26, tzinfo=timezone.utc).timestamp())))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def equal(a, b):
    assert math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12), (a, b)


def recompute(root):
    source = root / 'results' / CAMPAIGN / 'summary.json'
    data = json.loads(source.read_text())
    assert data['campaign_id'] == CAMPAIGN and data['experiment_id'] == 'exp-001'
    assert data['missing_valid_batch_slots'] == []
    assert digest(root/'experiments/exp-001/PLAN.md') == data['plan_sha256']
    inputs = {str(source.relative_to(root)): digest(source),
              'experiments/exp-001/PLAN.md': digest(root/'experiments/exp-001/PLAN.md')}
    rows = []
    per_program = []
    attempts = sorted((a for a in data['attempts'] if a['included']), key=lambda a: a['batch_slot'])
    assert [a['batch_slot'] for a in attempts] == [0, 1, 2]
    for attempt in attempts:
        run_id = attempt['run_id']
        assert attempt['status'] == 'passed_batch' and attempt['vm_id'] == run_id
        guest = root/'runs'/run_id/'guest-evidence/data'/run_id
        record_path = guest/'metrics/records.json'
        assert digest(record_path) == attempt['records_sha256']
        inputs[str(record_path.relative_to(root))] = digest(record_path)
        records = json.loads(record_path.read_text())
        assert len(records) == 72
        assert len({r['sample_id'] for r in records}) == 72
        for record in records:
            assert record['experiment_id'] == 'exp-001'
            assert record['batch_slot'] == attempt['batch_slot']
            assert record['valid'] and record['reference_match']
            assert not record['timed_out'] and not record['sanitizer_report']
            assert record['exit_code'] == record['program_exit_code'] == 0
            path = guest/'raw-outputs'/(record['sample_id']+'.time.txt')
            fields = dict(line.split() for line in path.read_text().splitlines())
            assert int(fields['exit']) == 0
            for field in ('real', 'user', 'sys'):
                assert float(fields[field]) == record[field+'_seconds']
        measured = [r for r in records if r['phase'] == 'measure']
        warmups = [r for r in records if r['phase'] == 'warmup']
        assert len(measured) == 60 and len(warmups) == 12
        values = []
        for benchmark in BENCHMARKS:
            means = {}
            for arm in ('baseline', 'asan'):
                times = [r['real_seconds'] for r in measured
                         if r['benchmark'] == benchmark and r['arm'] == arm]
                assert len(times) == 5 and all(t > 0 and math.isfinite(t) for t in times)
                means[arm] = mean(times)
                equal(means[arm], attempt['batch']['benchmarks'][benchmark]['arms'][arm]['mean_seconds'])
            ratio = means['asan']/means['baseline']
            equal(ratio, attempt['batch']['benchmarks'][benchmark]['runtime_ratio'])
            values.append(ratio)
            per_program.append({'batch': attempt['batch_slot']+1, 'run_id': run_id,
                                'benchmark': benchmark, 'baseline_mean_seconds': means['baseline'],
                                'asan_mean_seconds': means['asan'], 'runtime_ratio': ratio})
        ratio = mean(values)
        equal(ratio, attempt['batch']['arithmetic_mean_runtime_ratio'])
        rows.append({'batch': attempt['batch_slot']+1, 'run_id': run_id,
                     'runtime_ratio': ratio, 'measured_executions': 60,
                     'warmups': 12, 'benchmarks': 6})
    avg, sd = mean(r['runtime_ratio'] for r in rows), stdev(r['runtime_ratio'] for r in rows)
    aggregate = data['aggregate']['arithmetic_mean_runtime_ratio']
    equal(avg, aggregate['mean']); equal(sd, aggregate['sample_sd'])
    assert aggregate['n'] == 3
    return rows, per_program, avg, sd, inputs


def design(rows, avg, sd):
    width, height = 460, 280
    items = []
    def text(x,y,value,size=12,bold=False,anchor='start'):
        font = 'Times-Bold' if bold else 'Times-Roman'
        tw = pdfmetrics.stringWidth(value,font,size)
        left = x-tw if anchor == 'end' else x
        assert left >= 23 and left+tw <= width-23, (value, left, tw)
        items.append(dict(kind='text', x=x,y=y,value=value,size=size,bold=bold,anchor=anchor))
    def line(y, weight):
        items.append(dict(kind='line', x1=24,x2=436,y=y,weight=weight))
    text(24,256,'Main experiment: batch summary',13,True)
    text(24,239,'Six Olden benchmarks; three independent ARM64 VM batches',10)
    line(225,1.05)
    text(30,208,'VM batch',11,True)
    text(430,208,'Suite runtime ratio (×)',11,True,'end')
    line(199,.55)
    for row,y in zip(rows,[176,152,128]):
        text(30,y,f"Batch {row['batch']}")
        text(430,y,f"{row['runtime_ratio']:.4f}",anchor='end')
    text(30,97,'Mean ± SD',12,True)
    text(430,97,f'{avg:.4f} ± {sd:.4f}',12,True,'end')
    line(82,1.05)
    notes = [
        'Each batch value is the equal-weight mean of six program ratios (ASan mean / baseline mean).',
        'Five timings per arm and program; 60 timings per batch. Warmups are excluded.',
        'Final row: mean ± sample SD across three independent VM batches (n = 3).',
        'All six benchmarks retained; mst is short-running. Source: exp-001, protocol v0.2.'
    ]
    for note,y in zip(notes,[65,53,41,29]):
        text(24,y,note,8.5)
    return width,height,items


def render(out, rows, avg, sd):
    width,height,items = design(rows,avg,sd)
    pdf = out/(STEM+'.pdf')
    c = canvas.Canvas(str(pdf),pagesize=(width,height),pageCompression=1,invariant=1)
    c.setTitle('Formal main-experiment batch summary')
    c.setAuthor('OS-project; table generated from sealed formal exp-001 evidence')
    c.setSubject('Three independent VM batches; equal-weight arithmetic suite ratios; mean and sample SD')
    for item in items:
        if item['kind'] == 'line':
            c.setLineWidth(item['weight']); c.line(item['x1'],item['y'],item['x2'],item['y'])
        else:
            c.setFont('Times-Bold' if item['bold'] else 'Times-Roman',item['size'])
            method = c.drawRightString if item['anchor'] == 'end' else c.drawString
            method(item['x'],item['y'],item['value'])
    c.showPage(); c.save()
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}pt" height="{height}pt" viewBox="0 0 {width} {height}">',
           '<title>Formal main-experiment batch summary</title>',
           f'<rect width="{width}" height="{height}" fill="white"/>']
    for item in items:
        if item['kind'] == 'line':
            svg.append(f'<line x1="{item["x1"]}" x2="{item["x2"]}" y1="{height-item["y"]}" y2="{height-item["y"]}" stroke="black" stroke-width="{item["weight"]}"/>')
        else:
            svg.append(f'<text x="{item["x"]}" y="{height-item["y"]}" font-family="Times New Roman, Times, serif" font-size="{item["size"]}" font-weight="{"bold" if item["bold"] else "normal"}" text-anchor="{item["anchor"]}" fill="black">{escape(item["value"])}</text>')
    svg.append('</svg>')
    (out/(STEM+'.svg')).write_text('\n'.join(svg)+'\n')
    subprocess.run(['pdftoppm','-r','400','-singlefile','-png',str(pdf),str(out/STEM)],check=True,capture_output=True)
    return width,height


def write_csv(path,rows,fields):
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields)
        writer.writeheader();writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    root=args.root.resolve();out=args.out.resolve()
    assert not out.exists() or not any(out.iterdir()), 'Output directory must be new or empty'
    rows,programs,avg,sd,inputs = recompute(root)
    out.mkdir(parents=True,exist_ok=True)
    width,height=render(out,rows,avg,sd)
    write_csv(out/(STEM+'.csv'),rows,list(rows[0]))
    write_csv(out/'per-program-inputs.csv',programs,list(programs[0]))
    tex = ['% Requires \\usepackage{booktabs}. Values are recomputed from formal exp-001 evidence.',
           '\\begin{table}[t]','\\centering','\\caption{Main-experiment summary across three independent ARM64 VM batches.}',
           '\\label{tab:main-batch-summary}','\\begin{tabular}{lr}','\\toprule',
           'VM batch & Suite runtime ratio ($\\times$) \\\\','\\midrule']
    tex += [f"Batch {r['batch']} & {r['runtime_ratio']:.4f} \\\\" for r in rows]
    tex += ['\\addlinespace',f'\\textbf{{Mean $\\pm$ SD}} & \\textbf{{{avg:.4f} $\\pm$ {sd:.4f}}} \\\\',
            '\\bottomrule','\\end{tabular}',
            '\\par\\smallskip\\begin{minipage}{0.95\\linewidth}\\footnotesize',
            'Each batch value is the equal-weight arithmetic mean of six Olden program ratios. '
            'Each program ratio is mean ASan time divided by mean baseline time over five timed executions per arm. '
            'The final row reports the mean and sample SD across three independent VM batches ($n=3$). '
            'Warmups are excluded. All six programs, including short-running \\texttt{mst}, are retained.',
            '\\end{minipage}','\\end{table}']
    (out/(STEM+'.tex')).write_text('\n'.join(tex)+'\n')
    metadata={
        'artifact_id':'module-04-main-batch-summary','exact_version':'v0.0','created_date':'2026-11-26','timezone':'Asia/Shanghai',
        'source_campaign':CAMPAIGN,'source_protocol':'exp-001 PLAN v0.2, Section 4',
        'source_hashes':inputs,'generator_sha256':digest(Path(__file__)),
        'rows':rows,'aggregate':{'mean':avg,'sample_sd':sd,'n':3},
        'statistics':'Per program: ratio of arithmetic mean ASan seconds to arithmetic mean baseline seconds (five measured executions per arm). Per batch: equal-weight arithmetic mean of all six program ratios. Final: mean and sample SD of the three batch summaries.',
        'display_decimal_places':4,'rounding':'Display only; CSV/JSON preserve full precision.',
        'measurement_counts':{'benchmarks':6,'independent_vm_batches':3,'measured_executions':180,'warmups_excluded':36},
        'interpretation':'Dimensionless wall-clock time ratio, ASan/baseline. Above 1 indicates greater runtime.',
        'scope':'Formal original main-experiment batches only. Separate from extension, pilots and clean-entry acceptance.',
        'short_run_note':'mst baseline mean is below 0.05 s in all three batches; retained under the frozen primary estimand. Prespecified sensitivity analysis remains in the formal result summary.',
        'design':{'style':'Monochrome three-rule academic table; serif typography; right-aligned values; no vertical grid or decorative graphics.','page_points':[width,height],'png_dpi':400},
        'caption':'Formal main-experiment results on six Olden programs across three independent ARM64 VM batches. The final row reports the mean ± sample SD of the batch-level suite ratios (n = 3).',
        'rebuild':'python3 presentation/modules/module-04/source/build-main-batch-summary.py --root . --out <new-output-directory>',
        'experimental_impact':'None; no new measurements, protocol changes, verdict changes or raw-evidence edits.'
    }
    metadata['outputs']={p.name:{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(out.iterdir()) if p.is_file()}
    (out/'generation-v0.0.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'batch_values':[r['runtime_ratio'] for r in rows],'mean':avg,'sample_sd':sd,'output':str(out)},ensure_ascii=False))


if __name__=='__main__':
    main()
