# -*- coding: utf-8 -*-

import sys
import cv2
from PIL import Image
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.uic import loadUi

face = cv2.CascadeClassifier('face.xml')
eye = cv2.CascadeClassifier('eye.xml')
smile = cv2.CascadeClassifier('smile.xml')
overlay = 'overlay.png'

class Main(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        loadUi('gui.ui',self)

        self.image = None
        self.select_image.clicked.connect(self.selectImage)
        self.start.clicked.connect(self.start_cam)
        self.stop.clicked.connect(self.stop_cam)
        self.detect.toggled.connect(self.switch_detect)
        self.detect_enabled = True
        self.capture = cv2.VideoCapture(0)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)

    def selectImage(self):
        try:
            self.stop_cam()
            path,fil = QtWidgets.QFileDialog.getOpenFileName(self,
                                                        "Select image",'')
            image = cv2.imread(path)
            image = self.detect_face(image)
            self.displayImage(image)
        except Exception as e:print(e)

    def switch_detect(self, status):
        if status:
            self.detect.setText("Draw rectangles")
            self.detect_enabled = False
        else:
            self.detect.setText("Draw img above")
            self.detect_enabled = True

    def start_cam(self):
        try:
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.timer.start(5)
        except Exception as e:print(e)

    def update(self):
        try:
            ret, self.image = self.capture.read()
            detected_image = self.detect_face(self.image)
            self.displayImage(detected_image)    
        except Exception as e:print(e)

    def detect_face(self,img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #gray = cv2.GaussianBlur(gray,(5,5),1)

            # Detect faces
            faces = face.detectMultiScale(gray, 1.3,5, minSize = (30,30))

            # Draw face rectangles
            if self.detect_enabled:
                for (x,y,w,h) in faces:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
                    _gray = gray[y:y+h, x:x+w]
                    _img = img[y:y+h, x:x+w]

                    #Detect smiles
                    smiles = smile.detectMultiScale(_gray, 1.5, 25,
                                                         minSize=(25, 25))
                    #Draw smiles
                    for (x, y, w, h) in smiles:
                        cv2.rectangle(
                          _img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    #Detect eyes
                    eyes = eye.detectMultiScale(_gray, 1.5, 15,
                                                 minSize=(5, 5))
                    for (x,y,w,h) in eyes:
                        cv2.rectangle(_img, (x, y), (x + w, y + h), 
                                        (0, 0, 255), 2)
            #Convert image into QImage
            qformat = QtGui.QImage.Format_RGB888
            outImage = QtGui.QImage(img,img.shape[1], img.shape[0],
                                    img.strides[0] , qformat)
            outImage = outImage.rgbSwapped()

            #Draw overlay
            if not self.detect_enabled:
                for (x,y,w,h) in faces:
                    paint = QtGui.QPainter(outImage)
                    image = QtGui.QPixmap(overlay)
                    image = image.scaled(w, h)
                    paint.drawPixmap(x, y, image)

            return outImage
        except Exception as e: print(e)

    def stop_cam(self):
        self.timer.stop()

    def displayImage(self, outImage):
        try:
            self.display.setPixmap(QtGui.QPixmap.fromImage(outImage))
            self.display.setScaledContents(True)
        except Exception as e:print(e)

app = QtWidgets.QApplication(sys.argv)   
exe = Main()
exe.show()
sys.exit(app.exec_())