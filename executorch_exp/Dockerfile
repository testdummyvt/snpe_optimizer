FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu22.04

# Suppress interactive prompts (e.g. timezone selection) during apt installs
ENV DEBIAN_FRONTEND=noninteractive

# ── System packages ───────────────────────────────────────────────────────────
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:ubuntu-toolchain-r/test -y && \
    apt-get update && \
    apt-get install -y \
        python3-pip \
        cmake \
        git \
        flatbuffers-compiler \
        unzip \
        libc++1 \
        libc++abi1 && \
    rm -rf /var/lib/apt/lists/*

# ── Copy assets into the image ────────────────────────────────────────────────
WORKDIR /workspace

COPY android-ndk-r27d       /workspace/android-ndk-r27d
COPY qairt/2.37.0.250724    /workspace/qairt_2.37.0.250724
COPY executorch             /workspace/executorch

# ── Environment variables ─────────────────────────────────────────────────────
ENV ANDROID_NDK_ROOT=/workspace/android-ndk-r27d \
    ANDROID_NDK=/workspace/android-ndk-r27d \
    QNN_SDK_ROOT=/workspace/qairt_2.37.0.250724 \
    EXECUTORCH_ROOT=/workspace/executorch \
    PYTHONPATH=/workspace:/workspace/qairt_2.37.0.250724/lib/python

ENV LD_LIBRARY_PATH=/workspace/qairt_2.37.0.250724/lib/x86_64-linux-clang:${LD_LIBRARY_PATH}

# ── ExecuTorch base Python requirements ───────────────────────────────────────
RUN pip3 install --upgrade pip && \
    cd /workspace/executorch && \
    ./install_requirements.sh

# ── Qualcomm backend build (Android aarch64 + x86_64, release mode) ───────────
# build.sh installs backends/qualcomm/requirements.txt and runs both
# the x86_64 host build (build-x86/) and the Android cross-build (build-android/).
RUN cd /workspace/executorch && \
    ./backends/qualcomm/scripts/build.sh --release

# ── Additional Python packages ────────────────────────────────────────────────
# requirements-examples.txt and extras are installed before torch so that
# torch==2.11 (installed last) wins over any conflicting version pulled in
# by install_requirements.sh above.
RUN pip3 install -r /workspace/executorch/requirements-examples.txt && \
    pip3 install \
        ruamel.yaml \
        parameterized \
        numpy \
        onnx \
        flatbuffers \
        tabulate \
        typing-extensions && \
    pip3 uninstall -y torchvision && \
    pip3 install --no-cache-dir torch==2.11 torchvision \
        --index-url https://download.pytorch.org/whl/test/cu126

# ── Build ExecuTorch Qualcomm examples ───────────────────────────────────────
# build-x86/ is created by build.sh above; cmake wires examples against it.
RUN cd /workspace/executorch/build-x86 && \
    cmake ../examples/qualcomm \
        -DCMAKE_PREFIX_PATH="$PWD;$PWD/lib/cmake/ExecuTorch;$PWD/third-party/gflags;$PWD/third-party/abseil-cpp" \
        -DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=BOTH \
        -DPYTHON_EXECUTABLE=python3 \
        -Bexamples/qualcomm && \
    cmake --build examples/qualcomm -j$(nproc)

WORKDIR /workspace
