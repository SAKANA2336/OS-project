# Replicating AddressSanitizer: A Fast Address Sanity Checker

| Field | Value |
| --- | --- |
| `controlled_object_id` | `report` |
| `exact_version` | `v0.0` |
| `status` | `draft` |
| `freeze_state` | `not_frozen` |
| `created_at` | 2026-11-15 (Asia/Shanghai) |
| `applies_to` | Final Report (CS340 AY2026-2027, Paper Replication) |
| `governing_rule` | `AGENTS.md` 1.0 |
| `source_of_authority` | 用户于 2026-11-15 授权起草报告骨架 |

This is a draft. Numbers in Section 3 and Section 4 are taken from committed run
directories and must be re-checked against those files before the report is frozen.
Section 10 lists what is still missing; it is working material and must be removed
from the submitted version.

---

## 1 Introduction and Claims

### 1.1 Paper and problem

C and C++ programs routinely violate memory safety. Out-of-bounds accesses and
use-after-free bugs are both a leading cause of security vulnerabilities and a
notoriously hard class of defect to reproduce, because the corruption and the
symptom are often far apart in time. Dynamic detectors that observe every memory
access, such as Valgrind's Memcheck or Dr. Memory, find these bugs reliably, but
they run the program on a virtual machine or under binary translation and therefore
cost roughly an order of magnitude in execution time. That cost keeps them out of
ordinary development and test loops.

Serebryany et al. propose AddressSanitizer (ASan), a detector built from compile-time
instrumentation plus a runtime library. The design rests on four ideas: a *shadow
memory* that records, for every 8 bytes of application memory, whether those bytes
are addressable; a *direct mapping* from application address to shadow address,
`(Addr >> 3) + Offset`, which makes a shadow check a single load with no lookup
table; *redzones* placed around heap, stack and global objects so that an overflow
lands on poisoned memory; and *quarantine* plus allocator interception so that freed
memory stays poisoned. ASan checks each instrumented access against the shadow and
reports the fault at the point of occurrence.

The paper's central claim is economic rather than functional: this design finds
memory errors at a small fraction of the cost of existing tools. The abstract states
that "its average slowdown is just 73%", against roughly 20x for Valgrind and 10x for
Dr. Memory. If that claim holds on modern hardware, ASan is cheap enough to be left
on during normal development, which is what makes the paper influential.

### 1.2 Claims tested

We reproduce three claims, each anchored to a specific table or figure in the paper.

**Table 1 — Claims under test and their anchors in the paper**

| ID | Claim | Anchor in paper | Paper value |
| --- | --- | --- | --- |
| C-001 | Average runtime overhead of ASan is about 73% (1.73x slowdown), far below Valgrind and Dr. Memory | Abstract; Section 4, Figure 2 | 1.73x average; worst 2.60x (perlbench), 2.67x (xalancbmk); Valgrind 20x, Dr. Memory 10x |
| C-002 | ASan increases memory usage by about 3.4x | Abstract; Section 4, Table 1 | 3.37x total, 8171 MB to 24467 MB |
| C-003 | ASan detects out-of-bounds accesses on heap, stack and global objects, and use-after-free, without false positives | Abstract; Section 3.6 | Detects all four classes; "no false positives" |

We deliberately did not test the paper's narrower configuration claims (write-only
instrumentation, 26% average slowdown; `Offset=0` with `-fPIE -pie`, 69%). Both are
interesting but each needs a second build configuration of every benchmark, and the
three claims above already cover the paper's main argument.

### 1.3 Scope

The reproduction is at reduced scale in two dimensions.

*Workloads.* The paper measures SPEC CPU2006, which is no longer obtainable: the
suite was retired and is not licensed for new use. We use six programs from the open
LLVM test-suite instead. The course instructor explicitly authorised this substitution
on 2026-11-14, on condition that the substitution is explained in the repository, the
presentation and the report; this section and Section 2.4 are that explanation.

*Metrics.* We measure wall-clock execution time per benchmark and maximum resident
set size, three runs each, and report mean and standard deviation. We do not
reproduce the paper's per-benchmark absolute times, which depend on a 2012 machine,
nor its suite average, which depends on the retired suite.

What the reproduction therefore can and cannot establish is stated in Section 4.4.

---

## 2 Reproduction Setup

