from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QLabel, QDialog)
from PyQt6.QtGui import QPixmap

from ui_HighResolutionResearch import Ui_MainWindow
from ui_DemensionAndChannelSelection import Ui_Dialog

from methods.Bicubic_interpolation_method import bicubic_interpolation_method
from methods.IHS_method import IHS_method
from methods.Gram_Schmidt_method import Gram_Schmidt_method
from methods.Brovey_transforms_method import Brovey_transforms_method
from methods.Wavelet_transforms_method import Wavelet_transforms_method
from imagePreprocessing import *
from imageOpener import *
from metricProcess import *
from artifactDetection import *
from utils import *
import sys


class DialogWindow(QDialog):
    def __init__(self, parent=None):
        super(DialogWindow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.data = []
        self.ui.pushButton.clicked.connect(self.select_channels)


    def select_channels(self):
        image_shape = self.ui.lineEdit.text()
        k = self.ui.lineEdit_2.text()
        first_channel = self.ui.comboBox.currentText()
        second_channel = self.ui.comboBox_2.currentText()
        third_channel = self.ui.comboBox_3.currentText()

        self.data = [image_shape, k, first_channel, second_channel, third_channel]



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image_paths = dict(HR='', LR='')
        self.method = ''
        self.method_image = ''

        self.ui.action.triggered.connect(self.open_low_resolution_image)
        self.ui.action_2.triggered.connect(self.open_high_resolution_image)
        self.ui.action_3.triggered.connect(self.open_demension_n_channel_selection)

        self.ui.pushButton_1.clicked.connect(self.open_bicubic_image)
        self.ui.pushButton_2.clicked.connect(self.open_IHS_image)
        self.ui.pushButton_3.clicked.connect(self.open_Gram_Schmidt_image)
        self.ui.pushButton_4.clicked.connect(self.open_Brovey_transforms_image)
        self.ui.pushButton_5.clicked.connect(self.open_Wavelet_transforms_image)
        self.ui.pushButton_6.clicked.connect(self.open_Super_resolution_image)
        self.ui.pushButton_7.clicked.connect(self.get_metrics_for_method)
        self.ui.pushButton_8.clicked.connect(self.get_artifact_detection)
        self.ui.pushButton_9.clicked.connect(self.equalized_images)
        self.ui.pushButton_10.clicked.connect(self.return_basic_view)


    def open_demension_n_channel_selection(self):
        self.dialog_window = DialogWindow(self)

        self.dialog_window.exec()



    def open_low_resolution_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg)')
        self.image_paths['LR'] = image_path
        low_resolution_image = open_image(image_path)
        low_resolution_minmax = min_max_stretch(low_resolution_image)
        cv.imwrite('low_resolution_minmax.jpg', low_resolution_minmax)

        if image_path:
            self.ui.label_5.setText("Низкое пространственное разрешение")
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
            self.ui.label_6.setText("Высокое пространственное разрешение")
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

        if self.method == 'Бикубическая интерполяция':
            bicubic_interpolation_image = bicubic_interpolation_method(high_resolution_image, low_resolution_image)
            bicubic_interpolation_minmax = min_max_stretch(bicubic_interpolation_image)
            self.method_image = bicubic_interpolation_minmax

            cv.imwrite('bicubic_interpolation_minmax.jpg', bicubic_interpolation_minmax)
            self.ui.pixmap = QPixmap('bicubic_interpolation_minmax.jpg')


        elif self.method == 'IHS':
            IHS_image = IHS_method(high_resolution_transposed_red_channel, resized_low_resolution_image)
            IHS_minmax = min_max_stretch(IHS_image)
            self.method_image = IHS_minmax

            cv.imwrite('IHS_minmax.jpg', IHS_minmax)
            self.ui.pixmap = QPixmap('IHS_minmax.jpg')

        elif self.method == 'Gramm-Schmidt':
            Gram_Schmidt_image = Gram_Schmidt_method(high_resolution_transposed_red_channel,
                                                     resized_low_resolution_image)
            Gram_Schmidt_minmax = min_max_stretch(Gram_Schmidt_image)
            self.method_image = Gram_Schmidt_minmax

            cv.imwrite('Gram_Schmidt_minmax.jpg', Gram_Schmidt_minmax)
            self.ui.pixmap = QPixmap('Gram_Schmidt_minmax.jpg')

        elif self.method == 'Brovey':
            Brovey_transforms_image = Brovey_transforms_method(high_resolution_transposed_red_channel,
                                                               resized_low_resolution_image)
            Brovey_transforms_minmax = min_max_stretch(Brovey_transforms_image)
            self.method_image = Brovey_transforms_minmax

            cv.imwrite('Brovey_transforms_minmax.jpg', Brovey_transforms_minmax)
            self.ui.pixmap = QPixmap('Brovey_transforms_minmax.jpg')

        elif self.method == 'Wavelet':
            Wavelet_transforms_image = Wavelet_transforms_method(high_resolution_transposed_red_channel,
                                                                 resized_low_resolution_image)
            Wavelet_transforms_minmax = min_max_stretch(Wavelet_transforms_image)
            self.method_image = Wavelet_transforms_minmax

            cv.imwrite('Wavelet_transforms_minmax.jpg', Wavelet_transforms_minmax)
            self.ui.pixmap = QPixmap('Wavelet_transforms_minmax.jpg')

        elif self.method == 'Super Resolution':
            model_path, _ = QFileDialog.getOpenFileName(self, 'Open Model', '', 'Model File (*.h5)')
            Super_Resolution_image = Gram_Schmidt_method(high_resolution_transposed_red_channel,
                                                                 resized_low_resolution_image)
            Super_Resolution_minmax = min_max_stretch(Super_Resolution_image)
            self.method_image = Super_Resolution_minmax

            cv.imwrite('Super_Resolution_minmax.jpg', Super_Resolution_minmax)
            self.ui.pixmap = QPixmap('Super_Resolution_minmax.jpg')

        self.ui.label_3.setPixmap(self.ui.pixmap)
        self.ui.label_3.setScaledContents(True)
        self.ui.label_3.resize(480, 480)
        self.ui.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_3.show()


    def open_bicubic_image(self):
        self.ui.label_7.setText("Метод Бикубическая интерполяция")
        self.method = 'Бикубическая интерполяция'
        self.main_method_selection_algorithm()


    def open_IHS_image(self):
        self.ui.label_7.setText("Метод IHS")
        self.method = 'IHS'
        self.main_method_selection_algorithm()


    def open_Gram_Schmidt_image(self):
        self.method = 'Gramm-Schmidt'
        self.ui.label_7.setText("Метод Gramm-Schmidt")
        self.main_method_selection_algorithm()


    def open_Brovey_transforms_image(self):
        self.ui.label_7.setText("Метод Brovey")
        self.method = 'Brovey'
        self.main_method_selection_algorithm()

    def open_Wavelet_transforms_image(self):
        self.ui.label_7.setText("Метод Wavelet")
        self.method = 'Wavelet'
        self.main_method_selection_algorithm()

    def open_Super_resolution_image(self):
        self.ui.label_7.setText("Метод Super Resolution")
        self.method = 'Super Resolution'
        self.main_method_selection_algorithm()

    def get_metrics_for_method(self):
        high_resolution_image = open_image(self.image_paths['HR'])
        low_resolution_image = open_image(self.image_paths['LR'])

        high_resolution_transposed_red_channel = high_resolution_image[:, :, 0]
        high_resolution_transposed_red_channel = np.expand_dims(high_resolution_transposed_red_channel, -1)

        resized_low_resolution_image = cv2.resize(low_resolution_image, (480, 480))
        high_resolution_minmax = min_max_stretch(high_resolution_image)

        bicubic_interpolation_image = bicubic_interpolation_method(high_resolution_image, low_resolution_image)
        bicubic_interpolation_minmax = min_max_stretch(bicubic_interpolation_image)

        IHS_image = IHS_method(high_resolution_transposed_red_channel, resized_low_resolution_image)
        IHS_minmax = min_max_stretch(IHS_image)

        Gram_Schmidt_image = Gram_Schmidt_method(high_resolution_transposed_red_channel,
                                                 resized_low_resolution_image)
        Gram_Schmidt_minmax = min_max_stretch(Gram_Schmidt_image)

        Brovey_transforms_image = Brovey_transforms_method(high_resolution_transposed_red_channel,
                                                           resized_low_resolution_image)
        Brovey_transforms_minmax = min_max_stretch(Brovey_transforms_image)

        Wavelet_transforms_image = Wavelet_transforms_method(high_resolution_transposed_red_channel,
                                                             resized_low_resolution_image)
        Wavelet_transforms_minmax = min_max_stretch(Wavelet_transforms_image)

        metrics_table = metrics_report_of_method(high_resolution_minmax, bicubic_interpolation_minmax, IHS_minmax, Gram_Schmidt_minmax, Brovey_transforms_minmax, Wavelet_transforms_minmax)
        self.ui.label_4.setText(self.ui.label_4.text() + metrics_table + '\n')


    def equalized_images(self):
        low_res_img = open_image(self.image_paths['LR'])
        high_res_img = open_image(self.image_paths['HR'])

        ezualized_low_res_img = equalize_image(low_res_img)
        ezualized_high_res_img = equalize_image(high_res_img)
        equalized_method_img = equalize_image(self.method_image)

        cv.imwrite('ezualized_low_res_img.jpg', ezualized_low_res_img)
        self.ui.pixmap = QPixmap('ezualized_low_res_img.jpg')
        self.ui.label_1.setPixmap(self.ui.pixmap)
        self.ui.label_1.setScaledContents(True)
        self.ui.label_1.resize(480, 480)
        self.ui.label_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_1.show()

        cv.imwrite('ezualized_high_res_img.jpg', ezualized_high_res_img)
        self.ui.pixmap = QPixmap('ezualized_high_res_img.jpg')
        self.ui.label_2.setPixmap(self.ui.pixmap)
        self.ui.label_2.setScaledContents(True)
        self.ui.label_2.resize(480, 480)
        self.ui.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_2.show()

        cv.imwrite('equalized_method_img.jpg', equalized_method_img)
        self.ui.pixmap = QPixmap('equalized_method_img.jpg')
        self.ui.label_3.setPixmap(self.ui.pixmap)
        self.ui.label_3.setScaledContents(True)
        self.ui.label_3.resize(480, 480)
        self.ui.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_3.show()

    def get_artifact_detection(self):
        high_res_img = open_image(self.image_paths['HR'])
        high_res_img = min_max_stretch(high_res_img)
        method_img = self.method_image

        result = detect_artifacts_k(method_img, high_res_img)

        edges = result[0]
        HR_edges = result[1]
        edges_difference = result[2]

        self.ui.label_5.setText(f"Границы для метода: {self.method}")
        cv.imwrite('edges.jpg', edges)
        self.ui.pixmap = QPixmap('edges.jpg')
        self.ui.label_1.setPixmap(self.ui.pixmap)
        self.ui.label_1.setScaledContents(True)
        self.ui.label_1.resize(480, 480)
        self.ui.label_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_1.show()

        self.ui.label_6.setText(f"Границы для эталона с высоким разрешением")
        cv.imwrite('HR_edges.jpg', HR_edges)
        self.ui.pixmap = QPixmap('HR_edges.jpg')
        self.ui.label_2.setPixmap(self.ui.pixmap)
        self.ui.label_2.setScaledContents(True)
        self.ui.label_2.resize(480, 480)
        self.ui.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_2.show()

        self.ui.label_7.setText(f"Разница границ между эталоном и результатом работы метода")
        cv.imwrite('edges_difference.jpg', edges_difference)
        self.ui.pixmap = QPixmap('edges_difference.jpg')
        self.ui.label_3.setPixmap(self.ui.pixmap)
        self.ui.label_3.setScaledContents(True)
        self.ui.label_3.resize(480, 480)
        self.ui.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_3.show()

    def return_basic_view(self):
        low_res_img = open_image(self.image_paths['LR'])
        low_res_img = min_max_stretch(low_res_img)
        high_res_img = open_image(self.image_paths['HR'])
        high_res_img = min_max_stretch(high_res_img)
        method_img = self.method_image

        self.ui.label_5.setText(f"Низкое пространственное разрешение")
        cv.imwrite('low_res_img.jpg', low_res_img)
        self.ui.pixmap = QPixmap('low_res_img.jpg')
        self.ui.label_1.setPixmap(self.ui.pixmap)
        self.ui.label_1.setScaledContents(True)
        self.ui.label_1.resize(480, 480)
        self.ui.label_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_1.show()

        self.ui.label_6.setText(f"Высокое пространственное разрешение")
        cv.imwrite('high_res_img.jpg', high_res_img)
        self.ui.pixmap = QPixmap('high_res_img.jpg')
        self.ui.label_2.setPixmap(self.ui.pixmap)
        self.ui.label_2.setScaledContents(True)
        self.ui.label_2.resize(480, 480)
        self.ui.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_2.show()

        self.ui.label_7.setText(f"Метод {self.method}")
        cv.imwrite('method_img.jpg', method_img)
        self.ui.pixmap = QPixmap('method_img.jpg')
        self.ui.label_3.setPixmap(self.ui.pixmap)
        self.ui.label_3.setScaledContents(True)
        self.ui.label_3.resize(480, 480)
        self.ui.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ui.label_3.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

