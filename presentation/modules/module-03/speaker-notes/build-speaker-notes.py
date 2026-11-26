#!/usr/bin/env python3
"""Build the five-figure English notes PDF; refuse to overwrite an existing output.

Usage: python3 build-speaker-notes.py --output /tmp/module-03-notes.pdf
Dependencies: reportlab, Pillow. Source and image paths resolve from this module.
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
from reportlab.platypus import Flowable, Paragraph


def register_fonts():
    installed = Path('/System/Library/Fonts/Supplemental')
    bundled = Path(reportlab.__file__).parent / 'fonts'
    names = [('Body', 'Times New Roman.ttf', 'Vera.ttf'),
             ('BodyBold', 'Times New Roman Bold.ttf', 'VeraBd.ttf'),
             ('BodyItalic', 'Times New Roman Italic.ttf', 'VeraIt.ttf')]
    evidence = []
    for alias, system_name, fallback_name in names:
        font = installed / system_name
        if not font.is_file():
            font = bundled / fallback_name
        pdfmetrics.registerFont(TTFont(alias, str(font)))
        evidence.append({'alias': alias, 'filename': font.name,
                         'sha256': hashlib.sha256(font.read_bytes()).hexdigest()})
    pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='BodyItalic', boldItalic='BodyBold')
    return evidence


class Equation(Flowable):
    """Typeset the four equations as vector text, with actual bars and fractions."""
    def __init__(self, number, width):
        Flowable.__init__(self)
        self.number, self.width = number, width
        self.height = 54 if number == 3 else 46

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(colors.black)
        c.setStrokeColor(colors.black)
        c.setLineWidth(0.55)
        fs, y = 16, 17

        def text(x, baseline, value, size=fs, font='BodyItalic'):
            c.setFont(font, size)
            c.drawString(x, baseline, value)
            return pdfmetrics.stringWidth(value, font, size)

        def term(x, baseline, value, sub='', sup='', bar=False):
            w = text(x, baseline, value)
            if bar:
                c.line(x, baseline + fs * .91, x + w, baseline + fs * .91)
            sw = 0
            if sub:
                sw = max(sw, text(x + w + 1, baseline - 4.5, sub, 9.5))
            if sup:
                sw = max(sw, text(x + w + 1, baseline + 7.5, sup, 9.5))
            return w + sw + (1 if sw else 0)

        def fraction(x, numerator, denominator):
            wn = pdfmetrics.stringWidth(numerator, 'Body', 12)
            wd = pdfmetrics.stringWidth(denominator, 'Body', 12)
            w = max(wn, wd) + 8
            text(x + (w - wn)/2, y + 8, numerator, 12, 'Body')
            text(x + (w - wd)/2, y - 8, denominator, 12, 'Body')
            c.line(x, y + 4, x + w, y + 4)
            return w

        def sigma(x, lower, upper):
            w = text(x + 3, y - 3, '∑', 22, 'Body')
            text(x + 5, y + 18, upper, 9, 'Body')
            text(x, y - 16, lower, 9, 'BodyItalic')
            return max(w + 9, pdfmetrics.stringWidth(lower, 'BodyItalic', 9) + 4)

        x = 9
        if self.number == 0:
            x += term(x, y, 'R', sub='b,w') + 6
            x += text(x, y, ' = ', font='Body')
            x += term(x, y, 't', sub='b,w', sup='A', bar=True) + 7
            x += text(x, y, '/', font='Body') + 7
            term(x, y, 't', sub='b,w', sup='B', bar=True)
        elif self.number == 1:
            x += term(x, y, 'A', sub='b') + 5
            x += text(x, y, ' = ', font='Body')
            x += fraction(x, '1', '6') + 9
            x += sigma(x, 'w=1', '6') + 4
            term(x, y, 'R', sub='b,w')
        elif self.number == 2:
            x += term(x, y, 'A', bar=True) + 5
            x += text(x, y, ' = ', font='Body')
            x += fraction(x, '1', '3') + 9
            x += sigma(x, 'b=1', '3') + 4
            term(x, y, 'A', sub='b')
        else:
            x += term(x, y, 's', sub='A') + 5
            x += text(x, y, ' = ', font='Body')
            root_x = x
            x += 23
            radicand_start = x
            x += fraction(x, '1', '3 - 1') + 8
            x += sigma(x, 'b=1', '3') + 5
            x += text(x, y, '(', font='Body') + 1
            x += term(x, y, 'A', sub='b')
            x += text(x, y, ' - ', font='Body')
            x += term(x, y, 'A', bar=True)
            x += text(x, y, ')', font='Body')
            x += text(x, y + 8, '2', 9.5, 'Body')
            radical = c.beginPath()
            radical.moveTo(root_x, y + 3)
            radical.lineTo(root_x + 5, y + 6)
            radical.lineTo(root_x + 11, y - 10)
            radical.lineTo(root_x + 21, y + 29)
            radical.lineTo(x + 2, y + 29)
            c.drawPath(radical)
        c.restoreState()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    default_module = Path(__file__).resolve().parent.parent
    parser.add_argument('--module-dir', type=Path, default=default_module)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    module = args.module_dir.resolve()
    source = args.source or module / 'speaker-notes/source-v0.0.json'
    if args.output.exists():
        raise SystemExit('Refusing an existing output; use a new output path.')
    data = json.loads(source.read_text())
    assert [s['number'] for s in data['sections']] == list(range(1, 6))
    module_index = json.loads((module / 'module.json').read_text())
    images = {x['id']: x for x in module_index['images']}
    for s in data['sections']:
        assert s['image'] == images[s['id']]['path']
        assert hashlib.sha256((module / s['image']).read_bytes()).hexdigest() == images[s['id']]['sha256']

    fonts = register_fonts()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    width, height = landscape(A3)
    c = canvas.Canvas(str(args.output), pagesize=(width, height), pageCompression=1, invariant=1)
    c.setTitle('Module 03 - English speaker notes')
    c.setAuthor('CS340 paper replication project')
    c.setSubject('Five archived figures paired with the English translation of the confirmed Chinese narration')
    c.setCreator('ReportLab; AI-assisted translation and layout')
    left, gap, margin = 42, 32, 42
    left_w = 526
    right = left + left_w + gap
    right_w = width - right - margin
    body_style = ParagraphStyle('Narration', fontName='Body', fontSize=14, leading=20, textColor=colors.black)
    small_style = ParagraphStyle('Reference', fontName='Body', fontSize=9.2, leading=12.5, textColor=colors.HexColor('#555555'))
    page_records = []

    for section in data['sections']:
        n = section['number']
        c.bookmarkPage(section['id'])
        c.addOutlineEntry(f'{n}. {section["title"]}', section['id'], level=0, closed=False)
        c.setFont('Body', 10)
        c.setFillColor(colors.HexColor('#555555'))
        c.drawString(left, height - 35, 'MODULE 03  /  REPRODUCTION SETUP AND METHODOLOGY')
        c.setFillColor(colors.black)
        c.setFont('BodyBold', 25)
        c.drawString(left, height - 72, f'Figure {n}. {section["title"]}')
        c.setStrokeColor(colors.black)
        c.setLineWidth(.65)
        c.line(left, height - 91, width - margin, height - 91)
        c.setFont('BodyBold', 11)
        c.drawString(left, height - 114, 'Corresponding figure')
        c.drawString(right, height - 114, 'English narration')

        image_path = module / section['image']
        with Image.open(image_path) as image:
            iw, ih = image.size
        ratio = min(left_w / iw, 475 / ih)
        dw, dh = iw * ratio, ih * ratio
        image_top = height - 148
        image_region_bottom = 190
        iy = image_region_bottom + (image_top - image_region_bottom - dh) / 2
        c.drawImage(str(image_path), left + (left_w - dw)/2, iy, dw, dh, preserveAspectRatio=True, mask='auto')

        caption = Paragraph(f'<b>Figure {n} asset</b><br/>{escape(image_path.name)}', small_style)
        _, cap_h = caption.wrap(left_w, 80)
        caption.drawOn(c, left, 155 - cap_h)
        refs = 'Reference notes (not spoken):<br/>Project method: frozen exp-001 protocol v0.2, Sections 2-4.'
        if n == 2:
            refs += '<br/>Paper: Serebryany et al., <i>AddressSanitizer: A Fast Address Sanity Checker</i>, USENIX ATC 2012, Section 4.'
        if n == 5:
            refs += '<br/>Workloads: LLVM Test Suite llvmorg-18.1.3, Olden.'
        note = Paragraph(refs, small_style)
        _, nh = note.wrap(left_w, 90)
        note.drawOn(c, left, 104 - nh)

        y = height - 135
        equations = section.get('equations', [])
        for i, para in enumerate(section['en']):
            p = Paragraph(escape(para), body_style)
            _, ph = p.wrap(right_w, 1000)
            if y - ph < 57:
                raise RuntimeError(f'Narration overflow on figure {n}, paragraph {i}: {y-ph}')
            p.drawOn(c, right, y - ph)
            y -= ph + 9
            for equation_number, equation in enumerate(equations):
                if equation['after'] == i:
                    eq = Equation(equation_number, right_w)
                    eq.drawOn(c, right, y - eq.height + 2)
                    y -= eq.height + 1
        if y < 48:
            raise RuntimeError(f'Equation overflow on figure {n}: {y}')

        c.setStrokeColor(colors.HexColor('#b0b0b0'))
        c.setLineWidth(.35)
        c.line(left, 42, width - margin, 42)
        c.setFillColor(colors.HexColor('#555555'))
        c.setFont('Body', 9)
        c.drawString(left, 26, 'Module 03 - English speaker notes v0.0 - 26 November 2026')
        c.drawRightString(width - margin, 26, f'{n} / 5')
        page_records.append({'page': n, 'figure_id': section['id'], 'asset': section['image'], 'narration_bottom_pt': round(y, 2)})
        c.showPage()
    c.save()
    print(json.dumps({'pages': page_records, 'fonts': fonts, 'page_size_pt': [width, height], 'reportlab_version': reportlab.Version}, indent=2))


if __name__ == '__main__':
    main()
