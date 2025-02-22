import cv2

def resize_img(img, target_height=32):
    h, w = img.shape[:2]
    scale = target_height / h
    new_w = int(w * scale)
    resized_img = cv2.resize(img, (new_w, target_height), interpolation=cv2.INTER_AREA)
        
    return resized_img