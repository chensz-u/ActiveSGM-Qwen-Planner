#!/usr/bin/env python3
import argparse
import importlib
import platform
import sys
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    detail: str


def version_matches(actual: str, expected: str) -> bool:
    return actual.strip() == expected.strip()


def check_import(
    module_name: str,
    expected_version: Optional[str] = None,
    distribution_name: Optional[str] = None,
) -> CheckResult:
    try:
        importlib.import_module(module_name)
    except Exception as exc:
        return CheckResult(module_name, "FAIL", f"not importable ({type(exc).__name__})")

    if expected_version is None:
        return CheckResult(module_name, "PASS", "importable")

    distribution = distribution_name or module_name
    try:
        actual = metadata.version(distribution)
    except metadata.PackageNotFoundError:
        return CheckResult(module_name, "FAIL", f"distribution metadata missing: {distribution}")
    status = "PASS" if version_matches(actual, expected_version) else "FAIL"
    return CheckResult(module_name, status, f"expected {expected_version}, found {actual}")


def check_cuda(allow_no_gpu: bool) -> CheckResult:
    try:
        import torch
    except Exception as exc:
        return CheckResult("CUDA", "FAIL", f"PyTorch unavailable ({type(exc).__name__})")
    if torch.cuda.is_available():
        return CheckResult("CUDA", "PASS", torch.cuda.get_device_name(0))
    status = "SKIP" if allow_no_gpu else "FAIL"
    return CheckResult("CUDA", status, "no CUDA device visible")


def check_path(name: str, path: Path, allow_missing: bool) -> CheckResult:
    if path.exists():
        return CheckResult(name, "PASS", str(path))
    status = "SKIP" if allow_missing else "FAIL"
    return CheckResult(name, status, f"missing: {path}")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check the supported ActiveSGM runtime.")
    parser.add_argument("--allow-no-gpu", action="store_true")
    parser.add_argument("--allow-missing-assets", action="store_true")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    results = []
    linux_status = "PASS" if platform.system() == "Linux" else "FAIL"
    results.append(CheckResult("platform", linux_status, platform.platform()))
    python_status = "PASS" if sys.version_info[:2] == (3, 8) else "FAIL"
    results.append(CheckResult("python", python_status, platform.python_version()))

    package_checks = (
        ("torch", "1.13.1+cu117", "torch"),
        ("torchvision", "0.14.1+cu117", "torchvision"),
        ("mmcv", "1.6.0", "mmcv-full"),
        ("mmdet", "2.25.3", "mmdet"),
        ("mmseg", "0.26.0", "mmsegmentation"),
        ("transformers", "4.45.2", "transformers"),
        ("habitat_sim", None, None),
    )
    results.extend(check_import(*item) for item in package_checks)
    results.append(check_cuda(args.allow_no_gpu))

    asset_paths = (
        ("third_parties", REPO_ROOT / "third_parties"),
        ("Replica data", REPO_ROOT / "data/replica_v1"),
        ("Replica NVS data", REPO_ROOT / "data/replica_sim_nvs"),
        ("Qwen model", REPO_ROOT / "models/Qwen2.5-1.5B-Instruct"),
    )
    results.extend(
        check_path(name, path, args.allow_missing_assets) for name, path in asset_paths
    )

    for result in results:
        print(f"[{result.status:4}] {result.name}: {result.detail}")
    return 1 if any(result.status == "FAIL" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
