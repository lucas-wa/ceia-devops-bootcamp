docker run -it \
  --rm \
  --network=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm-cpu-env \
  --model Qwen/Qwen2-1.5B-Instruct \
  --trust-remote-code \
  --device cpu \
  --dtype bfloat16 \
  --tokenizer-mode auto