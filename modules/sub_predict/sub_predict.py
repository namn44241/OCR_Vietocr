# import built-in dependencies
import time

# import 3rd party dependencies
import cv2
import numpy as np
from PIL import Image

# import project dependencies
from .parse_words import parse_words
from .parse_lines import group_words_by_lines
from modules.preprocessing.resize import resize_img
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
    process_time = {"predict_total": 0, "parse_lines": 0, "parse_words": 0}
    
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    binary_img = cv2.bitwise_not(thresh)

    words, words_time = parse_words(binary_img)
    process_time["parse_words"] = words_time["parse_words"]

    lines, lines_time = group_words_by_lines(words)
    process_time["parse_lines"] = lines_time["parse_lines"]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    for line in lines:
        batch_size = max(1, len(line) // 2)
        batches = [line[i:i + batch_size] for i in range(0, len(line), batch_size)]
        
        batch_texts = []
        for batch in batches:
            batch_img = []

            for x, y, w, h in batch:
                word_img = add_white_padding(img[y:y + h, x:x + w])
                thin_img = cv2.erode(word_img, kernel, iterations = 1)
                resize = resize_img(thin_img, 32)
                batch_img.append(Image.fromarray(resize))
            
            batch_texts.extend(detector.predict_batch(batch_img))
        
        text += " ".join(batch_texts) + "\n"

    process_time["predict_total"] = time.time() - t0
    return text, process_time