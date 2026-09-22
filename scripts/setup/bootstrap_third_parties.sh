#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
LOCK_FILE="${SCRIPT_DIR}/third_party.lock"
BUILD=0

if [[ "${1:-}" == "--build" ]]; then
  BUILD=1
elif [[ $# -gt 0 ]]; then
  echo "Usage: $0 [--build]" >&2
  exit 2
fi

clone_or_verify() {
  local name="$1" url="$2" commit="$3" relative_destination="$4"
  local destination="${REPO_ROOT}/${relative_destination}"

  if [[ -e "${destination}" ]]; then
    if [[ ! -d "${destination}/.git" ]]; then
      echo "Refusing to overwrite non-Git directory: ${destination}" >&2
      exit 3
    fi
    if ! git -C "${destination}" diff --quiet || \
       ! git -C "${destination}" diff --cached --quiet || \
       [[ -n "$(git -C "${destination}" status --porcelain --untracked-files=normal)" ]]; then
      echo "Refusing to modify dirty checkout: ${destination}" >&2
      exit 3
    fi
    local current_url
    current_url="$(git -C "${destination}" remote get-url origin)"
    if [[ "${current_url%.git}" != "${url%.git}" ]]; then
      echo "Origin mismatch for ${name}: ${current_url}" >&2
      exit 3
    fi
  else
    git clone --filter=blob:none --no-checkout "${url}" "${destination}"
  fi

  git -C "${destination}" fetch --depth 1 origin "${commit}"
  git -C "${destination}" checkout --detach "${commit}"
  echo "Pinned ${name} at ${commit}"
}

while IFS='|' read -r name url commit destination; do
  [[ -z "${name}" || "${name}" == \#* ]] && continue
  clone_or_verify "${name}" "${url}" "${commit}" "${destination}"
done < "${LOCK_FILE}"

if [[ "${BUILD}" -eq 0 ]]; then
  echo "Sources are ready. Re-run with --build inside the activesgm-cu117 environment."
  exit 0
fi

python -m pip install "${REPO_ROOT}/third_parties/pytorch3d"
python -m pip install "${REPO_ROOT}/third_parties/tiny-cuda-nn/bindings/torch"
python -m pip install "${REPO_ROOT}/third_parties/diff-gaussian-rasterization-w-depth"
python -m pip install "${REPO_ROOT}/third_parties/channel_rasterization"
python -m pip install "${REPO_ROOT}/third_parties/sparse_channel_rasterization"
python -m pip install "${REPO_ROOT}/third_parties/coslam/external/NumpyMarchingCubes"

pushd "${REPO_ROOT}/third_parties/habitat_sim" >/dev/null
python -m pip install -r requirements.txt
python setup.py install --headless --bullet
popd >/dev/null

python -m pip install \
  "torch-scatter==2.1.1" \
  "torch-sparse==0.6.17" \
  -f https://data.pyg.org/whl/torch-1.13.1+cu117.html

echo "Third-party dependencies built successfully."
