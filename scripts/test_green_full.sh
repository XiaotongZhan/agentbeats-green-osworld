#!/bin/bash
set -e
source "$(dirname "$0")/setup_env.sh"
cd "$(dirname "$0")/.."

echo "Running full benchmark on OSWorld..."

python -m agents.green.run \
  --agent_name "qwen/qwen2.5-vl-32b-instruct" \
  --model "qwen/qwen2.5-vl-32b-instruct" \
  --test_all_meta_path third_party/osworld/evaluation_examples/test_all.json \
  --result_dir ./results_full \
  --provider_name aws \
  --os_type Ubuntu \
  --headless \
  --max_steps 5 \
  --num_envs 2

echo
echo "Full benchmark finished. Summary:"
jq '.meta, .results[:5]' ./results_full/metrics.json