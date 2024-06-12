import numpy as np
import pywt
from utils import get_interpolation_using_coefficient_23

def Wavelet_transforms_method(high_resolution_image, low_resolution_image):
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

        high_resolution_image = np.squeeze(high_resolution_image)
        coefficients = pywt.wavedec2(high_resolution_image, 'haar', level=2)

        reconstructions = []

        for element in range(low_resolution_image_channels):
            deconstructions = pywt.wavedec2(upsampled_low_resolution_image[:, :, element], 'haar', level=2)

            coefficients[0] = deconstructions[0]

            reconstruction = pywt.waverec2(coefficients, 'haar')
            reconstruction = np.expand_dims(reconstruction, -1)
            reconstructions.append(reconstruction)

        Wavelet_image = np.concatenate(reconstructions, axis=-1)

        Wavelet_image[Wavelet_image < 0] = 0
        Wavelet_image[Wavelet_image > 1] = 1

        return np.uint8(Wavelet_image * 255)

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")
