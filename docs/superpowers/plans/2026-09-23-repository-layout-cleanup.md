# Repository Layout Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize root-level experiment, analysis, record, test, and guide files into clear directories without changing ActiveSGM-Qwen planning behavior or experiment parameters.

**Architecture:** Keep `src/` and `configs/` intact. Treat `experiments/` as the home for research workflows and evidence, retain reusable operational tooling under `scripts/`, and use contract tests to keep the repository root clean and every moved shell entry point repository-relative.

**Tech Stack:** Git, Python 3.8+, `unittest`, Bash, PowerShell for local orchestration, Markdown.

---

### Task 1: Add repository-layout contracts

**Files:**
- Modify: `tests/test_repro_contract.py`
- Test: `tests/test_repro_contract.py`

- [ ] **Step 1: Add a failing root-layout contract**

Add this class before `ShellSyntaxTests`:

```python
class RepositoryLayoutTests(unittest.TestCase):
    def test_experiment_artifacts_do_not_live_at_repository_root(self):
        forbidden_patterns = (
            "analysis_*.py",
            "offline_*.py",
            "run_office0_*.sh",
            "run_offline_*.sh",
            "notes_*.txt",
            "test_*.sh",
        )
        offenders = sorted(
            path.name
            for pattern in forbidden_patterns
            for path in ROOT.glob(pattern)
            if path.is_file()
        )
        self.assertEqual([], offenders)

    def test_navigation_files_exist(self):
        expected = (
            ROOT / "PROJECT_MAP.md",
            ROOT / "experiments/README.md",
            ROOT / "docs/guides/BASELINE_OFFICE0_SUCCESS.md",
            ROOT / "docs/guides/VISUALIZATION_GUIDE.md",
        )
        self.assertEqual([], [str(path.relative_to(ROOT)) for path in expected if not path.is_file()])
```

- [ ] **Step 2: Run the new tests and confirm they fail for the expected reason**

Run:

```powershell
python -m unittest tests.test_repro_contract.RepositoryLayoutTests -v
```

Expected: two failures listing the current root-level clutter and missing navigation files.

- [ ] **Step 3: Commit the red contract separately**

```powershell
git add tests/test_repro_contract.py
git commit -m "test: define repository layout contract"
```

### Task 2: Move analysis programs and historical records

**Files:**
- Move to `experiments/analysis/`:
  - `analysis_apply_v2_guard_simulation_510729.py`
  - `analysis_derived_planner_metrics.py`
  - `analysis_inspect_rank_efficiency_accepts_510729.py`
  - `analysis_next_guard_policy.py`
  - `analysis_qwen_global_local_logonly_535859.py`
  - `analysis_qwen_global_local_v2_logonly_539645.py`
  - `analysis_qwen_rank_efficiency_apply_v2_524227.py`
  - `analysis_qwen_rank_efficiency_logonly_510729.py`
  - `analysis_rank_efficiency_guard_v1.py`
  - `analysis_view_decision_graph_enhanced.py`
  - `analysis_view_decision_graph.py`
  - `collect_three_run_summary.py`
  - `offline_qwen_guarded_rerank_analysis.py`
  - `offline_qwen_rerank_llm_logs_topk.py`
  - `offline_qwen_tiebreak_top3.py`
- Move to `experiments/records/`:
  - `notes_experiment_summary_for_paper.txt`
  - `notes_fake_llm_full_474606.txt`
  - `notes_online_qwen_reranker_unit_485490.txt`
  - `notes_qwen_global_local_logonly_inspection_535859.txt`
  - `notes_qwen_global_local_v3_soft_consistency_design.md`
  - `notes_qwen_json_test_477297.txt`
  - `notes_qwen_offline_rerank_delta_analysis.txt`
  - `notes_qwen_offline_rerank_topk_479180.txt`
  - `notes_qwen_rank_efficiency_accept_case_inspection.txt`
  - `notes_qwen_rank_efficiency_apply_v2_524227.txt`
  - `notes_qwen_rank_efficiency_logonly_510729.txt`
  - `notes_qwen_rank_efficiency_unit_509688.txt`
  - `notes_qwen_tiebreak_apply_491621.txt`
  - `notes_qwen_tiebreak_apply_strict_v1_499558.txt`
  - `notes_qwen_tiebreak_online_logonly_489943.txt`
  - `notes_qwen_tiebreak_top3_distance_strict.txt`
  - `notes_rank_efficiency_guard_analysis.txt`

