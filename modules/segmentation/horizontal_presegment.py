# import built-in dependencies
import time

# import 3rd party dependencies
import numpy as np

def horizontal_presegment(
        img: np.ndarray,
        threshold = 0.28,
        min_gap_height = 3,
        min_gap_width = 10
):
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
    t0 = time.time()

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

    t1 = time.time()
    return [(s, e) for (s, e) in text_segments if e <= h_crop], {"horizontal_presegment": t1 - t0}



