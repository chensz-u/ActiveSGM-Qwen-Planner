# Project Map

## Start Here

- [README](README.md): project scope and evidence boundary.
- [Quick Start](QUICK_START.md): reproducible Ubuntu/CUDA setup.
- [Experiments](experiments/README.md): launchers, analysis, and historical records.

## Repository Layout

| Path | Responsibility |
| --- | --- |
| `src/` | ActiveSGM, semantic mapping, planning, LLM reranking, and visualization code. |
| `configs/` | Dataset, scene, planner, and smoke-test configurations. |
| `experiments/` | Research launchers, offline analysis programs, and historical records. |
| `scripts/` | Reusable setup, reproduction, evaluation, data, and visualization utilities. |
| `tests/` | Python contracts and shell-based planner checks. |
| `docs/` | Current guides, project status, and design/implementation records. |
| `envs/` | Reproducible environment definitions. |

## Evidence Boundary

Local source checks do not replace the pending Ubuntu 20.04/CUDA 11.7 Qwen and mapping smoke tests. See [Reproducibility Status](docs/REPRODUCIBILITY_STATUS.md).
