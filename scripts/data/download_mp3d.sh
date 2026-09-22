#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
OUTPUT_DIR="${ACTIVESGM_MP3D_ROOT:-${ACTIVESGM_DATA_ROOT:-${REPO_ROOT}/data}/MP3D}"

while read p; do
  python "${REPO_ROOT}/src/data/download_mp.py" -o "${OUTPUT_DIR}" --id "$p" --task_data habitat
#  echo "$p"
done < "${SCRIPT_DIR}/scan_id.txt"