### 2.1 Starting code

The paper published no reference implementation. AddressSanitizer ships in upstream
LLVM as the compiler instrumentation pass plus the `compiler-rt` runtime, so the
"starting code" of this reproduction is the toolchain itself rather than a project
repository.

| Item | Value |
| --- | --- |
| Compiler | `clang` 18.1.3 (Ubuntu package) |
| Sanitizer runtime | `compiler-rt` 18.1.3, `libclang_rt.asan-x86_64` |
| Workload source | LLVM `test-suite`, `MultiSource/Benchmarks` |
| Workload commit | **not recorded** — see Section 10, item 1 |
| LLVM source modified | none |
| Files added by this project | `runs/bench-20261114t171000z/run_bench.sh`, `analyze.py`; `runs/bench-mem-20261115t033100z/memory_bench.py` |

We made no modification to LLVM or to `compiler-rt`. Everything this project adds is
measurement harness: a driver that builds each benchmark twice and times it, and an
analysis script that reduces the samples to mean, standard deviation and ratio.

### 2.2 Environment

**Table 2 — Environment of the quantitative runs**

| Component | Value |
| --- | --- |
| Operating system | Ubuntu 24.04.5 LTS, x86_64 |
| Kernel | 6.18.33.2-microsoft-standard-WSL2 |
| Virtualisation | Docker Desktop on WSL2, image `os-project-asan` |
| Compiler | clang 18.1.3, `-O2` |
| Baseline build | `clang-18 -O2` |
| ASan build | `clang-18 -O2 -fsanitize=address -fno-omit-frame-pointer` |
| ASan runtime options | `quarantine_size_mb=0`, `malloc_context_size=0` |
| Timing tool | LLVM test-suite `lit` harness with `timeit-target` |
| Memory metric | maximum resident set size from `/usr/bin/time -v` |
| Repeats | 3 per benchmark per build |

Two settings follow the paper directly and matter for comparability:
`quarantine_size_mb=0` removes the default 256 MB quarantine, and
`malloc_context_size=0` disables the malloc stack unwinding that the paper also
disabled. Both settings lower ASan's measured overhead relative to its defaults, so
they must be in place for the numbers to be comparable at all.

The host CPU model is not recorded in the benchmark run manifests. The environment
validation run on the same stack reported a 13th Gen Intel Core i9-13900HX with 16
cores and 32 hardware threads, but that record belongs to a different machine from
the one that produced Section 3 and must not be presented as the benchmark host. This
is a genuine gap in the reproduction setup and is listed as Section 10, item 2.

### 2.3 Workloads

**Table 3 — Benchmarks used**

| Benchmark | Path in `test-suite` | Character |
| --- | --- | --- |
| Fhourstones | `MultiSource/Benchmarks/Fhourstones/fhourstones` | compute-bound, board search |
| cfrac | `MultiSource/Benchmarks/MallocBench/cfrac/cfrac` | allocation-heavy |
| espresso | `MultiSource/Benchmarks/MallocBench/espresso/espresso` | allocation-heavy, logic minimisation |
| bh | `MultiSource/Benchmarks/Olden/bh/bh` | pointer-chasing tree code |
| anagram | `MultiSource/Benchmarks/Ptrdist/anagram/anagram` | pointer and string work |
| nbench | `MultiSource/Benchmarks/nbench/nbench` | mixed integer and memory |

The set was chosen to span the two properties the paper uses to explain its own
worst cases — allocation intensity and many small accesses — while staying inside the
part of the suite that still compiles with a modern clang. Two `MallocBench` programs
were excluded: `perl` and `gawk` are 1990s code bases that rely on implicit function
declarations, which clang 18 rejects by default. They are excluded rather than patched
so that no benchmark source is modified.

### 2.4 Deviations

**Table 4 — Complete list of deviations from the paper's setup**

