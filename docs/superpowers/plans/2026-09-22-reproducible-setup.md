# Reproducible Secure Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the source-only ActiveSGM-Qwen-Planner release into an auditable Ubuntu 20.04/CUDA 11.7 setup with safe asset handling, environment checks, and smoke-test entry points.

**Architecture:** Keep heavyweight or licensed assets outside Git and resolve them through environment variables or repository-relative defaults. Use small Python utilities for path validation, environment/security checks, and model download; use shell only to orchestrate Linux installation and experiment launches. Test pure behavior on Windows and label GPU-only verification separately.

**Tech Stack:** Python 3.8, `unittest`, Conda, Bash, PyTorch 1.13.1/CUDA 11.7, OpenMMLab 1.x, Hugging Face Transformers.

---

## File map

- `envs/environment-cu117.yml`: minimal reproducible Conda environment.
- `envs/requirements-repro.txt`: mutually compatible Python package pins.
- `scripts/setup/install_environment.sh`: ordered Linux installation with fail-fast behavior.
- `scripts/setup/third_party.lock`: public repository URLs and immutable commits.
- `scripts/setup/bootstrap_third_parties.sh`: safe clone/checkout/build orchestration.
- `.env.example`: non-secret runtime path template.
- `src/llm/runtime_paths.py`: repository-relative and environment-controlled path resolution.
- `scripts/setup/download_qwen.py`: guarded model download CLI.
- `scripts/repro/check_environment.py`: dependency, CUDA, asset, and import diagnostics.
- `scripts/repro/security_scan.py`: tracked-file secret, personal-path, and large-file gate.
- `scripts/repro/smoke_qwen.py`: minimal local Qwen structured-output check.
- `configs/Replica/office0/ActiveSemSmoke.py`: short mapping configuration.
- `scripts/repro/smoke_office0.sh`: GPU/data mapping smoke entry point.
- `tests/test_runtime_paths.py`: path and download safety tests.
- `tests/test_repro_tools.py`: environment and security-tool tests.
- `tests/test_repro_contract.py`: repository configuration contract tests.
- `README.md`, `QUICK_START.md`, `.gitignore`: public setup and safety documentation.

### Task 1: Lock the supported environment

**Files:**
- Create: `envs/environment-cu117.yml`
- Create: `envs/requirements-repro.txt`
- Create: `scripts/setup/install_environment.sh`
- Create: `tests/test_repro_contract.py`

- [ ] **Step 1: Write failing environment contract tests**

Create tests that assert Python 3.8, PyTorch `1.13.1+cu117`, `mmcv-full==1.6.0`, `mmdet==2.25.3`, `mmsegmentation==0.26.0`, and Transformers 4.45.2 appear exactly once and that the old incompatible `mmcv==2.0.0` pin is absent from the supported files.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_repro_contract -v`

Expected: failure because the new environment files do not exist.

- [ ] **Step 3: Add the minimal environment files and installer**

The installer must use `set -Eeuo pipefail`, verify Linux, create/update the named Conda environment, install the CUDA 11.7 PyTorch wheels, install `mmcv-full==1.6.0` from the matching OpenMMLab wheel index, install the reproducibility requirements, then call the environment checker. It must not set a proxy or embed a home directory.

- [ ] **Step 4: Run the contract test and verify GREEN**

Run: `python -m unittest tests.test_repro_contract -v`

Expected: all environment contract tests pass.

- [ ] **Step 5: Commit**

Run: `git add envs scripts/setup/install_environment.sh tests/test_repro_contract.py && git commit -m "build: add CUDA 11.7 reproducible environment"`

### Task 2: Bootstrap third-party projects without vendoring them

**Files:**
- Create: `scripts/setup/third_party.lock`
- Create: `scripts/setup/bootstrap_third_parties.sh`
- Modify: `.gitmodules`
- Modify: `.gitignore`
- Test: `tests/test_repro_contract.py`

- [ ] **Step 1: Add failing lock-file and safety tests**

Assert every lock entry contains a project name, HTTPS GitHub URL, 40-character commit, and destination under `third_parties/`; assert the bootstrap script refuses to overwrite a non-Git directory or a dirty checkout and never checks out a branch name.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest tests.test_repro_contract.ThirdPartyContractTests -v`

Expected: failure because the lock file and bootstrap script do not exist.

