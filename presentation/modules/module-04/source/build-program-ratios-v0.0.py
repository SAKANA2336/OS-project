#!/usr/bin/env python3
"""Create a temporary six-program plot from the sealed original exp-001 evidence.

Usage: python3 -B build-program-ratios.py --root <work-repository> --out <empty-directory>
Dependencies: ReportLab and pdftoppm. No experiment or repository write is performed.
"""
import argparse
import csv
import hashlib
import json
import math
import os
import subprocess
from pathlib import Path
from statistics import mean, stdev
from xml.sax.saxutils import escape

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

CAMPAIGN = "exp-001-v0-2-20261118t170938z"
ORDER = ("bisort", "em3d", "mst", "perimeter", "treeadd", "tsp")
STEM = "module-04-program-runtime-ratios-preview-v0.0"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def equal(actual, expected):
    if not math.isclose(actual, expected, rel_tol=1e-12, abs_tol=1e-12):
        raise AssertionError((actual, expected))


def read_and_check(root):
    source = root / "results" / CAMPAIGN / "summary.json"
    plan = root / "experiments/exp-001/PLAN.md"
    summary = json.loads(source.read_text())
    assert summary["experiment_id"] == "exp-001"
    assert summary["campaign_id"] == CAMPAIGN
    assert summary["missing_valid_batch_slots"] == []
    assert summary["plan_sha256"] == digest(plan)
    hashes = {str(p.relative_to(root)): digest(p) for p in (source, plan)}
    batches = sorted((a for a in summary["attempts"] if a["included"]),
                     key=lambda a: a["batch_slot"])
    assert [a["batch_slot"] for a in batches] == [0, 1, 2]
    input_rows = []
    for batch in batches:
        assert batch["status"] == "passed_batch"
        run_id = batch["run_id"]
        assert batch["vm_id"] == run_id
        guest = root / "runs" / run_id / "guest-evidence/data" / run_id
        record_path = guest / "metrics/records.json"
        assert digest(record_path) == batch["records_sha256"]
        hashes[str(record_path.relative_to(root))] = digest(record_path)
        records = json.loads(record_path.read_text())
        assert len(records) == 72 and len({r["sample_id"] for r in records}) == 72
        for r in records:
            assert r["experiment_id"] == "exp-001" and r["batch_slot"] == batch["batch_slot"]
            assert r["valid"] and r["reference_match"]
            assert r["exit_code"] == r["program_exit_code"] == 0
            assert not r["timed_out"] and not r["sanitizer_report"]
            raw = guest / "raw-outputs" / (r["sample_id"] + ".time.txt")
            raw_fields = dict(line.split() for line in raw.read_text().splitlines())
            assert int(raw_fields["exit"]) == 0
            for field in ("real", "user", "sys"):
                assert float(raw_fields[field]) == r[field + "_seconds"]
        timed = [r for r in records if r["phase"] == "measure"]
        assert len(timed) == 60
        assert len([r for r in records if r["phase"] == "warmup"]) == 12
        for name in ORDER:
            means = {}
            for arm in ("baseline", "asan"):
                values = [r["real_seconds"] for r in timed
                          if r["benchmark"] == name and r["arm"] == arm]
                assert len(values) == 5 and all(v > 0 and math.isfinite(v) for v in values)
                means[arm] = mean(values)
                equal(means[arm], batch["batch"]["benchmarks"][name]["arms"][arm]["mean_seconds"])
            ratio = means["asan"] / means["baseline"]
            equal(ratio, batch["batch"]["benchmarks"][name]["runtime_ratio"])
            input_rows.append({"program": name, "batch": batch["batch_slot"] + 1,
                               "run_id": run_id, "baseline_mean_seconds": means["baseline"],
                               "asan_mean_seconds": means["asan"], "runtime_ratio": ratio,
                               "timed_executions_per_arm": 5})
    plotted = []
    for name in ORDER:
        group = [r for r in input_rows if r["program"] == name]
        values = [r["runtime_ratio"] for r in group]
        mu, sd = mean(values), stdev(values)
        expected = summary["aggregate"]["benchmarks"][name]
        assert expected["n"] == len(values) == 3
        assert expected["batch_values"] == values
        equal(mu, expected["mean"])
        equal(sd, expected["sample_sd"])
        short = any(r["baseline_mean_seconds"] < .050 or r["asan_mean_seconds"] < .050 for r in group)
        assert short == (name == "mst")
        plotted.append({"program": name, "mean_runtime_ratio": mu,
                        "batch_sample_sd": sd, "n_vm_batches": len(values),
                        "short_run_flag": short, "display": f"{mu:.4f} ± {sd:.4f}"})
    return plotted, input_rows, hashes


