"""Backward-compatible entry point for the safe model downloader."""

from scripts.setup.download_qwen import main


if __name__ == "__main__":
    raise SystemExit(main())
