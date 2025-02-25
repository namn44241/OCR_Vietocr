# import built-in dependencies
import time

# import 3rd party dependencies
import cv2
import numpy as np
from sklearn.cluster import DBSCAN

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
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 3))
    dilated_img = cv2.dilate(img, kernel, iterations = 3)

    contours, _ = cv2.findContours(dilated_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = np.array([cv2.boundingRect(cnt) for cnt in contours])

    t1 = time.time()
    return boxes, {"parse_words": t1 - t0}

def group_words_by_lines(
        boxes
):
    """
    Nhóm các từ thành các dòng
    :param 
        - contours: list of contours
    :return: 
        - list of lines
    """

    t0 = time.time()

    boxes = boxes[boxes[:, 1].argsort()]

    lines = []
    current_line = []
    y_threshold = 10

    for box in boxes:
        x, y, w, h = box
        if not current_line:
            current_line.append(box)
        else:
            last_x, last_y, last_w, last_h = current_line[-1]
            if abs(y - last_y) < y_threshold:
                current_line.append(box)
            else:
                lines.append(sorted(current_line, key = lambda x: x[0]))
                current_line = [box]
    
    if current_line:
        lines.append(sorted(current_line, key = lambda x: x[0]))
    
    t1 = time.time()
    return lines, {"parse_lines": t1 - t0}
        