Copy /home/narsi/projects/mobile_exp/android-ndk-r27d -> /workspace/android-ndk-r27d, 
copy /home/narsi/projects/mobile_exp/qairt/2.37.0.250724 -> /workspace/qairt_2.37.0.250724
copy /home/narsi/projects/mobile_exp/executorch -> /workspace/executorch

export ANDROID_NDK_ROOT=/workspace/android-ndk-r27d
export ANDROID_NDK=/workspace/android-ndk-r27d
export QNN_SDK_ROOT=/workspace/snpe_optimizer/qairt/2.37.0.250724
export EXECUTORCH_ROOT=/workspace/executorch
export LD_LIBRARY_PATH=$QNN_SDK_ROOT/lib/x86_64-linux-clang/:$LD_LIBRARY_PATH
export PYTHONPATH=$EXECUTORCH_ROOT/..
# Fix the Python OpInfo warning
export PYTHONPATH=$PYTHONPATH:$QNN_SDK_ROOT/lib/python

apt update
apt install -y software-properties-common
add-apt-repository ppa:ubuntu-toolchain-r/test -y
apt update
apt install pip cmake git flatbuffers-compiler unzip
apt install -y libc++1 libc++abi1 pkg-config

cd $EXECUTORCH_ROOT
./install_requirements.sh
# android target
./backends/qualcomm/scripts/build.sh
# (optional) linux embedded target
./backends/qualcomm/scripts/build.sh --enable_linux_embedded
# for release build
./backends/qualcomm/scripts/build.sh --release

pip install -r requirements-examples.txt

pip install ruamel.yaml parameterized numpy onnx flatbuffers tabulate typing-extensions
pip install --no-cache-dir torch==2.11 torchvision --index-url https://download.pytorch.org/whl/test/cu126

cd $EXECUTORCH_ROOT/build-x86
cmake ../examples/qualcomm \
  -DCMAKE_PREFIX_PATH="$PWD;$PWD/lib/cmake/ExecuTorch;$PWD/third-party/gflags;$PWD/third-party/abseil-cpp" \
  -DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=BOTH \
  -DPYTHON_EXECUTABLE=python3 \
  -Bexamples/qualcomm
cmake --build examples/qualcomm -j$(nproc)



apt install python3-pip
apt install python3.10-venv
apt-get install python3.10-dev python3.10-distutils python3-tk libfuse2 graphviz libgraphviz-dev
pip install pygraphviz
apt install wslu
