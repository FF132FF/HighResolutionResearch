import numpy as np
from utils import get_bicubic_interpolation


def bicubic_interpolation_method(high_resolution_image, low_resolution_image):
    try:
        high_resolution_image_height, high_resolution_image_width, high_resolution_image_channels = \
            high_resolution_image.shape
        low_resolution_image_height, low_resolution_image_width, low_resolution_image_channels = \
            low_resolution_image.shape

        image_height_ratio = int(np.round(high_resolution_image_height / low_resolution_image_height))
        image_width_ratio = int(np.round(high_resolution_image_width / low_resolution_image_width))

        if image_height_ratio == image_width_ratio:
            print("Получившееся соотношение изображений: ", image_width_ratio)

        bicubic_interpolated_image = get_bicubic_interpolation(low_resolution_image, image_width_ratio)

        bicubic_interpolated_image[bicubic_interpolated_image < 0] = 0
        bicubic_interpolated_image[bicubic_interpolated_image > 255] = 255

        return bicubic_interpolated_image

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")
        return None