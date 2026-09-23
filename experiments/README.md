# Experiments

This directory keeps research launchers, offline analysis programs, and historical experiment notes together. For the supported setup and current verification status, see [Quick Start](../QUICK_START.md) and [Reproducibility Status](../docs/REPRODUCIBILITY_STATUS.md).

Run commands from the repository root after activating the documented environment. Slurm launchers retain the historical `gpu_4090` partition name; adapt that scheduler field locally if the target cluster differs.

## Online log-only launchers

These launchers record Qwen decisions without applying them to the planner trajectory:

- `experiments/launchers/online/run_office0_qwen_tiebreak_logonly.sh`
- `experiments/launchers/online/run_office0_qwen_rank_efficiency_logonly.sh`
- `experiments/launchers/online/run_office0_qwen_global_local_logonly.sh`
- `experiments/launchers/online/run_office0_qwen_global_local_v2_logonly.sh`

The earlier logging prototype is `experiments/launchers/online/run_office0_llm_log_test.sh`.

## Online apply-mode launchers

These are guarded research experiments that can change the selected next view when their explicit application settings and numeric checks allow it:

- `experiments/launchers/online/run_office0_qwen_tiebreak_apply.sh`
- `experiments/launchers/online/run_office0_qwen_tiebreak_apply_strict_v1.sh`
- `experiments/launchers/online/run_office0_qwen_rank_efficiency_apply_v2.sh`

Other historical online launchers are `experiments/launchers/online/run_office0_mainonly_semfix.sh`, `experiments/launchers/online/run_office0_full_semfix.sh`, and `experiments/launchers/online/run_office0_fake_llm_full_night.sh`. They provide baseline or fake-LLM runs, not Qwen apply-mode evidence.

## Offline Qwen reranking

- `experiments/launchers/offline/run_offline_qwen_rerank_topk.sh` runs `experiments/analysis/offline_qwen_rerank_llm_logs_topk.py`.
- `experiments/launchers/offline/run_offline_qwen_tiebreak_top3.sh` runs `experiments/analysis/offline_qwen_tiebreak_top3.py`.

## Analysis and historical records

`experiments/analysis/` contains offline reranking, guard-policy, decision-graph, and run-summary programs. For example, `experiments/analysis/offline_qwen_guarded_rerank_analysis.py` examines guarded reranking, and `experiments/analysis/collect_three_run_summary.py` collects a three-run comparison.

`experiments/records/` contains historical job notes and research-design records, including `experiments/records/notes_experiment_summary_for_paper.txt` and `experiments/records/notes_qwen_global_local_v3_soft_consistency_design.md`. These records describe prior experiments; their presence does not establish that every launcher has passed in the newly documented Ubuntu/CUDA environment.