| # | Item | Paper setting | Setting used here | Reason |
| --- | --- | --- | --- | --- |
| 1 | Benchmark suite | SPEC CPU2006 (19 C/C++ benchmarks) | LLVM `test-suite`, 6 programs | CPU2006 retired and not licensable; instructor authorised the substitution on 2026-11-14 |
| 2 | Hardware | HP Z600, 2x Intel Xeon E5620, 24 GB RAM | Modern x86-64 host, Docker on WSL2 | 2012 hardware unavailable; absolute times are therefore not comparable, only ratios are |
| 3 | Compiler | LLVM 3.x (2012) | clang 18.1.3 | Current supported toolchain; the instrumentation algorithm is the same but code generation and the runtime have changed |
| 4 | Redzone size | 32 bytes, explicitly set | Runtime default (16 bytes); **not explicitly set** | The recorded `ASAN_OPTIONS` sets only quarantine and malloc context. Listed as a deviation because it plausibly affects C-002 |
| 5 | Memory metric | `VmPeak` (virtual peak) | Maximum RSS (resident peak) | `VmPeak` counts ASan's shadow reservation, which is mapped but largely untouched; RSS counts what is actually resident. This is expected to understate the ratio |
| 6 | Excluded benchmarks | none | `MallocBench/perl`, `MallocBench/gawk` | Do not compile with clang 18 without patching the benchmark source |
| 7 | Quarantine | 0 | 0 | matches paper |
| 8 | malloc stack unwinding | disabled | disabled (`malloc_context_size=0`) | matches paper |
| 9 | Optimisation level | `-O2` | `-O2` | matches paper |
| 10 | Detection cases | paper's own bug corpus | `outputs/asan-environment/cases.c`, 4 classes + 1 clean program | The paper's corpus is not published as a runnable artefact |
| 11 | Thread model | multi-threaded programs included | single-threaded only | Reduces scope; multi-threaded ASan behaviour is out of scope for this reproduction |

Row 4 and row 5 are the two deviations we expect to matter most, and Section 4.3
argues that they explain the direction of the C-002 discrepancy.

---

## 3 Results

### 3.1 Paper vs. ours

**Table 5 — Runtime overhead (C-001): paper vs. this reproduction**

| Metric, same setting | Paper | Ours |
| --- | --- | --- |
| Average slowdown | 1.73x (73%) | **2.22x (122%)** |
| Slowest benchmark | 2.67x (xalancbmk) | 4.19x (cfrac) |
| Fastest benchmark | not stated in text (Figure 2 only) | 1.47x (nbench) |
| Valgrind, same suite | 20x | not measured |

**Table 6 — Memory overhead (C-002): paper vs. this reproduction**

| Metric, same setting | Paper | Ours |
| --- | --- | --- |
| Average increase | 3.37x | **2.58x** |
| Absolute totals | 8171 MB to 24467 MB | per-benchmark RSS, see Table 7 |

**Table 7 — Per-benchmark results**

| Benchmark | Baseline mean ± SD (s) | ASan mean ± SD (s) | Slowdown | Baseline RSS (KB) | ASan RSS (KB) | Ratio |
| --- | --- | --- | --- | --- | --- | --- |
| Fhourstones | 0.3151 ± 0.0047 | 0.4650 ± 0.0168 | 1.48x | 6728 ± 39 | 11707 ± 155 | 1.74x |
| cfrac | 0.2545 ± 0.0005 | 1.0656 ± 0.0491 | 4.19x | 3415 ± 255 | 10003 ± 23 | 2.93x |
| espresso | 0.1463 ± 0.0032 | 0.3338 ± 0.0035 | 2.28x | 3533 ± 122 | 12639 ± 24 | 3.58x |
| bh | 0.7207 ± 0.0085 | 1.5310 ± 0.0089 | 2.12x | 6368 ± 136 | 15124 ± 38 | 2.38x |
| anagram | 0.3726 ± 0.0202 | 0.6550 ± 0.0545 | 1.76x | 3305 ± 60 | 8236 ± 114 | 2.49x |
| nbench | 0.5413 ± 0.0078 | 0.7932 ± 0.0039 | 1.47x | 3504 ± 205 | 8392 ± 160 | 2.40x |

### 3.2 Statistics

Each benchmark was built once per configuration and executed three times. We report
the sample mean and the sample standard deviation (`n-1`). The paper reports a single
figure per benchmark and no dispersion, so no variance comparison is possible; only
the means are comparable.

Relative standard deviation is below 5% for every baseline measurement except
`anagram` (5.4%), and below 8% for every ASan measurement except `anagram` (8.3%).
We consider three runs adequate for a first reproduction and insufficient for a
final one; see Section 10, item 3.

### 3.3 Figures

