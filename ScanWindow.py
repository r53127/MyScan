# -*- coding: utf-8 -*-

"""
Module implementing ScanWindow.
"""
import os
import shutil
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
            #如果未选择，返回
            if not file:
                return
            # 读取答案
            self.dto.nowAnswer = AnswerDB.importAnswer(file)
            #如果答案为空，返回
            if self.dto.nowAnswer is None:
                return
            self.dto.nowAnswerFile = file
            #答案校对
            ansinfo=''
            for answer in self.dto.nowAnswer.items():
                ansinfo+='题号:'+str(answer[0])+' 答案为：'+str(answer[1][0])+" 分值为："+str(answer[1][1])+"\n"
            QMessageBox.information(None, '请核对答案分值:', ansinfo)
        except BaseException as e:
            QMessageBox.information(None, '错误:', "错误是："+str(e)+"，请导入有效的答案文件！")

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        #未导入答案，返回
        if not self.dto.nowAnswer:
            QMessageBox.information(None,'提示','请先导入答案!')
            return
        files, filetype = QFileDialog.getOpenFileNames(self, '打开文件', r'.', r'图片文件 (*.jpg;*.png;*.bmp)')
        # 如果未选择，返回
        if not files:
            return
        #开始阅卷
        for file in files:
            try:
                self.dto.setCurrentPaper(file)
                self.examControl.startMarking()
            except Exception as e:
                reply = QMessageBox.question(None, "提示",
                                             "该卡无法识别，错误是"+str(e)+"，文件名是："+file+"，是否继续？",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == 16384:
                    self.dto.failedFiles.append(file)
                    continue
                else:
                    break


    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        #未导入答案，返回
        if not self.dto.nowAnswer:
            QMessageBox.information(None,'提示','请先导入答案!')
            return
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
    
    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        Slot documentation goes here.
        """
        pass
    
    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    
    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        """
        Slot documentation goes here.
        """
        if not self.dto.failedFiles:
            QMessageBox.information(None, '提示', '尚未有阅卷失败的文件！')
            return
        direc = QFileDialog.getExistingDirectory(self, '另存为目录', r'.')
        if not dir:
            return
        for file in self.dto.failedFiles:
            self.saveFailedFiles(file,direc)

    def saveFailedFiles(self,file,dstPath):
        try:
            newfilepath=os.path.join(dstPath,os.path.basename(file))
            shutil.copyfile(file, newfilepath)
        except Exception as e:
            QMessageBox.information(None, '提示', '另存失败！错误是：'+str(e))


