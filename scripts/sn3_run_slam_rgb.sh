export SN_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/ScanNet
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/
export SN_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/scannet/scene0003_02.yaml

export SCENE_NAME=scene0003_02

python $CG_FOLDER/conceptgraph/scripts/run_slam_rgb.py \
  --dataset_root $SN_ROOT \
  --dataset_config $SN_CONFIG_PATH \
  --scene_id $SCENE_NAME \
  --image_height 480 \
  --image_width 640 \
  --stride 5 \
  --device cuda:1 \
  --end 900 \
  --save_pcd \
  --visualize