def design(rows):
    width, height = 560, 375
    x_min, x_max, plot_left, plot_right = .8, 5., 105., 408.
    plot_bottom, plot_top = 92., 300.
    marks = []
    def x(value):
        assert x_min <= value <= x_max, value
        return plot_left + (value - x_min) / (x_max - x_min) * (plot_right - plot_left)
    def text(px, py, value, size=10, bold=False, anchor="start"):
        font = "Times-Bold" if bold else "Times-Roman"
        tw = pdfmetrics.stringWidth(value, font, size)
        left = px - (tw if anchor == "end" else tw/2 if anchor == "middle" else 0)
        assert 23 <= left and left + tw <= width - 23, (value, left, tw)
        assert 10 <= py and py + size <= height - 10
        marks.append({"kind": "text", "x": px, "y": py, "text": value,
                      "size": size, "bold": bold, "anchor": anchor})
    def line(x1, y1, x2, y2, weight=.8, gray=0., dash=None):
        assert 0 <= x1 <= width and 0 <= x2 <= width
        assert 0 <= y1 <= height and 0 <= y2 <= height
        marks.append({"kind": "line", "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                      "weight": weight, "gray": gray, "dash": dash})
    text(24, 350, "Main experiment: program runtime ratios", 13.5, True)
    text(24, 331, "Mean ± sample SD across three independent ARM64 VM batches (n = 3)", 10)
    text(plot_left, 310, "Baseline = 1.0", 9)
    text(536, 310, "Mean ± SD", 10, True, "end")
    y_rows = (286, 251, 216, 181, 146, 111)
    for y in y_rows:
        line(plot_left, y, plot_right, y, .35, .87)
    line(x(1.), plot_bottom, x(1.), plot_top, .8, .30, [3, 3])
    for row, y in zip(rows, y_rows):
        mu, sd = row["mean_runtime_ratio"], row["batch_sample_sd"]
        text(24, y-3.5, row["program"], 11)
        line(x(mu-sd), y, x(mu+sd), y, 1.05)
        line(x(mu-sd), y-3.4, x(mu-sd), y+3.4, 1.05)
        line(x(mu+sd), y-3.4, x(mu+sd), y+3.4, 1.05)
        marks.append({"kind": "circle", "x": x(mu), "y": y, "radius": 2.7})
        text(536, y-3.5, row["display"], 10.3, False, "end")
    line(plot_left, plot_bottom, plot_right, plot_bottom, .8)
    for tick in (1., 2., 3., 4., 5.):
        line(x(tick), plot_bottom, x(tick), plot_bottom-3.5, .8)
        text(x(tick), 75, f"{tick:.1f}", 9.5, False, "middle")
    text((plot_left+plot_right)/2, 56, "Runtime ratio (ASan / baseline, ×)", 10.5, False, "middle")
    text(24, 36, "Each batch ratio uses five timed executions per arm; warmups are excluded.", 8.5)
    text(24, 24, "mst: baseline mean < 0.050 s in all three batches; retained in the main analysis.", 8.5)
    text(24, 12, "Source: original formal exp-001, frozen PLAN v0.2. Error bars show ±1 batch sample SD.", 8.5)
    return width, height, marks


def render(out, rows, renderer):
    width, height, marks = design(rows)
    pdf = out / (STEM + ".pdf")
    c = canvas.Canvas(str(pdf), pagesize=(width, height), invariant=1)
    c.setTitle("ASan runtime ratios for six Olden programs")
    c.setAuthor("OS-project; temporary preview from original formal exp-001 evidence")
    c.setSubject("Three independent VM batches; means and batch sample SD; preview only")
    for m in marks:
        if m["kind"] == "text":
            c.setFillGray(0)
            c.setFont("Times-Bold" if m["bold"] else "Times-Roman", m["size"])
            method = {"start": c.drawString, "end": c.drawRightString, "middle": c.drawCentredString}[m["anchor"]]
            method(m["x"], m["y"], m["text"])
        elif m["kind"] == "line":
            c.setStrokeGray(m["gray"])
            c.setLineWidth(m["weight"])
            c.setDash(m["dash"] or [])
            c.line(m["x1"], m["y1"], m["x2"], m["y2"])
        else:
            c.setFillGray(0)
            c.setDash([])
            c.circle(m["x"], m["y"], m["radius"], stroke=0, fill=1)
    c.showPage()
    c.save()
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}pt" height="{height}pt" viewBox="0 0 {width} {height}">',
           '<title>ASan runtime ratios for six Olden programs</title>',
           '<desc>Means and plus or minus one batch sample standard deviation across three original formal ARM64 VM batches.</desc>',
           f'<rect width="{width}" height="{height}" fill="white"/>']
    for m in marks:
        if m["kind"] == "text":
            weight = "bold" if m["bold"] else "normal"
            svg.append(f'<text x="{m["x"]}" y="{height-m["y"]}" font-family="Times New Roman, Times, serif" font-size="{m["size"]}" font-weight="{weight}" text-anchor="{m["anchor"]}" fill="black">{escape(m["text"])}</text>')
        elif m["kind"] == "line":
            gray = round(m["gray"] * 255)
            dash = (' stroke-dasharray="' + ','.join(str(v) for v in m["dash"]) + '"') if m["dash"] else ''
            svg.append(f'<line x1="{m["x1"]}" y1="{height-m["y1"]}" x2="{m["x2"]}" y2="{height-m["y2"]}" stroke="rgb({gray},{gray},{gray})" stroke-width="{m["weight"]}"{dash}/>')
        else:
            svg.append(f'<circle cx="{m["x"]}" cy="{height-m["y"]}" r="{m["radius"]}" fill="black"/>')
    svg.append("</svg>")
    (out / (STEM + ".svg")).write_text("\n".join(svg) + "\n")
    # Keep font lookup/cache inside the explicitly authorized temporary subtree.
    font_cache = out / "font-cache"
    font_cache.mkdir()
    font_config = out / "fonts.conf"
    font_config.write_text('<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n'
                           '<fontconfig><cachedir>' + escape(str(font_cache)) + '</cachedir></fontconfig>\n')
    render_env = dict(os.environ, FONTCONFIG_FILE=str(font_config), FONTCONFIG_PATH=str(out),
                      XDG_CACHE_HOME=str(font_cache))
    process = subprocess.run([str(renderer), "-r", "360", "-singlefile", "-png", str(pdf), str(out/STEM)],
                             check=True, capture_output=True, text=True, env=render_env)
    return {"page_points": [width, height], "png_dpi": 360,
            "renderer_stdout": process.stdout, "renderer_stderr": process.stderr,
            "text_and_geometry_bounds": "passed"}


