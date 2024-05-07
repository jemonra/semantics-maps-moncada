import numpy as np
from PIL import Image


def crop_image_and_mask(image: Image, mask: np.ndarray, x1: int, y1: int, x2: int, y2: int, padding: int = 0):
    """
    TODO
    """

    image = np.array(image)
    # Verify initial dimensions
    if image.shape[:2] != mask.shape:
        raise ValueError(
            f"Initial shape mismatch, image.shape {image.shape} != mask.shape {mask.shape}"
        )

    # Define the cropping coordinates
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(image.shape[1], x2 + padding)
    y2 = min(image.shape[0], y2 + padding)

    # Round the coordinates to integers
    x1, y1, x2, y2 = round(x1), round(y1), round(x2), round(y2)

    # Crop the image and the mask
    image_crop = image[y1:y2, x1:x2]
    mask_crop = mask[y1:y2, x1:x2]

    # Verify cropped dimensions
    if image_crop.shape[:2] != mask_crop.shape:
        raise ValueError(
            f"Cropped shape mismatch, image.shape {image_crop.shape} != mask.shape {mask.shape}"
        )

    # Convert the image back to a pil image
    image_crop = Image.fromarray(image_crop)

    return image_crop, mask_crop
