# -*- coding: utf-8 -*-

import sys
import cv2
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.uic import loadUi

face = cv2.CascadeClassifier('face.xml')
eye = cv2.CascadeClassifier('eye.xml')
smile = cv2.CascadeClassifier('smile.xml')

class Main(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        loadUi('gui.ui',self)

        self.image = None
        self.select_image.clicked.connect(self.selectImage)
        self.start.clicked.connect(self.start_cam)
        self.stop.clicked.connect(self.stop_cam)
        self.detect.toggled.connect(self.switch_detect_face)
        self.face_Enabled = False
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
            self.displayImage(image,1)
        except Exception as e:print(e)

    def switch_detect_face(self, status):
        if status:
            self.detect.setText("Stop detect")
            self.face_Enabled = True
        else:
            self.detect.setText("Detect")
            self.face_Enabled = False

    def start_cam(self):
        try:
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
            self.timer.start(5)
        except Exception as e:print(e)

    def update(self):
        try:
            ret, self.image = self.capture.read()

            if self.face_Enabled:
                detected_image = self.detect_face(self.image)
                self.displayImage(detected_image,1)
            else: self.displayImage(self.image,1)    

        except Exception as e:print(e)

    def detect_face(self,img):
        try:
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(5,5),1)

            faces = face.detectMultiScale(gray,1.3,5,minSize = (25,25))
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                _gray = gray[y:y+h, x:x+w]
                _img = img[y:y+h, x:x+w]
                
                smiles = smile.detectMultiScale(_gray, 1.5, 15,
                                                     minSize=(25, 25),)
                
                for (x, y, w, h) in smiles:
                    cv2.rectangle(
                      _img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                eyes = eye.detectMultiScale(_gray, 1.5, 10,
                                                 minSize=(5, 5))
                       
                for (x,y,w,h) in eyes:
                    cv2.rectangle(_img, (x, y), (x + w, y + h), 
                                 (0, 0, 255), 2)
            return img
        except Exception as e: print(e)

    def stop_cam(self):
        self.timer.stop()

    def displayImage(self, img,window = 1):
        qformat = QtGui.QImage.Format_RGB888

        outImage = QtGui.QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.display.setPixmap(QtGui.QPixmap.fromImage(outImage))
            self.display.setScaledContents(True)

app = QtWidgets.QApplication(sys.argv)   
exe = Main()
exe.show()
sys.exit(app.exec_())