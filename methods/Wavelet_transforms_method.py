import numpy as np
import pywt
from utils import get_interpolation_using_coefficient_23

def Wavelet_transforms_method(high_resolution_image, low_resolution_image):
    try:
        low_resolution_image_height, low_resolution_image_width, low_resolution_image_channels = \
            low_resolution_image.shape

        upsampled_low_resolution_image = low_resolution_image

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
        Wavelet_image[Wavelet_image > 255] = 255

        return Wavelet_image

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")
        return None