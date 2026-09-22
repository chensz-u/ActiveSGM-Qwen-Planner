import os
from pathlib import Path
from typing import Mapping, Optional


REPO_ROOT = Path(__file__).resolve().parents[2]


def resolve_qwen_model_path(
    environ: Optional[Mapping[str, str]] = None,
) -> Path:
    """Return an existing local Qwen model directory.

    The environment override is intentionally explicit so model weights remain
    outside Git. A repository-local ignored directory is the convenient default.
    """
    values = os.environ if environ is None else environ
    configured = values.get("QWEN_PLANNER_MODEL_PATH")
    path = Path(configured).expanduser() if configured else (
        REPO_ROOT / "models/Qwen2.5-1.5B-Instruct"
    )
    path = path.resolve()
    if not path.is_dir():
        raise FileNotFoundError(
            f"Qwen model directory not found: {path}. "
            "Set QWEN_PLANNER_MODEL_PATH or run "
            "python scripts/setup/download_qwen.py --output-dir <path>."
        )
    return path