def write_csv(path, rows):
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--pdftoppm", type=Path, default=Path("pdftoppm"))
    parser.add_argument("--font-dir", type=Path, required=True,
                        help="Directory containing Times New Roman.ttf and Times New Roman Bold.ttf")
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    assert out != root and root not in out.parents, "Generate outside the source repository"
    assert not out.exists() or (out.is_dir() and not any(out.iterdir())), "Output directory must be new or empty"
    out.mkdir(parents=True, exist_ok=True)
    expected_outputs = [out/(STEM+ext) for ext in (".csv", ".json", ".pdf", ".svg", ".png")]
    expected_outputs += [out/"batch-inputs.csv", out/"generation-v0.0.json"]
    assert not any(p.exists() for p in expected_outputs), "Do not overwrite an earlier preview"
    rows, inputs, hashes = read_and_check(root)
    fonts = {"Times-Roman": args.font_dir / "Times New Roman.ttf",
             "Times-Bold": args.font_dir / "Times New Roman Bold.ttf"}
    for name, path in fonts.items():
        pdfmetrics.registerFont(TTFont(name, str(path)))
    write_csv(out/(STEM+".csv"), rows)
    write_csv(out/"batch-inputs.csv", inputs)
    (out/(STEM+".json")).write_text(json.dumps(rows, indent=2, ensure_ascii=False)+"\n")
    rendering = render(out, rows, args.pdftoppm)
    metadata = {
        "artifact_id": "module-04-program-runtime-ratios-preview", "exact_version": "v0.0",
        "status": "temporary_preview_only_not_archived", "created_date": "2026-11-26",
        "source_campaign": CAMPAIGN, "source_plan": "exp-001 PLAN v0.2, Section 4",
        "source_hashes": hashes, "generator_sha256": digest(Path(__file__)),
        "program_order": list(ORDER), "plotted_rows": rows,
        "statistics": "For each program and batch: arithmetic mean ASan wall-clock seconds divided by arithmetic mean baseline wall-clock seconds, using five measured executions per arm. Each point is the arithmetic mean of its three batch ratios; each error bar is plus or minus one sample SD (denominator n-1), n=3 independent fresh VM batches on the same host. Warmups are excluded.",
        "checks": {"underlying_records": 216, "timed_executions": 180, "warmups_excluded": 36,
                   "program_batch_ratios_recomputed": 18, "program_means_checked": 6,
                   "program_sample_sds_checked": 6, "raw_time_files_checked": 216,
                   "source_record_hashes": "passed", "summary_and_raw_statistics_agreement": "passed"},
        "display_decimal_places": 4, "rounding": "Display only. CSV/JSON retain full precision.",
        "axis": {"scale": "linear", "limits": [.8, 5.], "baseline_reference": 1.,
                 "interpretation": "Dimensionless ASan/baseline runtime ratio; greater than one means longer runtime."},
        "design": {"type": "horizontal dot and error-bar plot with numerical mean-SD column",
                   "palette": "black and neutral grays on white", "font": "Embedded Times New Roman, regular and bold",
                   "font_hashes": {path.name: digest(path) for path in fonts.values()},
                   **rendering},
        "caption": "Program-level ASan runtime ratios in the original formal main experiment. Points show the mean and horizontal error bars show plus or minus one batch sample SD across three independent ARM64 VM batches (n=3). All six programs are retained, including short-running mst.",
        "experimental_impact": "None. No new measurements, protocol or verdict changes, raw-evidence edits, repository writes or archive/index updates.",
        "rebuild": "python3 -B build-program-ratios.py --root <work-repository> --out <new-directory-inside-authorized-preview-subtree> --pdftoppm <renderer> --font-dir <Times-New-Roman-directory>",
    }
    metadata["outputs"] = {p.name: {"bytes": p.stat().st_size, "sha256": digest(p)}
                           for p in sorted(out.iterdir()) if p.is_file()}
    (out/"generation-v0.0.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False)+"\n")
    print(json.dumps({"status": "generated", "directory": str(out), "programs": rows,
                      "checks": metadata["checks"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
