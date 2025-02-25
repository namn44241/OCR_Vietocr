# import build-in dependencies
import time

# import 3rd part dependencies
import cv2
import numpy as np

# import project dependencies
from ...helpers.timer import timer

@timer
def noise_removal(
        img: np.ndarray,
        area_threshold: int = 1000
):
    """
    Hàm xóa nhiễu ảnh nhị phân
    :param
        - img: ảnh nhị phân
        - area_threshold: ngưỡng xóa nhiễu (xóa contour có diện tích nhỏ hơn area_threshold)
    :return
        - noise_removed: ảnh sau khi được xóa nhiễu
    """
    cimg = img.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    dilated = cv2.dilate(img, kernel, iterations = 2)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < area_threshold:
            x, y, w, h = cv2.boundingRect(cnt)
            cimg[y: y + h, x: x + w] = np.zeros((h, w), dtype = np.uint8)
    
    return cimg