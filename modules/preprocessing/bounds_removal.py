# import build-in dependencies
import time
from typing import *

# import 3rd part dependencies
import cv2
import numpy as np

def find_bound(
        arr: List[Any],
        step: int,
        type: str
):
    """
    Hàm tìm mode cận dưới của một tập hợp các giá trị số
    :param
        - arr: tập hợp các giá trị
        - step: bước nhảy (định nghĩa các interval)
    :return
        - bound: cận dưới của tập hợp
    """
    t0 = time.time()

    start = (min(arr) // step) * step
    stop = (max(arr) // step + 1) * step
    bins = np.arange(start = start, stop = stop, step = step)

    hist, _ = np.histogram(arr, bins = bins)
    max_idx = np.argmax(hist)
    
    bound = _[max_idx]
    bound = bound - 10 if bound >= 10 else bound 

    t1 = time.time()
    return bound, {f"find_{type}_bound": t1 - t0}

def find_bounds(
        img: np.ndarray,
        step: int,
):
    """
    Hàm tìm khoảng cách lề của hình ảnh nhị phân, giúp giảm nhiễu cho bước tách văn bản.
    :param
        - img: ảnh nhị phân
        - step: bước nhảu
    :return
        - bounds: khoảng cách lề trái, phải
    """
    t0 = time.time()

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
    dilated = cv2.dilate(img, kernel, iterations = 2)

    left, right = [], []
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        left.append(x)
        right.append(img.shape[1] - (x + w))
    
    left_bound, left_time = find_bound(left, step, "left")
    right_bound, right_time = find_bound(right, step, "right")

    t1 = time.time()
    return (left_bound, right_bound), {"find_bounds": t1 - t0, **left_time, **right_time}






    