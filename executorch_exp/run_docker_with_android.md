docker run -it --privileged --name executorch \
  --runtime=nvidia \
  -v /dev/bus/usb:/dev/bus/usb \
  -v /home/narsi/projects/mobile_exp:/workspace/mobile_exp \
executorch-qnn:latest bash

# Install new package

apt update
apt install usbutils android-sdk-platform-tools pkg-config default-jdk openjdk-17-jdk android-sdk wget libpython3.10-dev
ulimit -n 4096
alias python=python3

export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
export ANDROID_HOME=/usr/lib/android-sdk
export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$PATH

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$EXECUTORCH_ROOT/build-x86/lib/

export DEMO_APP=/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo

ANDROID_ABIS=arm64-v8a ./scripts/build_android_library.sh


root@88e4d0e96967:/workspace/executorch# ./ 
.Package.swift/          .github/                 build-x86/               desktop/                 export/                  profiler/                shim/                    tools/                   
.ci/                     .wiki/                   cmake-android-out/       devtools/                extension/               run_python_script.sh     shim_et/                 util/                    
.claude/                 __pycache__/             codegen/                 docs/                    install_executorch.sh    runtime/                 src/                     website/                 
.git/                    backends/                configurations/          examples/                install_requirements.sh  schema/                  test/                    zephyr/                  
.githooks/               build-android/           data/                    exir/                    kernels/                 scripts/                 third-party/             
root@88e4d0e96967:/workspace/executorch# cd ../mobile_exp/executorch-examples/llm/android/LlamaDemo
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# cp /workspace/           
android-ndk-r27d/    executorch/          mobile_exp/          qairt_2.37.0.250724/ 
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# cp /workspace/mobile_exp/
.dockerignore                   android-ndk-r27d/               dlc_files/                      executorch-examples/            executorch__back/               qairt/                          
Dockerfile                      build_android_library_patch.sh  executorch/                     executorch.aar                  executorch_insall_tips.md       
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# cp /workspace/mobile_exp/executorch.aar ./app/libs/executorch.aar
cp: cannot create regular file './app/libs/executorch.aar': No such file or directory
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# ls
README.md  SDK-quick-setup-guide.md  app  build.gradle.kts  docs  gradle  gradle.properties  gradlew  gradlew.bat  run_instrumentation_test.sh  scripts  settings.gradle.kts
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# ./app/src/
androidTest/ main/        test/        
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# ./app/src/
androidTest/ main/        test/        
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# mkdir ./app/libs
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# cp /workspace/mobile_exp/executorch.aar ./app/libs/executorch.aar
root@88e4d0e96967:/workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo# 



The fact that `$ANDROID_HOME/tools/bin/` contains `e2fsck` and `mkfs.ext4` is a red flag. Those are Linux filesystem utilities, not Android development tools. This confirms that the Android SDK package currently installed in your environment is likely a "gutted" version provided by the Linux distribution that lacks the actual Google binaries.

Since the "Quick Fix" from my previous message didn't find the binary, you need to manually install the official **Android Command Line Tools**. 

Run these commands in order to set up a working `sdkmanager`:

### 1. Download and Install the Official Tools
We will download the tools directly from Google and place them in your existing SDK folder.

```bash
# Ensure we are in a temporary spot


# Download the latest command line tools (Linux version)
cd /tmp
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
apt-get install -y unzip
unzip commandlinetools-linux-*.zip -d /usr/lib/android-sdk/

# Unzip them into your SDK directory
# Note: This creates a folder named 'cmdline-tools'
apt-get install -y unzip
unzip commandlinetools-linux-*.zip -d /usr/lib/android-sdk/
```

---

### 2. Fix the Directory Structure (Crucial)
The `sdkmanager` is very picky. It expects to be inside a folder named `latest`. If you don't do this, it will throw an error saying it "could not determine the SDK root."

```bash
mkdir -p /usr/lib/android-sdk/cmdline-tools/latest
mv /usr/lib/android-sdk/cmdline-tools/bin /usr/lib/android-sdk/cmdline-tools/latest/
mv /usr/lib/android-sdk/cmdline-tools/lib /usr/lib/android-sdk/cmdline-tools/latest/
mv /usr/lib/android-sdk/cmdline-tools/source.properties /usr/lib/android-sdk/cmdline-tools/latest/
mv /usr/lib/android-sdk/cmdline-tools/NOTICE.txt /usr/lib/android-sdk/cmdline-tools/latest/
```

---

### 3. Accept Licenses and Install Build-Tools
Now that the real tool is in the right place, run the following:

```bash
# Accept all licenses
yes | /usr/lib/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses --sdk_root=/usr/lib/android-sdk
/usr/lib/android-sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=/usr/lib/android-sdk "platforms;android-35" "build-tools;35.0.0"
```

---

### 4. Run the Build
Now go back to your project directory and run the Gradle command again:

```bash
cd /workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo
./gradlew clean assembleDebug -PuseLocalAar=true
```

**What this did:**
You replaced the broken/empty system tools with the official Google binaries. By moving the files into the `latest` folder, you satisfied the `sdkmanager`'s requirement to know where the rest of the SDK lives. Gradle should now be able to find everything it needs.



