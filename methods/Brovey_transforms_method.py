import numpy as np
from utils import get_interpolation_using_coefficient_23


def Brovey_transforms_method(high_resolution_image, low_resolution_image):
    try:
        low_resolution_image_height, low_resolution_image_width, low_resolution_image_channels = \
            low_resolution_image.shape

        upsampled_low_resolution_image = low_resolution_image

        intensity = np.mean(upsampled_low_resolution_image, axis=-1)

        res_high_resolution_image = (high_resolution_image - np.mean(high_resolution_image)) * \
                                    (np.std(intensity, ddof=1) / np.std(high_resolution_image, ddof=1)) + \
                                    np.mean(intensity)
        res_high_resolution_image = np.squeeze(res_high_resolution_image)

        Brovey_image = []

        for element in range(low_resolution_image_channels):
            coefficients = res_high_resolution_image * upsampled_low_resolution_image[:, :, element] / \
                           (intensity + 1e-8)
            coefficients = np.expand_dims(coefficients, axis=-1)
            Brovey_image.append(coefficients)

        Brovey_image = np.concatenate(Brovey_image, axis=-1)

        Brovey_image[Brovey_image < 0] = 0
        Brovey_image[Brovey_image > 255] = 255

        return Brovey_image

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")
        return None
