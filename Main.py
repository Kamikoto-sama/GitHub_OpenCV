# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets,QtCore,QtGui
import sys
import os

import Form
import ImageDetect
import VideoDetect

class Main(QtWidgets.QMainWindow,Form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.selectImage.clicked.connect(self.SelectImage)
        self.selectVideo.clicked.connect(self.SelectVideo)

    def SelectImage(self):
        try:
            image = QtWidgets.QFileDialog.getOpenFileName(self,"Select image",'')[0]
            ImageDetect.Detect_Faces(image)
            image = QtGui.QPixmap("image.png")
            self.label.setPixmap(image)
            os.remove("image.png")
        except Exception as e:print(e)

    def SelectVideo(self):
      path = QtWidgets.QFileDialog.getOpenFileName(self,"Select video",'')[0]
      VideoDetect.Detect_Faces(path)

app = QtWidgets.QApplication(sys.argv)   
exe = Main()
exe.show()
sys.exit(app.exec_())