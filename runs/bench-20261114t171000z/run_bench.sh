#!/bin/bash
# ============================================================
# ASan 运行时间开销测量脚本（在 Docker 容器内运行）
# 复现 AddressSanitizer (USENIX ATC 2012) 的「平均 73% slowdown」主张
# 用法：容器里执行  bash /bench/run_bench.sh
# ============================================================
set -e

TS=/bench/llvm-test-suite
WORK=/bench

# 选定的 benchmark（整数/计算/指针密集，性质接近 SPEC CPU2006 的整数部分）
# 注：MallocBench/perl 与 MallocBench/gawk 因 1990 年代旧代码（隐式函数声明等）与现代 clang 不兼容，已排除
SUBDIRS="MultiSource/Benchmarks/MallocBench/espresso;MultiSource/Benchmarks/MallocBench/cfrac;MultiSource/Benchmarks/Olden/bh;MultiSource/Benchmarks/Ptrdist/anagram;MultiSource/Benchmarks/nbench;MultiSource/Benchmarks/Fhourstones"

# 先切到稳定目录，避免删除当前所在目录导致 cwd 失效
cd $WORK

# 清理上次残留的 build 目录（避免旧配置缓存干扰）
rm -rf $WORK/build-native $WORK/build-asan

# 创建 cc/c++ 符号链接（test-suite 的 host 工具编译默认用 cc）
ln -sf /usr/bin/clang-18 /usr/bin/cc
ln -sf /usr/bin/clang++-18 /usr/bin/c++

echo "=========================================="
echo "[1/6] 安装 lit（离线，wheel 已随 /bench 挂载）"
echo "=========================================="
mkdir -p /opt/lit
python3 -c "import zipfile; zipfile.ZipFile('/bench/lit-18.1.8-py3-none-any.whl').extractall('/opt/lit')"
export PYTHONPATH=/opt/lit:$PYTHONPATH
# 创建 lit 命令入口（wheel 的 console entry 是 lit.main:main，需手动包装）
cat > /usr/local/bin/lit << 'EOF'
#!/usr/bin/env python3
import sys
from lit.main import main
sys.argv[0] = "lit"
main()
EOF
chmod +x /usr/local/bin/lit
echo "lit 已就绪（离线）"

echo ""
echo "=========================================="
echo "[2/6] 编译 native 基线（clang-18 -O2）"
echo "=========================================="
cmake -B $WORK/build-native \
  -DCMAKE_C_COMPILER=clang-18 -DCMAKE_CXX_COMPILER=clang++-18 \
  -DCMAKE_C_FLAGS="-Wno-implicit-function-declaration" \
  -DTEST_SUITE_SUBDIRS="$SUBDIRS" \
  -DTEST_SUITE_COLLECT_CODE_SIZE=OFF \
  -C $TS/cmake/caches/O2.cmake \
  $TS
cmake --build $WORK/build-native -j"$(nproc)"
# 修复：test-suite 未把源码目录的 lit.local.cfg 复制进 build 目录，需手动补 traditional_output
echo "config.traditional_output = True" > $WORK/build-native/lit.local.cfg

echo ""
echo "=========================================="
echo "[3/6] 运行 native，共 3 次"
echo "=========================================="
for i in 1 2 3; do
  echo "--- native 第 $i 次 ---"
  lit -j 1 -o $WORK/native_$i.json $WORK/build-native || echo "(第 $i 次有 test 失败，继续)"
done

echo ""
echo "=========================================="
echo "[4/6] 编译 ASan（clang-18 -O2 -fsanitize=address）"
echo "=========================================="
cmake -B $WORK/build-asan \
  -DCMAKE_C_COMPILER=clang-18 -DCMAKE_CXX_COMPILER=clang++-18 \
  -DCMAKE_C_FLAGS="-fsanitize=address -fno-omit-frame-pointer -Wno-implicit-function-declaration" \
  -DCMAKE_CXX_FLAGS="-fsanitize=address -fno-omit-frame-pointer" \
  -DTEST_SUITE_SUBDIRS="$SUBDIRS" \
  -DTEST_SUITE_COLLECT_CODE_SIZE=OFF \
  -C $TS/cmake/caches/O2.cmake \
  $TS
cmake --build $WORK/build-asan -j"$(nproc)"
# 修复：同上，为 ASan build 目录也补上 traditional_output
echo "config.traditional_output = True" > $WORK/build-asan/lit.local.cfg

echo ""
echo "=========================================="
echo "[5/6] 运行 ASan，共 3 次（对齐论文设置：quarantine=0、禁用 malloc 栈回溯）"
echo "=========================================="
export ASAN_OPTIONS=quarantine_size_mb=0:malloc_context_size=0
for i in 1 2 3; do
  echo "--- ASan 第 $i 次 ---"
  lit -j 1 -o $WORK/asan_$i.json $WORK/build-asan || echo "(第 $i 次有 test 失败，继续)"
done

echo ""
echo "=========================================="
echo "[6/6] 分析结果，计算 slowdown"
echo "=========================================="
python3 $WORK/analyze.py

echo ""
echo "========== 全部完成 =========="
