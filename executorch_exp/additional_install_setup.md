# Additional notes for LLAMMA:
alias python=python3
pip install hydra-core huggingface_hub tiktoken torchtune sentencepiece tokenizers snakeviz lm_eval==0.4.5 blobfile safetensors
apt update
apt install libgflags-dev libgoogle-glog-dev usbutils android-sdk-platform-tools pkg-config default-jdk openjdk-17-jdk android-sdk  wget libpython3.10-dev

// cp /usr/include/x86_64-linux-gnu/python3.10/pyconfig.h /usr/include/python3.10/

ulimit -n 4096

cd /tmp
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
apt-get install -y unzip
unzip commandlinetools-linux-*.zip -d /usr/lib/android-sdk/

mkdir -p /usr/lib/android-sdk/cmdline-tools/latest
mv /usr/lib/android-sdk/cmdline-tools/bin /usr/lib/android-sdk/cmdline-tools/latest/
mv /usr/lib/android-sdk/cmdline-tools/lib /usr/lib/android-sdk/cmdline-tools/latest/
mv /usr/lib/android-sdk/cmdline-tools/source.properties /usr/lib/android-sdk/cmdline-tools/latest/
mv /usr/lib/android-sdk/cmdline-tools/NOTICE.txt /usr/lib/android-sdk/cmdline-tools/latest/

yes | /usr/lib/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses --sdk_root=/usr/lib/android-sdk
/usr/lib/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/usr/lib/android-sdk "platforms;android-35" "build-tools;35.0.0"


cd $EXECUTORCH_ROOT
./backends/qualcomm/scripts/build.sh

# Assuming the AOT component is already built
cd $EXECUTORCH_ROOT/build-x86
cmake ../examples/qualcomm \
  -DCMAKE_PREFIX_PATH="$PWD/lib/cmake/ExecuTorch;$PWD/third-party/gflags;" \
  -DCMAKE_FIND_ROOT_PATH_MODE_PACKAGE=BOTH \
  -DPYTHON_EXECUTABLE=python3 \
  -Bexamples/qualcomm

cmake --build examples/qualcomm -j$(nproc)

# Confirm the runner binary exists
ls examples/qualcomm/executor_runner/qnn_executor_runner


export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
export ANDROID_HOME=/usr/lib/android-sdk
export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$EXECUTORCH_ROOT/build-x86/lib/
echo "sdk.dir=/usr/lib/android-sdk" > extension/android/local.properties

ANDROID_ABIS=arm64-v8a ./scripts/build_android_library.sh