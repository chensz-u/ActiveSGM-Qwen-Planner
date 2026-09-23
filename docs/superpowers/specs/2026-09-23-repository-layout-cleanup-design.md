# Repository Layout Cleanup Design

## Goal

Reorganize the public ActiveSGM-Qwen-Planner repository so that a new reader can
identify the core implementation, reproducible experiment entry points, analysis
utilities, tests, and historical research records without searching through a
crowded repository root.

The cleanup is structural only. It must not change planning behavior, experiment
parameters, recorded results, or the public reproducibility boundary.

## Scope

The cleanup will:

- move root-level experiment launchers into categorized experiment directories;
- move root-level analysis programs into a dedicated analysis directory;
- move historical experiment notes into a records directory;
- move shell-based checks into the test tree;
- move visualization and result-collection entry points into the existing script
  hierarchy;
- move focused guides into the documentation tree;
- add a concise repository map and an experiment index;
- update path resolution, documentation, and tests for the new locations.

The cleanup will not:

- reorganize `src/` or change planner, mapper, LLM, or visualization algorithms;
- reorganize the internal `configs/` hierarchy;
- change environment versions, model choices, experiment budgets, or guard
  thresholds;
- delete historical experiment records;
- add datasets, model weights, checkpoints, generated results, or other large
  artifacts;
- claim that the pending Ubuntu/CUDA/GPU smoke tests have passed.

## Target Layout

```text
ActiveSGM-Qwen-Planner/
|-- README.md
|-- QUICK_START.md
|-- PROJECT_MAP.md
|-- LICENSE
|-- .env.example
|-- src/
|-- configs/
|-- envs/
|-- data/
|-- experiments/
|   |-- README.md
|   |-- launchers/
|   |   |-- online/
|   |   `-- offline/
|   |-- analysis/
|   `-- records/
|-- scripts/
|   |-- setup/
|   |-- repro/
|   |-- evaluation/
|   `-- visualization/
|-- tests/
|   |-- shell/
|   `-- test_*.py
`-- docs/
    |-- guides/
    `-- superpowers/
```

## File Classification

### Experiment launchers

All root-level `run_office0_*.sh` files move to
`experiments/launchers/online/`. Root-level `run_offline_*.sh` files move to
`experiments/launchers/offline/`.

Each moved launcher must compute the repository root from its new location before
changing directory. A launcher must therefore remain callable from any working
directory and continue to place results under the same repository-relative
`results/` paths.

### Analysis programs

Root-level `analysis_*.py`, `offline_*.py`, and
`collect_three_run_summary.py` move to `experiments/analysis/`.

These programs currently treat input and output paths as relative to the process
working directory. That behavior is preserved: documented commands run them from
the repository root, so existing input and output locations do not change merely
because the source file moved.

### Research records

Root-level `notes_*.txt` and the Markdown research-design note move to
`experiments/records/`. These files remain historical evidence and are not
rewritten as current performance claims. References to renamed launcher paths are
updated only where needed to keep the record understandable.

### Tests

Root-level `test_*.sh` files move to `tests/shell/`. Like experiment launchers,
they must resolve the repository root from the script location before importing
project modules or reading repository assets.

Python unit and contract tests remain directly under `tests/`.

### Utilities and guides

- `run_visualization.sh` moves to `scripts/visualization/run_visualization.sh`.
- `collect_three_run_summary.py` is classified as experiment analysis rather than
  a reusable library and therefore moves to `experiments/analysis/`.
- `BASELINE_OFFICE0_SUCCESS.md` and `VISUALIZATION_GUIDE.md` move to
  `docs/guides/`.
- `download_qwen25_1_5b.py` remains at the repository root as a backward-compatible
  wrapper around `scripts/setup/download_qwen.py`.

## Navigation Documentation

`PROJECT_MAP.md` will describe the responsibility of every top-level directory,
identify the supported entry points, and direct readers to the detailed setup and
experiment guides.

`experiments/README.md` will group launchers by purpose and label historical,
offline-analysis, log-only, and apply-mode workflows. It will not imply that all
workflows have been rerun on the newly documented environment.

`README.md`, `QUICK_START.md`, moved guides, and current status documents will be
updated to use the new paths. Historical design and implementation plans may keep
old paths when they are describing what existed at the time, unless an old path
would be mistaken for a current command.

## Compatibility Rules

1. Use Git-aware moves so file history remains traceable.
2. Do not change exported environment variables, Slurm resources, experiment
   configuration files, result directory names, or Python entry points.
3. Every moved shell file must derive `REPO_ROOT` from its own new location and
   run project commands from that root.
4. Current public documentation must contain no executable commands pointing to
   obsolete root-level launcher or test paths.
5. The Qwen downloader compatibility wrapper remains callable as
   `python download_qwen25_1_5b.py`.
6. Generated analysis files remain ignored and are not committed as part of the
   cleanup.

## Validation

The completed cleanup must pass all of the following checks:

1. `python -m unittest discover -s tests -v`
2. `python -m compileall -q src scripts tests configs experiments`
3. the existing shell syntax contract over every tracked shell script;
4. `python scripts/repro/security_scan.py`
5. a repository-reference scan showing no current documentation or executable
   wrapper points to an obsolete root-level experiment path;
6. a root-layout contract test that rejects future tracked `analysis_*.py`,
   `offline_*.py`, `run_office0_*.sh`, `run_offline_*.sh`, `notes_*.txt`, and
   `test_*.sh` files at the repository root;
7. `git diff --check` and a final review of deleted versus renamed files.

GPU-only mapping and Qwen smoke runs remain pending unless they are actually run
on the supported Ubuntu 20.04/CUDA 11.7 environment. Structural validation must
not be reported as real-flight or full-experiment validation.

## Delivery

The work will be implemented on `codex/repository-layout-cleanup`. The branch will
contain only the structural moves, required path repairs, navigation documents,
and regression tests described above. Integration into `main` will occur only
after the full local validation suite passes and the resulting diff is reviewed.
