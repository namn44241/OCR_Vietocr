# import build-in dependencies
from typing import *

# import 3rd part dependencies
import cv2
import numpy as np

# import project depndencies
from . import  binarization, skew_correction, noise_removal, bounds_removal
from . import segment
from ...helpers import file_helpers
from ...helpers.timer import timer

@timer
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
    img = file_helpers.load_img(file_path)
    _, w = img.shape[:2]
    
    # B1: Binarization
    bitwise_binary_img = binarization.BGR_2_Binary(img)

    # B2: Skew correction
    skew_corrected, best_angle = skew_correction.projection_profile_method(bitwise_binary_img)

    # B3:Noise removal
    noise_removed = noise_removal.noise_removal(skew_corrected)

    # B4: Bounds removal
    (left_bound, right_bound) = bounds_removal.find_bounds(noise_removed, step = 20)
    removed_bounds = noise_removed[:, left_bound: w - right_bound]

    # B5: Segmentation
    segments = segment.profile_projection_segment(removed_bounds)
    
    resp_objs = {"need_correct": [], "corrected": []}
    for key, value in segments.items():
        for (pt1, pt2) in value:
            y_start , x_start = pt1
            y_end, x_end = pt2
            region = skew_corrected[y_start: y_end, x_start + left_bound: x_end + left_bound]

            resp_objs[key].append(
                file_helpers.add_black_padding(
                    img = region,
                    padding = 20
                )
            )

    return resp_objs