export CUDA_HOME=/home/ubuntu/miniconda3/envs/conceptgraph/
export RAVH_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/RobotAtVirtualHome/
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/
export RAVH_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/robotatvirtualhome/robotatvirtualhome.yaml
export GSA_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/Grounded-Segment-Anything/

export SCENE_NAME=living_room_home30

python $CG_FOLDER/conceptgraph/scripts/generate_gsa_results.py \
  --dataset_root $RAVH_ROOT \
  --dataset_config $RAVH_CONFIG_PATH \
  --scene_id $SCENE_NAME \
  --class_set none \
  --stride 5 \
  --device cuda:0