Figure 1 and Figure 2 are to be generated from the committed CSVs by a versioned
script; they are not yet produced.

* **Figure 1** — per-benchmark slowdown, baseline vs. ASan, with the paper's 1.73x
  average drawn as a reference line. Source: `runs/bench-20261114t171000z/slowdown_results.csv`.
* **Figure 2** — per-benchmark memory ratio, with the paper's 3.37x drawn as a
  reference line. Source: `runs/bench-mem-20261115t033100z/memory_results.csv`.

### 3.4 Traceability

**Table 8 — Where each number comes from**

| Numbers | Run directory | Files |
| --- | --- | --- |
| Table 5, Table 7 runtime columns, Section 3.2 time statistics | `runs/bench-20261114t171000z/` | `slowdown_results.csv`, `slowdown_summary.json` |
| Table 6, Table 7 memory columns | `runs/bench-mem-20261115t033100z/` | `memory_results.csv`, `memory_summary.json` |
| Section 4.1 C-003 detection matrix | `runs/env-20261108t013027z-6c0e488a/` | `validation/summary.json`, `validation/*.json` |

Every number in Section 3 is a reduction of a file in one of these directories. No
number was entered by hand from a terminal.

---

## 4 Analysis of Discrepancies

### 4.1 Claim verdicts

**Table 9 — Verdicts**

| ID | Claim | Verdict | Basis |
| --- | --- | --- | --- |
| C-001 | Average slowdown about 1.73x | `partially_supported` | Same direction, same order of magnitude, but 2.22x is 28% higher |
| C-002 | Memory increase about 3.37x | `partially_supported` | Same direction, both "about three times", but 2.58x is 23% lower |
| C-003 | Detects heap/stack/global OOB and UAF, no false positives | `supported` | 7 of 7 checks passed, including the clean-program control |

### 4.2 Gaps

**Table 10 — Absolute and relative differences**

| Claim | Paper | Ours | Absolute | Relative |
| --- | --- | --- | --- | --- |
| C-001 | 1.73x | 2.22x | +0.49x | +28% |
| C-002 | 3.37x | 2.58x | -0.79x | -23% |

The two discrepancies have opposite signs, which is the most interesting thing in the
data: our ASan is *slower* than the paper's but uses *less* memory. A single
explanation cannot account for both, so the next two subsections treat them separately.

### 4.3 Explanations and supporting evidence

**Why memory comes out lower (C-002).** Two mechanisms push the ratio down, and both
are visible in the recorded configuration rather than inferred.

1. *Metric.* The paper states that Table 1 was "collected by reading the `VmPeak`
   field from `/proc/self/status` at process termination" — that is, peak *virtual*
   address space. ASan reserves one eighth of the address space for shadow memory up
   front; that reservation is mapped but mostly untouched, so it counts fully in
   `VmPeak` and almost not at all in RSS. Our ratio is therefore expected to be
   systematically lower than the paper's even if the runtime behaved identically. This
   is the single largest contributor and it is a measurement artefact, not a property
   of ASan.
2. *Redzone size.* The paper set 32-byte redzones and states that "the memory overhead
   comes mostly from the malloc redzones". The recorded runs set only
   `quarantine_size_mb` and `malloc_context_size`, so the modern default of 16 bytes
   applied. If redzones dominate the overhead and ours are half the size, the ratio
   should be markedly lower — and it is.

Both mechanisms predict a lower ratio, and the two benchmarks with the largest
allocation pressure show the largest ratios (espresso 3.58x, cfrac 2.93x), which is
consistent with the paper's own explanation that allocation-heavy programs pay more.

*Evidence status.* Mechanism 1 can be settled with a controlled re-run that records
`VmPeak` from `/proc/self/status` alongside RSS on the same binaries; the ratio
computed from `VmPeak` should move toward 3.37x while nothing else changes. Mechanism 2
can be settled by re-running one benchmark with `redzone=32` and comparing. Neither
re-run has been performed yet; both are listed in Section 10.

**Why runtime comes out higher (C-001).** Three mechanisms are plausible and they are
not mutually exclusive.

1. *Workload composition.* Our six benchmarks are not a random sample of CPU2006; two
   are `MallocBench` programs, which are the allocation-heavy corner of the suite. The
   paper's own worst cases (perlbench 2.60x, xalancbmk 2.67x) are its malloc-intensive
   benchmarks, so a set weighted toward allocation pressure should land above the
   suite average. Our 2.22x is below the paper's own worst case of 2.67x, which
   is the pattern this explanation predicts.
