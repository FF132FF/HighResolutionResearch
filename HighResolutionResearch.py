from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QWidgetAction, QMenuBar,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QSizePolicy, QLabel)
from PyQt6.QtGui import QBrush, QPainter, QPen, QPixmap, QPolygonF, QImage, QDesktopServices
from PyQt6.QtWidgets import QWidget
from ui_HighResolutionResearch import Ui_MainWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from imagePreprocessing import *
import numpy as np
import sys
# import qimage2ndarray
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.action.triggered.connect(self.open_lr_image)
        self.ui.action_2.triggered.connect(self.open_hr_image)

    # paths = dict(LR='', HR='')
    def open_lr_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg)')
        if image_path:
            self.ui.label_1 = QLabel(self.ui.label_1)
            self.ui.pixmap = QPixmap(image_path)
            self.ui.label_1.setPixmap(self.ui.pixmap)
            self.ui.label_1.setScaledContents(True)
            self.ui.label_1.resize(480, 480)
            self.ui.label_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.label_1.show()

    def open_hr_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.jpeg)')
        if image_path:
            self.ui.label_2 = QLabel(self.ui.label_2)
            self.ui.pixmap = QPixmap(image_path)
            self.ui.label_2.setPixmap(self.ui.pixmap)
            self.ui.label_2.setScaledContents(True)
            self.ui.label_2.resize(480, 480)
            self.ui.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.label_2.show()

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
