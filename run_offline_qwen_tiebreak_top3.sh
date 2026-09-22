#!/bin/bash
#SBATCH -J qwen_tiebreak3
#SBATCH -p gpu_4090
#SBATCH --gpus=1
#SBATCH --cpus-per-task=4
#SBATCH -t 00:30:00

: "${CONDA_PREFIX:?Activate the activesgm-cu117 environment before submitting this job}"
REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "${REPO_ROOT}"
export PYTHONPATH="${REPO_ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
: "${QWEN_PLANNER_MODEL_PATH:?Set QWEN_PLANNER_MODEL_PATH before submitting this job}"
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128

echo "===== ENV CHECK ====="
hostname
date
pwd
which python
python --version
nvidia-smi
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"

echo "===== START OFFLINE QWEN TOP3 TIEBREAK ====="
python offline_qwen_tiebreak_top3.py
