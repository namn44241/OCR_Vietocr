import cv2
import numpy as np

from ...helpers.timer import timer

def parse_lines(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = np.array([cv2.boundingRect(cnt) for cnt in contours], dtype = np.int32)
    if len(boxes) == 0:
        return []

    return boxes[boxes[:, 1].argsort()]

def group_lines(img, threshold = 10):
    """
    Nhóm các từ thành các dòng
    :param 
        - contours: list of contours
    :return: 
        - list of lines
    """
    boxes = parse_lines(img)

    lines = []
    current_line = [boxes[0]]

    for i in range(1, len(boxes)):
        _, y, _, h = boxes[i]
        _, last_y, _, last_h = current_line[-1]

        if abs(y - last_y) < threshold or abs(y + h - (last_y + last_h)) < threshold:
            current_line.append(boxes[i])
        
        else:
            lines.append(np.array(sorted(current_line, key = lambda x: x[0]), dtype = np.int32))
            current_line = [boxes[i]]

    if current_line:
        lines.append(np.array(sorted(current_line, key = lambda x: x[0]), dtype = np.int32))

    return lines
        