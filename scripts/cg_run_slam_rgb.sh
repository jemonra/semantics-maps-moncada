export REPLICA_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/Replica

export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/

export REPLICA_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/replica/replica.yaml

export SCENE_NAME=room0

SCENE_NAME=room0
python $CG_FOLDER/conceptgraph/scripts/run_slam_rgb.py \
  --dataset_root $REPLICA_ROOT \
  --dataset_config $REPLICA_CONFIG_PATH \
  --scene_id $SCENE_NAME \
  --image_height 480 \
  --image_width 640 \
  --stride 5 \
  --device cuda:1 \
  --save_pcd
