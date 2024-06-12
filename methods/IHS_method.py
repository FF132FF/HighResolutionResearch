import numpy as np
from utils import get_interpolation_using_coefficient_23


def IHS_method(high_resolution_image, low_resolution_image):
    try:
        high_resolution_image_height, high_resolution_image_width, high_resolution_image_channels = \
            high_resolution_image.shape
        low_resolution_image_height, low_resolution_image_width, low_resolution_image_channels = \
            low_resolution_image.shape

        image_height_ratio = int(np.round(high_resolution_image_height / low_resolution_image_height))
        image_width_ratio = int(np.round(high_resolution_image_width / low_resolution_image_width))

        if image_height_ratio == image_width_ratio:
            print("Получившееся соотношение изображений: ", image_width_ratio)

        upsampled_low_resolution_image = get_interpolation_using_coefficient_23(low_resolution_image, image_width_ratio)

        mean_low = np.mean(upsampled_low_resolution_image, axis=-1, keepdims=True)
        mean_high = (high_resolution_image - np.mean(high_resolution_image)) * np.std(mean_low, ddof=1) / \
            np.std(high_resolution_image, ddof=1) + np.mean(mean_low)

        IHS_image = upsampled_low_resolution_image + np.tile(mean_high - mean_low,
                                                                          (1, 1, low_resolution_image_channels))
        IHS_image[IHS_image < 0] = 0
        IHS_image[IHS_image > 1] = 1

        return np.uint8(IHS_image * 255)

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")
        return None

