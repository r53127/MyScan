# -*- coding: utf-8 -*-

"""
Module implementing ScanWindow.
"""
import cv2

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QTabWidget, QFileDialog

from Ui_ScanWindow import Ui_TabWidget


class ScanWindow(QTabWidget, Ui_TabWidget):
    """
    Class documentation goes here.
    """
    def __init__(self, dto,examControl):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ScanWindow, self).__init__()
        self.dto=dto
        self.examControl=examControl
        self.files=[]
        self.setupUi(self)
        self.show()
    

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            files,filetype=QFileDialog.getOpenFileNames(self,'打开文件',r'.',r'图片文件 (*.jpg;*.png;*.bmp)')
            if not files:
                return
            for file in files:
                self.dto.setCurrentPaper(file)
                self.examControl.startMarking()
        except BaseException as e:
            print(e)
            
            
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        direc = QFileDialog.getExistingDirectory(self, '打开阅卷目录', r'.')
        if not dir:
            return
        self.direc=direc
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        try:
            if not self.dto.currentPaper:
                return
            if self.dto.currentPaper.img is not None:
                self.showImg(self.dto.currentPaper.img)
        except BaseException as e:
            print(e)

    def showImg(self,img):
        height, width, bytesPerComponent = img.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        # 转为QImage对象
        showimage = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.label_2.setGeometry(100, 30, 400, 380)
        # self.label_2.setScaledContents(True)
        self.label_2.setPixmap(QPixmap.fromImage(showimage).scaled(self.label_2.width(), self.label_2.height()))



    



