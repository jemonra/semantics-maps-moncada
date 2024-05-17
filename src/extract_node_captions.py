import argparse
import gzip
import os
import pickle
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm

import slam.slam_classes
from llm.gemini_provider import GoogleGeminiProvider
from utils.file_utils import (create_directories_for_file, read_text_from_file,
                              save_as_json, save_text_to_file)
from utils.image_utils import crop_image_and_mask

# Credentials
GOOGLE_GEMINI_CREDENTIALS_FILE_PATH = "./credentials/concept-graphs-moncada-a807e893ef12.json"
GOOGLE_GEMINI_PROJECT_ID = "concept-graphs-moncada"
GOOGLE_GEMINI_PROJECT_LOCATION = "us-central1"

# Paths
CAPTIONS_FILENAME = "cfslam_llava_captions.json"


def load_scene_map(map_file_path: str):
    """
    TODO
    WARNING: repeated method
    """
    scene_map = slam.slam_classes.MapObjectList()
    with gzip.open(Path(map_file_path), "rb") as file:

        loaded_data = pickle.load(file)

        if not isinstance(loaded_data, dict):
            raise ValueError("Map file is not a dictionary")
        if not "objects" in loaded_data:
            raise ValueError("Map file does not contain 'objects' key")

        scene_map.load_serializable(loaded_data["objects"])

        print(f"Loaded {len(scene_map)} objects from map file")

    return scene_map


def main(args):

    # Create Gemini instance
    llm_service = GoogleGeminiProvider(credentials_file=GOOGLE_GEMINI_CREDENTIALS_FILE_PATH,
                                       project_id=GOOGLE_GEMINI_PROJECT_ID,
                                       project_location=GOOGLE_GEMINI_PROJECT_LOCATION,
                                       model_name=GoogleGeminiProvider.GEMINI_1_0_PRO_VISION)

    # Load the scene map
    scene_map = load_scene_map(map_file_path=args.map_file_path)

    caption_dict_list = []

    for obj_idx, obj in tqdm(enumerate(scene_map), total=len(scene_map), desc="Iterating over objects..."):  # for each object

        # Get images confidence
        conf = np.array(obj["conf"])

        # Get (first args.max_detections_per_object) most reliable detections
        det_idx_most_conf = np.argsort(
            conf)[::-1][: args.max_detections_per_object]

        # If less than two reliable detections, skip object
        if (len(det_idx_most_conf)) < 2:
            continue

        # Result variables
        # One caption per detection
        captions = list()
        # One low (True) or high (False) confidence per detection
        low_confidences = list()

        for det_idx in tqdm(det_idx_most_conf, desc=f"Iterating over detections from object {obj_idx}..."):

            image = Image.open(
                obj["color_path"][det_idx]).convert("RGB")  # image

            x1, y1, x2, y2 = obj["xyxy"][det_idx]  # bounding box
            class_id = obj["class_id"][det_idx]  # object class
            # TODO: get class name
            mask = obj["mask"][det_idx]  # mask

            cropped_image, cropped_mask = crop_image_and_mask(
                image, mask, x1, y1, x2, y2, padding=args.object_images_padding)
            # TODO: apply masking option? modify cropped_image?

            if cropped_image.size[0] * cropped_image.size[1] < 70 * 70:
                low_confidences.append(True)
                print(
                    f"Small object ({cropped_image.size[0] * cropped_image.size[1]}), low confidence"
                )
            else:
                low_confidences.append(False)

            # Get caption result file
            caption_output_file_path = os.path.join(args.scene_dir_path,
                                                    "llm_results",
                                                    "extract_node_captions",
                                                    f"object_{obj_idx}",
                                                    f"detection_{obj_idx}_{det_idx}.txt")

            if os.path.exists(caption_output_file_path):  # File already exists
                print(f"File already exists {caption_output_file_path}")
                caption = read_text_from_file(
                    file_path=caption_output_file_path)
            else:  # File doesn't exist
                caption = llm_service.generate_text_with_images(prompt="Describe with 2 or 3 sentences maximum the central element of the image",
                                                                pil_images=[cropped_image])
                create_directories_for_file(caption_output_file_path)
                save_text_to_file(text=caption,
                                  output_path=caption_output_file_path)

            captions.append(caption)

        # Add object captions to caption_dict_list
        caption_dict_list.append(
            {"id": obj_idx,
             "captions": captions,
             "low_confidences": low_confidences})

    # Save result to a JSON file
    result_file_path = os.path.join(args.cache_dir_path, CAPTIONS_FILENAME)
    create_directories_for_file(result_file_path)
    save_as_json(obj=caption_dict_list,
                 file_path=result_file_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="TODO: program description")

    parser.add_argument("--scene-dir-path",
                        "-s",
                        type=str,
                        required=True,
                        help="Path to the scene folder")

    parser.add_argument("--map-file-path",
                        "-m",
                        type=str,
                        required=True,
                        help="Path to the map file")

    # TODO: help
    parser.add_argument("--max-detections-per-object",
                        "-d",
                        type=int,
                        default=10,
                        help="")

    # TODO: help
    parser.add_argument("--cache-dir-path",
                        "-c",
                        type=str,
                        required=True,
                        help="")

    # TODO: help
    parser.add_argument("--object-images-padding",
                        "-p",
                        type=int,
                        default=50,
                        help="")

    args = parser.parse_args()

    main(args)
