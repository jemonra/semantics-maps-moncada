export REPLICA_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/Replica/
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/

export LLAVA_PYTHON_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/LLaVA/
export LLAVA_MODEL_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Models/LLaVA-7B-v0/

export SCENE_NAME=room0

export PKL_FILENAME=full_pcd_none_overlap_maskconf0.95_simsum1.2_dbscan.1_merge20_masksub_post.pkl.gz

python ./src/extract_node_captions.py \
    --map-file-path ${REPLICA_ROOT}/${SCENE_NAME}/pcd_saves/${PKL_FILENAME} \
    --result-dir-path ${REPLICA_ROOT}/${SCENE_NAME}/sg_cache \
