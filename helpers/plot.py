from typing import *

import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_img(img: np.ndarray) -> None:
    """
    In ra hình ảnh yêu cầu.
    :param
        - img: ảnh cần in ra trong phần output.
    """
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb)
    plt.axis("off")
    plt.show()

def display_imgs(
        imgs: List[np.ndarray], 
        imgs_per_row: int = 3
):
    num_imgs = len(imgs)
    num_rows = (num_imgs + imgs_per_row - 1) // imgs_per_row

    fig, axes = plt.subplots(num_rows, imgs_per_row, figsize=(15, 5 * num_rows))
    axes = np.array(axes).reshape(num_rows, imgs_per_row)

    for i, img in enumerate(imgs):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        row, col = divmod(i, imgs_per_row)
        axes[row, col].imshow(img_rgb)
        axes[row, col].axis("off")

    for i in range(num_imgs, num_rows * imgs_per_row):
        row, col = divmod(i, imgs_per_row)
        axes[row, col].axis("off")

    plt.tight_layout()
    plt.show()

def display_histogram(
        img: np.ndarray, 
        angle: int
):
    horizontal_sum = np.sum(img, axis = 1)
    plt.figure(figsize = (8, 4))
    plt.plot(horizontal_sum, color = "black")
    plt.title(f"Histogram projection profile: Góc xoay {angle}")
    plt.xlabel("Row index")
    plt.ylabel("Pixels sum")
    plt.show()

def display_interval_distribution(
        arr: List[Any], 
        step: int
):
    start = (min(arr) // step) * step 
    end = (max(arr) // step + 1) * step
    bins = np.arange(start, end + step, step)
    
    hist, bin_edges = np.histogram(arr, bins = bins)

    plt.figure(figsize=(10, 5))
    plt.bar(bin_edges[:-1], hist, width=step, align="edge", edgecolor="black", alpha=0.7)
    plt.xlabel("Khoảng giá trị")
    plt.ylabel("Số lượng phần tử")
    plt.title("Biểu đồ phân bố giá trị")
    plt.xticks(bin_edges, rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.show()




