# import built-in dependencies
import time

# import 3rd party dependencies
import cv2
import numpy as np

def parse_words(
        img: np.ndarray
):
    """
    Tách văn bản thành các chữ
    :param
        - img: ảnh nhị phân văn bản
    :return
        - các contours của các chữ
    """
    t0 = time.time()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 2))
    dilated_img = cv2.dilate(img, kernel, iterations = 3)

    contours, _ = cv2.findContours(dilated_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = np.array([cv2.boundingRect(cnt) for cnt in contours])

    t1 = time.time()
    return boxes, {"parse_words": t1 - t0}