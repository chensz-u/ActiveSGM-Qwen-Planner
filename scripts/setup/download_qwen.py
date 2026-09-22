#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from typing import Optional, Sequence


DEFAULT_MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"
REPO_ROOT = Path(__file__).resolve().parents[2]


def prepare_download_target(path: Path, force: bool = False) -> Path:
    target = path.expanduser().resolve()
    if target.exists() and not target.is_dir():
        raise NotADirectoryError(f"Download target is not a directory: {target}")
    if target.is_dir() and any(target.iterdir()) and not force:
        raise FileExistsError(
            f"Download target is not empty: {target}. "
            "Use --force to resume into it without deleting existing files."
        )
    target.mkdir(parents=True, exist_ok=True)
    return target


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a local Qwen planner model safely.")
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "models/Qwen2.5-1.5B-Instruct",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow resume into a non-empty directory; existing files are not deleted.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    target = prepare_download_target(args.output_dir, force=args.force)

    from huggingface_hub import snapshot_download

    snapshot_download(
        repo_id=args.model_id,
        local_dir=str(target),
        token=os.environ.get("HF_TOKEN") or None,
    )
    print(f"Downloaded {args.model_id} to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
