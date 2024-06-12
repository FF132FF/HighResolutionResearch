from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QWidgetAction, QMenuBar,
                             QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QSizePolicy)
from PyQt6.QtGui import QBrush, QPainter, QPen, QPixmap, QPolygonF, QImage
from ui_HighResolutionResearch import Ui_MainWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from imagePreprocessing import *
import numpy as np
import sys
# import qimage2ndarray

app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()

paths = dict(LR='', HR='')

def openLRImage():
    image_path, _ = QFileDialog.getOpenFileName()
    # paths['LR'] = image_path
    image = open_tiff_image(image_path)
    # q_image = qimage2ndarray.array2qimage(image)
    qimage = QImage(image.data, image.shape[1], image.shape[0],
                    QImage.Format.Format_RGB888)
    pixmap = QPixmap(qimage)
    pixmap = pixmap.scaled(320, 320)
    # ui.label_24.setSizePolicy(QSizePolicy.Policy, QSizePolicy.Policy)
    ui.label_24.resize(320, 320)
    ui.label_24.setAlignment(Qt.AlignmentFlag.AlignCenter)
    ui.label_24.setPixmap(pixmap)
    ui.label_24.setPixmap(ui.label_24)

    # ui.setCentralWidget(ui.label_24)
    # ui.show()
    # print(image)
    # pixmap = QPixmap.fromImage(image).scaled(320, 320, transformMode=QtCore.Qt.SSmoothTransformation,
    #                                          aspectRatioMode=QtCore.Qt.AspectRatioMode)
    #
    # ui.grphics_scene.clear()
    # pixmap_item = QGraphicsPixmapItem(pixmap)
    # ui.graphics_scene.addItem(pixmap_item)
    # ui.label_24.setScene(ui.graphics_scene)
    # ui.label_24.setRenderHint(QPainter.RenderHint.Antialiasing)
    # ui.setCentralWidget(ui.label_24)
    # ui.resize(pixmap.width(), pixmap.height())
    # ui.scene = QGraphicsScene()
    # ui.graphicsView_25.setScene(ui.scene)
    #
    # ui.figure = visualize_images(paths['LR'], title='изображения с низким пространственным разрешением')
    # ui.axes = ui.figure.gca()
    # ui.canvas = FigureCanvas(ui.figure)
    # ui.proxy_widget = ui.scene.addWidget(ui.canvas)

# print(paths['LR'], paths['HR'])

def openHRImage():
    image_path, _ = QFileDialog.getOpenFileName()
    paths['HR'] = image_path
    print(paths['LR'], paths['HR'])

ui.action.triggered.connect(openLRImage)
ui.action_2.triggered.connect(openHRImage)
print(paths['LR'])
print(paths['HR'])





def on_click():
    selected_methods = dict(BI=False, IHS=False, GS=False, BT=False, WT=False, SR=False)
    selected_methods['BI'] = ui.checkBox.isChecked()
    selected_methods['IHS'] = ui.checkBox_2.isChecked()
    selected_methods['GS'] = ui.checkBox_3.isChecked()
    selected_methods['BT'] = ui.checkBox_4.isChecked()
    selected_methods['WT'] = ui.checkBox_5.isChecked()
    selected_methods['SR'] = ui.checkBox_6.isChecked()
    print(selected_methods)


ui.pushButton.clicked.connect(on_click)


sys.exit(app.exec())