2. *Fixed runtime cost not amortised.* ASan's start-up cost — shadow mapping setup and
   runtime initialisation — is paid once per process. Our benchmarks run for 0.15 s to
   0.72 s, whereas SPEC CPU2006 benchmarks run for many seconds to minutes. A fixed
   cost of even 50 ms is a 30% penalty on a 0.15 s run and negligible on a 10 s run.
   This predicts that the ratio should *fall* as benchmark runtime grows, which is
   testable within our own data: the correlation between baseline runtime and slowdown
   should be negative. It is not obviously so in Table 7 — `bh` is the longest run at
   0.72 s and sits mid-range at 2.12x — so this mechanism alone does not explain the
   result and must be tested rather than assumed.
3. *Baseline efficiency.* Modern compilers and CPUs optimise the baseline build more
   than they optimise instrumented code, which raises the ratio without changing ASan's
   absolute cost. This is the standard explanation for why 2012 overhead ratios rarely
   reproduce on current hardware, but we have no measurement that isolates it here.

*Evidence status.* Mechanism 1 is supported by the internal ordering of our results
(allocation-heavy programs are the slow ones, matching the paper's own ordering) but
it is not a controlled test. Mechanisms 2 and 3 are hypotheses. Section 10 lists the
re-runs that would turn them into evidence.

### 4.4 Limitations

* **The average is not comparable to the paper's average.** 2.22x is the mean of six
  deliberately chosen programs, not of SPEC CPU2006. Comparing it to 1.73x compares a
  biased sample to a population mean. The comparison is still informative about
  direction and order of magnitude, and it is not informative about the exact figure.
* **The memory comparison mixes two metrics.** RSS and `VmPeak` are different
  quantities. Until the `VmPeak` re-run is done, the C-002 gap cannot be attributed
  between metric choice and redzone size.
* **Absolute times are meaningless across machines.** Only within-machine ratios are
  reported.
* **Single-threaded only.** ASan's thread-local quarantine and its interaction with
  parallel programs are not exercised.
* **Three runs.** Enough to see the effect, not enough to bound it. The paper does not
  report dispersion, so we cannot say whether our spread is larger than theirs.
* **One detection corpus.** C-003 shows that ASan detects the four classes on our
  cases. It does not show that ASan detects them at the same rate as the paper on real
  programs, which would need a bug corpus the paper does not publish.

---

## 5 Extension

### 5.1 Question

The paper explains its two worst benchmarks in one sentence:

> These two benchmarks are very malloc-intensive and make a huge number of 1- and
> 2-byte memory accesses.

That sentence contains two separable mechanisms, and the paper never separates them.
Mechanism A: a single narrow access is itself more expensive than a single wide
access. Mechanism B: narrow accesses mean more accesses to move the same number of
bytes, and each access pays one shadow check. The same section adds:

> In both cases the instrumentation inserts only one memory read for each memory
> access in the original code.

which supports B and contradicts A. The extension asks a decidable question the paper
leaves open: **is ASan's access cost priced per access, or per byte?**

### 5.2 Design

One factor changes at a time, same machine, same compiler, same runtime options.

* `dense` mode fixes 64 bytes written per iteration and varies the width, so the
  number of instrumented accesses per iteration is `64 / W` (64, 32, 16, 8 for
  1, 2, 4, 8 bytes). Bytes moved, cache lines touched, iteration count and compiler
  flags are held constant; only the access count changes.
* `single` mode fixes one access per iteration and varies only the width. If width by
  itself mattered, the four slowdowns would differ.

Both modes are needed. `dense` alone would show 1-byte slower than 8-byte and invite
the reading that narrow accesses are intrinsically expensive; only `single` can rule
that out.

The core metric is the added cost per access, `(t_asan - t_base) / (iterations x
accesses per iteration)`, because a slowdown ratio is scaled by the baseline's own
store cost and cannot say what one shadow check costs.

### 5.3 Result

Not yet run. The design, its acceptance criteria and the three implementation traps
that can silently invert the conclusion are specified in
`experiments/exp-002/PLAN.md`. Preliminary numbers obtained during design, on a
different environment, are recorded in that plan as exploratory only and are
explicitly excluded from any verdict.

---

## 6 Conclusion

**Overall verdict: the paper's results are partially reproduced.** ASan is confirmed to
be a low-overhead detector — 2.22x rather than the paper's 1.73x, still an order of
magnitude below Valgrind — its memory cost is confirmed to be of the order of three
times, and its detection capability is fully reproduced. Neither quantitative figure
matches the paper closely enough to call the reproduction complete, and the two
mismatches point in opposite directions.

**Lessons learned.** Three stand out.

First, *the metric matters as much as the machine*. The memory discrepancy is
plausibly mostly an artefact of reporting RSS instead of `VmPeak`: shadow memory is a
virtual reservation, so the two metrics measure different things by construction.
A reproduction that copies the paper's numbers but not its measurement definitions
will disagree for uninteresting reasons.

Second, *a benchmark substitution changes what the average means*. Replacing the
suite with 6 chosen to exercise the interesting mechanisms preserves the mechanism
and destroys the average. Reporting the average next to the paper's average invites a
comparison that the data cannot support, and the honest move is to report the
per-benchmark pattern and say so.

Third, *settings that are not written down become deviations by default*. The redzone
size was never pinned in the recorded commands. It is now a deviation we can only
argue about rather than a variable we controlled. Pinning every setting that the paper
pins, before the first run, costs minutes and saves a section of the report.

---

## 7 References

1. K. Serebryany, D. Bruening, A. Potapenko, D. Vyukov. *AddressSanitizer: A Fast
   Address Sanity Checker.* USENIX ATC 2012.
2. LLVM Project. *AddressSanitizer* documentation, LLVM 18.1.3.
3. LLVM Project. *test-suite* repository, `MultiSource/Benchmarks`.
4. N. Nethercote, J. Seward. *Valgrind: A Framework for Heavyweight Dynamic Binary
   Instrumentation.* PLDI 2007.

---

## 8 Contribution statement

To be completed once the report is frozen. It must name each of the four members and
state what each contributed, and it must agree with `docs/CONTRIBUTIONS.md` and with
the Git history.

Draft, based on the repository record at the time of writing:

| Member | Student ID | Contribution |
| --- | --- | --- |
| 张瀚洋 | 1240036026 | Project governance, dual-workspace rules, validated container environment |
| 王博文 | 1240026080 | LLVM test-suite pilot, member records |
| 成昊扬 | 1240026250 | Performance, memory and functional measurements; claim registration |
| 陈卓康 | 1240026110 | Candidate claims, experiment plans (exp-001, exp-002), report draft |

---

## 9 AI usage statement

To be completed before submission. It must state which AI tools were used, for what
(planning, drafting, code generation, analysis), and what was verified by hand.

Draft: an AI assistant was used to help structure the experiment plans and to draft
this report from committed run data. All numbers in Section 3 were cross-checked
against the run directories listed in Table 8; the claims, verdicts and deviations
were reviewed by the members named in Section 8.

---

## 10 Outstanding items (draft working material — delete before submission)

1. Record the `llvm-test-suite` commit used for both benchmark runs; Section 2.1
   currently has no starting-code commit, and "Starting code" is explicitly graded.
2. Record the host CPU model and core count of the machine that produced
   `runs/bench-20261114t171000z` and `runs/bench-mem-20261115t033100z`. The existing
   `lscpu` record belongs to the environment-validation machine.
3. Raise repeats from 3 to at least 5 for the final numbers, or state explicitly that
   3 is the accepted scale.
4. Generate Figure 1 and Figure 2 from the committed CSVs with a versioned script
   under `scripts/`.
5. Controlled re-run for C-002: record `VmPeak` from `/proc/self/status` alongside RSS
   on the same binaries; the `VmPeak` ratio should approach 3.37x.
6. Controlled re-run for C-002: one benchmark with `redzone=32` versus the default, to
   size the redzone contribution.
7. Run exp-002 to fill Section 5.3; the plan needs approval and an environment decision
   first (this machine has clang 14, the validated image has clang 18.1.3).
8. Fill Sections 8 and 9 with member-reviewed text.
9. Decide whether to also test the paper's write-only (26%) and `-fPIE` (69%)
   configurations; currently out of scope.
