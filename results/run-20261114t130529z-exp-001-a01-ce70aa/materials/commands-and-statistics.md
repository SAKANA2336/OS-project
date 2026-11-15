# Commands and Statistics

## Entry points

From the project root, with Docker Desktop's Linux engine running:

```powershell
python .\scripts\llvm-asan.py fetch
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run-llvm-asan.ps1
```

The runner creates a new run ID for every attempt. It does not reuse an old run
directory. The analysis implementation is:

`../../../scripts/llvm-asan.py`

## Configure and build

The following are the exact command shapes recorded by the successful run.
All argv arrays, including the per-run build directories and exit status, are
preserved under `commands/logs/`.

Baseline configure:

```text
cmake -G Ninja -S /suite -B /tmp/llvm-asan-build/baseline
  -DCMAKE_C_COMPILER=clang-18
  -DCMAKE_CXX_COMPILER=clang++-18
  -DTEST_SUITE_HOST_CC=clang-18
  -DCMAKE_BUILD_TYPE=Release
  -DCMAKE_C_FLAGS_RELEASE=
  -DCMAKE_CXX_FLAGS_RELEASE=
  -DCMAKE_C_FLAGS="-O2 -g -fno-omit-frame-pointer -std=gnu89"
  -DCMAKE_CXX_FLAGS="-O2 -g -fno-omit-frame-pointer"
  -DCMAKE_EXE_LINKER_FLAGS=
  -DTEST_SUITE_COLLECT_CODE_SIZE=OFF
  -DTEST_SUITE_COLLECT_COMPILE_TIME=OFF
  -DTEST_SUITE_COPY_DATA=ON
  -DTEST_SUITE_SUBDIRS="MultiSource/Benchmarks/Olden/bisort;MultiSource/Benchmarks/Olden/em3d;MultiSource/Benchmarks/Olden/mst;MultiSource/Benchmarks/Olden/perimeter;MultiSource/Benchmarks/Olden/treeadd;MultiSource/Benchmarks/Olden/tsp"
```

ASan configure uses the same command and adds
`-fsanitize=address` to the C and C++ flags and to
`CMAKE_EXE_LINKER_FLAGS`.

Both arms are then built with:

```text
cmake --build /tmp/llvm-asan-build/<arm> --parallel 2
```

The captured CMake cache and Ninja files are in
`provenance/baseline/` and `provenance/asan/`.

## Runtime and validation

Each execution uses the baseline-built LLVM Test Suite `tools/timeit`:

```text
/tmp/llvm-asan-build/baseline/tools/timeit
  --timeout 60
  --limit-core 0
  --append-exitstatus
  --redirect-output /evidence/raw-outputs/<label>.output.txt
  --summary /evidence/raw-outputs/<label>.time.txt
  --chdir /tmp/llvm-asan-build/<arm>/MultiSource/Benchmarks/Olden/<benchmark>
  /tmp/llvm-asan-build/<arm>/MultiSource/Benchmarks/Olden/<benchmark>/<benchmark>
  <fixed arguments>
```

The output is compared with the baseline-built `fpcmp`:

```text
/tmp/llvm-asan-build/baseline/tools/fpcmp
  /evidence/validation/normalized-output/<label>.txt
  /evidence/validation/normalized-reference/<benchmark>.txt
```

The `commands/logs/` directory contains 76 execution/build command records
(configure, build, warmup and measurement). The `commands/validation/`
directory contains all 72 reference-comparison command records. The raw output
and timer files are in `raw-outputs/`.

## Repetition design

- Programs: 6
- Arms: baseline and ASan
- Warmups: 1 per program and arm
- Measurements: 5 per program and arm
- Total records: `6 * 2 * (1 + 5) = 72`
- Measured samples: `6 * 2 * 5 = 60`
- Fresh process for every invocation
- Odd measurement iterations: baseline then ASan
- Even measurement iterations: ASan then baseline
- Program order: `bisort`, `em3d`, `mst`, `perimeter`, `treeadd`, `tsp`

Warmups are retained in `records.json` but excluded from the timing means.

## Validity

A record is valid only when all of the following hold:

- the timer did not time out;
- the timer command exited with code 0;
- the program exit status was 0;
- the reference comparison succeeded;
- no sanitizer report was found in captured output.

No failed record was deleted, turned into a speedup, or replaced by another
benchmark. The successful run has 72 valid records. `mst` is marked with a
short-run warning because its minimum arm mean is below 0.05 seconds.

## Formulas

For each benchmark and arm, over the five valid measurement samples
`t_1, ..., t_5`:

```text
mean = (t_1 + ... + t_5) / 5

sample standard deviation =
  sqrt(sum((t_i - mean)^2) / (5 - 1))

runtime ratio = mean(ASan) / mean(baseline)

extra time overhead = (runtime ratio - 1) * 100%
```

The suite-level number is the equal-weight geometric mean of the six benchmark
ratios:

```text
geometric mean = exp(mean(log(ratio_1), ..., log(ratio_6)))
```

For this run the geometric mean runtime ratio is `1.8988062382555193`.
The formal claim verdict remains `inconclusive` because the workload and
toolchain are different from the SPEC CPU2006 experiment.

The implementation that writes `samples.csv`, `summary.json` and the report
README is `scripts/llvm-asan.py`, especially its `summarize()` and
`write_report()` functions.

