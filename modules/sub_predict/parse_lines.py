# import built-in dependencies
import time

# import 3rd party dependencies
import cv2
import numpy as np


def group_words_by_lines(
        contours
):
    """
    Nhóm các từ thành các dòng
    :param 
        - contours: list of contours
    :return: 
        - list of lines
    """
    t0 = time.time()
    boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        boxes.append((cnt, x, y, w, h))

    boxes.sort(key=lambda box: box[2])
    lines = []
    current_line = [boxes[0]]

    for box in boxes[1:]:
        _, _, y, _, _ = box
        _, _, prev_y, _, prev_h = current_line[-1]

        # Nếu y của box hiện tại gần với y của box trước, thêm vào dòng hiện tại
        if abs(y - prev_y) <= 10:
            current_line.append(box)
        else:
            # Sắp xếp các chữ trong dòng theo x
            current_line.sort(key=lambda box: box[1])
            lines.append(current_line)
            current_line = [box]

    # Thêm dòng cuối cùng
    if current_line:
        current_line.sort(key=lambda box: box[1])
        lines.append(current_line)

    t1 = time.time()
    return lines, {"parse_lines": t1 - t0}