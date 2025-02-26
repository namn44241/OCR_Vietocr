import cv2
import numpy as np

def parse_lines(img):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 20]

    boxes = np.array([cv2.boundingRect(cnt) for cnt in filtered_contours], dtype = np.int32)
    return boxes[boxes[:, 1].argsort()]

def group_lines(img):
    """
    Nhóm các từ thành các dòng
    :param 
        - contours: list of contours
    :return: 
        - list of lines
    """
    boxes = parse_lines(img)

    avg_height = np.mean(
        [h for _, _, _, h in boxes]
    )
    threshold = avg_height * 0.4

    lines = []
    current_line = [boxes[0]]
    center_y_curr = boxes[0][1] + (boxes[0][3] // 2)
    for i in range(1, len(boxes)):
        _, y, _, h = boxes[i]
        center_y = y + (h // 2)

        if abs(center_y - center_y_curr) < threshold:
            current_line.append(boxes[i])
        
        else:
            lines.append(np.array(sorted(current_line, key = lambda x: x[0]), dtype = np.int32))
            current_line = [boxes[i]]
            center_y_curr = center_y

    if current_line:
        lines.append(np.array(sorted(current_line, key = lambda x: x[0]), dtype = np.int32))

    return lines