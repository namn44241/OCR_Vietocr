import os
from typing import *

import cv2
import numpy as np
import pdf2image


def pdf_2_img(file, dir, output_dir):
    """
    Hàm convert file pdf thành file jpg. (chỉ lấy trang đầu tiên)
    :param
        - file: tên file
        - dir: thư mục gốc của file
        - output_dir: thư mục lưu file
    """
    file_path = os.path.join(dir, file)

    if not file.endswith(".pdf"):
        print(f"chỉ hỗ trợ file pdf")
        return 

    imgs = pdf2image.convert_from_path(file_path, first_page = 1)
    file_name = file.replace("pdf", "jpg")
    imgs[0].save(os.path.join(output_dir, file_name))

    return 


def load_img(file_path: Union[str, np.ndarray]):
    """
    Hàm load ảnh trả về np.ndarray của ảnh.
    :param
        - file_path: đường dẫn hoặc np.ndarray
    :return
        - img: np.ndarray
    """
    if isinstance(file_path, str):
        return cv2.imread(file_path)

    if isinstance(file_path, np.ndarray):
        return file_path
    
    raise ValueError("file_path phải là dường dẫn file ảnh hoặc np.ndarray")

    
def add_padding(
        img:np.ndarray,
        color: str,
        padding: int = 20
):
    h, w = img.shape[:2]

    if color == "black":
        black_img = np.zeros(
            shape = (h + 2 * padding, w + 2 * padding),
            dtype = np.uint8
        )

        black_img[padding: padding + h, padding: padding + w] = img
        return black_img
    
    elif color == "white":
        white_img = np.ones(
            shape = (h + 2 * padding, w + 2 * padding),
            dtype = np.uint8
        ) * 255

        white_img[padding: padding + h, padding: padding + w] = img
        return white_img

    else:
        raise ValueError("Chỉ hỗ trợ color = black || white")
        

