# Reproducibility Status

Last updated: 2026-09-22

## Verified on the development machine

Platform: Windows 11, Python 3.13.5, NVIDIA RTX 4060 Laptop GPU. This machine is used only for source-level validation; it is not the supported runtime environment.

| Check | Command | Result |
| --- | --- | --- |
| Unit and contract tests | `python -m unittest discover -s tests -v` | PASS, 20 tests |
| Python syntax/import compilation | `python -m compileall -q src scripts tests configs` | PASS |
| Shell syntax | Included in `ShellSyntaxTests` using Git Bash `bash -n` | PASS, 68 scripts |
| Publication safety | `python scripts/repro/security_scan.py` | PASS, 466 tracked files |
| Environment diagnosis | `python scripts/repro/check_environment.py --allow-no-gpu --allow-missing-assets` | Expected FAIL: this machine has Python 3.13.5 and PyTorch 2.7.1+cu118; OpenMMLab, Transformers, Habitat, data, third parties, and the local Qwen model are absent |

The environment diagnostic failure is evidence that this Windows environment is not being represented as a successful ActiveSGM installation.

## Pending on the supported GPU server

Target: Ubuntu 20.04, Python 3.8, NVIDIA GPU, CUDA 11.7.

The following checks have not yet been executed on that target and therefore are not claimed as passing:

1. `bash scripts/setup/install_environment.sh`
2. `bash scripts/setup/bootstrap_third_parties.sh --build`
3. `python scripts/repro/check_environment.py`
4. `python scripts/repro/smoke_qwen.py`
5. `bash scripts/repro/smoke_office0.sh`

The final command is a 20-step `Replica office0` Qwen log-only smoke run. Passing it establishes that the installation path can enter the mapping/planning loop; it does not reproduce the full 2000-step experiment or validate a paper-level performance claim.