python examples/qualcomm/oss_scripts/llama/qwen3_0_6b_qcs6490.py  \
  -b build-android -s 976b79f9 \ 
  -m QCM6490 \
  --decoder_model qwen3-0_6b \
  --prefill_ar_len 128 --max_seq_len 1024 \
  --prompt "I would like to learn python, could you teach me with a simple example?" \

python -m examples.qualcomm.oss_scripts.llama.llama -b build-android -s 976b79f9 -m QCM6490 --decoder_model qwen3-0_6b --prefill_ar_len 128 --max_seq_len 1024 --prompt "I would like to learn python, could you teach me with a simple example?" --ptq "8a8w" 


CUDA_VISIBLE_DEVICES="" python examples/qualcomm/oss_scripts/llama/qwen3_0_6b_qcs6490.py    -b build-android -s 976b79f9   --decoder_model qwen3-0_6b   --prefill_ar_len 128 --max_seq_len 1024   --prompt "I would like to learn python, could you teach me with a simple example?"   --tasks wikitext --limit 1

[INFO 2026-05-08 15:58:20,788 qnn_preprocess.py:70] Visiting: aten__to_copy_default_2293, aten._to_copy.default
[INFO 2026-05-08 15:58:20,790 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_15, aten.matmul.default
[INFO 2026-05-08 15:58:20,792 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_14, aten.matmul.default
[INFO 2026-05-08 15:58:20,794 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_13, aten.matmul.default
[INFO 2026-05-08 15:58:20,796 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_12, aten.matmul.default
[INFO 2026-05-08 15:58:20,798 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_11, aten.matmul.default
[INFO 2026-05-08 15:58:20,799 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_10, aten.matmul.default
[INFO 2026-05-08 15:58:20,801 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_9, aten.matmul.default
[INFO 2026-05-08 15:58:20,803 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_8, aten.matmul.default
[INFO 2026-05-08 15:58:20,805 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_7, aten.matmul.default
[INFO 2026-05-08 15:58:20,807 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_6, aten.matmul.default
[INFO 2026-05-08 15:58:20,808 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_5, aten.matmul.default
[INFO 2026-05-08 15:58:20,810 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_4, aten.matmul.default
[INFO 2026-05-08 15:58:20,812 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_3, aten.matmul.default
[INFO 2026-05-08 15:58:20,814 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_2, aten.matmul.default
[INFO 2026-05-08 15:58:20,816 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_1, aten.matmul.default
[INFO 2026-05-08 15:58:20,817 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_h_0, aten.matmul.default
[INFO 2026-05-08 15:58:20,819 qnn_preprocess.py:70] Visiting: aten_matmul_default_55_sha_concat, aten.cat.default
[INFO 2026-05-08 15:58:20,827 qnn_preprocess.py:70] Visiting: aten_view_copy_default_333, aten.view_copy.default
[INFO 2026-05-08 15:58:20,828 qnn_preprocess.py:70] Visiting: aten_permute_copy_default_2436, aten.permute_copy.default
[INFO 2026-05-08 15:58:20,829 qnn_preprocess.py:70] Visiting: aten__to_copy_default_2294, aten._to_copy.default
[INFO 2026-05-08 15:58:20,833 qnn_preprocess.py:70] Visiting: aten_convolution_default_192, aten.convolution.default
[INFO 2026-05-08 15:58:20,844 qnn_preprocess.py:70] Visiting: aten_permute_copy_default_2437, aten.permute_copy.default
[INFO 2026-05-08 15:58:20,846 qnn_preprocess.py:70] Visiting: aten_view_copy_default_334, aten.view_copy.default
[INFO 2026-05-08 15:58:20,847 qnn_preprocess.py:70] Visiting: aten_add_tensor_138, aten.add.Tensor
[INFO 2026-05-08 15:58:20,849 qnn_preprocess.py:70] Visiting: aten_rms_norm_default_111, aten.rms_norm.default
[INFO 2026-05-08 15:58:20,852 qnn_preprocess.py:70] Visiting: aten_view_copy_default_335, aten.view_copy.default
[INFO 2026-05-08 15:58:20,853 qnn_preprocess.py:70] Visiting: aten_permute_copy_default_2438, aten.permute_copy.default
[INFO 2026-05-08 15:58:20,855 qnn_preprocess.py:70] Visiting: aten_convolution_default_193, aten.convolution.default
[INFO 2026-05-08 15:58:20,876 qnn_preprocess.py:70] Visiting: aten_convolution_default_194, aten.convolution.default
[INFO 2026-05-08 15:58:20,896 qnn_preprocess.py:70] Visiting: aten_sigmoid_default_27, aten.sigmoid.default
[INFO 2026-05-08 15:58:20,898 qnn_preprocess.py:70] Visiting: aten_mul_tensor_279, aten.mul.Tensor
[INFO 2026-05-08 15:58:20,901 qnn_preprocess.py:70] Visiting: aten_mul_tensor_280, aten.mul.Tensor
[INFO 2026-05-08 15:58:20,904 qnn_preprocess.py:70] Visiting: aten__to_copy_default_2295, aten._to_copy.default
[INFO 2026-05-08 15:58:20,907 qnn_preprocess.py:70] Visiting: aten_convolution_default_195, aten.convolution.default
[INFO 2026-05-08 15:58:20,918 qnn_preprocess.py:70] Visiting: aten_permute_copy_default_2439, aten.permute_copy.default
[INFO 2026-05-08 15:58:20,920 qnn_preprocess.py:70] Visiting: aten_view_copy_default_336, aten.view_copy.default
[INFO 2026-05-08 15:58:20,921 qnn_preprocess.py:70] Visiting: aten__to_copy_default_2296, aten._to_copy.default
[INFO 2026-05-08 15:58:20,923 qnn_preprocess.py:70] Visiting: aten_add_tensor_139, aten.add.Tensor
[INFO 2026-05-08 15:58:20,925 qnn_preprocess.py:70] Visiting: aten_rms_norm_default_112, aten.rms_norm.default
[INFO 2026-05-08 15:58:20,930 qnn_preprocess.py:70] Visiting: aten_view_copy_default_337, aten.view_copy.default
[INFO 2026-05-08 15:58:20,931 qnn_preprocess.py:70] Visiting: aten_permute_copy_default_2440, aten.permute_copy.default
[INFO 2026-05-08 15:58:20,932 qnn_preprocess.py:70] Visiting: aten__to_copy_default_2297, aten._to_copy.default
[INFO 2026-05-08 15:58:20,936 qnn_preprocess.py:70] Visiting: aten_convolution_default_196, aten.convolution.default
[INFO 2026-05-08 15:58:21,969 qnn_preprocess.py:70] Visiting: aten_permute_copy_default_2441, aten.permute_copy.default
[INFO 2026-05-08 15:58:21,971 qnn_preprocess.py:70] Visiting: aten_squeeze_copy_dims_84, aten.squeeze_copy.dims

====== DDR bandwidth summary ======
spill_bytes=772096
fill_bytes=772096
write_total_bytes=3524864
read_total_bytes=690520320


====== DDR bandwidth summary ======
spill_bytes=1048576
fill_bytes=1048576
write_total_bytes=319553536
read_total_bytes=839995392

[INFO] [Qnn ExecuTorch]: Destroy Qnn context
/usr/lib/python3.10/copyreg.py:101: FutureWarning: `isinstance(treespec, LeafSpec)` is deprecated, use `isinstance(treespec, TreeSpec) and treespec.is_leaf()` instead.
  return cls.__new__(cls, *args)
[WARNING 2026-05-08 16:11:46,264 _program.py:1091] Op aten.unbind.int was requested for preservation by partitioner.  This request is ignored because it is in a blocklist.
[WARNING 2026-05-08 16:11:46,266 _program.py:1091] Op aten.unbind.int was requested for preservation by partitioner.  This request is ignored because it is in a blocklist.
[INFO] [Qnn ExecuTorch]: Destroy Qnn device
[INFO] [Qnn ExecuTorch]: Destroy Qnn backend
/workspace/executorch/exir/tensor.py:83: FutureWarning: guard_size_oblivious will be removed. Consider using explicit unbacked handling     potentially utilizing guard_or_false, guard_or_true, or statically_known_true
  return guard_size_oblivious(self.stride < other.stride)
/workspace/executorch/exir/tensor.py:83: FutureWarning: guard_size_oblivious will be removed. Consider using explicit unbacked handling     potentially utilizing guard_or_false, guard_or_true, or statically_known_true
  return guard_size_oblivious(self.stride < other.stride)
[INFO 2026-05-08 16:11:50,378 base_component.py:56] HybridTextDecoder::compile completed in 1268.269560098648s
[INFO 2026-05-08 16:11:50,379 base_component.py:56] MultiModalManager::compile completed in 1268.2697880268097s
[INFO 2026-05-08 16:11:50,379 export_utils.py:172] Using parser's config
[INFO 2026-05-08 16:11:50,379 export_utils.py:172] Using parser's config
./llama_qnn/hybrid_llama_qnn.pte: 1 file pushed. 165.5 MB/s (765402112 bytes in 4.410s)
build-android/examples/qualcomm/oss_scripts/llama/qnn_llama_runner: 1 file pushed. 186.5 MB/s (91320368 bytes in 0.467s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnHtp.so: 1 file pushed. 119.9 MB/s (2465168 bytes in 0.020s)
/workspace/qairt_2.37.0.250724/lib/hexagon-v68/unsigned/libQnnHtpV68Skel.so: 1 file pushed. 182.1 MB/s (8096348 bytes in 0.042s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnHtpV68Stub.so: 1 file pushed. 146.5 MB/s (708176 bytes in 0.005s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnHtpPrepare.so: 1 file pushed. 222.9 MB/s (69147960 bytes in 0.296s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnSystem.so: 1 file pushed. 150.7 MB/s (2549880 bytes in 0.016s)
build-android/backends/qualcomm/libqnn_executorch_backend.so: 1 file pushed. 77.3 MB/s (597792 bytes in 0.007s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnModelDlc.so: 1 file pushed. 105.2 MB/s (2479520 bytes in 0.022s)
/tmp/tmp7kzysf8a/input_list.txt: 1 file pushed.
./llama_qnn/tokenizer.json: 1 file pushed. 123.5 MB/s (11422638 bytes in 0.088s)
I tokenizers:regex.cpp:27] Registering override fallback regex
I 00:00:00.001690 executorch:runner.cpp:150] creating module: model_path=hybrid_llama_qnn.pte
I 00:00:00.001771 executorch:runner.cpp:151] creating runner: tokenizer_path=tokenizer.json
I 00:00:00.001813 executorch:runner.cpp:152] eval mode=1
I tokenizers:normalizer.cpp:102] Using NFC normalizer. Please notice that our implementation may not handle all edge cases.
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
E0000 00:00:1778256716.458879   26183 re2.cc:237] Error parsing '((?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s...': invalid perl operator: (?!
I tokenizers:re2_regex.cpp:27] Re2 failed to compile regex: ((?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}| ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+), error: invalid perl operator: (?!
This may be ok if a fallback regex is used.
I tokenizers:regex_lookahead.cpp:27] Creating PCRE2 regex
I 00:00:00.867238 executorch:llm_runner_helper.cpp:55] Loaded json tokenizer
[INFO] [Qnn ExecuTorch]: Deserializing processed data using QnnContextCustomProtocol
[INFO] [Qnn ExecuTorch]: Creating new backend bundle.
[INFO] [Qnn ExecuTorch]: create QNN Logger with log_level 1
[INFO] [Qnn ExecuTorch]: Initialize Qnn backend parameters for Qnn executorch backend type 2
[INFO] [Qnn ExecuTorch]: Caching: Caching is in RESTORE MODE.
[INFO] [Qnn ExecuTorch]: QnnContextCustomProtocol expected magic number: 0x5678abcd but get: 0x2000000
[INFO] [Qnn ExecuTorch]: Running level=1 optimization.
[INFO] [Qnn ExecuTorch]: Running level=1 optimization.
[INFO] [Qnn ExecuTorch]: Deserializing processed data using QnnContextCustomProtocol
[INFO] [Qnn ExecuTorch]: Use cached delegate handle for current method: kv_forward
I 00:00:02.917270 executorch:runner.cpp:231] Reading metadata from model
I 00:00:02.970067 executorch:runner.cpp:352] creating io_memory
I 00:00:02.974671 executorch:prompt_processor.cpp:271] Prompt Processor: total 23 prompt tokens (AR-128 * 1 iters)
I 00:00:03.145733 executorch:runner.cpp:466] RSS after prompt prefill: 829.218750 MiB (0 if unsupported)
I 00:01:15.509470 executorch:token_generator.cpp:356] Warning: Generation stopped at seq_len limit (1024) without reaching EOS token. Response may be incomplete.
I 00:01:15.509881 executorch:token_generator.cpp:363] - seq_len (1024) already equals compiled max_context_len (1024). Consider recompiling with larger --max_context_len.
I 00:01:15.510014 executorch:runner.cpp:481] RSS after finishing text generation: 829.218750 MiB (0 if unsupported)
I 00:01:15.513054 executorch:stats.h:161] 	Prompt Tokens: 23    Generated Tokens: 1000
I 00:01:15.513236 executorch:stats.h:167] 	Model Load Time:		2.968000 (seconds)
I 00:01:15.513360 executorch:stats.h:177] 	Total inference time:		72.540000 (seconds)		 Rate: 	13.785498 (tokens/second)
I 00:01:15.513477 executorch:stats.h:185] 		Prompt evaluation:	0.175000 (seconds)		 Rate: 	131.428571 (tokens/second)
I 00:01:15.513593 executorch:stats.h:196] 		Generated 1000 tokens:	72.365000 (seconds)		 Rate: 	13.818835 (tokens/second)
I 00:01:15.513708 executorch:stats.h:204] 	Time to first generated token:	0.175000 (seconds)
I 00:01:15.513819 executorch:stats.h:211] 	Sampling time over 1023 tokens:	1.580000 (seconds)
[INFO] [Qnn ExecuTorch]: Destroy Qnn context
[INFO] [Qnn ExecuTorch]: Destroy Qnn device
[INFO] [Qnn ExecuTorch]: Destroy Qnn backend

