export REPLICA_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/Replica/
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/
export REPLICA_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/replica/replica.yaml
export GSA_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/Grounded-Segment-Anything/

export AM_I_DOCKER=False
export BUILD_WITH_CUDA=True
export CUDA_HOME=/home/ubuntu/miniconda3/envs/conceptgraph/

export SCENE_NAME=room0
export CLASS_SET=ram

python $CG_FOLDER/conceptgraph/scripts/generate_gsa_results.py \
  --dataset_root $REPLICA_ROOT \
  --dataset_config $REPLICA_CONFIG_PATH \
  --scene_id $SCENE_NAME \
  --class_set $CLASS_SET \
  --box_threshold 0.2 \
  --text_threshold 0.2 \
  --stride 5 \
  --add_bg_classes \
  --accumu_classes \
  --exp_suffix withbg_allclasses \
  --device cuda:0
