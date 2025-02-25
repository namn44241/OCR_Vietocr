# import build-in dependencies
from typing import *

# import 3rd part dependencies
import cv2
import numpy as np

# import project dependencies
from ...helpers.timer import timer


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
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
    dilated = cv2.dilate(img, kernel, iterations = 2)

    left, right = [], []
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, _, w, _ = cv2.boundingRect(cnt)
        left.append(x)
        right.append(img.shape[1] - (x + w))
    
    left_bound = find_bound(left, step)
    right_bound = find_bound(right, step)

    return (left_bound, right_bound)    


def find_bound(
        arr: List[Any],
        step: int,
):
    """
    Hàm tìm mode cận dưới của một tập hợp các giá trị số
    :param
        - arr: tập hợp các giá trị
        - step: bước nhảy (định nghĩa các interval)
    :return
        - bound: cận dưới của tập hợp
    """
    start = (min(arr) // step) * step
    stop = (max(arr) // step + 1) * step
    bins = np.arange(start = start, stop = stop, step = step)

    hist, _ = np.histogram(arr, bins = bins)
    max_idx = np.argmax(hist)
    
    bound = _[max_idx]
    bound = bound - 10 if bound >= 10 else bound 

    return bound
