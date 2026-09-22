#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "This installer supports Ubuntu 20.04/Linux only." >&2
  exit 2
fi

if ! command -v conda >/dev/null 2>&1; then
  echo "conda was not found. Install Miniconda or Mambaforge first." >&2
  exit 2
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
ENV_FILE="${REPO_ROOT}/envs/environment-cu117.yml"
ENV_NAME="${ACTIVESGM_ENV_NAME:-activesgm-cu117}"

eval "$(conda shell.bash hook)"

if conda env list | awk '{print $1}' | grep -Fxq "${ENV_NAME}"; then
  conda env update --name "${ENV_NAME}" --file "${ENV_FILE}" --prune
else
  conda env create --name "${ENV_NAME}" --file "${ENV_FILE}"
fi

conda activate "${ENV_NAME}"
python -m pip install --upgrade "pip==24.0"
python -m pip install \
  "torch==1.13.1+cu117" \
  "torchvision==0.14.1+cu117" \
  "torchaudio==0.13.1+cu117" \
  --extra-index-url https://download.pytorch.org/whl/cu117
python -m pip install \
  "mmcv-full==1.6.0" \
  -f https://download.openmmlab.com/mmcv/dist/cu117/torch1.13.0/index.html
python -m pip install -r "${REPO_ROOT}/envs/requirements-repro.txt"

echo "Base environment installed. Next run:"
echo "  bash scripts/setup/bootstrap_third_parties.sh --build"
if [[ -f "${REPO_ROOT}/scripts/repro/check_environment.py" ]]; then
  python "${REPO_ROOT}/scripts/repro/check_environment.py" --allow-missing-assets
fi
