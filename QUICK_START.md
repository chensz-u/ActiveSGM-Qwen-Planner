# Ubuntu 20.04 / CUDA 11.7 快速开始

本指南面向 NVIDIA GPU 服务器。当前仓库不包含数据集、模型权重、第三方源码或检查点；这些内容由脚本获取或由使用者按许可证自行准备。

## 1. 克隆与创建环境

```bash
git clone https://github.com/chensz-u/ActiveSGM-Qwen-Planner.git
cd ActiveSGM-Qwen-Planner
bash scripts/setup/install_environment.sh
conda activate activesgm-cu117
```

安装脚本固定 Python 3.8、PyTorch 1.13.1 + CUDA 11.7，以及与本项目兼容的 OpenMMLab 1.x 依赖。不要再同时安装 `mmcv 2.x`。

## 2. 获取并构建第三方依赖

```bash
bash scripts/setup/bootstrap_third_parties.sh
bash scripts/setup/bootstrap_third_parties.sh --build
```

脚本按照 `scripts/setup/third_party.lock` 的提交号获取公开上游代码。如果目标目录不是 Git 仓库或含有未提交修改，脚本会停止，不会覆盖它。

## 3. 准备 Qwen 模型

默认下载到仓库中已被 Git 忽略的 `models/`：

```bash
python scripts/setup/download_qwen.py
export QWEN_PLANNER_MODEL_PATH="$PWD/models/Qwen2.5-1.5B-Instruct"
```

如果模型放在其他磁盘：

```bash
export QWEN_PLANNER_MODEL_PATH=/srv/models/Qwen2.5-1.5B-Instruct
```

需要 Hugging Face 凭据时，只在当前终端设置 `HF_TOKEN`。不要把 token 写进 `.env`、脚本或提交记录。

## 4. 准备 Replica 数据

请遵守 Replica/Habitat 的原始许可证。将数据整理为：

```text
<ACTIVESGM_DATA_ROOT>/
├── Replica/office0/
├── replica_v1/office_0/habitat/
└── replica_sim_nvs/
```

然后设置：

```bash
export ACTIVESGM_DATA_ROOT=/srv/datasets/activesgm
```

Matterport3D 等受许可限制的数据不由本仓库自动下载或再分发。

## 5. 分层检查

先检查依赖和资产：

```bash
python scripts/repro/check_environment.py
```

再检查本地 Qwen 能否输出结构化结果：

```bash
python scripts/repro/smoke_qwen.py
```

最后运行 20 步 `office0` 的 Qwen log-only 主流程：

```bash
bash scripts/repro/smoke_office0.sh
```

该脚本固定 `ACTIVE_SGM_LLM_APPLY=0`，不会让未经验证的 Qwen 决策直接替换 ActiveSGM 轨迹。

以上是当前支持的安装与 20 步冒烟路径。历史完整实验及其 Slurm 启动脚本见 [experiments/README.md](experiments/README.md)；这些启动脚本不属于上述冒烟验证流程。

## 6. 发布前检查

```bash
python -m unittest discover -s tests -v
python -m compileall -q src scripts tests configs
python scripts/repro/security_scan.py
```

安全扫描会检查已跟踪文件中的常见凭据、旧机器路径、固定代理和超过 10 MiB 的文件。

## 验证边界

- Windows 可以验证 Python 语法、路径逻辑、单元测试和安全扫描。
- Ubuntu 20.04/CUDA 11.7 才能验证 Habitat、CUDA 扩展、Qwen 加载和 ActiveSGM 冒烟运行。
- 20 步冒烟通过仅代表安装链路可工作，不代表完整 2000 步实验或论文指标已经复现。
