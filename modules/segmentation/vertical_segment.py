# import built-in dependencies
import time

# import 3rd party dependencies
import numpy as np

def vertical_segment(
        img: np.ndarray, 
        min_gap_height = 50, 
        min_gap_width = 60
):
    """
    Xác định khoảng trống giữa các cột bằng tổng số pixels theo hàng dọc thỏa mãn điều kiện
    :param
        - img: np.ndarry
        - min_gap_height: chiều cao tối thiểu của khoảng trống
        - min_gap_width: chiều rộng tối thiểu của khoảng trống
    :return
        - List[(s, e)]: danh sách các đoạn chữ được tách cột
    """
    t0 = time.time()

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
    
    t1 = time.time()
    return text_segments, {"vertical_segment": t1 - t0}