from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QWidgetAction, QMenuBar,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QSizePolicy, QLabel)
from PyQt6.QtGui import QBrush, QPainter, QPen, QPixmap, QPolygonF, QImage, QDesktopServices
from PyQt6.QtWidgets import QWidget

from ui_HighResolutionResearch import Ui_MainWindow

from PIL import Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import cv2 as cv
import numpy as np
import json
import sys

# import tensorflow as tf
# import tensorflow
# from tensorflow import keras
# from keras.preprocessing.image import img_to_array
# from keras.preprocessing.image import array_to_img

from methods.Bicubic_interpolation_method import bicubic_interpolation_method
from methods.IHS_method import IHS_method
from methods.Gram_Schmidt_method import Gram_Schmidt_method
from methods.Brovey_transforms_method import Brovey_transforms_method
from methods.Wavelet_transforms_method import Wavelet_transforms_method
from imagePreprocessing import *
from utils import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image_paths = dict(HR='', LR='')
        self.method = ''

        self.ui.action.triggered.connect(self.open_low_resolution_image)
        self.ui.action_2.triggered.connect(self.open_high_resolution_image)

        self.ui.pushButton_1.clicked.connect(self.open_bicubic_image)
        self.ui.pushButton_2.clicked.connect(self.open_IHS_image)
        self.ui.pushButton_3.clicked.connect(self.open_Gram_Schmidt_image)
        self.ui.pushButton_4.clicked.connect(self.open_Brovey_transforms_image)
        self.ui.pushButton_5.clicked.connect(self.open_Wavelet_transforms_image)


    def open_low_resolution_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg)')
        self.image_paths['LR'] = image_path
        low_resolution_image = open_image(image_path)
        low_resolution_minmax = min_max_stretch(low_resolution_image)
        cv.imwrite('low_resolution_minmax.jpg', low_resolution_minmax)

        if image_path:
            self.ui.label_1 = QLabel(self.ui.label_1)
            self.ui.pixmap = QPixmap('low_resolution_minmax.jpg')
            self.ui.label_1.setPixmap(self.ui.pixmap)
            self.ui.label_1.setScaledContents(True)
            self.ui.label_1.resize(480, 480)
            self.ui.label_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.label_1.show()

    def open_high_resolution_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg)')
        self.image_paths['HR'] = image_path
        high_resolution_image = open_image(image_path)
        high_resolution_minmax = min_max_stretch(high_resolution_image)
        cv.imwrite('high_resolution_minmax.jpg', high_resolution_minmax)
        
        if image_path:
            self.ui.label_2 = QLabel(self.ui.label_2)
            self.ui.pixmap = QPixmap('high_resolution_minmax.jpg')
            self.ui.label_2.setPixmap(self.ui.pixmap)
            self.ui.label_2.setScaledContents(True)
            self.ui.label_2.resize(480, 480)
            self.ui.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.label_2.show()


    def main_method_selection_algorithm(self):
        high_resolution_image = open_image(self.image_paths['HR'])
        low_resolution_image = open_image(self.image_paths['LR'])

        high_resolution_transposed_red_channel = high_resolution_image[:, :, 0]
        high_resolution_transposed_red_channel = np.expand_dims(high_resolution_transposed_red_channel, -1)

        resized_low_resolution_image = cv2.resize(low_resolution_image, (480, 480))

        self.ui.label_3 = QLabel(self.ui.label_3)

        if self.method == 'Bicubic_interpolation':
            bicubic_interpolation_image = bicubic_interpolation_method(high_resolution_image, low_resolution_image)
            bicubic_interpolation_minmax = min_max_stretch(bicubic_interpolation_image)

            cv.imwrite('bicubic_interpolation_minmax.jpg', bicubic_interpolation_minmax)
            self.ui.pixmap = QPixmap('bicubic_interpolation_minmax.jpg')


        elif self.method == 'IHS':
            IHS_image = IHS_method(high_resolution_transposed_red_channel, resized_low_resolution_image)
            IHS_minmax = min_max_stretch(IHS_image)

            cv.imwrite('IHS_minmax.jpg', IHS_minmax)
            self.ui.pixmap = QPixmap('IHS_minmax.jpg')

        elif self.method == 'Gram_Schmidt':
            Gram_Schmidt_image = Gram_Schmidt_method(high_resolution_transposed_red_channel,
                                                     resized_low_resolution_image)
            Gram_Schmidt_minmax = min_max_stretch(Gram_Schmidt_image)

            cv.imwrite('Gram_Schmidt_minmax.jpg', Gram_Schmidt_minmax)
            self.ui.pixmap = QPixmap('Gram_Schmidt_minmax.jpg')

        elif self.method == 'Brovey_transforms':
            Brovey_transforms_image = Brovey_transforms_method(high_resolution_transposed_red_channel,
                                                               resized_low_resolution_image)
            Brovey_transforms_minmax = min_max_stretch(Brovey_transforms_image)

            cv.imwrite('Brovey_transforms_minmax.jpg', Brovey_transforms_minmax)
            self.ui.pixmap = QPixmap('Brovey_transforms_minmax.jpg')

        elif self.method == 'Wavelet_transforms':
            Wavelet_transforms_image = Wavelet_transforms_method(high_resolution_transposed_red_channel,
                                                                 resized_low_resolution_image)
            Wavelet_transforms_minmax = min_max_stretch(Wavelet_transforms_image)

            cv.imwrite('Wavelet_transforms_minmax.jpg', Wavelet_transforms_minmax)
            self.ui.pixmap = QPixmap('Wavelet_transforms_minmax.jpg')

        self.ui.label_3.setPixmap(self.ui.pixmap)
        self.ui.label_3.setScaledContents(True)
        self.ui.label_3.resize(480, 480)
        self.ui.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_3.show()

    def open_bicubic_image(self):
        self.method = 'Bicubic_interpolation'
        self.main_method_selection_algorithm()


    def open_IHS_image(self):
        self.method = 'IHS'
        self.main_method_selection_algorithm()


    def open_Gram_Schmidt_image(self):
        self.method = 'Gram_Schmidt'
        self.main_method_selection_algorithm()


    def open_Brovey_transforms_image(self):
        self.method = 'Brovey_transforms'
        self.main_method_selection_algorithm()

    def open_Wavelet_transforms_image(self):
        self.method = 'Wavelet_transforms'
        self.main_method_selection_algorithm()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


# print(paths['LR'])
# print(paths['HR'])
#
# selected_methods = dict(BI=False, IHS=False, GS=False, BT=False, WT=False, SR=False)
#
# def on_click():
#     selected_methods['BI'] = ui.checkBox.isChecked()
#     selected_methods['IHS'] = ui.checkBox_2.isChecked()
#     selected_methods['GS'] = ui.checkBox_3.isChecked()
#     selected_methods['BT'] = ui.checkBox_4.isChecked()
#     selected_methods['WT'] = ui.checkBox_5.isChecked()
#     selected_methods['SR'] = ui.checkBox_6.isChecked()
#     selection_methods_text = json.dumps(selected_methods)
#     ui.label.setText(ui.label.text() + selection_methods_text + '\n')
#
#
# ui.pushButton.clicked.connect(on_click)
