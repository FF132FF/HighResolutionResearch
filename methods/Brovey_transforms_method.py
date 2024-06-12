import numpy as np
from utils import get_interpolation_using_coefficient_23

def Brovey_transforms_method(high_resolution_image, low_resolution_image):
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

        intensity = np.mean(upsampled_low_resolution_image, axis=-1)

        res_high_resolution_image = (high_resolution_image - np.mean(high_resolution_image)) * \
                                    (np.std(intensity, ddof=1) / np.std(high_resolution_image, ddof=1)) + \
                                    np.mean(intensity)
        res_high_resolution_image = np.squeeze(res_high_resolution_image)

        Brovey_image=[]

        for element in range(low_resolution_image_channels):
            coefficients = res_high_resolution_image * upsampled_low_resolution_image[:, :, element] / (element + 1e-8)
            coefficients = np.expand_dims(coefficients, axis=-1)
            Brovey_image.append(coefficients)

        Brovey_image = np.concatenate(Brovey_image, axis=-1)

        Brovey_image[Brovey_image < 0] =0
        Brovey_image[Brovey_image > 1] =1

        return np.uint8(Brovey_image * 255)

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")
        return None