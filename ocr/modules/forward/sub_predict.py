# import built-in dependencies
import time

# import 3rd party dependencies
import cv2
import numpy as np
from PIL import Image

# import project dependencies
from .parse_lines import group_lines
from ..post_processing.correction import correct
from ...helpers.file_helpers import add_white_padding
from ...helpers.timer import timer
from ...helpers.plot import display_img, display_imgs

@timer
def sub_predict(img: np.ndarray, detector, corrector, corrected):
    """
    OCR dự đoán với từng hình ảnh nhỏ
    """
    display_img(img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 3))
    dilated_img = cv2.dilate(img, kernel, iterations = 3)
    display_img(dilated_img)

    lines = group_lines(dilated_img)
    if not lines: return ""

    lines_text = []
    for line in lines:
        line_text = ""
        word_imgs = [
            add_white_padding(
                cv2.bitwise_not(img[y: y + h, x: x + w]),
                padding = 15
            )
        for x, y, w, h in line]

        for word_img in word_imgs:
            line_text += detector.predict(Image.fromarray(word_img)).lower() + " "
        
        lines_text.append(line_text)
    
    lines_text = "\n".join(lines_text)

    if not corrected:
        lines_text = correct(lines_text, corrector)

    print(lines_text)
    return lines_text