- [ ] **Step 1: Create the target directories**

```powershell
New-Item -ItemType Directory -Path experiments/analysis -Force
New-Item -ItemType Directory -Path experiments/records -Force
```

- [ ] **Step 2: Move every listed file with Git history preserved**

Use `git mv <old-path> <new-path>` for each file listed above. Do not alter input/output constants in the analysis programs; they remain relative to the caller's working directory.

- [ ] **Step 3: Compile the relocated Python programs**

```powershell
python -m compileall -q experiments/analysis
```

Expected: exit code 0 and no output.

- [ ] **Step 4: Review rename detection**

```powershell
git status --short
git diff --summary
```

Expected: moves are shown as renames or delete/add pairs with identical content; there must be no unplanned deletion.

- [ ] **Step 5: Commit the analysis and record moves**

```powershell
git add experiments
git commit -m "refactor: group experiment analysis and records"
```

### Task 3: Move launchers and shell tests, then repair repository-root discovery

**Files:**
- Move to `experiments/launchers/online/`:
  - `run_office0_fake_llm_full_night.sh`
  - `run_office0_full_semfix.sh`
  - `run_office0_llm_log_test.sh`
  - `run_office0_mainonly_semfix.sh`
  - `run_office0_qwen_global_local_logonly.sh`
  - `run_office0_qwen_global_local_v2_logonly.sh`
  - `run_office0_qwen_rank_efficiency_apply_v2.sh`
  - `run_office0_qwen_rank_efficiency_logonly.sh`
  - `run_office0_qwen_tiebreak_apply.sh`
  - `run_office0_qwen_tiebreak_apply_strict_v1.sh`
  - `run_office0_qwen_tiebreak_logonly.sh`
- Move to `experiments/launchers/offline/`:
  - `run_offline_qwen_rerank_topk.sh`
  - `run_offline_qwen_tiebreak_top3.sh`
- Move to `tests/shell/`:
  - `test_online_qwen_reranker_unit.sh`
  - `test_qwen_global_local_unit.sh`
  - `test_qwen_global_local_v2_unit.sh`
  - `test_qwen_global_local_v3_unit.sh`
  - `test_qwen_planner_json_v2.sh`
  - `test_qwen_rank_efficiency_unit.sh`
- Move: `run_visualization.sh` to `scripts/visualization/run_visualization.sh`
- Modify: all moved shell files
- Test: `tests/test_repro_contract.py`

- [ ] **Step 1: Move the shell entry points with Git history preserved**

Create `experiments/launchers/online`, `experiments/launchers/offline`, `tests/shell`, and `scripts/visualization`, then use `git mv` for every file listed above.

- [ ] **Step 2: Repair online and offline launcher root discovery**

In every file under `experiments/launchers/online/` and `experiments/launchers/offline/`, replace the old root calculation with:

```bash
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../../.." && pwd)"
cd "${REPO_ROOT}"
```

Keep the existing `PYTHONPATH`, environment variables, Slurm directives, result paths, and experiment arguments unchanged.

- [ ] **Step 3: Repair offline Python entry points**

In `experiments/launchers/offline/run_offline_qwen_rerank_topk.sh`, change only the final command to:

```bash
python experiments/analysis/offline_qwen_rerank_llm_logs_topk.py
```

In `experiments/launchers/offline/run_offline_qwen_tiebreak_top3.sh`, change only the final command to:

```bash
python experiments/analysis/offline_qwen_tiebreak_top3.py
```

- [ ] **Step 4: Repair shell-test root discovery**

