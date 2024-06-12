import cv2 as cv
import numpy as np
from scipy import ndimage

def get_bicubic_interpolation(original_image, image_ratio):
    image_height, image_width, image_channels = original_image.shape
    resized_image = cv.resize(original_image, (image_width * image_ratio, image_height * image_ratio),
                              interpolation=cv.INTER_CUBIC)

    return resized_image

def get_interpolation_using_coefficient_23(original_image, image_ratio):
    global low_resolution_upsampled_image

    transposed_image = np.transpose(original_image, (2, 0, 1))
    image_height, image_width, image_channels = transposed_image.shape
    cdf_23 = 2 * np.array([0.5, 0.305334091185, 0, -0.072698593239, 0, 0.021809577942, 0, -0.005192756653, 0,
                           0.000807762146, 0, -0.000060081482])
    index = cdf_23[::-1]
    cdf_23 = np.insert(cdf_23, 0, index[:-1])
    base_coefficient = cdf_23

    first = 1

    for element in range(1, int(np.log2(image_ratio)) + 1):
        low_resolution_upsampled_image = np.zeros((image_height, 2 ** element * image_width, 2 ** element *
                                                   image_channels))
        if first:
            low_resolution_upsampled_image[:, 1:low_resolution_upsampled_image.shape[1]:2,
            1:low_resolution_upsampled_image.shape[2]:2] = transposed_image
            first = 0
        else:
            low_resolution_upsampled_image[:, 0:low_resolution_upsampled_image.shape[1]:2,
            0:low_resolution_upsampled_image.shape[2]:2] = transposed_image

        for second_element in range(0, image_height):
            num = low_resolution_upsampled_image[second_element, :, :]

            for i in range(0, num.shape[0]):
                num[i, :] = ndimage.correlate(num[i, :], base_coefficient, mode='wrap')

            for j in range(0, num.shape[1]):
                num[:, j] = ndimage.correlate(num[:, j], base_coefficient, mode='wrap')

            low_resolution_upsampled_image[second_element, :, :] = num

    resized_image = np.transpose(low_resolution_upsampled_image, (1, 2, 0))

    return resized_image