PyTorchObserver {"prefill_token_per_sec":131.429,"decode_token_per_sec":13.8188,"prompt_tokens":23,"generated_tokens":1000,"model_load_start_ms":1778256716039,"model_load_end_ms":1778256719007,"inference_start_ms":1778256719007,"inference_end_ms":1778256791547,"prompt_eval_end_ms":1778256719182,"first_token_ms":1778256719182,"aggregate_sampling_time_ms":1580,"SCALING_FACTOR_UNITS_PER_SECOND":1000}
/data/local/tmp/root/executorch/static_llm/outputs/outputs.txt: 1 file pulled. 0.4 MB/s (2299 bytes in 0.005s)
[ERROR 2026-05-08 16:13:11,729 qwen3_0_6b_qcs6490.py:123] Export failed: 'utf-8' codec can't decode byte 0x89 in position 641: invalid start byte
Traceback (most recent call last):
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/qwen3_0_6b_qcs6490.py", line 121, in main
    export_llama(args)
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 725, in export_llama
    inference(
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 236, in inference
    output_prompt = prompt_evaluator.run(prompt=args.prompt)
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/decoder_runtime_evaluator.py", line 352, in run
    self.adb.pull(
  File "/workspace/executorch/backends/qualcomm/export_utils.py", line 484, in pull
    callback()
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/decoder_runtime_evaluator.py", line 57, in post_process_model_output
    output_holder.append(f.read())
  File "/usr/lib/python3.10/codecs.py", line 322, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 641: invalid start byte
Traceback (most recent call last):
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/qwen3_0_6b_qcs6490.py", line 131, in <module>
    main()
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/qwen3_0_6b_qcs6490.py", line 121, in main
    export_llama(args)
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 725, in export_llama
    inference(
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 236, in inference
    output_prompt = prompt_evaluator.run(prompt=args.prompt)
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/decoder_runtime_evaluator.py", line 352, in run
    self.adb.pull(
  File "/workspace/executorch/backends/qualcomm/export_utils.py", line 484, in pull
    callback()
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/decoder_runtime_evaluator.py", line 57, in post_process_model_output
    output_holder.append(f.read())
  File "/usr/lib/python3.10/codecs.py", line 322, in decode
    (result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 641: invalid start byte


adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtp.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnSystem.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV69Stub.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV73Stub.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV75Stub.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV79Stub.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/hexagon-v69/unsigned/libQnnHtpV69Skel.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/hexagon-v73/unsigned/libQnnHtpV73Skel.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/hexagon-v75/unsigned/libQnnHtpV75Skel.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/hexagon-v79/unsigned/libQnnHtpV79Skel.so ${DEVICE_DIR}

adb push ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV68Stub.so ${DEVICE_DIR}
adb push ${QNN_SDK_ROOT}/lib/hexagon-v68/unsigned/libQnnHtpV68Skel.so ${DEVICE_DIR}

adb shell "cd ${DEVICE_DIR} \
           && export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${DEVICE_DIR} \
           && export ADSP_LIBRARY_PATH=$ADSP_LIBRARY_PATH:${DEVICE_DIR}"


adb shell "cd /data/local/tmp/llama && ./llama_main --model_path hybrid_llama_qnn.pte --tokenizer_path tokenizer.json --prompt 'Hello'"


# 1. Ensure you're in the LlamaDemo directory
cd /workspace/mobile_exp/executorch-examples/llm/android/LlamaDemo

# 2. Create jniLibs directory
mkdir -p app/src/main/jniLibs/arm64-v8a/

cp $QNN_SDK_ROOT/lib/aarch64-android/libQnnHtp.so app/src/main/jniLibs/arm64-v8a/
cp $QNN_SDK_ROOT/lib/aarch64-android/libQnnSystem.so app/src/main/jniLibs/arm64-v8a/
cp $QNN_SDK_ROOT/lib/aarch64-android/libQnnHtpV69Stub.so app/src/main/jniLibs/arm64-v8a/
cp $QNN_SDK_ROOT/lib/aarch64-android/libQnnHtpV73Stub.so app/src/main/jniLibs/arm64-v8a/
cp $QNN_SDK_ROOT/lib/aarch64-android/libQnnHtpV75Stub.so app/src/main/jniLibs/arm64-v8a/
cp $QNN_SDK_ROOT/lib/aarch64-android/libQnnHtpV79Stub.so app/src/main/jniLibs/arm64-v8a/
cp $QNN_SDK_ROOT/lib/aarch64-android/libQnnDsp.so app/src/main/jniLibs/arm64-v8a/

# 4. Copy DSP skel files to assets (critical for HTP firmware)
mkdir -p app/src/main/assets/
cp $QNN_SDK_ROOT/lib/hexagon-v69/unsigned/libQnnHtpV69Skel.so app/src/main/assets/
cp $QNN_SDK_ROOT/lib/hexagon-v73/unsigned/libQnnHtpV73Skel.so app/src/main/assets/
cp $QNN_SDK_ROOT/lib/hexagon-v75/unsigned/libQnnHtpV75Skel.so app/src/main/assets/
cp $QNN_SDK_ROOT/lib/hexagon-v79/unsigned/libQnnHtpV79Skel.so app/src/main/assets/

cp ${QNN_SDK_ROOT}/lib/aarch64-android/libQnnHtpV68Stub.so app/src/main/jniLibs/arm64-v8a/
cp ${QNN_SDK_ROOT}/lib/hexagon-v68/unsigned/libQnnHtpV68Skel.so app/src/main/assets/

# 5. Also ensure executorch libs are there
cp /workspace/executorch/cmake-android-out/extension/android/libexecutorch_jni.so \
   app/src/main/jniLibs/arm64-v8a/libexecutorch.so
cp /workspace/executorch/cmake-android-out/lib/libqnn_executorch_backend.so \
   app/src/main/jniLibs/arm64-v8a/

# 6. REBUILD APK
./gradlew clean assembleDebug

# 7. Reinstall
adb install -r app/build/outputs/apk/debug/app-debug.apk


adb shell "cd ${DEVICE_DIR} \
           && ./qnn_executor_runner --model_path ./dlv3_qnn.pte"


 00:00:01.846631 executorch:runner.cpp:231] Reading metadata from model
I 00:00:01.865104 executorch:runner.cpp:352] creating io_memory
I 00:00:01.867249 executorch:prompt_processor.cpp:271] Prompt Processor: total 23 prompt tokens (AR-1 * 23 iters)
I 00:00:03.631205 executorch:runner.cpp:466] RSS after prompt prefill: 824.355469 MiB (0 if unsupported)
I 00:01:35.770932 executorch:token_generator.cpp:356] Warning: Generation stopped at seq_len limit (1024) without reaching EOS token. Response may be incomplete.
I 00:01:35.771269 executorch:token_generator.cpp:363] - seq_len (1024) already equals compiled max_context_len (1024). Consider recompiling with larger --max_context_len.
I 00:01:35.771407 executorch:runner.cpp:481] RSS after finishing text generation: 824.355469 MiB (0 if unsupported)
I 00:01:35.771705 executorch:stats.h:161] 	Prompt Tokens: 23    Generated Tokens: 1000
I 00:01:35.771837 executorch:stats.h:167] 	Model Load Time:		1.864000 (seconds)
I 00:01:35.771956 executorch:stats.h:177] 	Total inference time:		93.906000 (seconds)		 Rate: 	10.648947 (tokens/second)
I 00:01:35.772074 executorch:stats.h:185] 		Prompt evaluation:	1.765000 (seconds)		 Rate: 	13.031161 (tokens/second)
I 00:01:35.772189 executorch:stats.h:196] 		Generated 1000 tokens:	92.141000 (seconds)		 Rate: 	10.852932 (tokens/second)
I 00:01:35.772306 executorch:stats.h:204] 	Time to first generated token:	1.765000 (seconds)
I 00:01:35.772420 executorch:stats.h:211] 	Sampling time over 1023 tokens:	17.339000 (seconds)
[INFO] [Qnn ExecuTorch]: Destroy Qnn context
[INFO] [Qnn ExecuTorch]: Destroy Qnn device
[INFO] [Qnn ExecuTorch]: Destroy Qnn backend


