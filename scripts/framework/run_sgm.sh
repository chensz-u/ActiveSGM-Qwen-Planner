#!/usr/bin/env bash
set -euo pipefail

scene=${1:-office0}
exp=${2:-ActiveSem}
gpus=${3:-0}
dry_run=${4:-1}

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

cmd=(python "${REPO_ROOT}/src/main/sgm_launcher.py" \
  --dataset Replica \
  --scene "$scene" \
  --exp "$exp" \
  --gpus "$gpus" \
  --enable_vis 0)

if [[ "$dry_run" == "1" ]]; then
  cmd+=(--dry_run)
fi

"${cmd[@]}"
