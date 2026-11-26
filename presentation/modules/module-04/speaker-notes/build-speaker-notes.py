#!/usr/bin/env python3
"""Pair the two approved Module 4 figures with confirmed English narration.

Usage: python3 build-speaker-notes.py --output /tmp/module-04-notes.pdf
Requires Python 3, reportlab and Pillow. All project paths are module-relative.
The output must not already exist. Fonts are embedded; --font-dir is optional.
"""
import argparse
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

import reportlab
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def register_fonts(font_dir=None):
    installed = font_dir or Path('/System/Library/Fonts/Supplemental')
    bundled = Path(reportlab.__file__).parent / 'fonts'
    evidence = []
    for alias, preferred, fallback in [
        ('Body', 'Times New Roman.ttf', 'Vera.ttf'),
        ('BodyBold', 'Times New Roman Bold.ttf', 'VeraBd.ttf')
    ]:
        font = installed / preferred
        if not font.is_file():
            if font_dir:
                raise ValueError(f'Missing requested font: {preferred}')
            font = bundled / fallback
        pdfmetrics.registerFont(TTFont(alias, str(font)))
        evidence.append({'alias': alias, 'filename': font.name, 'sha256': sha256(font)})
    pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold')
    return evidence


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--module-dir', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--font-dir', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing an existing output; use a new output path.')
    module = args.module_dir.resolve()
    source = args.source or module / 'speaker-notes/source-v0.0.json'
    data = json.loads(source.read_text())
    index = json.loads((module / 'module.json').read_text())
    figures = {f['id']: f['formats']['png'] for f in index['figures']}
    sections = data['sections']
    if [s['number'] for s in sections] != [1, 2] or [s['id'] for s in sections] != ['main-batch-summary', 'program-runtime-ratios']:
        raise ValueError('Expected exactly the two confirmed figure/narration pairs in order.')
    for s in sections:
        expected = figures[s['id']]
        if s['image'] != expected['path'] or s['image_sha256'] != expected['sha256'] or sha256(module / s['image']) != s['image_sha256']:
            raise ValueError(f'Figure identity or SHA-256 mismatch: {s["id"]}')
        if len(s['zh']) != len(s['en']):
            raise ValueError('Chinese and English paragraph counts differ.')
    fonts = register_fonts(args.font_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    width, height = landscape(A3)
    c = canvas.Canvas(str(args.output), pagesize=(width, height), pageCompression=1, invariant=1)
    c.setTitle('Module 04 - English speaker notes')
    c.setAuthor('CS340 paper replication project')
    c.setSubject('Two archived main-result figures paired with English translations of the confirmed Chinese narration')
    c.setCreator('ReportLab; AI-assisted translation and layout')
    left, gap, margin, left_w = 42, 32, 42, 526
    right = left + left_w + gap
    right_w = width - right - margin
    body = ParagraphStyle('Narration', fontName='Body', fontSize=14, leading=20, textColor=colors.black)
    small = ParagraphStyle('Reference', fontName='Body', fontSize=9.2, leading=12.5, textColor=colors.HexColor('#555555'))
    page_records = []
    for s in sections:
        n = s['number']
        c.bookmarkPage(s['id'])
        c.addOutlineEntry(f'{n}. {s["title"]}', s['id'], level=0, closed=False)
        c.setFillColor(colors.HexColor('#555555'))
        c.setFont('Body', 10)
        c.drawString(left, height - 35, 'MODULE 04  /  MAIN RESULTS')
        c.setFillColor(colors.black)
        c.setFont('BodyBold', 25)
        heading = f'Figure {n}. {s["title"]}'
        if pdfmetrics.stringWidth(heading, 'BodyBold', 25) > width - left - margin:
            raise RuntimeError('Heading exceeds page width.')
        c.drawString(left, height - 72, heading)
        c.setStrokeColor(colors.black)
        c.setLineWidth(.65)
        c.line(left, height - 91, width - margin, height - 91)
        c.setFont('BodyBold', 11)
        c.drawString(left, height - 114, 'Corresponding figure')
        c.drawString(right, height - 114, 'English narration')
        image_path = module / s['image']
        with Image.open(image_path) as im:
            iw, ih = im.size
        scale = min(left_w / iw, 475 / ih)
        dw, dh = iw * scale, ih * scale
        top, bottom = height - 148, 190
        iy = bottom + (top - bottom - dh) / 2
        ix = left + (left_w - dw) / 2
        c.drawImage(str(image_path), ix, iy, dw, dh, preserveAspectRatio=True, mask='auto')
        cap = Paragraph(f'<b>Figure {n} asset</b><br/>{escape(image_path.name)}', small)
        _, ch = cap.wrap(left_w, 80)
        cap.drawOn(c, left, 155 - ch)
        refs = Paragraph('Reference notes (not spoken):<br/>' + '<br/>'.join(escape(t) for t in s['reference_notes']), small)
        _, rh = refs.wrap(left_w, 100)
        if 104 - rh < 48:
            raise RuntimeError('Reference notes overlap the footer.')
        refs.drawOn(c, left, 104 - rh)
        y = height - 135
        for para in s['en']:
            p = Paragraph(escape(para), body)
            _, ph = p.wrap(right_w, 1000)
            if y - ph < 57:
                raise RuntimeError(f'Narration overflow on figure {n}.')
            p.drawOn(c, right, y - ph)
            y -= ph + 9
        if s.get('transition'):
            y -= 12
            c.setFont('BodyBold', 11)
            c.drawString(right, y - 11, 'Transition to the next figure')
            y -= 23
            p = Paragraph(escape(s['transition']['en']), body)
            _, ph = p.wrap(right_w, 1000)
            if y - ph < 57:
                raise RuntimeError('Transition overlaps footer.')
            p.drawOn(c, right, y - ph)
            y -= ph + 9
        c.setStrokeColor(colors.HexColor('#b0b0b0'))
        c.setLineWidth(.35)
        c.line(left, 42, width - margin, 42)
        c.setFillColor(colors.HexColor('#555555'))
        c.setFont('Body', 9)
        c.drawString(left, 26, 'Module 04 - English speaker notes v0.0 - 26 November 2026')
        c.drawRightString(width - margin, 26, f'{n} / 2')
        page_records.append({'page': n, 'figure_id': s['id'], 'asset': s['image'], 'image_sha256': s['image_sha256'], 'image_bounds_pt': [round(v, 2) for v in (ix, iy, dw, dh)], 'narration_bottom_pt': round(y, 2)})
        c.showPage()
    c.save()
    print(json.dumps({'pages': page_records, 'fonts': fonts, 'page_size_pt': [width, height], 'reportlab_version': reportlab.Version}, indent=2))


if __name__ == '__main__':
    main()
