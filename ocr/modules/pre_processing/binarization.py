# import 3rd part dependencies
import cv2
import numpy as np

# import project dependencies
from ...helpers.timer import timer

def BGR_2_Binary(img: np.ndarray):
    """
    Hàm chuyển đổi ảnh từ ảnh màu sang ảnh nhị phân (ảnh gồm 2 pixel: 0 và 1).
    :param
        - img: ảnh màu BGR được đọc mặc định bằng ``cv2.imread``
    :return
        - binary: ảnh nhị phân
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray, 145, 255, cv2.THRESH_BINARY)

    binary_img = cv2.bitwise_not(binary_img)

    return binary_img