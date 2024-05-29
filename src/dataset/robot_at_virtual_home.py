
import csv
import os
import re
from typing import Optional

import numpy as np
import torch

from dataset.grad_slam_dataset import GradSLAMDataset
from utils.transformations import rotation_matrix


class RobotAtVirtualHomeDataset(GradSLAMDataset):
    def __init__(
        self,
        config_dict,  # dataset configuration file as dict
        basedir,
        sequence,
        stride: Optional[int] = None,
        start: Optional[int] = 0,
        end: Optional[int] = -1,
        desired_height: Optional[int] = 480,
        desired_width: Optional[int] = 640,
        load_embeddings: Optional[bool] = False,
        embedding_dir: Optional[str] = "embeddings",
        embedding_dim: Optional[int] = 512,
        **kwargs,
    ):
        self.input_folder = os.path.join(basedir, sequence)
        self.pose_path = os.path.join(self.input_folder, "LogImg.csv")
        super().__init__(
            config_dict,
            stride=stride,
            start=start,
            end=end,
            desired_height=desired_height,
            desired_width=desired_width,
            load_embeddings=load_embeddings,
            embedding_dir=embedding_dir,
            embedding_dim=embedding_dim,
            ** kwargs,
        )

    def filename_number_sort(self, filename):
        number = re.findall(r'(\d+)', filename)[0]
        number = int(number)
        return number

    def get_filepaths(self):
        # (Color) Get sorted filenames
        color_filenames = os.listdir(os.path.join(self.input_folder,
                                                  "results"))
        color_filenames = [
            f for f in color_filenames if re.match(r'^\d+_rgb\.jpg$', f)]
        color_filenames.sort(key=self.filename_number_sort)
        # (Color) Get full paths
        color_paths = [os.path.join(os.path.join(self.input_folder,
                                                 "results"), f) for f in color_filenames]
        print(f"len color paths= {len(color_paths)}")

        # (Depth) Get sorted filenames
        depth_filenames = os.listdir(os.path.join(self.input_folder,
                                                  "results"))
        depth_filenames = [
            f for f in depth_filenames if re.match(r'^\d+_depth\.png$', f)]
        depth_filenames.sort(key=self.filename_number_sort)
        # (Depth) Get full paths
        depth_paths = [os.path.join(os.path.join(self.input_folder,
                                                 "results"), f) for f in depth_filenames]
        print(f"len depth paths= {len(depth_paths)}")

        embedding_paths = None
        if self.load_embeddings:
            raise NotImplementedError(
                "Embeddings not implemented for this dataset")

        return color_paths, depth_paths, embedding_paths

    def convert_pose_unity_to_ros(self, pose):
        Rz = rotation_matrix(np.radians(270) - np.radians(pose[4]), (0, 0, 1))
        pose_t = Rz
        pose_t[:3, 3] = [pose[2], -pose[0], pose[1]]
        # print(pose_t)
        return pose_t

    def load_poses(self):
        poses = []

        with open(self.pose_path, "r", newline="") as f:
            unity_poses = [[float(x) for x in line[7:13]] for idx, line in enumerate(
                csv.reader(f)) if idx > 0 and (idx-1) % 3 == 0]

        print(f"len unity poses = {len(unity_poses)}")

        for i in range(len(unity_poses)):
            pose = self.convert_pose_unity_to_ros(unity_poses[i])
            pose = torch.from_numpy(pose).float()
            poses.append(pose)

        print(f"len unity poses = {len(unity_poses)}")

        return poses
