# import built-in dependencies
import time

# import 3rd party dependencies
import cv2
import numpy as np

# import project dependencies
from .horizontal_presegment import horizontal_presegment
from .vertical_segment import vertical_segment

def profile_projection_segment(
        img: np.ndarray
):
    """
    Cắt một hình ảnh văn bản lớn thành nhiều văn bản nhỏ hơn
    :param 
        img: hình ảnh nhị phân văn bản lớn
    :return:
        list image segments
    """
    t0 = time.time()
    process_time = {"segmentation_total": 0,
                    "segmentation_parts": {
                        "horizontal_presegment": 0,
                        "vertical_segment": 0
                    }}
    resp_objs = []

    horizontal_text_segments, horizontal_time = horizontal_presegment(img)
    process_time["segmentation_parts"]["horizontal_presegment"] = horizontal_time["horizontal_presegment"]

    for y_start, y_end in horizontal_text_segments:
        sub_img = img[y_start: y_end, :]

        vertical_text_segments, vertical_time = vertical_segment(sub_img)
        process_time["segmentation_parts"]["vertical_segment"] += vertical_time["vertical_segment"]    

        for x_start, x_end in vertical_text_segments:
            resp_objs.append(((y_start, x_start), (y_end, x_end)))
    
    t1 = time.time()
    process_time["segmentation_total"] = t1 - t0
    return resp_objs, process_time