#!/usr/bin/env python3
import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAX_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True)
class Finding:
    path: Path
    kind: str
    message: str


PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN " + r"(?:OPENSSH |RSA |EC )?PRIVATE KEY-----")),
    ("hf-token", re.compile(r"hf_" + r"[A-Za-z0-9]{20,}")),
    ("github-token", re.compile(r"gh[pousr]_" + r"[A-Za-z0-9]{30,}")),
    ("aws-key", re.compile(r"AKIA" + r"[A-Z0-9]{16}")),
    (
        "personal-path",
        re.compile(
            r"/data/run01/"
            + r"scxj889|/home/"
            + r"chen(?:/|\b)|~/run/"
            + r"miniconda3|/mnt/"
            + r"Data\d+/"
        ),
    ),
    (
        "private-endpoint",
        re.compile(
            r"[A-Za-z0-9._-]+@"
            + r"(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}):"
        ),
    ),
    ("fixed-proxy", re.compile(r"172\.24\.206\.4:3128")),
)


def tracked_paths() -> List[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [
        REPO_ROOT / item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    ]


def scan_paths(paths: Iterable[Path], max_bytes: int = DEFAULT_MAX_BYTES) -> List[Finding]:
    findings: List[Finding] = []
    for path in paths:
        path = Path(path)
        try:
            size = path.stat().st_size
        except OSError as exc:
            findings.append(Finding(path, "unreadable", f"cannot inspect file ({type(exc).__name__})"))
            continue
        if size > max_bytes:
            findings.append(Finding(path, "large-file", f"file exceeds {max_bytes} bytes"))
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        text = data.decode("utf-8", errors="replace")
        for kind, pattern in PATTERNS:
            if pattern.search(text):
                findings.append(Finding(path, kind, f"{kind} pattern detected"))
    return findings


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan tracked files before publication.")
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    paths = args.paths or tracked_paths()
    findings = scan_paths(paths, max_bytes=args.max_bytes)
    for finding in findings:
        try:
            display = finding.path.resolve().relative_to(REPO_ROOT)
        except ValueError:
            display = finding.path
        print(f"FAIL {display}: {finding.message}")
    if findings:
        print(f"Security scan failed with {len(findings)} finding(s).")
        return 1
    print(f"Security scan passed for {len(paths)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