build-android/examples/qualcomm/oss_scripts/llama/qnn_llama_runner: 1 file pushed. 244.2 MB/s (91320368 bytes in 0.357s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnHtp.so: 1 file pushed. 163.2 MB/s (2465168 bytes in 0.014s)
/workspace/qairt_2.37.0.250724/lib/hexagon-v68/unsigned/libQnnHtpV68Skel.so: 1 file pushed. 193.4 MB/s (8096348 bytes in 0.040s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnHtpV68Stub.so: 1 file pushed. 118.8 MB/s (708176 bytes in 0.006s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnHtpPrepare.so: 1 file pushed. 239.3 MB/s (69147960 bytes in 0.276s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnSystem.so: 1 file pushed. 154.0 MB/s (2549880 bytes in 0.016s)
build-android/backends/qualcomm/libqnn_executorch_backend.so: 1 file pushed. 79.1 MB/s (597792 bytes in 0.007s)
/workspace/qairt_2.37.0.250724/lib/aarch64-android/libQnnModelDlc.so: 1 file pushed. 87.9 MB/s (2479520 bytes in 0.027s)

I 00:00:01.675943 executorch:runner.cpp:231] Reading metadata from model
I 00:00:01.711552 executorch:runner.cpp:352] creating io_memory
I 00:00:01.716823 executorch:prompt_processor.cpp:271] Prompt Processor: total 23 prompt tokens (AR-128 * 1 iters)
I 00:00:01.874784 executorch:runner.cpp:466] RSS after prompt prefill: 788.113281 MiB (0 if unsupported)
I 00:01:34.040719 executorch:token_generator.cpp:356] Warning: Generation stopped at seq_len limit (1024) without reaching EOS token. Response may be incomplete.
I 00:01:34.041083 executorch:token_generator.cpp:363] - seq_len (1024) already equals compiled max_context_len (1024). Consider recompiling with larger --max_context_len.
I 00:01:34.041190 executorch:runner.cpp:481] RSS after finishing text generation: 788.113281 MiB (0 if unsupported)
I 00:01:34.044587 executorch:stats.h:161] 	Prompt Tokens: 23    Generated Tokens: 1000
I 00:01:34.044756 executorch:stats.h:167] 	Model Load Time:		1.710000 (seconds)
I 00:01:34.044859 executorch:stats.h:177] 	Total inference time:		92.329000 (seconds)		 Rate: 	10.830833 (tokens/second)
I 00:01:34.044961 executorch:stats.h:185] 		Prompt evaluation:	0.163000 (seconds)		 Rate: 	141.104294 (tokens/second)
I 00:01:34.045096 executorch:stats.h:196] 		Generated 1000 tokens:	92.166000 (seconds)		 Rate: 	10.849988 (tokens/second)
I 00:01:34.045237 executorch:stats.h:204] 	Time to first generated token:	0.163000 (seconds)
I 00:01:34.045340 executorch:stats.h:211] 	Sampling time over 1023 tokens:	17.295000 (seconds)
[INFO] [Qnn ExecuTorch]: Destroy Qnn context
[INFO] [Qnn ExecuTorch]: Destroy Qnn device
[INFO] [Qnn ExecuTorch]: Destroy Qnn backend



