#!/usr/bin/env python3
"""
解析 lit 输出的 results.json，计算每个 benchmark 的运行时间 mean±std，
以及 ASan 相对 native 的 slowdown。
"""
import json
import glob
import os
import statistics

WORK = "/bench"

def load_exec_times(pattern):
    """读取多个 results.json，返回 {benchmark_name: [exec_time, ...]}"""
    times = {}
    files = sorted(glob.glob(os.path.join(WORK, pattern)))
    for f in files:
        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)
        for t in data.get("tests", []):
            name = t.get("name", "")
            # 去掉 "test-suite :: " 前缀和 ".test" 后缀
            key = name.replace("test-suite :: ", "")
            if key.endswith(".test"):
                key = key[:-5]
            metrics = t.get("metrics", {})
            et = metrics.get("exec_time")
            if et is None:
                # 老版本 lit 可能把 exec_time 放在顶层
                et = t.get("exec_time")
            if et is None:
                continue
            times.setdefault(key, []).append(float(et))
    return times

def main():
    native = load_exec_times("native_*.json")
    asan = load_exec_times("asan_*.json")

    if not native or not asan:
        print("错误：没读到 native_*.json 或 asan_*.json，请确认 lit 已成功运行。")
        return 1

    rows = []
    for bench in sorted(native.keys()):
        if bench not in asan:
            continue
        n = native[bench]
        a = asan[bench]
        n_mean = statistics.mean(n)
        n_std = statistics.stdev(n) if len(n) > 1 else 0.0
        a_mean = statistics.mean(a)
        a_std = statistics.stdev(a) if len(a) > 1 else 0.0
        slowdown = a_mean / n_mean if n_mean > 0 else float("inf")
        rows.append((bench, n_mean, n_std, a_mean, a_std, slowdown))

    # 输出表格
    print("\n" + "=" * 90)
    print(f"{'benchmark':<58}{'native(s)':>12}{'asan(s)':>12}{'slowdown':>10}")
    print("=" * 90)
    for bench, n_mean, n_std, a_mean, a_std, slowdown in rows:
        short = bench.split("/")[-1]
        print(f"{bench:<58}{n_mean:>12.4f}{a_mean:>12.4f}{slowdown:>9.2f}x")
    print("=" * 90)

    # 平均 slowdown
    slowdowns = [r[5] for r in rows]
    avg = statistics.mean(slowdowns)
    print(f"\n平均 slowdown: {avg:.2f}x  （论文报告 73% 开销 = 1.73x）")
    print(f"平均开销: {(avg-1)*100:.1f}%")
    print(f"benchmark 数量: {len(rows)}")

    # 保存 CSV
    csv_path = os.path.join(WORK, "slowdown_results.csv")
    with open(csv_path, "w", encoding="utf-8") as fp:
        fp.write("benchmark,native_mean_s,native_std_s,asan_mean_s,asan_std_s,slowdown\n")
        for bench, n_mean, n_std, a_mean, a_std, slowdown in rows:
            fp.write(f"{bench},{n_mean:.6f},{n_std:.6f},{a_mean:.6f},{a_std:.6f},{slowdown:.6f}\n")
    print(f"\n结果已保存到 {csv_path}")

    # 保存原始 mean±std 汇总（供报告引用）
    summary_path = os.path.join(WORK, "slowdown_summary.json")
    summary = {
        "paper_claim": "average slowdown 73% (1.73x) on SPEC CPU2006",
        "benchmarks_used": [r[0] for r in rows],
        "native": {r[0]: {"mean": r[1], "std": r[2]} for r in rows},
        "asan": {r[0]: {"mean": r[3], "std": r[4]} for r in rows},
        "slowdown": {r[0]: r[5] for r in rows},
        "average_slowdown": avg,
    }
    with open(summary_path, "w", encoding="utf-8") as fp:
        json.dump(summary, fp, indent=2, ensure_ascii=False)
    print(f"汇总已保存到 {summary_path}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
