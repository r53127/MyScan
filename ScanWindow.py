# -*- coding: utf-8 -*-

"""
Module implementing ScanWindow.
"""
import win32api

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTabWidget, QFileDialog, QMessageBox

from DB import AnswerDB
from Ui_ScanWindow import Ui_TabWidget


class ScanWindow(QTabWidget, Ui_TabWidget):
    """
    Class documentation goes here.
    """

    def __init__(self, dto, examControl):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(ScanWindow, self).__init__()
        self.dto = dto
        self.examControl = examControl
        self.files = []
        self.setupUi(self)
        self.show()

    @pyqtSlot()
    def on_pushButton_1_clicked(self):
        """
        Slot documentation goes here.
        """
        win32api.ShellExecute(0, 'open', 'data\答案.xlsx', '', '', 1)

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        try:
            file, filetype = QFileDialog.getOpenFileName(self, '导入答案文件', r'.\data', r'EXCEL文件 (*.xlsx)')
            if not file:
                return
            else:
                self.dto.nowAnswerFile = file
                # 读取答案
                self.dto.nowAnswer = AnswerDB.importAnswer(file)
                QMessageBox.information(None, '请核对导入的答案：', str(self.dto.nowAnswer))
        except BaseException as e:
            print(e)

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            files, filetype = QFileDialog.getOpenFileNames(self, '打开文件', r'.', r'图片文件 (*.jpg;*.png;*.bmp)')
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
        self.direc = direc

    # def paintEvent(self, QPaintEvent):
    #     super().paintEvent(QPaintEvent)
    #     try:
    #         if not self.dto.nowPaper:
    #             return
    #         if self.dto.nowPaper.showingImg is not None:
    #             self.showImg(self.dto.nowPaper.showingImg)
    #     except BaseException as e:
    #         print(e)

    # def showImg(self, img):
    #     height, width, bytesPerComponent = img.shape
    #     bytesPerLine = bytesPerComponent * width
    #     # 变换彩色空间顺序
    #     cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
    #     # 转为QImage对象
    #     showimage = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
    #     self.label_2.setGeometry(100, 30, 400, 380)
    #     self.label_2.setAlignment(Qt.AlignCenter)
    #     # self.label_2.setScaledContents(True)
    #     self.label_2.setPixmap(QPixmap.fromImage(showimage).scaled(self.label_2.width(), self.label_2.height()))
