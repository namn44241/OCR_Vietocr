# import built-in dependencies
import time

# import 3rd party dependencies
import cv2
import numpy as np

# import project dependencies
from .parse_lines import group_lines
from ...helpers import image_helpers, timer, plot
from ...schemas import OcrModel

# @timer.timer
def sub_predict(img: np.ndarray, detector: OcrModel.OcrModel):
    """
    OCR dự đoán với từng hình ảnh nhỏ
    """
    plot.display_img(img)
    
    if detector.model_name == "Pytesseract":
        text = detector.forward(img)
        print(text)
        return text

    else:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 3))
        dilated_img = cv2.dilate(img, kernel, iterations = 2)

        lines = group_lines(dilated_img)
        if not lines: return ""

        lines_text = []
        for line in lines:
            line_text = ""
            sorted_line = sorted(line, key=lambda box: box[0])

            for x, y, w, h in sorted_line:
                word_img = cv2.bitwise_not(img[y: y + h, x: x + w])
                padded_word_img = image_helpers.add_padding(word_img, "white", 15)
                line_text += detector.forward(padded_word_img)
            
            lines_text.append(line_text)
        
        lines_text = "\n".join(lines_text)

        print(lines_text)
        return lines_text