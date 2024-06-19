import numpy as np
import cv2


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


