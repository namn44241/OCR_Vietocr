from typing import *

import numpy as np

from ...helpers import plot

def horizontal_presegment(
        img: np.ndarray,
        threshold = 0.35,
        min_gap_height = 25,
        min_gap_width = 30
) -> List[Tuple[int, int]]:
    """
    Xác định khoảng trống giữa các dòng bằng tổng số pixels theo hàng ngang thỏa mãn điều kiện
    :param
        - img: ảnh nhị phân
        - threshold: ngưỡng cắt ảnh (chỉ lấy thông tin cần thiết)
        - min_gap_height: chiều cao tối thiểu của khoảng trống
        - min_gap_width: chiều rộng tối thiểu của khoảng trống
    :return
        - List[(s, e)]: danh sách các đoạn chữ được tách dòng
    """
    h_crop = int(img.shape[0] * threshold)
    horizontal_sum = np.sum(img, axis = 1)

    gaps = np.where(horizontal_sum <= min_gap_height)[0]
    if gaps.size == 0:
        return [(0, img.shape[0])]
    
    gap_diff = np.diff(gaps)
    gap_starts = np.hstack(([gaps[0]], gaps[1:][gap_diff > 1]))
    gap_ends = np.hstack((gaps[:-1][gap_diff > 1], [gaps[-1]]))
    gap_ranges = [(s, e) for s, e in zip(gap_starts, gap_ends) if (e - s) >= min_gap_width]

    text_segments = []
    current_pos = 0

    for gap_start, gap_end in gap_ranges:
        if current_pos < gap_start:
            text_segments.append((current_pos, gap_start))

        current_pos = gap_end + 1

    if current_pos < img.shape[0]:
        text_segments.append((current_pos, img.shape[0]))

    resp_objs = []
    for (s, e) in text_segments:
        if e > h_crop: continue

        if s >= 10: s -= 10
        if e <= img.shape[0] - 10:
            e += 10
        
        resp_objs.append((s, e))

    return resp_objs

def vertical_segment(
        img: np.ndarray, 
        min_gap_height = 40, 
        min_gap_width = 50
) -> List[Tuple[int, int]]:
    """
    Xác định khoảng trống giữa các cột bằng tổng số pixels theo hàng dọc thỏa mãn điều kiện
    :param
        - img: np.ndarry
        - min_gap_height: chiều cao tối thiểu của khoảng trống
        - min_gap_width: chiều rộng tối thiểu của khoảng trống
    :return
        - List[(s, e)]: danh sách các đoạn chữ được tách cột
    """
    vertical_sum = np.sum(img, axis = 0)

    gaps = np.where(vertical_sum <= min_gap_height)[0]
    if gaps.size == 0:
        return [(0, img.shape[1])]

    gap_starts = np.hstack(([gaps[0]], gaps[1:][np.diff(gaps) > 1]))
    gap_ends = np.hstack((gaps[:-1][np.diff(gaps) > 1], [gaps[-1]]))
    gap_ranges = [(s, e) for s, e in zip(gap_starts, gap_ends) if (e - s) >= min_gap_width]

    text_segments = []
    current_pos = 0

    for gap_start, gap_end in gap_ranges:
        if current_pos < gap_start:
           text_segments.append((current_pos, gap_start))
        current_pos = gap_end + 1

    if current_pos < img.shape[1]:
        text_segments.append((current_pos, img.shape[1]))

    resp_objs = []
    for (s, e) in text_segments:
        if s >= 60: s -= 60
        if e <= img.shape[1] - 60:
            e += 60
        
        resp_objs.append((s, e))
    return resp_objs

def profile_projection_segment(
        img: np.ndarray
):
    """
    Cắt một hình ảnh văn bản lớn thành nhiều văn bản nhỏ hơn
    :param 
        img: hình ảnh nhị phân văn bản lớn
    :return:
        list image segments
    """
    resp_objs = []
    
    h_segments = horizontal_presegment(img)
    h_segments = sorted(h_segments, key = lambda x: x[0])

    check = False
    for i, (ys, ye) in enumerate(h_segments):
        ys, ye = int(ys), int(ye)
        sub_img = img[ys: ye, :]

        v_segments = vertical_segment(sub_img)

        if len(v_segments) > 1:
            check = True
            continue

        else:
            if check: 
        # if len(v_segments) == 1 and (i != 0):
                xs, xe = map(int, v_segments[0])

                resp_objs.append((
                    (ys, xs), (ye, xe)
                ))
                break
    
    return resp_objs