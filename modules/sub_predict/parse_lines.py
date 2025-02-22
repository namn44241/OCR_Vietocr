# import built-in dependencies
import time

# import 3rd party dependencies
import numpy as np
from sklearn.cluster import DBSCAN


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