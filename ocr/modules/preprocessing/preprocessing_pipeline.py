# import build-in dependencies
import time
from typing import *

# import 3rd part dependencies
import cv2
import numpy as np

# import project depndencies
from . import  binarization, skew_correction, noise_removal, bounds_removal
from . import segment
from ...helpers import file_helpers


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
    t0 = time.time()
    img = file_helpers.load_img(file_path)

    h, w = img.shape[:2]
    binary, binary_time = binarization.binarization(img)

    skew_corrected, best_angle, skew_time = skew_correction.projection_profile_method(binary)
    img = skew_correction.rotate(img, best_angle)

    noise_removed, noise_time = noise_removal.noise_removal(skew_corrected)

    (left_bound, right_bound), find_bounds_time = bounds_removal.find_bounds(noise_removed, step = 20)
    removed_bounds = noise_removed[:, left_bound: w - right_bound]

    segments, segment_time = segment.profile_projection_segment(removed_bounds)
    
    resp_objs = []
    for (pt1, pt2) in segments:
        y_start , x_start = pt1
        y_end, x_end = pt2
        region = img[y_start: y_end, x_start + left_bound: x_end + left_bound]

        resp_objs.append(
            file_helpers.add_white_padding(
                img = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY),
                padding = 20
            )
        )


    t1 = time.time()
    return resp_objs, {"preprocessing_total": t1 - t0, 
                       "preprocessing_parts": {
                           **binary_time, 
                           **skew_time, 
                           **noise_time, 
                           **find_bounds_time, 
                           **segment_time
                       }} 