05-09 01:29:00.174  3696  7163 D iris@ForegroundUtils: Id: 7292 ProcessName: com.example.executorchllamademo  Label: ExecuTorchLlamaDemo
05-09 01:29:18.343  7292  7350 I ExecuTorch: Reading file /sys/devices/soc0/image_version
05-09 01:29:18.344  7292  7350 I ExecuTorch: Failed to open midr file /sys/devices/soc0/image_version
05-09 01:29:18.344  7292  7350 I ExecuTorch: Number of efficient cores 4
05-09 01:29:18.344  7292  7350 I ExecuTorch: Resetting threadpool to 3 threads
05-09 01:29:18.344  7292  7350 I ExecuTorch: Reading file /sys/devices/soc0/image_version
05-09 01:29:18.344  7292  7350 I ExecuTorch: Failed to open midr file /sys/devices/soc0/image_version
05-09 01:29:18.344  7292  7350 I ExecuTorch: Number of efficient cores 4
05-09 01:29:18.344  7292  7350 I ExecuTorch: Resetting threadpool to 3 threads.
05-09 01:29:18.345  7292  7350 I ExecuTorch: creating module: model_path=/data/local/tmp/llama/hybrid_llama_qnn.pte
05-09 01:29:18.345  7292  7350 I ExecuTorch: creating runner: tokenizer_path=/data/local/tmp/llama/tokenizer.json
05-09 01:29:18.345  7292  7350 I ExecuTorch: eval mode=1
05-09 01:29:19.189  7292  7350 I ExecuTorch: Loaded json tokenizer
05-09 01:29:19.190  7292  7350 I [Qnn ExecuTorch]: Deserializing processed data using QnnContextCustomProtocol
05-09 01:29:19.191  7292  7350 I [Qnn ExecuTorch]: Creating new backend bundle.
05-09 01:29:19.192  7292  7350 I [Qnn ExecuTorch]: create QNN Logger with log_level 1
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> DspTransport.openSession qnn_open failed, 0x80000406, prio 100
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> IDspTransport: Unable to load lib 0x80000406
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> DspTransport.getHandle failed, error 0x00000008
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> createDspTransportInstance failed to config transport object
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> error in creation of transport instance
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> Failed to create transport for device, error: 1002
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> Failed to load skel, error: 1002
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> Transport layer setup failed: 14001
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> Failed to parse default platform info: 14001
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> Failed to load default platform info: 14001
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: QnnDsp <E> Failed to parse platform config: 14001
05-09 01:29:19.272  7292  7350 E [Qnn ExecuTorch]: Failed to create device_handle for Backend ID 6, error=14001
05-09 01:29:19.272  7292  7350 E ExecuTorch: Fail to configure Qnn device
05-09 01:29:19.272  7292  7350 I [Qnn ExecuTorch]: Destroy Qnn backend
05-09 01:29:19.272  7292  7350 E ExecuTorch: Fail to get or create shared Qnn backend bundle. Error code: 1
05-09 01:29:19.272  7292  7350 E ExecuTorch: Fail to initialize Qnn Manager
05-09 01:29:19.272  7292  7350 E ExecuTorch: Init failed for backend QnnBackend: 0x1