In every file under `tests/shell/`, use:

```bash
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"
```

Do not change the inline test cases or expected planner behavior.

- [ ] **Step 5: Repair visualization root discovery**

In `scripts/visualization/run_visualization.sh`, use:

```bash
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"
```

- [ ] **Step 6: Extend the contract tests for moved shell paths**

Add this method to `RepositoryLayoutTests`:

```python
    def test_moved_shell_entry_points_resolve_repository_root(self):
        expectations = {
            ROOT / "experiments/launchers/online": '${SCRIPT_DIR}/../../..',
            ROOT / "experiments/launchers/offline": '${SCRIPT_DIR}/../../..',
            ROOT / "tests/shell": '${SCRIPT_DIR}/../..',
            ROOT / "scripts/visualization": '${SCRIPT_DIR}/../..',
        }
        for directory, marker in expectations.items():
            scripts = sorted(directory.glob("*.sh"))
            self.assertTrue(scripts, msg=str(directory.relative_to(ROOT)))
            for script in scripts:
                content = script.read_text(encoding="utf-8")
                self.assertIn(marker, content, msg=str(script.relative_to(ROOT)))
```

- [ ] **Step 7: Run the shell and layout contracts**

```powershell
python -m unittest tests.test_repro_contract.RepositoryLayoutTests tests.test_repro_contract.ShellSyntaxTests -v
```

Expected: shell-root and shell-syntax checks pass; navigation-file checks may remain red until Task 4.

- [ ] **Step 8: Commit the relocated shell workflows**

```powershell
git add experiments/launchers tests/shell scripts/visualization tests/test_repro_contract.py
git commit -m "refactor: organize experiment and test launchers"
```

### Task 4: Move guides and add repository navigation

**Files:**
- Move: `BASELINE_OFFICE0_SUCCESS.md` to `docs/guides/BASELINE_OFFICE0_SUCCESS.md`
- Move: `VISUALIZATION_GUIDE.md` to `docs/guides/VISUALIZATION_GUIDE.md`
- Create: `PROJECT_MAP.md`
- Create: `experiments/README.md`
- Modify: `docs/guides/VISUALIZATION_GUIDE.md`
- Test: `tests/test_repro_contract.py`

- [ ] **Step 1: Move the two guides**

Create `docs/guides/` and use `git mv` for both guide files.

- [ ] **Step 2: Update visualization commands in the moved guide**

Replace every executable example of:

```bash
bash run_visualization.sh
```

with the full repository-relative entry point:

```bash
bash scripts/visualization/run_visualization.sh
```

Preserve all arguments following the script name.

- [ ] **Step 3: Create `PROJECT_MAP.md`**

The document must contain these sections and links:

```markdown
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
```

- [ ] **Step 4: Create `experiments/README.md`**

Document these four groups with exact repository-relative paths:

- online log-only launchers under `experiments/launchers/online/`;
- online apply-mode launchers under the same directory, clearly marked as guarded research experiments;
- offline Qwen reranking launchers under `experiments/launchers/offline/`;
- analysis programs and historical evidence under `experiments/analysis/` and `experiments/records/`.

Include this execution convention:

```markdown
Run commands from the repository root after activating the documented environment. Slurm launchers retain the historical `gpu_4090` partition name; adapt that scheduler field locally if the target cluster differs.
```

Do not claim that every historical launcher has passed on the newly documented environment.

- [ ] **Step 5: Run the navigation contract**

```powershell
python -m unittest tests.test_repro_contract.RepositoryLayoutTests -v
```

Expected: all repository-layout tests pass.

- [ ] **Step 6: Commit the navigation layer**

```powershell
git add PROJECT_MAP.md experiments/README.md docs/guides tests/test_repro_contract.py
git commit -m "docs: add repository and experiment navigation"
```

### Task 5: Update current documentation and references