- [ ] **Step 3: Implement immutable bootstrap behavior**

Resolve compatible upstream commits from the original ActiveSGM tree where possible. Parse the lock file, clone only missing directories, verify each URL, fetch the single requested commit, detach-checkout it, and stop on dirty or mismatched existing repositories. Keep `third_parties/` ignored and remove misleading inactive submodule declarations.

- [ ] **Step 4: Run the contract test and shell syntax check**

Run: `python -m unittest tests.test_repro_contract.ThirdPartyContractTests -v`

Run on Linux or Git Bash: `bash -n scripts/setup/bootstrap_third_parties.sh`

Expected: tests pass and Bash reports no syntax error.

- [ ] **Step 5: Commit**

Run: `git add .gitignore .gitmodules scripts/setup tests/test_repro_contract.py && git commit -m "build: pin third-party bootstrap sources"`

### Task 3: Make local assets explicit and safe

**Files:**
- Create: `.env.example`
- Create: `src/llm/runtime_paths.py`
- Create: `scripts/setup/download_qwen.py`
- Modify: `download_qwen25_1_5b.py`
- Modify: `src/llm/planner_reranker.py`
- Create: `tests/test_runtime_paths.py`

- [ ] **Step 1: Write failing path and overwrite-safety tests**

Cover environment override, repository-relative model default, a helpful missing-directory error, refusal to download into a non-empty directory, and explicit `--force` permission. Tests must use temporary directories and no network.

- [ ] **Step 2: Run the focused tests and verify RED**

Run: `python -m unittest tests.test_runtime_paths -v`

Expected: import failure because `runtime_paths.py` and the safe downloader do not exist.

- [ ] **Step 3: Implement path resolution and guarded download**

`resolve_qwen_model_path()` must read `QWEN_PLANNER_MODEL_PATH`, otherwise use `models/Qwen2.5-1.5B-Instruct`, expand and resolve the path, and raise a message pointing to the downloader if absent. The downloader must accept `--output-dir`, `--model-id`, and `--force`; read `HF_TOKEN` only from the process environment; and never print the token.

- [ ] **Step 4: Run focused and planner tests**

Run: `python -m unittest tests.test_runtime_paths -v`

Run: `python -m unittest discover -s tests -v`

Expected: all local tests pass without downloading a model.

- [ ] **Step 5: Commit**

Run: `git add .env.example src/llm scripts/setup/download_qwen.py download_qwen25_1_5b.py tests && git commit -m "feat: add safe runtime asset configuration"`

### Task 4: Add diagnostics and publication security gates

**Files:**
- Create: `scripts/repro/check_environment.py`
- Create: `scripts/repro/security_scan.py`
- Create: `tests/test_repro_tools.py`
- Modify: `.gitignore`

- [ ] **Step 1: Write failing diagnostic and scanner tests**

Test exact-version comparison, missing-import reporting, detection of private keys/Hugging Face tokens/personal absolute paths, large-file rejection, and successful scanning of harmless text. Use dependency injection and temporary files so tests run without CUDA.

- [ ] **Step 2: Run the focused tests and verify RED**

Run: `python -m unittest tests.test_repro_tools -v`

Expected: import failure because both tools are absent.

- [ ] **Step 3: Implement minimal tools**

The environment checker prints PASS/FAIL/SKIP rows and exits nonzero for required failures. `--allow-no-gpu` changes only the CUDA check to SKIP. The security scanner scans Git-tracked files by default, accepts explicit paths for tests, skips binary decoding safely, rejects files over 10 MiB, and never prints matched secret contents.

- [ ] **Step 4: Run focused tests and scan the repository**

Run: `python -m unittest tests.test_repro_tools -v`

Run: `python scripts/repro/security_scan.py`

Expected: all tests pass and the repository scan reports no findings.

- [ ] **Step 5: Commit**

Run: `git add .gitignore scripts/repro tests/test_repro_tools.py && git commit -m "test: add environment and release safety gates"`

### Task 5: Add GPU smoke-test entry points

**Files:**
- Create: `scripts/repro/smoke_qwen.py`
- Create: `configs/Replica/office0/ActiveSemSmoke.py`
- Create: `scripts/repro/smoke_office0.sh`
- Test: `tests/test_repro_contract.py`

