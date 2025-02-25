# import build-in dependencies
import os
from typing import *

# import 3rd part dependencies
import cv2
import numpy as np
import pdf2image

def pdf_2_jpg(file, dir, output_dir):
    file_path = os.path.join(dir, file)
    if not file.endswith(".pdf"):
        print(f"Chỉ hỗ trợ file .pdf") 
        return
    
    imgs = pdf2image.convert_from_path(file_path, first_page = 1)
    file_name = file.replace("pdf", "jpg")
    imgs[0].save(os.path.join(output_dir, file_name))
    return

def load_img(
        file_path: Union[str, np.ndarray]
):
    """
    Nhận đầu vào là đường dẫn file ảnh hoặc np.ndarray
    :param
        - file_path: đường dẫn file ảnh hoặc np.ndarray
    :return
        - img: np.ndarray
    """

    if isinstance(file_path, str):
        img = cv2.imread(file_path)

    elif isinstance(file_path, np.ndarray):
        img = file_path
    
    else:
        raise ValueError("file_path phải là đường dẫn file ảnh hoặc np.ndarray")
    
    return img

def add_black_padding(
        img: np.ndarray,
        padding: int = 20
):
    h, w = img.shape[:2]

    black_img = np.zeros((h + 2 * padding, w + 2 * padding), np.uint8)
    black_img[padding:h + padding, padding:w + padding] = img

    return black_img

def add_white_padding(
        img: np.ndarray,
        padding:  int = 20
):
    h, w = img.shape[:2]

    white_img = np.ones((h + 2 * padding, w + 2 * padding), np.uint8) * 255
    white_img[padding:h + padding, padding:w + padding] = img

    return white_img