#!/bin/bash
set -euo pipefail

# ActiveSGM 可视化运行脚本
# 用法: bash scripts/visualization/run_visualization.sh [scene] [exp] [gpus] [enable_vis]
# 示例: bash scripts/visualization/run_visualization.sh office0 ActiveSem4060Vis 0 1

scene=${1:-office0}
exp=${2:-ActiveSem4060Vis}
gpus=${3:-0}
enable_vis=${4:-1}

echo "=========================================="
echo "ActiveSGM 可视化启动"
echo "=========================================="
echo "场景 (Scene): $scene"
echo "实验配置 (Experiment): $exp"
echo "GPU设备 (GPUs): $gpus"
echo "启用可视化 (Enable Visualization): $enable_vis"
echo "=========================================="

# 使用调用者已激活的环境，并从脚本位置解析项目目录。
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

# Reduce allocator fragmentation on 8GB GPUs.
export PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF:-max_split_size_mb:64,expandable_segments:True}

# 运行 ActiveSGM
python src/main/sgm_launcher.py \
  --dataset Replica \
  --scene "$scene" \
  --exp "$exp" \
  --gpus "$gpus" \
  --enable_vis "$enable_vis"

echo "=========================================="
echo "运行完成"
echo "=========================================="
