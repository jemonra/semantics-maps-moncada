export CG_FOLDER=/home/ubuntu/tfg_jesus_moncada_ramirez/Repos/concept-graphs/
export SCENE_NAME=room0

python $CG_FOLDER/conceptgraph/scripts/visualize_cfslam_results.py --result_path /home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/Replica/$SCENE_NAME/pcd_saves/full_pcd_ram_withbg_allclasses_overlap_maskconf0.25_simsum1.2_dbscan.1.pkl.gz

python $CG_FOLDER/conceptgraph/scripts/visualize_cfslam_results.py --result_path /home/ubuntu/tfg_jesus_moncada_ramirez/Datasets/Replica/$SCENE_NAME/pcd_saves/full_pcd_ram_withbg_allclasses_overlap_maskconf0.25_simsum1.2_dbscan.1_post.pkl.gz