- [ ] **Step 1: Add failing smoke-contract tests**

Assert the mapping config inherits `ActiveSem.py` and limits `general.num_iter` to 20, the launcher computes the repository root instead of using an absolute path, and the Qwen smoke uses the shared model-path resolver.

- [ ] **Step 2: Run the smoke contract and verify RED**

Run: `python -m unittest tests.test_repro_contract.SmokeContractTests -v`

Expected: failure because the smoke files do not exist.

- [ ] **Step 3: Add minimal smoke programs**

The Qwen check loads the configured local model, generates at most 32 new tokens, and verifies that the decoded output contains a JSON object. The mapping shell script requires the Replica asset directories, creates a timestamped ignored result directory, and launches `src/main/activesgm.py` with the 20-step config and visualization disabled.

- [ ] **Step 4: Run local contract tests**

Run: `python -m unittest tests.test_repro_contract.SmokeContractTests -v`

Expected: pass. Record Qwen and mapping execution as pending until run on the target GPU host.

- [ ] **Step 5: Commit**

Run: `git add scripts/repro configs/Replica/office0/ActiveSemSmoke.py tests/test_repro_contract.py && git commit -m "test: add GPU reproducibility smoke checks"`

### Task 6: Remove active personal paths and publish accurate instructions

**Files:**
- Modify: `README.md`
- Modify: `QUICK_START.md`
- Modify: active root `run_*.sh`, `test_*.sh`, and offline Qwen scripts containing personal paths
- Modify: `scripts/framework/*.sh`
- Modify: `envs/Dockerfile`
- Modify: `VISUALIZATION_GUIDE.md`
- Test: `tests/test_repro_contract.py`

- [ ] **Step 1: Add a failing no-personal-path contract**

Scan tracked operational code and public instructions for the known old username, old project root, old Conda root, and fixed proxy address. Allow research notes to describe historical results but not expose machine-specific paths.

- [ ] **Step 2: Run the contract and verify RED**

Run: `python -m unittest tests.test_repro_contract.PersonalPathContractTests -v`

Expected: failure listing current path-bearing files.

- [ ] **Step 3: Replace personal assumptions**

All launchers compute `REPO_ROOT` from their own location, use the currently activated environment, and read `QWEN_PLANNER_MODEL_PATH`. Remove fixed proxy settings. Rewrite README and QUICK_START as clone-to-smoke instructions, including license boundaries and the four verification levels.

- [ ] **Step 4: Run all local verification**

Run: `python -m unittest discover -s tests -v`

Run: `python -m compileall -q src scripts tests configs`

Run: `python scripts/repro/check_environment.py --allow-no-gpu`

Run: `python scripts/repro/security_scan.py`

Expected: unit/contract tests and compilation pass; environment checker may report unavailable optional GPU-only packages on Windows but must clearly separate them from source failures; security scan reports no findings.

- [ ] **Step 5: Commit**

Run: `git add README.md QUICK_START.md VISUALIZATION_GUIDE.md envs scripts *.sh *.py tests && git commit -m "docs: publish secure reproducible quick start"`

### Task 7: Final audit and safe GitHub upload

**Files:**
- Create: `docs/REPRODUCIBILITY_STATUS.md`

- [ ] **Step 1: Record verification truthfully**

List each validation command, date, platform, exit status, and whether it was executed locally or remains pending on Ubuntu/CUDA. Do not mark Qwen or mapping GPU smoke as passed without actual output.

- [ ] **Step 2: Inspect the complete branch**

Run: `git status --short`

Run: `git diff main...HEAD --check`

Run: `git diff --stat main...HEAD`

Run: `git log --oneline main..HEAD`

Expected: only planned files and commits appear.

- [ ] **Step 3: Re-run release gates**

Run: `python -m unittest discover -s tests -v`

Run: `python -m compileall -q src scripts tests configs`

Run: `python scripts/repro/security_scan.py`

Expected: all locally executable gates pass.

- [ ] **Step 4: Verify remote and push once**

Run one remote/authentication check, then `git push -u origin codex/reproducible-setup`. Do not force-push and do not modify `main`.

- [ ] **Step 5: Verify the pushed ref once**

Compare the local branch SHA with `refs/heads/codex/reproducible-setup` using a single remote query and report the exact URL and remaining GPU-server validation.
