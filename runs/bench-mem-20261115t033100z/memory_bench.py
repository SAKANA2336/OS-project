#!/usr/bin/env python3
"""
测量 AddressSanitizer 的内存开销（最大驻留内存 max RSS），
复现论文 Table 1 的「平均 3.37x 内存增长」主张。
每个 benchmark 各跑 3 次，报告 mean ± std 和内存增长倍数。
"""
import subprocess
import os
import statistics
import json

WORK = "/bench"
NATIVE = f"{WORK}/build-native"
ASAN = f"{WORK}/build-asan"

# 对齐论文设置：quarantine=0、禁用 malloc 栈回溯
os.environ["ASAN_OPTIONS"] = "quarantine_size_mb=0:malloc_context_size=0"

# (名称, 相对 build 根的目录, 运行命令含重定向)
BENCHES = [
    ("Fhourstones", "MultiSource/Benchmarks/Fhourstones", "./fhourstones < input"),
    ("cfrac", "MultiSource/Benchmarks/MallocBench/cfrac", "./cfrac 41757646344123832613190542166099121"),
    ("espresso", "MultiSource/Benchmarks/MallocBench/espresso", "./espresso -t INPUT/largest.espresso"),
    ("bh", "MultiSource/Benchmarks/Olden/bh", "./bh 20000 20"),
    ("anagram", "MultiSource/Benchmarks/Ptrdist/anagram", "./anagram words 2 < input.OUT"),
    ("nbench", "MultiSource/Benchmarks/nbench", "./nbench"),
]


def measure_rss(build, dirname, cmd):
    """在指定 build 目录里跑 benchmark，返回 max RSS (KB)。"""
    cwd = os.path.join(build, dirname)
    full = f"/usr/bin/time -v bash -c '{cmd}'"
    p = subprocess.run(
        full, shell=True, cwd=cwd,
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        stdin=subprocess.DEVNULL,
    )
    for line in p.stderr.splitlines():
        if "Maximum resident set size" in line:
            # 形如 "Maximum resident set size (kbytes): 12345"
            return int(line.split(":")[1].strip().split()[0])
    return None


def main():
    rows = []
    for name, dirname, cmd in BENCHES:
        native_vals, asan_vals = [], []
        for _ in range(3):
            n = measure_rss(NATIVE, dirname, cmd)
            a = measure_rss(ASAN, dirname, cmd)
            if n is None or a is None:
                print(f"[警告] {name} 内存测量失败，跳过")
                break
            native_vals.append(n)
            asan_vals.append(a)
        if len(native_vals) < 3:
            continue
        n_mean = statistics.mean(native_vals)
        n_std = statistics.stdev(native_vals)
        a_mean = statistics.mean(asan_vals)
        a_std = statistics.stdev(asan_vals)
        ratio = a_mean / n_mean if n_mean else float("inf")
        rows.append((name, n_mean, n_std, a_mean, a_std, ratio))

    if not rows:
        print("错误：没有成功的测量结果")
        return 1

    print("\n" + "=" * 80)
    print(f"{'benchmark':<14}{'native(KB)':>16}{'asan(KB)':>16}{'ratio':>10}")
    print("=" * 80)
    for name, n_mean, n_std, a_mean, a_std, ratio in rows:
        print(f"{name:<14}{n_mean:>14.0f}±{n_std:.0f}{a_mean:>14.0f}±{a_std:.0f}{ratio:>9.2f}x")
    print("=" * 80)

    ratios = [r[5] for r in rows]
    avg = statistics.mean(ratios)
    print(f"\n平均内存增长: {avg:.2f}x  （论文 Table 1 报告 3.37x）")
    print(f"benchmark 数量: {len(rows)}")

    csv_path = os.path.join(WORK, "memory_results.csv")
    with open(csv_path, "w", encoding="utf-8") as fp:
        fp.write("benchmark,native_kb_mean,native_kb_std,asan_kb_mean,asan_kb_std,ratio\n")
        for name, n_mean, n_std, a_mean, a_std, ratio in rows:
            fp.write(f"{name},{n_mean:.0f},{n_std:.0f},{a_mean:.0f},{a_std:.0f},{ratio:.4f}\n")
    print(f"\n结果已保存到 {csv_path}")

    summary = {
        "paper_claim": "average memory usage increase 3.37x (Table 1)",
        "metric": "maximum resident set size (KB), measured via /usr/bin/time -v",
        "benchmarks": [r[0] for r in rows],
        "native_kb": {r[0]: {"mean": r[1], "std": r[2]} for r in rows},
        "asan_kb": {r[0]: {"mean": r[3], "std": r[4]} for r in rows},
        "ratio": {r[0]: r[5] for r in rows},
        "average_ratio": avg,
    }
    json_path = os.path.join(WORK, "memory_summary.json")
    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2, ensure_ascii=False)
    print(f"汇总已保存到 {json_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
