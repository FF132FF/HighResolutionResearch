import cv2
import numpy as np
import matplotlib.pyplot as plt


def detect_artifacts_k(image, HR):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray_HR = cv2.cvtColor(HR, cv2.COLOR_RGB2GRAY)

    edges = cv2.Canny(gray_image, 100, 200)
    edges_HR = cv2.Canny(gray_HR, 100, 200)

    # contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # contours_HR, _ = cv2.findContours(edges_HR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    # mask = np.zeros_like(gray_image)
    # mask_HR = np.zeros_like(gray_HR)
    #
    # cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)
    # cv2.drawContours(mask_HR, contours_HR, -1, (255), thickness=cv2.FILLED)
    #
    # # Наложение маски на оригинальное изображение
    # highlighted_image = cv2.bitwise_and(HR, HR, mask=mask_HR)
    return [edges, edges_HR, edges_HR - edges]