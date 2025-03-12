from typing import *

import numpy as np

from .pre_processing.binarization import binarization
from .pre_processing.skew_correction import projection_profile_method, rotate
from .pre_processing.noise_removal import noise_removal
from .pre_processing.bounds_removal import find_bounds
from .pre_processing.segment import profile_projection_segment
from ..helpers import image_helpers, timer, plot

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
    bitwise_binary_img = binarization(img)

    # B2: Skew correction
    skew_corrected, best_angle = projection_profile_method(bitwise_binary_img)
    img = rotate(img, best_angle)

    # B3:Noise removal
    noise_removed = noise_removal(skew_corrected)

    # B4: Bounds removal
    (left_bound, right_bound) = find_bounds(noise_removed, step = 20)
    removed_bounds = noise_removed[:, left_bound: w - right_bound]

    # B5: Segmentation
    segments = profile_projection_segment(removed_bounds)
    
    resp_objs = []
    for (pts, pte) in segments:
        ys, xs = pts
        ye, xe = pte

        region = img[
            int(ys): int(ye), 
            int(xs + left_bound): int(xe + left_bound)
        ]

        resp_objs.append(region)
    return resp_objs