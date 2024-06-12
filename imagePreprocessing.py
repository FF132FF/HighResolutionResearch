import os
from skimage import exposure
import numpy as np
from numpy import asarray
from PIL import Image
import matplotlib.pyplot as plt
import tifffile
import cv2
# from scipy import ndimagepyuic6
from PyQt6.QtGui import QImage

def open_tiff_image(file_path):

    try:
        image = tifffile.imread(file_path)
        image_np = np.array(image)
        image_np = np.transpose(image_np, (1, 0, 2))
        image_np = np.ascontiguousarray(image_np)
        return image_np
    except Exception as e:
        print("Ошибка при открытии изображения:", e)
        return None

def open_image(file_path):
    try:
        image = Image.open(file_path)
        numpydata = np.array(image)
        return numpydata
    except Exception as e:
        print("Ошибка при открытии изображения:", e)
        return None

def plot_histogram(image_path, title='изображения'):
    if image_path.lower().endswith('.tif'):
        image = open_tiff_image(image_path)
    else:
        image = open_image(image_path)

    fig, axes = plt.subplots(figsize=(12, 8))

    axes[0].hist(image.flatten(), bins=256, range=[0, 256], color='r')
    axes[0].set_title('Гистограмма ' + title)
    axes[0].grid(True)

    # plt.tight_layout()
    # plt.show()
    return fig

def visualize_images(image_path, title='изображения'):
    if image_path.lower().endswith('.tif'):
        image = open_tiff_image(image_path)
    else:
        image = open_image(image_path)

    fig, axes = plt.subplots(figsize=(12, 6))

    im_before = axes[0].imshow(image)
    axes[0].set_title('Отображение ' + title)
    axes[0].axis('off')

    cbar_before = fig.colorbar(im_before, ax=axes[0])
    cbar_before.set_label('Значения пикселей')

    # plt.tight_layout()
    # plt.show()
    return image
