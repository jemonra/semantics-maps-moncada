export CUDA_HOME=/home/ubuntu/miniconda3/envs/conceptgraph/
export REPLICA_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/Replica/
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/
export REPLICA_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/replica/replica.yaml
export GSA_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/Grounded-Segment-Anything/

export SCENE_NAME=room0
export THRESHOLD=1.2

python $CG_FOLDER/conceptgraph/slam/cfslam_pipeline_batch.py \
    dataset_root=$REPLICA_ROOT \
    dataset_config=$REPLICA_CONFIG_PATH \
    stride=5 \
    scene_id=$SCENE_NAME \
    spatial_sim_type=overlap \
    mask_conf_threshold=0.25 \
    match_method=sim_sum \
    sim_threshold=${THRESHOLD} \
    dbscan_eps=0.1 \
    gsa_variant=ram_withbg_allclasses \
    skip_bg=False \
    max_bbox_area_ratio=0.5 \
    save_suffix=overlap_maskconf0.25_simsum${THRESHOLD}_dbscan.1