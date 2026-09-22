#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../.." && pwd)"

echo "This compatibility entry point now uses the reproducible installer."
bash "${REPO_ROOT}/scripts/setup/install_environment.sh"
echo "Activate activesgm-cu117, then run:"
echo "  bash scripts/setup/bootstrap_third_parties.sh --build"
