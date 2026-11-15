#!/usr/bin/env python3
"""Acquire pinned LLVM workloads and run a bounded ASan pilot on Linux."""

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import signal
import statistics
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def normalize_crlf_bytes(data):
    return data.replace(b"\r\n", b"\n")


def normalize_crlf(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(normalize_crlf_bytes(Path(source).read_bytes()))


def within(root, relative):
    candidate = (Path(root) / relative).resolve()
    if not candidate.is_relative_to(Path(root).resolve()):
        raise ValueError("Path escapes its declared root")
    return candidate


def command(argv, prefix, timeout, cwd=None, env=None):
    """Keep stdout, stderr and failure state, including on a timeout."""
    prefix = Path(prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    metadata = {"argv": [str(x) for x in argv], "timeout_seconds": timeout}
    start = time.monotonic()
    with prefix.with_suffix(".stdout.log").open("wb") as out:
        with prefix.with_suffix(".stderr.log").open("wb") as err:
            process = subprocess.Popen(
                [str(x) for x in argv], cwd=cwd, env=env, stdout=out, stderr=err,
                start_new_session=(os.name != "nt"),
            )
            try:
                metadata["exit_code"] = process.wait(timeout=timeout)
                metadata["timed_out"] = False
            except subprocess.TimeoutExpired:
                if os.name == "nt":
                    process.kill()
                else:
                    os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                metadata.update(exit_code=process.returncode, timed_out=True)
    metadata["elapsed_seconds"] = time.monotonic() - start
    save(prefix.with_suffix(".command.json"), metadata)
    return metadata


def checked(argv, prefix, timeout, **kwargs):
    result = command(argv, prefix, timeout, **kwargs)
    if result["timed_out"] or result["exit_code"] != 0:
        raise RuntimeError("Command failed; inspect " + str(prefix) + ".stderr.log")
    return result


def check_source(source, config):
    source = Path(source).resolve()
    lock = load(ROOT / "workloads/llvm-suite-lock.json")
    if lock["commit"] != config["source"]["commit"]:
        raise ValueError("Workload lock and configuration disagree")
    for item in lock["files"]:
        path = within(source, item["path"])
        if not path.is_file() or sha256(path) != item["sha256"]:
            raise ValueError("Upstream file missing or changed: " + item["path"])
    # CMake discovers sources using globs: reject extra sources as well.
    for benchmark in config["benchmarks"]:
        directory = benchmark["directory"]
        actual = {
            p.relative_to(source).as_posix()
            for p in within(source, directory).rglob("*") if p.is_file()
        }
        expected = {f["path"] for f in lock["files"] if f["path"].startswith(directory + "/")}
        if actual != expected:
            raise ValueError("Unexpected files in benchmark: " + directory)
    return {"commit": lock["commit"], "files_verified": len(lock["files"])}


def fetch(args, config):
    source = Path(args.source).resolve()
    logs = ROOT / "scratch" / ("llvm-fetch-" + time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
    logs.mkdir(parents=True, exist_ok=False)
    git = ["git", "-c", "http.sslBackend=openssl", "-c", "credential.helper="]
    if args.proxy is not None:
        git += ["-c", "http.proxy=" + args.proxy]
    git += ["-c", "http.lowSpeedLimit=1024", "-c", "http.lowSpeedTime=25"]
    if not source.exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        checked(
            git + ["clone", "--depth", "1", "--filter=blob:none", "--sparse",
                   "--config", "core.autocrlf=false", "--branch", config["source"]["tag"],
                   "--single-branch", config["source"]["url"], str(source)],
            logs / "clone", 300,
        )
        checked(
            git + ["-C", str(source), "sparse-checkout", "set"]
            + config["source"]["sparse_directories"],
            logs / "checkout", 180,
        )
    revision = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True, timeout=15,
    ).strip()
    if revision != config["source"]["commit"]:
        raise ValueError("Existing checkout has a different commit; use another destination")
    print(json.dumps(check_source(source, config), indent=2))


def parse_time(path):
    data = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        key, value = line.split()
        data[key] = int(value) if key == "exit" else float(value)
    if not {"exit", "real", "user", "sys"}.issubset(data):
        raise ValueError("Incomplete upstream timeit output")
    return data


def check_isolation(config, source, output):
    limits = config["limits"]
    memory_unit = {"m": 1024 ** 2, "g": 1024 ** 3}
    memory_budget = int(limits["memory"][:-1]) * memory_unit[limits["memory"][-1].lower()]
    cgroup = Path("/sys/fs/cgroup")
    cpu_quota, cpu_period = (cgroup / "cpu.max").read_text().split()
    status = dict(
        line.split(":", 1) for line in Path("/proc/self/status").read_text().splitlines()
        if ":" in line
    )
    checks = {
        "non_root": os.geteuid() != 0,
        "cpu_limit": cpu_quota != "max" and int(cpu_quota) / int(cpu_period) <= limits["cpus"],
        "memory_limit": int((cgroup / "memory.max").read_text()) <= memory_budget,
        "no_swap": (cgroup / "memory.swap.max").read_text().strip() == "0",
        "pid_limit": int((cgroup / "pids.max").read_text()) <= limits["pids"],
        "no_capabilities": int(status["CapEff"].strip(), 16) == 0,
        "no_new_privileges": status["NoNewPrivs"].strip() == "1",
        "network_disabled": set(os.listdir("/sys/class/net")) == {"lo"},
        "readonly_root": bool(os.statvfs("/").f_flag & os.ST_RDONLY),
        "readonly_project": bool(os.statvfs(ROOT).f_flag & os.ST_RDONLY),
        "readonly_source": bool(os.statvfs(source).f_flag & os.ST_RDONLY),
    }
    save(output / "validation/isolation.json", checks)
    if not all(checks.values()):
        raise ValueError("Container isolation differs from plan; inspect validation/isolation.json")


def summarize(records, config):
    rows = []
    for benchmark in config["benchmarks"]:
        name = benchmark["name"]
        groups = {}
        for arm in ("baseline", "asan"):
            samples = [
                r for r in records
                if r["benchmark"] == name and r["arm"] == arm and r["phase"] == "measure"
            ]
            indexes = [r["iteration"] for r in samples]
            complete = sorted(indexes) == list(range(1, config["repetitions"] + 1))
            valid = [
                r for r in samples
                if r["valid"] and isinstance(r.get("real_seconds"), (float, int))
                and math.isfinite(r["real_seconds"]) and r["real_seconds"] > 0
            ]
            times = [r["real_seconds"] for r in valid]
            warmups = [
                r for r in records
                if r["benchmark"] == name and r["arm"] == arm and r["phase"] == "warmup"
            ]
            warmup_complete = (
                sorted(r["iteration"] for r in warmups)
                == list(range(1, config["warmups"] + 1))
                and all(r["valid"] for r in warmups)
            )
            ok = complete and len(valid) == config["repetitions"] and warmup_complete
            groups[arm] = {
                "complete": ok, "valid_runs": len(valid),
                "warmups_valid": warmup_complete,
                "invalid_or_missing": max(0, config["repetitions"] - len(valid)),
                "mean_seconds": statistics.mean(times) if times else None,
                "sample_stddev_seconds": statistics.stdev(times) if len(times) >= 2 else None,
            }
        complete = all(g["complete"] for g in groups.values())
        baseline_mean = groups["baseline"]["mean_seconds"]
        asan_mean = groups["asan"]["mean_seconds"]
        ratio = asan_mean / baseline_mean if complete else None
        rows.append({
            "benchmark": name, **groups,
            "status": "valid_pilot" if complete else "incomplete_or_invalid",
            "runtime_ratio": ratio,
            "overhead_percent": (ratio - 1) * 100 if ratio is not None else None,
            "short_run_warning": complete and min(baseline_mean, asan_mean)
            < config["minimum_interpretable_seconds"],
        })
    complete = all(row["status"] == "valid_pilot" for row in rows)
    ratios = [row["runtime_ratio"] for row in rows] if complete else []
    return {
        "kind": config["kind"], "formal_claim_verdict": "inconclusive",
        "reason": "Different workloads/toolchain; exploratory pilot, not SPEC CPU2006 reproduction.",
        "all_benchmarks_valid": complete,
        "geometric_mean_runtime_ratio": math.exp(statistics.mean(map(math.log, ratios)))
        if ratios else None,
        "benchmarks": rows,
    }


def write_report(output, records, config):
    (output / "metrics").mkdir(parents=True, exist_ok=True)
    summary = summarize(records, config)
    save(output / "metrics/summary.json", summary)
    with (output / "metrics/samples.csv").open("w", newline="", encoding="utf-8") as stream:
        columns = [
            "benchmark", "arm", "phase", "iteration", "valid", "real_seconds",
            "user_seconds", "sys_seconds", "exit_code", "reference_match", "output_sha256",
        ]
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    lines = [
        "# LLVM / ASan exploratory pilot", "",
        "This is workload-transfer evidence, not a reproduction of SPEC CPU2006 values.",
        "Wall time includes process startup and program output; units are seconds.",
        "Standard deviation is the sample standard deviation (n-1).",
        "Runtime ratio = mean(ASan) / mean(baseline). No failed sample is a speedup.", "",
        "| Benchmark | Baseline mean +/- SD | ASan mean +/- SD | Ratio | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in summary["benchmarks"]:
        def formatted(arm):
            group = row[arm]
            if not group["complete"]:
                return "invalid/missing (" + str(group["valid_runs"]) + " valid)"
            return f'{group["mean_seconds"]:.4f} +/- {group["sample_stddev_seconds"]:.4f}'
        ratio = f'{row["runtime_ratio"]:.3f}x' if row["runtime_ratio"] is not None else "N/A"
        status = row["status"] + ("; short run" if row["short_run_warning"] else "")
        lines.append(f'| {row["benchmark"]} | {formatted("baseline")} | {formatted("asan")} | {ratio} | {status} |')
    lines += ["", "Failed, missing, very short or sanitizer-reporting runs require investigation.",
              "No benchmark replacement or outlier removal was applied.", ""]
    (output / "README.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def run(args, config):
    if platform.system() != "Linux":
        raise ValueError("Execution requires the documented Linux container")
    output = Path(args.output).resolve()
    source = Path(args.source).resolve()
    if (output / "run-manifest.json").exists():
        raise ValueError("Run already exists; create a new run ID")
    for directory in ("logs", "raw-outputs", "metrics", "config", "provenance", "validation"):
        (output / directory).mkdir(parents=True, exist_ok=True)
    save(output / "config/effective.json", config)
    lock_path = ROOT / "workloads/llvm-suite-lock.json"
    shutil.copyfile(lock_path, output / "provenance/llvm-suite-lock.json")
    shutil.copyfile(__file__, output / "provenance/llvm-asan.py")
    for name, relative in (("LLVM-LICENSE.TXT", "LICENSE.TXT"),
                           ("OLDEN-LICENSE.TXT", "MultiSource/Benchmarks/Olden/LICENSE.TXT")):
        shutil.copyfile(source / relative, output / "provenance" / name)
    manifest = {
        "run_id": args.run_id, "status": "started", "kind": config["kind"],
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "project_commit": args.project_commit, "image_id": args.image,
        "config_sha256": sha256(output / "config/effective.json"),
        "runner_sha256": sha256(__file__), "paper_claim_verdict": "inconclusive",
        "platform": platform.platform(), "python": sys.version,
    }
    records = []
    save(output / "metrics/records.json", records)
    save(output / "run-manifest.json", manifest)
    env = dict(os.environ, ASAN_OPTIONS=config["asan_options"], LC_ALL="C", TZ="UTC")
    env.pop("LD_PRELOAD", None)
    build_root = Path("/tmp/llvm-asan-build")
    if build_root.exists():
        raise ValueError("Build directory already exists in this container")
    try:
        check_isolation(config, source, output)
        manifest["source"] = check_source(source, config)
        for label, argv in (
            ("compiler", [config["cc"], "--version"]),
            ("kernel", ["uname", "-a"]), ("cpu", ["lscpu"]),
            ("packages", ["dpkg-query", "-W"]),
        ):
            checked(argv, output / "provenance" / label, 20)
        for label, path in (
            ("os-release", "/etc/os-release"), ("cpu-max", "/sys/fs/cgroup/cpu.max"),
            ("memory-max", "/sys/fs/cgroup/memory.max"), ("pids-max", "/sys/fs/cgroup/pids.max"),
            ("cpuinfo", "/proc/cpuinfo"),
        ):
            if Path(path).is_file():
                shutil.copyfile(path, output / "provenance" / (label + ".txt"))
        for arm in ("baseline", "asan"):
            print("Building " + arm, flush=True)
            build = build_root / arm
            sanitizer = " " + config["asan_flags"] if arm == "asan" else ""
            configure = [
                "cmake", "-G", "Ninja", "-S", str(source), "-B", str(build),
                "-DCMAKE_C_COMPILER=" + config["cc"],
                "-DCMAKE_CXX_COMPILER=" + config["cxx"],
                "-DTEST_SUITE_HOST_CC=" + config["cc"],
                "-DCMAKE_BUILD_TYPE=Release", "-DCMAKE_C_FLAGS_RELEASE=",
                "-DCMAKE_CXX_FLAGS_RELEASE=",
                "-DCMAKE_C_FLAGS=" + config["c_flags"] + sanitizer,
                "-DCMAKE_CXX_FLAGS=" + config["cxx_flags"] + sanitizer,
                "-DCMAKE_EXE_LINKER_FLAGS=" + sanitizer.strip(),
                "-DTEST_SUITE_COLLECT_CODE_SIZE=OFF",
                "-DTEST_SUITE_COLLECT_COMPILE_TIME=OFF",
                "-DTEST_SUITE_COPY_DATA=ON",
                "-DTEST_SUITE_SUBDIRS=" + ";".join(b["directory"] for b in config["benchmarks"]),
            ]
            checked(configure, output / "logs" / ("configure-" + arm),
                    config["configure_timeout_seconds"], env=env)
            checked(["cmake", "--build", str(build), "--parallel",
                     str(config["limits"]["build_jobs"])],
                    output / "logs" / ("build-" + arm),
                    config["build_timeout_seconds"], env=env)
            provenance = output / "provenance" / arm
            provenance.mkdir()
            shutil.copyfile(build / "CMakeCache.txt", provenance / "cmake-cache.txt")
            shutil.copyfile(build / "build.ninja", provenance / "build.ninja")
            save(provenance / "binaries.json", {
                b["name"]: sha256(build / b["directory"] / b["name"])
                for b in config["benchmarks"]
            })
            for b in config["benchmarks"]:
                shutil.copyfile(build / b["directory"] / (b["name"] + ".test"),
                                provenance / (b["name"] + ".test"))
        available = sorted(os.sched_getaffinity(0))
        os.sched_setaffinity(0, {available[0]})
        manifest["cpu_affinity"] = sorted(os.sched_getaffinity(0))
        save(output / "run-manifest.json", manifest)
        timer = build_root / "baseline/tools/timeit"
        compare = build_root / "baseline/tools/fpcmp"
        for b in config["benchmarks"]:
            print("Running " + b["name"], flush=True)
            for phase, count in (("warmup", config["warmups"]),
                                 ("measure", config["repetitions"])):
                for iteration in range(1, count + 1):
                    arms = ("baseline", "asan") if iteration % 2 else ("asan", "baseline")
                    for arm in arms:
                        label = f'{b["name"]}-{phase}-{iteration:02}-{arm}'
                        raw = output / "raw-outputs"
                        stdout = raw / (label + ".output.txt")
                        timing = raw / (label + ".time.txt")
                        executable = build_root / arm / b["directory"] / b["name"]
                        argv = [
                            str(timer), "--timeout", str(config["command_timeout_seconds"]),
                            "--limit-core", "0", "--append-exitstatus",
                            "--redirect-output", str(stdout), "--summary", str(timing),
                            "--chdir", str(executable.parent), str(executable),
                        ] + b["args"]
                        result = command(argv, output / "logs" / label,
                                         config["command_timeout_seconds"] + 5, env=env)
                        record = {
                            "benchmark": b["name"], "arm": arm, "phase": phase,
                            "iteration": iteration, "valid": False,
                            "exit_code": result["exit_code"],
                            "timed_out": result["timed_out"], "reference_match": False,
                        }
                        if timing.exists():
                            measured = parse_time(timing)
                            record.update(real_seconds=measured["real"],
                                          user_seconds=measured["user"],
                                          sys_seconds=measured["sys"],
                                          program_exit_code=measured["exit"])
                        if stdout.exists():
                            record["output_sha256"] = sha256(stdout)
                            reference = source / b["directory"] / (b["name"] + ".reference_output")
                            normalized_output = (
                                output / "validation" / "normalized-output" / (label + ".txt")
                            )
                            normalized_reference = (
                                output / "validation" / "normalized-reference"
                                / (b["name"] + ".txt")
                            )
                            normalize_crlf(stdout, normalized_output)
                            if not normalized_reference.exists():
                                normalize_crlf(reference, normalized_reference)
                            verification = command(
                                [str(compare), str(normalized_output), str(normalized_reference)],
                                output / "validation" / label, 10, env=env,
                            )
                            record["reference_match"] = verification["exit_code"] == 0
                            record["reference_line_endings"] = config["reference_line_endings"]
                            record["normalized_output_sha256"] = sha256(normalized_output)
                            record["normalized_reference_sha256"] = sha256(normalized_reference)
                            record["sanitizer_report"] = b"AddressSanitizer" in stdout.read_bytes()
                        record["valid"] = (
                            not result["timed_out"] and result["exit_code"] == 0
                            and record.get("program_exit_code") == 0
                            and record["reference_match"] and not record.get("sanitizer_report", False)
                        )
                        records.append(record)
                        save(output / "metrics/records.json", records)
        summary = write_report(output, records, config)
        manifest["status"] = "passed_pilot" if summary["all_benchmarks_valid"] else "invalid_pilot"
        manifest["samples"] = len(records)
    except Exception as error:
        manifest.update(status="failed", error=str(error))
        write_report(output, records, config)
        raise
    finally:
        manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        manifest["evidence_sha256"] = {
            p.relative_to(output).as_posix(): sha256(p)
            for p in output.rglob("*") if p.is_file() and p.name != "run-manifest.json"
        }
        save(output / "run-manifest.json", manifest)
    print("Evidence: " + str(output), flush=True)
    return 0 if manifest["status"] == "passed_pilot" else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("fetch", "check-source", "run", "analyze"))
    parser.add_argument("--config", default=str(ROOT / "config/llvm-asan.json"))
    parser.add_argument("--source", default=str(ROOT / "workloads/downloads/llvm-test-suite"))
    parser.add_argument("--proxy", default=None)
    parser.add_argument("--output", default="/evidence")
    parser.add_argument("--report-dir")
    parser.add_argument("--run-id", default="unassigned")
    parser.add_argument("--project-commit", default="unassigned")
    parser.add_argument("--image", default="unassigned")
    args = parser.parse_args()
    config = load(args.config)
    if args.action == "fetch":
        fetch(args, config)
    elif args.action == "check-source":
        print(json.dumps(check_source(args.source, config), indent=2))
    elif args.action == "analyze":
        output = Path(args.output).resolve()
        config = load(output / "config/effective.json")
        manifest = load(output / "run-manifest.json")
        for relative, expected in manifest["evidence_sha256"].items():
            if sha256(within(output, relative)) != expected:
                raise ValueError("Run evidence changed: " + relative)
        report = Path(args.report_dir) if args.report_dir else ROOT / "results" / output.name
        report.mkdir(parents=True, exist_ok=False)
        write_report(report, load(output / "metrics/records.json"), config)
    else:
        return run(args, config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
