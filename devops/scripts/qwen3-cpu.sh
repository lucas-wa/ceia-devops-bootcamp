#!/bin/bash

export VLLM_TARGET_DEVICE="cpu"

vllm serve unsloth/Qwen3-8B-bnb-4bit --multi-step-stream-outputs --dtype 'float16' --device 'cpu' --max-num-batched-tokens 2048