from typing import *

import numpy as np

from .pre_processing import (
    binarization, 
    skew_correction, 
    noise_removal, 
    bounds_removal, 
    segment
)
from ..helpers import image_helpers, timer

# @timer.timer
def preprocessing_pipeline(
        file_path: Union[str, np.ndarray]
):
    """
    Pipeline tiền xử lý ảnh
    :param
        - file_path: đường dẫn file ảnh hoặc np.ndarray
    :return
        - img: ảnh sau khi được tiền xử lý
    """

    # Load ảnh
    img = image_helpers.load_img(file_path)
    _, w = img.shape[:2]
    
    # B1: Binarization
    bitwise_binary_img = binarization.binarization(img)

    # B2: Skew correction
    skew_corrected, best_angle = skew_correction.projection_profile_method(bitwise_binary_img)
    img = skew_correction.rotate(img, best_angle)

    # B3:Noise removal
    noise_removed = noise_removal.noise_removal(skew_corrected)

    # B4: Bounds removal
    (left_bound, right_bound) = bounds_removal.find_bounds(noise_removed, step = 20)
    removed_bounds = noise_removed[:, left_bound: w - right_bound]

    # B5: Segmentation
    segments = segment.profile_projection_segment(removed_bounds)
    
    resp_objs = {"VietOcr": [], "Pytesseract": []}
    for key, value in segments.items():
        corrected = True if key == "VietOcr" else False

        for (pt1, pt2) in value:
            (y_start , x_start), (y_end, x_end) = pt1, pt2

            if corrected:
                region = skew_corrected[y_start: y_end, x_start + left_bound: x_end + left_bound]
                region = image_helpers.add_padding(region, "black", 20)
            
            else:
                region = img[y_start: y_end, x_start + left_bound: x_end + left_bound]

            resp_objs[key].append(region)

    return resp_objs