adb shell "cd /data/local/tmp/root/executorch/static_llm && export LD_LIBRARY_PATH=. && export ADSP_LIBRARY_PATH='.;/vendor/lib/rfsa/adsp' && ./qnn_llama_runner --model_path ./hybrid_llama_qnn.pte --tokenizer_path ./tokenizer.json --prompt '<|im_start|>user\nI would like to learn python, could you teach me with a simple example?<|im_end|>\n<|im_start|>assistant' && cat outputs.txt"


adb longcat -c && adb logcat | grep -E "ExecuTorch"

adb shell "rm -rf /data/local/tmp/llama" && adb shell "mkdir /data/local/tmp/llama" && adb push *_llama_qnn.pte /data/local/tmp/llama/ && adb push tokenizer.json /data/local/tmp/llama/

python -m examples.qualcomm.oss_scripts.llama.llama -b build-android -s 976b79f9 -m QCM6490 --decoder_model qwen3-0_6b --max_seq_len 1024 --prompt "I would like to learn python, could you teach me with a simple example?" --model_mode kv hybrid --prefill_ar_len 128


























1.7B

ERROR] [Qnn ExecuTorch]: QnnDsp <E> fastrpc memory map for fd: 19 with length: 2040528896 failed with error: 0x1

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> fastrpc memory map error reporting failed

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Mapping buffer fd 19 to FastRpc failed on domain 3

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> SharedMemoryMod failed to Map Buffer to SMMU for domain 0

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to map buffer of size 2040528896

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to map weights buffer to device!

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Could not allocate persistent weights buffer!

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to initialize graph memory

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to initialize graph with id 256 context 1 deviceId 0 coreId 0 pdId 0 with err 1002

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Context create from binary failed for deviceId 0 coreId 0 pdId 0 for context 1, err 1002

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Context 1 failed on pd 0

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Cannot establish more than one connection to QNN skel: 1009

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to create a new transport session for deviceId 0, coreId 0, pdId 2: err: 1009

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Error in creating transport session for deviceId 0, coreId 0, pdId 2, err: 1009

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Error in creating transport session for deviceId 0, coreId 0, pdId 2, err: 1009

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Cannot establish more than one connection to QNN skel: 1009

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to create a new transport session for deviceId 0, coreId 0, pdId 3: err: 1009

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Error in creating transport session for deviceId 0, coreId 0, pdId 3, err: 1009

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Error in creating transport session for deviceId 0, coreId 0, pdId 3, err: 1009

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> DspTransport.openSession qnn_open failed, 0x00000200, prio 100

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> DspTransport.getHandle failed, error 0x0000000f

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> createDspTransportInstance failed to config transport object

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> error in creation of transport instance

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to create a new transport session for deviceId 0, coreId 0, pdId 1: err: 1002

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Error in creating transport session for deviceId 0, coreId 0, pdId 1, err: 1002

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Error in creating transport session for deviceId 0, coreId 0, pdId 1, err: 1002

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to find available PD for contextId 1 on deviceId 0 coreId 0with context size estimate 2107622144

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> context create from binary failed on contextId 1

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Fail to create context from binary with err 1002

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Size Calculation encounter error! Doing Hard reset of reserved mem to 0.

