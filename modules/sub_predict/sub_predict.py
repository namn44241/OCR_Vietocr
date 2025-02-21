# import built-in dependencies
import time

# import 3rd party dependencies
import cv2
import numpy as np
from PIL import Image

# import project dependencies
from .parse_words import parse_words
from .parse_lines import group_words_by_lines
from helpers.file_helpers import add_white_padding

def sub_predict(
        img: np.ndarray,
        detector
):
    """
    OCR dự đoán với từng hình ảnh nhỏ
    """
    t0 = time.time()

    text = ""
    process_time = {"predict_total": 0,
                    "parse_lines": 0,
                    "parse_words": 0
                    }
    
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    binary_img = cv2.bitwise_not(thresh)

    words, words_time = parse_words(binary_img)
    process_time["parse_words"] = words_time["parse_words"]

    lines, lines_time = group_words_by_lines(words)
    process_time["parse_lines"] = lines_time["parse_lines"]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    for line in lines:
        line_text = []

        for cnt, x, y, w, h in line:
            word_img = img[y: y + h, x: x + w]
            word_img = add_white_padding(word_img, 20)

            thin_word_img = cv2.erode(word_img, kernel, iterations=1)
            thin_word_img = Image.fromarray(thin_word_img)
            line_text.append(detector.predict(thin_word_img))
        
        text += " ".join(line_text) + "\n"
    
    t1 = time.time()
    process_time["predict_total"] = t1 - t0
    return text, process_time
