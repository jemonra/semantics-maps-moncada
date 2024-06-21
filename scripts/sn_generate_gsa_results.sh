export CUDA_HOME=/home/ubuntu/miniconda3/envs/conceptgraph/
export SN_ROOT=/home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/ScanNet
export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/
export SN_CONFIG_PATH=${CG_FOLDER}/conceptgraph/dataset/dataconfigs/scannet/scene0003_02.yaml
export GSA_PATH=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/Grounded-Segment-Anything/

export SCENE_NAME=scene0003_02

python $CG_FOLDER/conceptgraph/scripts/generate_gsa_results.py \
  --dataset_root $SN_ROOT \
  --dataset_config $SN_CONFIG_PATH \
  --scene_id $SCENE_NAME \
  --class_set none \
  --stride 5 \
  --device cuda:0
