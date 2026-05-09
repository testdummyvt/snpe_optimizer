# Copyright (c) Qualcomm Innovation Center, Inc.
# All rights reserved
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""
Qwen3-0.6B export & inference for QCS6490 (QCM6490 / V68 NPU).

The QCS6490 uses a V68 HTP which does NOT support 4-bit weights.
This script overrides the default Qwen3-0.6B quantization recipe to use
8-bit activations and 8-bit weights (W8A8) with selective 16a8w layers,
then re-uses llama.py's compile and inference pipeline.
"""

import logging
import sys
from dataclasses import dataclass

import torch
from executorch.backends.qualcomm.quantizer.custom_annotation import annotate_kv_8bit
from executorch.backends.qualcomm.quantizer.quant_recipe import (
    QuantGranularity,
    QuantRecipe,
)
from executorch.backends.qualcomm.quantizer.quantizer import QuantDtype
from executorch.examples.qualcomm.oss_scripts.llama import (
    Qwen3_0_6B,
    SUPPORTED_LLM_MODELS,
)
from executorch.examples.qualcomm.oss_scripts.llama.static_llm_quant_recipe import (
    StaticLLMQuantRecipe,
)
from torchao.quantization.pt2e import MinMaxObserver


class Qwen3_0_6BQuantRecipe(StaticLLMQuantRecipe):
    default_quant_dtype = QuantDtype.use_16a8w

    def __init__(self, verbose: bool = False):
        super().__init__()

        self.recipe = (
            QuantRecipe(
                self.default_quant_dtype,
                False,
                act_observer=MinMaxObserver,
                granularity=QuantGranularity.PER_TENSOR,
                verbose=verbose,
            )
            .add_node_target(
                {
                    torch.ops.aten.conv2d.default,
                },
                QuantDtype.use_16a8w,
                False,
                act_observer=MinMaxObserver,
                granularity=QuantGranularity.PER_CHANNEL,
            )
            .add_regex(
                {
                    r"layers\..*\.feed_forward\.w2_conv",
                },
                QuantDtype.use_16a8w,
                False,
                act_observer=MinMaxObserver,
                granularity=QuantGranularity.PER_CHANNEL,
            )
        )
        self.recipe.custom_quant_annotations.append(annotate_kv_8bit)


class Qwen3_0_6B_QCS6490_QuantRecipe(StaticLLMQuantRecipe):
    """
    8a8w recipe for Qwen3-0.6B on QCS6490 (V68).
    V68 does not support 4-bit weights, so we fall back to 8a8w
    with 16a8w for a few accuracy-sensitive layers.
    """

    default_quant_dtype = QuantDtype.use_8a8w

    def __init__(self, verbose: bool = False):
        super().__init__()

        self.recipe = (
            QuantRecipe(
                self.default_quant_dtype,
                False,
                act_observer=MinMaxObserver,
                granularity=QuantGranularity.PER_TENSOR,
                verbose=verbose,
            )
            .add_node_target(
                {
                    torch.ops.aten.conv2d.default,
                },
                QuantDtype.use_8a8w,
                False,
                act_observer=MinMaxObserver,
                granularity=QuantGranularity.PER_CHANNEL,
            )
            .add_regex(
                {
                    r"layers\..*\.feed_forward\.w2_conv",
                },
                QuantDtype.use_16a8w,
                False,
                act_observer=MinMaxObserver,
                granularity=QuantGranularity.PER_CHANNEL,
            )
            .add_regex(
                {
                    r"output\.conv",
                },
                QuantDtype.use_16a8w,
                False,
                act_observer=MinMaxObserver,
                granularity=QuantGranularity.PER_CHANNEL,
            )
        )
        self.recipe.custom_quant_annotations.append(annotate_kv_8bit)


# The decorator in __init__.py returns an instance, so grab the underlying class.
_Qwen3_0_6B_Class = type(Qwen3_0_6B)


@dataclass(init=False, frozen=True)
class Qwen3_0_6B_QCS6490(_Qwen3_0_6B_Class):
    quant_recipe = Qwen3_0_6B_QCS6490_QuantRecipe


# Replace the original qwen3-0_6b config with our QCS6490-safe one.
SUPPORTED_LLM_MODELS["qwen3-0_6b"] = Qwen3_0_6B_QCS6490()

# Now safe to import llama.py machinery.
from executorch.examples.qualcomm.oss_scripts.llama.llama import (
    _build_parser,
    export_llama,
)


def main():
    parser = _build_parser()

    # Override defaults for QCS6490 convenience.
    parser.set_defaults(
        decoder_model="qwen3-0_6b",
        soc_model="QCM6490",
        temperature=0,
        model_mode="hybrid",
    )

    args = parser.parse_args()

    try:
        export_llama(args)
    except Exception as e:
        logging.error(f"Export failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    FORMAT = "[%(levelname)s %(asctime)s %(filename)s:%(lineno)s] %(message)s"
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    sys.setrecursionlimit(4096)
    main()
