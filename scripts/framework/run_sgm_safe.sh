#!/usr/bin/env bash
set -euo pipefail

scene=${1:-office0}
gpus=${2:-0}
dry_run=${3:-1}

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

cmd=(bash "${SCRIPT_DIR}/run_sgm.sh" "$scene" ActiveSafe "$gpus" "$dry_run")
"${cmd[@]}"
