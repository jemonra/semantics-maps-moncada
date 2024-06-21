export SN_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/ScanNet
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/

export SCENE_NAME=scene0003_02

export PKL_FILENAME=full_pcd_none_overlap_maskconf0.95_simsum1.0_dbscan.1_merge20_masksub_post.pkl.gz

python ./src/extract_node_captions.py \
    --scene-dir-path ${SN_ROOT}/${SCENE_NAME} \
    --map-file-path ${SN_ROOT}/${SCENE_NAME}/pcd_saves/${PKL_FILENAME} \
    --cache-dir-path ${SN_ROOT}/${SCENE_NAME}/sg_cache \
