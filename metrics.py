from skimage.metrics import mean_squared_error
from skimage.metrics import structural_similarity
from skimage.metrics import peak_signal_noise_ratio
import numpy as np
from scipy import ndimage
import cv2


def psnr_metric(result_high_resolution_image, original_high_resolution_image, dynamic_range=255):
    try:
        if result_high_resolution_image.shape == original_high_resolution_image.shape:
            result_high_resolution_image = result_high_resolution_image.astype(np.float64)
            original_high_resolution_image = original_high_resolution_image.astype(np.float64)

            mean_squared_errors = np.mean((result_high_resolution_image - original_high_resolution_image) ** 2)

            if mean_squared_errors <= 1e-10:
                return np.inf

            return 20 * np.log10(dynamic_range / (np.sqrt(mean_squared_errors) + np.finfo(np.float64).eps))

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")


def sam_metric(result_high_resolution_image, original_high_resolution_image):
    try:
        if result_high_resolution_image.shape == original_high_resolution_image.shape:
           if result_high_resolution_image.ndim == 3 and result_high_resolution_image.shape[2] > 1:
                result_high_resolution_image = result_high_resolution_image.astype(np.float64)
                original_high_resolution_image = original_high_resolution_image.astype(np.float64)

                content = (result_high_resolution_image * original_high_resolution_image).sum(axis=2)

                result_spectral_norm = np.sqrt((result_high_resolution_image ** 2).sum(axis=2))
                original_spectral_norm = np.sqrt((original_high_resolution_image ** 2).sum(axis=2))

                cos_theta = (content / (result_spectral_norm * original_spectral_norm + np.finfo(np.float64).eps)).clip(min=0, max=1)

                return np.mean(np.arccos(cos_theta))

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")

def scc_metric(result_high_resolution_image, original_high_resolution_image):
    try:
        if result_high_resolution_image.shape == original_high_resolution_image.shape:
            result_high_resolution_image = result_high_resolution_image.astype(np.float64)
            original_high_resolution_image = original_high_resolution_image.astype(np.float64)

            if result_high_resolution_image.ndim == 2:

                return np.corrcoef(result_high_resolution_image.reshape(1, -1),
                                   original_high_resolution_image.rehshape(1, -1))[0, 1]

            elif result_high_resolution_image.ndim == 3:
                scc_metric = [np.corrcoef(result_high_resolution_image[..., element].reshape(1, -1),
                                   original_high_resolution_image[..., element].reshape(1, -1))[0, 1]
                       for element in range(result_high_resolution_image.shape[2])]

                return np.mean(scc_metric)

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")


def ergas_metric(result_high_resolution_image, original_high_resolution_image, scale=4):
    try:
        if result_high_resolution_image.shape == original_high_resolution_image.shape:
            result_high_resolution_image = result_high_resolution_image.astype(np.float64)
            original_high_resolution_image = original_high_resolution_image.astype(np.float64)

            if result_high_resolution_image.ndim == 2:
                mean_original_high_resolution_image = original_high_resolution_image.mean()
                mean_squared_errors = np.mean((result_high_resolution_image - original_high_resolution_image) ** 2)

                return 100 / scale * np.sqrt(mean_squared_errors / (mean_original_high_resolution_image ** 2 +
                                                                    np.finfo(np.float64).eps))

            elif result_high_resolution_image.ndim == 3:
                mean_original_high_resolution_image = original_high_resolution_image\
                    .reshape(-1, original_high_resolution_image.shape[2]).mean(axis=0)
                mean_squared_errors = ((result_high_resolution_image - original_high_resolution_image) ** 2)\
                    .reshape(-1,  result_high_resolution_image.shape[2]).mean(axis=0)

                return 100 / scale * np.sqrt((mean_squared_errors / (mean_original_high_resolution_image ** 2 +
                                                                     np.finfo(np.float64).eps)).mean())

    except ValueError:
        print("Соотношение сторон изображений, поданных на вход функции, не совпадает")
