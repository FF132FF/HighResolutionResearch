import numpy as np
from numpy import asarray
from PIL import Image
import matplotlib.pyplot as plt
import tifffile
import cv2


def open_tiff_image(file_path):
    try:
        image = tifffile.imread(file_path)
        numpy_data = asarray(image)
        return numpy_data

    except Exception as e:
        print("Ошибка при открытии изображения:", e)
        return None


def open_image(file_path):
    try:
        image = Image.open(file_path)
        numpy_data = asarray(image)
        return numpy_data

    except Exception as e:
        print("Ошибка при открытии изображения:", e)
        return None


def min_max_stretch(image):
    try:
        min_val = np.min(image)
        max_val = np.max(image)
        stretched_image = 255 * ((image - min_val) / (max_val - min_val))

        return stretched_image.astype(np.uint8)

    except Exception as e:
        print("Ошибка при применении минимаксного растяжения:", e)
        return None

def normalize_image(image):
    try:
        mean_value = np.mean(image)
        std_dev = np.std(image)
        normalized_image = (image - mean_value) / std_dev

        return abs(normalized_image)

    except Exception as e:
        print("Ошибка при применении нормализации:", e)
        return None


def equalize_image(image):
    try:
        if len(image.shape) == 3 and image.shape[2] == 3:
            b, g, r = cv2.split(image)

            b_eq = cv2.equalizeHist(b)
            g_eq = cv2.equalizeHist(g)
            r_eq = cv2.equalizeHist(r)

            equalized_image = cv2.merge((b_eq, g_eq, r_eq))

        else:
            equalized_image = cv2.equalizeHist(image)

        return equalized_image

    except Exception as e:
        print("Ошибка при применении эквализации:", e)
        return None


def plot_histogram(image_path, title='изображения'):
    try:
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

    except Exception as e:
        print("Ошибка при получении гистограммы:", e)
        return None


def visualize_images(image_path, title='изображения'):
    try:
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

    except Exception as e:
        print("Ошибка при отображении изображения:", e)
        return None