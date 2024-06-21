export CUDA_HOME=/home/ubuntu/miniconda3/envs/conceptgraph/
export REPLICA_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/Replica/
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/
export REPLICA_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/replica/replica.yaml
export GSA_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/Grounded-Segment-Anything/

export SCENE_NAME=office0

python $CG_FOLDER/conceptgraph/scripts/generate_gsa_results.py \
  --dataset_root $REPLICA_ROOT \
  --dataset_config $REPLICA_CONFIG_PATH \
  --scene_id $SCENE_NAME \
  --class_set none \
  --stride 5 \
  --device cuda:0
