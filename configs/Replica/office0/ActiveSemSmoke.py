import os


_base_ = "./ActiveSem.py"

data_root = os.environ.get("ACTIVESGM_DATA_ROOT", "data")

general = dict(num_iter=20)

dirs = dict(data_dir=data_root)

slam = dict(
    dataset_eval_basedir=os.path.join(data_root, "replica_sim_nvs"),
    semantic_dir=os.path.join(data_root, "replica_v1", "office_0", "habitat"),
    semantic_device="cuda:0",
    override=dict(
        map_every=5,
        report_global_progress_every=5,
        tracking=dict(use_gt_poses=True),
    ),
)

planner = dict(
    max_exploration_steps=20,
    post_refine_steps=0,
    max_refinement_steps=0,
    SLAMData_dir=os.path.join(data_root, "Replica", "office0"),
)

visualizer = dict(vis_rgbd=False)
