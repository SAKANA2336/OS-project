"""Bounded functional checks, not a reproduction of the 2012 benchmarks."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


OPTIONS = (
    "detect_leaks=0:detect_stack_use_after_return=0:"
    "halt_on_error=1:abort_on_error=0:exitcode=86:symbolize=1"
)
ERRORS = {
    "heap": "heap-buffer-overflow",
    "uaf": "heap-use-after-free",
    "stack": "stack-buffer-overflow",
    "global": "global-buffer-overflow",
}


def write_json(path, value):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")


def as_text(value):
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value or ""


def run_logged(output, name, argv, timeout=30):
    env = dict(os.environ)
    env["ASAN_OPTIONS"] = OPTIONS
    env["ASAN_SYMBOLIZER_PATH"] = "/usr/bin/llvm-symbolizer-18"
    try:
        completed = subprocess.run(
            argv, capture_output=True, text=True, errors="replace",
            timeout=timeout, env=env, check=False,
        )
        result = {
            "argv": argv, "returncode": completed.returncode, "timed_out": False,
            "stdout": completed.stdout, "stderr": completed.stderr,
        }
    except subprocess.TimeoutExpired as exc:
        result = {
            "argv": argv, "returncode": None, "timed_out": True,
            "stdout": as_text(exc.stdout), "stderr": as_text(exc.stderr),
        }
    except OSError as exc:
        result = {
            "argv": argv, "returncode": None, "timed_out": False,
            "stdout": "", "stderr": str(exc),
        }
    write_json(output / (name + ".json"), result)
    return result


def valid_normal(result):
    return (
        not result["timed_out"] and result["returncode"] == 0
        and result["stdout"].strip() == "OK 7" and not result["stderr"].strip()
    )


def valid_error(result, category):
    return (
        not result["timed_out"] and result["returncode"] == 86
        and f"ERROR: AddressSanitizer: {category}" in result["stderr"]
        and f"SUMMARY: AddressSanitizer: {category}" in result["stderr"]
        and re.search(r"cases\.c:\d+", result["stderr"]) is not None
    )


def require_limits():
    root = Path("/sys/fs/cgroup")
    memory = (root / "memory.max").read_text().strip()
    pids = (root / "pids.max").read_text().strip()
    quota, period = (root / "cpu.max").read_text().split()
    if not (memory.isdigit() and 0 < int(memory) <= 2 * 1024**3):
        raise RuntimeError("A cgroup-v2 memory limit of at most 2 GiB is required.")
    if not (pids.isdigit() and 0 < int(pids) <= 128):
        raise RuntimeError("A cgroup-v2 PID limit of at most 128 is required.")
    if not (quota.isdigit() and 0 < int(quota) / int(period) <= 2):
        raise RuntimeError("A cgroup-v2 CPU quota of at most 2 CPUs is required.")
    return {"memory.max": memory, "pids.max": pids, "cpu.max": f"{quota} {period}"}


def verify(output):
    source = Path(__file__).resolve().parent
    output.mkdir(parents=True, exist_ok=False)
    summary = {
        "kind": "environment-functional-validation",
        "paper_claims_tested": [],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "status": "failed",
        "checks": [],
    }
    try:
        if platform.system() != "Linux" or platform.machine() != "x86_64":
            raise RuntimeError("Linux x86_64 is required; no emulated target is accepted.")
        if os.getuid() == 0:
            raise RuntimeError("Validation must run as a non-root user.")
        environment = {
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "os_release": Path("/etc/os-release").read_text(),
            "limits": require_limits(),
            "asan_options": OPTIONS,
            "sources_sha256": {
                name: hashlib.sha256((source / name).read_bytes()).hexdigest()
                for name in ("cases.c", "normal.cpp", "verify.py")
            },
        }
        write_json(output / "environment.json", environment)
        commands = {
            "clang-version": ["clang-18", "--version"],
            "clangxx-version": ["clang++-18", "--version"],
            "symbolizer-version": ["llvm-symbolizer-18", "--version"],
            "cmake-version": ["cmake", "--version"],
            "ninja-version": ["ninja", "--version"],
            "cpu": ["lscpu", "--json"],
            "packages": ["dpkg-query", "-W", "-f=${binary:Package}\t${Version}\n"],
        }
        for name, argv in commands.items():
            result = run_logged(output, name, argv)
            if result["returncode"] != 0 or result["timed_out"]:
                raise RuntimeError(f"Environment query failed: {name}")
        with tempfile.TemporaryDirectory(prefix="asan-check-") as temp:
            baseline = str(Path(temp) / "baseline")
            asan = str(Path(temp) / "asan")
            cpp = str(Path(temp) / "normal-cpp")
            flags = ["-O1", "-g", "-fno-omit-frame-pointer", "-fno-optimize-sibling-calls"]
            builds = {
                "build-baseline": ["clang-18", *flags, str(source / "cases.c"), "-o", baseline],
                "build-asan": [
                    "clang-18", *flags, "-fsanitize=address",
                    str(source / "cases.c"), "-o", asan,
                ],
                "build-cpp": [
                    "clang++-18", "-std=c++17", *flags, "-fsanitize=address",
                    str(source / "normal.cpp"), "-o", cpp,
                ],
            }
            for name, argv in builds.items():
                result = run_logged(output, name, argv, timeout=60)
                if result["returncode"] != 0 or result["timed_out"]:
                    raise RuntimeError(f"Compilation failed: {name}")
            for name, argv in (
                ("normal-baseline", [baseline, "normal"]),
                ("normal-asan", [asan, "normal"]),
                ("normal-cpp", [cpp]),
            ):
                result = run_logged(output, name, argv, timeout=10)
                summary["checks"].append({"name": name, "passed": valid_normal(result)})
            # Do not execute the intentionally invalid cases without instrumentation.
            for name, category in ERRORS.items():
                result = run_logged(output, name, [asan, name], timeout=10)
                summary["checks"].append(
                    {"name": name, "expected": category, "passed": valid_error(result, category)}
                )
        if len(summary["checks"]) == 7 and all(item["passed"] for item in summary["checks"]):
            summary["status"] = "passed"
    except Exception as exc:
        summary["error"] = f"{type(exc).__name__}: {exc}"
    summary["finished_at"] = datetime.now(timezone.utc).isoformat()
    write_json(output / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary["status"] == "passed" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    sys.exit(verify(arguments.output))
