#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
DATA_ROOT="${ACTIVESGM_DATA_ROOT:-${REPO_ROOT}/data}"

required_paths=(
  "${DATA_ROOT}/replica_v1/office_0/habitat"
  "${DATA_ROOT}/replica_sim_nvs"
  "${DATA_ROOT}/Replica/office0"
)
for path in "${required_paths[@]}"; do
  if [[ ! -e "${path}" ]]; then
    echo "Required Replica asset is missing: ${path}" >&2
    exit 4
  fi
done

if [[ -z "${QWEN_PLANNER_MODEL_PATH:-}" || ! -d "${QWEN_PLANNER_MODEL_PATH}" ]]; then
  echo "Set QWEN_PLANNER_MODEL_PATH to the local Qwen2.5 model directory." >&2
  exit 4
fi

export ACTIVESGM_DATA_ROOT="${DATA_ROOT}"
export ACTIVE_SGM_LLM_MODE="${ACTIVE_SGM_LLM_MODE:-qwen_rank_efficiency_logonly}"
export ACTIVE_SGM_LLM_APPLY=0
export TRANSFORMERS_OFFLINE=1
export HF_HUB_OFFLINE=1
export WANDB_MODE=disabled

RESULT_DIR="${REPO_ROOT}/results/smoke/office0_$(date +%Y%m%d_%H%M%S)"
mkdir -p "${RESULT_DIR}"
cd "${REPO_ROOT}"

python src/main/activesgm.py \
  --cfg configs/Replica/office0/ActiveSemSmoke.py \
  --seed 0 \
  --result_dir "${RESULT_DIR}" \
  --enable_vis 0

echo "Office0 smoke run completed: ${RESULT_DIR}"
