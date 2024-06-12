import numpy as np
from utils import get_interpolation_using_coefficient_23

def Gram_Schmidt_method(high_resolution_image, low_resolution_image):
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

        mean_values = np.mean(upsampled_low_resolution_image, axis=(0, 1))
        res_low_resolution_image = upsampled_low_resolution_image - mean_values

        intensity = np.mean(upsampled_low_resolution_image, axis=2, keepdims=True)
        intensity_difference = intensity - np.mean(intensity)

        res_high_resolution_image = (high_resolution_image - np.mean(high_resolution_image)) * \
                   (np.std(intensity_difference, ddof=1) / np.std(high_resolution_image, ddof=1)) + \
                                    np.mean(intensity_difference)

        coefficients = []
        coefficients.append(1)

        for element in range(low_resolution_image_channels):
            channel = res_low_resolution_image[:, :, element]
            high_resolution_image_channels = np.cov(np.reshape(intensity_difference, (-1,)),
                                                    np.reshape(channel, (-1,)), ddof=1)
            coefficients.append(high_resolution_image_channels[0, 1] / np.var(intensity_difference))

        coefficients = np.array(coefficients)

        extracted_detail = res_high_resolution_image - intensity_difference
        res_extracted_detail = np.tile(extracted_detail, (1, 1, low_resolution_image_channels + 1))

        fusioned = np.concatenate((intensity_difference, res_low_resolution_image), axis=-1)

        coefficients = np.expand_dims(coefficients, 0)
        coefficients = np.expand_dims(coefficients, 0)

        coefficients = np.tile(coefficients, (high_resolution_image_height, high_resolution_image_width, 1))

        fusioned_cooficients = fusioned + coefficients * res_extracted_detail

        Gram_Schmidt_image = fusioned_cooficients[:, :, 1:]
        Gram_Schmidt_image = Gram_Schmidt_image - np.mean(Gram_Schmidt_image, axis=(0, 1)) + mean_values

        Gram_Schmidt_image[Gram_Schmidt_image < 0] = 0
        Gram_Schmidt_image[Gram_Schmidt_image > 1] = 1

        return np.uint8(Gram_Schmidt_image * 255)

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")
