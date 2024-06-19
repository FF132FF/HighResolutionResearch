from numpy import asarray
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
        image = cv2.imread(file_path)
        numpy_data = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return numpy_data

    except Exception as e:
        print("Ошибка при открытии изображения:", e)
        return None