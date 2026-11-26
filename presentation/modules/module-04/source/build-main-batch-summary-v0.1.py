#!/usr/bin/env python3
"""Build one combined main-results PNG; auxiliary files stay in local build storage."""
import argparse
import hashlib
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, stdev

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

STEM='module-04-main-batch-summary-v0.1'
CAMPAIGN='exp-001-v0-2-20261118t170938z'
os.environ.setdefault('SOURCE_DATE_EPOCH',str(int(datetime(2026,11,26,tzinfo=timezone.utc).timestamp())))


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--pymupdf-dir',type=Path)
    args=ap.parse_args();root=args.root.resolve();out=args.out.resolve()
    assert not out.exists() or not any(out.iterdir()),'Refusing to overwrite an existing build'
    source=root/'results'/CAMPAIGN/'summary.json'
    data=json.loads(source.read_text());a=data['aggregate']['arithmetic_mean_runtime_ratio']
    assert data['campaign_id']==CAMPAIGN and a['n']==3 and len(a['batch_values'])==3
    assert math.isclose(a['mean'],mean(a['batch_values']),abs_tol=1e-12)
    assert math.isclose(a['sample_sd'],stdev(a['batch_values']),abs_tol=1e-12)
    paper=data['paper_figure_2_descriptive']['paper_runtime_ratio'];assert paper==1.73
    gap=a['mean']-paper;relative=100*gap/paper
    previous=root/'presentation/modules/module-04/versions/module-v0.0.json'
    old=json.loads(previous.read_text());asset=old['figures'][0]['formats']['png']
    old_png=root/'presentation/modules/module-04'/asset['path']
    assert sha(old_png)==asset['sha256']
    plan=root/'experiments/exp-001/PLAN.md';assert sha(plan)==data['plan_sha256']
    paper_pdf=root/'.local/sources/papers/addresssanitizer-atc12-2012.pdf'
    assert sha(paper_pdf)=='adf8b68d3dfeb8fac172e16e4e985a806226a9f904708c12a101d2b765b758e7'
    items=[];W,H=620,410
    def text(x,y,value,size=12,bold=False,anchor='start'):
        font='Times-Bold' if bold else 'Times-Roman';w=pdfmetrics.stringWidth(value,font,size)
        x0=x-w if anchor=='end' else x-w/2 if anchor=='middle' else x
        assert x0>=23 and x0+w<=597,(value,x0,w)
        items.append({'kind':'text','x':x,'y':y,'value':value,'size':size,'bold':bold,'anchor':anchor})
    def rule(y,weight=1.0):items.append({'kind':'line','x1':24,'x2':596,'y':y,'weight':weight})
    text(24,H-24,'Main experiment: batch summary and paper comparison',14,True)
    text(24,H-41,'Six Olden benchmarks; three independent ARM64 VM batches',11)
    rule(H-57)
    text(30,H-74,'VM batch',12,True)
    text(590,H-74,'Suite runtime ratio (×)',12,True,'end')
    rule(H-83,.55)
    for b,(value,y) in enumerate(zip(a['batch_values'],[H-105,H-129,H-153]),1):
        text(30,y,f'Batch {b}',12.4)
        text(590,y,f'{value:.4f}',12.4,anchor='end')
    text(30,H-184,'Mean ± SD',12.4,True)
    text(590,H-184,f"{a['mean']:.4f} ± {a['sample_sd']:.4f}",12.4,True,'end')
    rule(H-199)
    text(24,H-224,'Paper vs. Ours',12,True)
    rule(H-236)
    for x,value,anchor in [(30,'Metric','start'),(209,'Paper (Figure 2)','middle'),(354,'Ours','middle'),(520,'Descriptive gap','middle')]:
        text(x,H-253,value,11,True,anchor)
    rule(H-262,.55)
    text(30,H-287,'Runtime ratio',11.6)
    text(209,H-287,f'{paper:.2f}×',12.2,anchor='middle')
    text(354,H-287,f"{a['mean']:.4f} ± {a['sample_sd']:.4f}×",12.2,True,'middle')
    text(520,H-287,f'+{gap:.4f}×',12.2,anchor='middle')
    text(520,H-301,f'(+{relative:.2f}% relative)',10.2,anchor='middle')
    rule(H-316)
    notes=[
        'Ours: suite ratios are equal-weight arithmetic means of six program ratios (ASan mean / baseline mean).',
        'Five timings per arm and program; 60 timings per batch; warmups excluded.',
        'Ours: mean ± sample SD across n = 3 VM batches; all six programs retained, including short-running mst.',
        'Descriptive comparison only; platform/workload differences are in Module 3. Paper SD is not reported.',
        'Sources: formal exp-001 v0.2; Serebryany et al., USENIX ATC 2012, §4 / Figure 2.'
    ]
    for note,y in zip(notes,[H-333,H-346,H-359,H-372,H-385]):text(24,y,note,9.4)
    out.mkdir(parents=True,exist_ok=True)
    pdf=out/(STEM+'.pdf')
    c=canvas.Canvas(str(pdf),pagesize=(W,H),pageCompression=1,invariant=1)
    c.setTitle('Main experiment: batch summary and compact paper comparison')
    c.setAuthor('OS-project')
    c.setSubject('Three formal VM batches; compact descriptive paper comparison; only PNG approved for asset archival')
    for item in items:
        if item['kind']=='line':c.setLineWidth(item['weight']);c.line(item['x1'],item['y'],item['x2'],item['y'])
        else:
            c.setFont('Times-Bold' if item['bold'] else 'Times-Roman',item['size'])
            method={'start':c.drawString,'middle':c.drawCentredString,'end':c.drawRightString}[item['anchor']]
            method(item['x'],item['y'],item['value'])
    c.showPage();c.save()
    if args.pymupdf_dir:sys.path.insert(0,str(args.pymupdf_dir))
    import fitz
    doc=fitz.open(pdf);png=out/(STEM+'.png')
    doc[0].get_pixmap(dpi=400,alpha=False).save(png)
    metadata={
        'artifact_id':'module-04-main-batch-summary','exact_version':'v0.1','created_date':'2026-11-26','timezone':'Asia/Shanghai',
        'authorization':'User explicitly requested combining only the selected compact Paper vs. Ours row with the accepted first image and archiving only the new combined image.',
        'asset_archive_allowlist':[STEM+'.png'],
        'excluded_from_asset_archive':'Only the new PNG is an archived figure format. Auxiliary PDF remains temporary. Generator and provenance are supporting records; unapproved program plot and detailed comparison previews are not archived.',
        'source_campaign':CAMPAIGN,'batch_values':a['batch_values'],'ours_mean':a['mean'],'ours_sample_sd':a['sample_sd'],'statistical_n':3,
        'paper_runtime_ratio':paper,'absolute_ratio_gap':gap,'relative_gap_percent':relative,
        'source_hashes':{str(p.relative_to(root)):sha(p) for p in [source,plan,previous,old_png,paper_pdf]},
        'generator_sha256':sha(Path(__file__)),
        'statistics':'ASan/baseline ratio of five-run means per program; equal-weight arithmetic mean of six program ratios within batch; mean and sample SD across three independent VM batches.',
        'comparison_scope':'Descriptive comparison across different workloads/platforms; numerical equivalence and causal attribution are not established. Setup differences are referenced to Module 3.',
        'notes':notes,'page_points':[W,H],'png_dpi':400,
        'known_results':'All original formal main, extension and clean-entry acceptance results were known before this presentation change. No new observation or experimental change.',
        'outputs':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in [pdf,png]}
    }
    (out/'generation-v0.1.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'png':str(png),'page_points':[W,H],'ratio':a['mean'],'sd':a['sample_sd'],'gap':gap,'relative':relative},ensure_ascii=False))


if __name__=='__main__':main()
