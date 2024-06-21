export CUDA_HOME=/home/ubuntu/miniconda3/envs/conceptgraph/
export RAVH_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/RobotAtVirtualHome
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/
export RAVH_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/robotatvirtualhome/robotatvirtualhome.yaml
export GSA_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/Grounded-Segment-Anything/

export SCENE_NAME=kitchen_home20
export THRESHOLD=1.2

python $CG_FOLDER/conceptgraph/slam/cfslam_pipeline_batch.py \
    dataset_root=$RAVH_ROOT \
    dataset_config=$RAVH_CONFIG_PATH \
    stride=5 \
    scene_id=$SCENE_NAME \
    spatial_sim_type=overlap \
    mask_conf_threshold=0.95 \
    match_method=sim_sum \
    sim_threshold=${THRESHOLD} \
    dbscan_eps=0.1 \
    gsa_variant=none \
    class_agnostic=True \
    skip_bg=True \
    max_bbox_area_ratio=0.5 \
    save_suffix=overlap_maskconf0.95_simsum${THRESHOLD}_dbscan.1_merge20_masksub \
    merge_interval=20 \
    merge_visual_sim_thresh=0.8 \
    merge_text_sim_thresh=0.8