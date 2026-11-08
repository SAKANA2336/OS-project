ARG BASE_IMAGE
FROM ${BASE_IMAGE}

LABEL org.os-project.environment="asan-functional-v0"

ARG DEBIAN_FRONTEND=noninteractive
RUN timeout --kill-after=10s 600s sh -eu -c \
    'apt-get -o Acquire::Retries=2 -o Acquire::http::Timeout=30 update; \
     apt-get -o Acquire::Retries=2 -o Acquire::http::Timeout=30 install -y --no-install-recommends \
       ca-certificates clang-18 llvm-18 libclang-rt-18-dev libc6-dev libstdc++-13-dev \
       cmake ninja-build make git python3 time util-linux; \
     apt-get clean; \
     rm -rf /var/lib/apt/lists/*'

ENV CC=clang-18 \
    CXX=clang++-18 \
    ASAN_SYMBOLIZER_PATH=/usr/bin/llvm-symbolizer-18 \
    PYTHONDONTWRITEBYTECODE=1 \
    LC_ALL=C.UTF-8 \
    HOME=/tmp

WORKDIR /opt/asan-check
COPY cases.c normal.cpp verify.py ./
USER 65534:65534
ENTRYPOINT ["python3", "/opt/asan-check/verify.py"]
CMD ["--output", "/evidence/validation"]
