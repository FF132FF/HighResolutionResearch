import cv2
import numpy as np
import matplotlib.pyplot as plt


def detect_artifacts_k(image, HR):
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray_HR = cv2.cvtColor(HR, cv2.COLOR_RGB2GRAY)

    edges = cv2.Canny(gray_image, 100, 200)
    edges_HR = cv2.Canny(gray_HR, 100, 200)

    return [edges, edges_HR, edges_HR - edges]