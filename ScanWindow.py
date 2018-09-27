# -*- coding: utf-8 -*-

"""
Module implementing ScanWindow.
"""
import os
import shutil
import traceback
import win32api

from PyQt5.QtCore import pyqtSlot, QRect
from PyQt5.QtGui import QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QTabWidget, QFileDialog, QMessageBox, QGraphicsScene, QGraphicsItem

from DB import AnswerDB
from Ui_ScanWindow import Ui_TabWidget

import cv2 as cv

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
        self.scene=QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.show()

    def startScan(self, files):
        for file in files:
            try:
                self.dto.setCurrentPaper(file)
                self.examControl.startMarking()
            except Exception as e:
                reply = QMessageBox.question(None, "提示",
                                             "该卡无法识别，错误是" + str(e) + "，文件名是：" + file + "，是否继续？",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                self.dto.failedFiles.append(file)
                if reply == 16384:
                    continue
                else:
                    break

    @pyqtSlot()
    def on_pushButton_1_clicked(self):
        """
        Slot documentation goes here.
        """
        answerfile='data\答案.xlsx'
        if not os.path.exists(answerfile):
            QMessageBox.information(None, '错误:', "答案文件不存在！")
            return
        try:
            win32api.ShellExecute(0, 'open', answerfile, '', '', 1)
        except Exception as e:
            QMessageBox.information(None, '错误:', "错误是：" + str(e) + "！")

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        try:
            file, filetype = QFileDialog.getOpenFileName(self, '导入答案文件', r'.\data', r'EXCEL文件 (*.xlsx)')
            # 如果未选择，返回
            if not file:
                return
            # 读取答案
            answers = AnswerDB.importAnswerFromXLS(file)
            # 如果答案为空，返回
            if answers is None:
                return
            self.dto.nowAnswerFile = file
            self.dto.nowAnswer=answers
            # 答案校对
            ansinfo = ''
            for answer in self.dto.nowAnswer.items():
                ansinfo += '题号:' + str(answer[0]) + ' 答案为：' + str(answer[1][0]) + " 分值为：" + str(answer[1][1]) + "\n"
            QMessageBox.information(None, '请核对答案分值:', ansinfo)
        except BaseException as e:
            QMessageBox.information(None, '错误:', "错误是：" + str(e) + "，请导入有效的答案文件！")

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # 未导入答案，返回
        if not self.dto.nowAnswer:
            QMessageBox.information(None, '提示', '请先导入答案!')
            return
        files, filetype = QFileDialog.getOpenFileNames(self, '打开文件', r'.', r'图片文件 (*.jpg;*.png;*.bmp)')
        # 如果未选择，返回
        if not files:
            return
        # 开始阅卷
        self.startScan(files)

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        # 未导入答案，返回
        if not self.dto.nowAnswer:
            QMessageBox.information(None, '提示', '请先导入答案!')
            return
        direc = QFileDialog.getExistingDirectory(self, '打开阅卷目录', r'.')
        if not direc:
            return
        # 生成文件列表
        files = []
        filesname = os.listdir(direc)
        for filename in filesname:
            files.append(os.path.join(direc + '/', filename))
        # 开始阅卷
        self.startScan(files)



    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        try:
            if not self.dto.nowPaper:
                return
            if self.dto.nowPaper.showingImg is not None:
                pic=ScanWindow.convertImg(self.dto.nowPaper.showingImg)
                painter=QPainter()
                painter.drawImage(50,50,pic)

                # view_size=self.graphicsView.size()
                # pic_size=pic.size()
                # print(view_size,pic_size)
                # ratio=(view_size.height()*view_size.width())/(pic_size.height()*pic_size.width())
                # pic.scaled(view_size,1)
                # self.graphicsItem=self.scene.addPixmap(pic)
                # self.graphicsItem.setFlag(QGraphicsItem.ItemIsMovable)


        except:
            traceback.print_exc()

    @staticmethod
    def convertImg(img):
        height, width, bytesPerComponent = img.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cv.cvtColor(img, cv.COLOR_BGR2RGB, img)
        # 转为QImage对象
        showimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        showpix = QPixmap.fromImage(showimg)
        return showimg


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
            self.saveFailedFiles(file, direc)

    def saveFailedFiles(self, file, dstPath):
        try:
            newfilepath = os.path.join(dstPath, os.path.basename(file))
            shutil.copyfile(file, newfilepath)
        except Exception as e:
            QMessageBox.information(None, '提示', '另存失败！错误是：' + str(e))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        file, filetype = QFileDialog.getOpenFileName(self, '导入学生库', r'.\data', r'EXCEL文件 (*.xlsx)')
        # 如果未选择，返回
        if not file:
            return
        if self.examControl.stu_data.importStuFromXLS(file):
            QMessageBox.information(None, '消息', '结束！')
    
    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        """
        Slot documentation goes here.
        """
        stufile=r'data\学生库.xlsx'
        if not os.path.exists(stufile):
            QMessageBox.information(None, '错误', "学生库不存在！")
            return
        try:
            win32api.ShellExecute(0, 'open', stufile, '', '', 1)
        except Exception as e:
            QMessageBox.information(None, '错误:', "错误是：" + str(e) + "！")
    
    @pyqtSlot()
    def on_pushButton_9_clicked(self):
        """
        Slot documentation goes here.
        """
        file, filetype = QFileDialog.getOpenFileName(self, '打开文件', r'.', r'图片文件 (*.jpg;*.png;*.bmp)')
        # 如果未选择，返回
        if not file:
            return
        # 开始阅卷
        self.examControl.test(file)