[ERROR] [Qnn ExecuTorch]: QnnDsp <E> Failed to create context from binary with err 0x3ea

[ERROR] [Qnn ExecuTorch]: Can't create context from binary. Error 1002.
E 00:00:01.863995 executorch:QnnManager.cpp:268] Fail to configure Qnn context
E 00:00:01.864013 executorch:QnnExecuTorchBackend.cpp:99] Fail to initialize Qnn Manager
E 00:00:01.864027 executorch:method.cpp:132] Init failed for backend QnnBackend: 0x1
F 00:00:01.866276 executorch:result.h:170] In function CheckOk(), assert failed: hasValue_
Aborted 
Traceback (most recent call last):
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 744, in main
    export_llama(args)
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 725, in export_llama
    inference(
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 236, in inference
    output_prompt = prompt_evaluator.run(prompt=args.prompt)
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/decoder_runtime_evaluator.py", line 351, in run
    self.adb.execute(custom_runner_cmd=runner_cmd)
  File "/workspace/executorch/backends/qualcomm/export_utils.py", line 475, in execute
    self._adb(
  File "/workspace/executorch/backends/qualcomm/export_utils.py", line 365, in _adb
    raise RuntimeError(f"adb command failed: {cmds}")
RuntimeError: adb command failed: ['adb', '-s', '976b79f9', 'shell', 'cd /data/local/tmp/root/executorch/static_llm && ./qnn_llama_runner --decoder_model_version qwen3 --tokenizer_path tokenizer.json --output_path /data/local/tmp/root/executorch/static_llm/outputs/outputs.txt --performance_output_path /data/local/tmp/root/executorch/static_llm/outputs/inference_speed.txt --shared_buffer --model_path kv_llama_qnn.pte  --eval_mode 0 --temperature 0.8 --system_prompt \'\'  --seq_len 1024 --prompt "I would like to learn python, could you teach me with a simple example?" --seq_len 1024']

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.10/runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib/python3.10/runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 755, in <module>
    main()
  File "/workspace/executorch/examples/qualcomm/oss_scripts/llama/llama.py", line 750, in main
    raise Exception(e)
Exception: adb command failed: ['adb', '-s', '976b79f9', 'shell', 'cd /data/local/tmp/root/executorch/static_llm && ./qnn_llama_runner --decoder_model_version qwen3 --tokenizer_path tokenizer.json --output_path /data/local/tmp/root/executorch/static_llm/outputs/outputs.txt --performance_output_path /data/local/tmp/root/executorch/static_llm/outputs/inference_speed.txt --shared_buffer --model_path kv_llama_qnn.pte  --eval_mode 0 --temperature 0.8 --system_prompt \'\'  --seq_len 1024 --prompt "I would like to learn python, could you teach me with a simple example?" --seq_len 1024']
root@0714455ac877:/workspace/executorch# 



INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_add_tensor_138, aten.add.Tensor
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_rms_norm_default_111, aten.rms_norm.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_view_copy_default_335, aten.view_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_permute_copy_default_2438, aten.permute_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten__to_copy_default_1088, aten._to_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_convolution_default_193, aten.convolution.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten__to_copy_default_1089, aten._to_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_convolution_default_194, aten.convolution.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten__to_copy_default_1090, aten._to_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_sigmoid_default_27, aten.sigmoid.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_mul_tensor_279, aten.mul.Tensor
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_mul_tensor_280, aten.mul.Tensor
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten__to_copy_default_1091, aten._to_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_convolution_default_195, aten.convolution.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_permute_copy_default_2439, aten.permute_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_view_copy_default_336, aten.view_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten__to_copy_default_1092, aten._to_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_add_tensor_139, aten.add.Tensor
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_rms_norm_default_112, aten.rms_norm.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_view_copy_default_337, aten.view_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_permute_copy_default_2440, aten.permute_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten__to_copy_default_1093, aten._to_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_convolution_default_196, aten.convolution.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_permute_copy_default_2441, aten.permute_copy.default
INFO:executorch.backends.qualcomm.qnn_preprocess:Visiting: aten_squeeze_copy_dims_84, aten.squeeze_copy.dims
[ERROR] [Qnn ExecuTorch]: grdep_clone_op.cc:340::ERROR:failed to clone op(0x939A500000A99)

Segmentation fault (core dumped)
root@0714455ac877:/workspace/executorch# 