**Files:**
- Modify: `README.md`
- Modify: `QUICK_START.md`
- Modify: `docs/REPRODUCIBILITY_STATUS.md`
- Modify: `experiments/records/notes_*.txt` only where a script label would otherwise be unusable
- Modify: `experiments/records/notes_qwen_global_local_v3_soft_consistency_design.md` only where a current command is shown
- Test: `tests/test_repro_contract.py`

- [ ] **Step 1: Replace the root-clutter description in `README.md`**

Replace the current root-level `analysis_*.py`, `offline_*.py`, and `notes_*.txt` entry with links to:

```markdown
- `experiments/`: online/offline launchers, analysis programs, and historical experiment records.
- `tests/`: Python contracts and shell-based Qwen planner checks.
- `docs/guides/`: baseline and visualization guides.
- `PROJECT_MAP.md`: concise navigation for contributors and AI assistants.
```

- [ ] **Step 2: Add experiment navigation to `QUICK_START.md`**

After the smoke-test section, point users to `experiments/README.md` for historical full experiments and explicitly retain the distinction between the supported smoke path and historical Slurm launchers.

- [ ] **Step 3: Update the reproducibility-status command inventory**

Do not change any PASS/PENDING result. Only add the new navigation locations if the status document refers to moved current entry points.

- [ ] **Step 4: Repair script labels inside historical records**

For records containing a line such as `Script: run_office0_...sh`, replace only the path portion with the new `experiments/launchers/online/...` or `experiments/launchers/offline/...` location. Do not rewrite numerical results, interpretations, dates, or evidence claims.

- [ ] **Step 5: Scan current files for obsolete executable paths**

Run:

```powershell
rg -n "bash (run_office0_|run_offline_|test_qwen_|test_online_|run_visualization\.sh)|python (analysis_|offline_)" README.md QUICK_START.md PROJECT_MAP.md experiments docs/guides docs/REPRODUCIBILITY_STATUS.md
```

Expected: no executable command uses an obsolete root-level path. Mentions inside append-only historical plans are allowed when they describe the old layout and are not presented as current commands.

- [ ] **Step 6: Commit documentation reference repairs**

```powershell
git add README.md QUICK_START.md docs/REPRODUCIBILITY_STATUS.md experiments/records
git commit -m "docs: update paths for organized repository layout"
```

### Task 6: Run full verification and review the structural diff

**Files:**
- Verify: all changed and moved files

- [ ] **Step 1: Run all unit and contract tests**

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests pass, including the original 20 tests and the new layout contracts.

- [ ] **Step 2: Compile all tracked Python source groups**

```powershell
python -m compileall -q src scripts tests configs experiments
```

Expected: exit code 0 and no output.

- [ ] **Step 3: Run the publication-safety scan**

```powershell
python scripts/repro/security_scan.py
```

Expected: exit code 0 and a passing tracked-file count.

- [ ] **Step 4: Check whitespace and stale paths**

```powershell
git diff main...HEAD --check
rg -n "bash (run_office0_|run_offline_|test_qwen_|test_online_|run_visualization\.sh)|python (analysis_|offline_)" README.md QUICK_START.md PROJECT_MAP.md experiments docs/guides docs/REPRODUCIBILITY_STATUS.md
```

Expected: no whitespace errors and no obsolete executable paths.

- [ ] **Step 5: Inspect the final tree and diff summary**

```powershell
Get-ChildItem -Force | Sort-Object @{Expression={$_.PSIsContainer};Descending=$true},Name | Select-Object Mode,Name
git status --short --branch
git diff --stat main...HEAD
git diff --summary main...HEAD
```

Expected: root contains only the approved navigation/configuration files and top-level directories; the diff is dominated by renames, path repairs, navigation docs, and tests.

- [ ] **Step 6: Record final verification without changing evidence claims**

If verification requires a small repair, apply the minimal fix, rerun the affected check and the full unit suite, then commit:

```powershell
git add -A
git commit -m "test: finalize repository layout verification"
```

If no repair is needed, do not create an empty commit. Do not mark GPU Qwen loading, the 20-step mapping smoke, full 2000-step experiments, or real-flight validation as passed.
