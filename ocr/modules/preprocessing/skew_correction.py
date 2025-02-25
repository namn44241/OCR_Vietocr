# import build-in dependencies
import time

# import 3rd part dependencies
import cv2
import numpy as np

# import project dependencies
from ...helpers.timer import timer

def rotate(
        binary_img: np.ndarray,
        angle: int
):
    """
    Hàm xoay ảnh theo một góc.
    :param
        - img: ảnh nhị phân
        - angle: góc xoay (đơn vị độ, chiều dương ngược chiều kim đồng hồ)
    :return
        - ảnh đã được xoay
    """

    (h, w) = binary_img.shape[:2]
    center = (h//2, w//2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(binary_img, M, (w, h), flags = cv2.INTER_CUBIC, borderMode = cv2.BORDER_REPLICATE)

@timer
def projection_profile_method(
        binary_img: np.ndarray,
        angle_range = (-2, 2)
):
    """
    Hàm xoay chỉnh ảnh bằng phương pháp ``projection profile``.
    :param
        - img: ảnh nhị phân
        - angle_range: khoảng góc thực hiện xoay ảnh
    :return
        - rotated: ảnh được xoay một góc tối ưu sao cho các dòng văn bản nằm trên 1 dòng 
    """
    rotated = binary_img.copy()
    best_angle, max_var = 0, -np.inf

    (angle, end) = angle_range
    while angle <= end:
        rotated_img = rotate(img = binary_img, angle = angle)

        horizontal_proj = np.sum(rotated_img, axis = 1)

        variance = np.var(horizontal_proj)
        if variance > max_var:
            max_var, best_angle = variance, angle
            rotated = rotated_img
        
        angle += 1
    
    t1 = time.time()
    return rotated, best_angle