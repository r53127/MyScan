# -*- coding: utf-8 -*-

"""
Module implementing ScanMainWindow.
"""

import logging
import os
import shutil
import traceback
import win32api
import cv2 as cv


from PyQt5.QtCore import pyqtSlot, Qt, QDateTime, QRect, QTimer
from PyQt5.QtGui import QPainter, QPalette, QFont, QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow

from DB import AnswerDB
from Ui_ScanMainWindow import Ui_MainWindow


class ScanMainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, dto, examControl, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ScanMainWindow, self).__init__(parent)
        self.dto = dto
        self.examControl = examControl
        #初始化攝像頭
        self.camera_init()
        self.timer_camera.timeout.connect(self.show_camera)

        self.setupUi(self)

        # 设置错误消息label_4的字体
        errorFont = QFont()
        errorFont.setBold(True)
        errorFont.setPointSize(14)
        errorPal = QPalette()
        errorPal.setColor(QPalette.WindowText, Qt.red)
        self.label_4.setFont(errorFont)
        self.label_4.setPalette(errorPal)
        # self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # 初始化时间控件
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        # 刷新班级控件
        self.updateComboBox()
        # 显示窗体
        self.showMaximized()
        self.timer_camera.start(30)

    def camera_init(self):
        self.timer_camera = QTimer()
        self.cap = cv.VideoCapture()
        self.CAM_NUM = 0
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            QMessageBox.warning(None, u"Warning", u"请检测相机与电脑是否连接正确", buttons=Qt.QMessageBox.Ok,
                                            defaultButton=Qt.QMessageBox.Ok)

    def show_camera(self):
        ret, camImg = self.cap.read()
        show = cv.resize(camImg, (280, 280))
        show = cv.cvtColor(show, cv.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.update()
        return  QPixmap.fromImage(showImage)

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        try:
            painter = QPainter(self)
            painter.drawPixmap(QRect(20, 20, 280, 280), self.show_camera())
            self.label_4.setText(self.dto.errorMsg)
            self.label_4.adjustSize()
            if not self.dto.nowPaper:
                return
            if self.dto.nowPaper.showingImg is not None:
                painter.drawPixmap(QRect(310, 20,450, 400),self.dto.nowPaper.showingImg)
                painter.drawPixmap(QRect(780, 20, 450, 400), self.dto.nowPaper.showingThresh)
                painter.drawPixmap(QRect(1250, 20, 450, 400), self.dto.nowPaper.showingWrong)

        except:
            traceback.print_exc()

    # 刷新班级控件
    def updateComboBox(self):
        self.comboBox_2.clear()
        if self.dto.allClassID is not None:
            for i in self.dto.allClassID:
                for j in i:
                    self.comboBox_2.addItem(j)


    def getID(self):
        self.dto.examID = self.dateEdit.date().toString("yyyyMMdd")
        self.dto.classID = self.comboBox_2.currentText()


    def startScan(self, files):
        failedCount = 0
        for file in files:
            try:
                self.dto.setCurrentPaper(file)
                markingFlag = self.examControl.startMarking()
                if markingFlag==0:
                    failedCount += 1
                    self.dto.failedFiles.append(file)
            except Exception as e:
                failedCount += 1
                self.dto.failedFiles.append(file)
                logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)
                logging.debug(traceback.format_exc())
                # traceback.print_exc()
                continue
        else:
            if failedCount != 0:
                QMessageBox.information(None, "提示", "共有" + str(failedCount) + '张图片阅卷失败！')
            else:
                QMessageBox.information(None, '提示', '已結束！')


    @pyqtSlot()
    def on_pushButton_1_clicked(self):
        """
        Slot documentation goes here.
        """
        answerfile = 'data\答案.xlsx'
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
            self.dto.nowAnswer = answers
            # 答案校对
            # ansinfo = ''
            # for answer in self.dto.nowAnswer.items():
            #     ansinfo += '题号:' + str(answer[0]) + ' 答案为：' + str(answer[1][0]) + " 分值为：" + str(answer[1][1]) + "\n"
            QMessageBox.information(None, '提示:', '成功导入！')
        except BaseException as e:
            QMessageBox.information(None, '错误:', "错误是：" + str(e) + "，请导入有效的答案文件！")


    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """

        # 獲取班級和examID
        self.getID()
        if not self.dto.classID:
            QMessageBox.information(None, '提示', '请先导入学生库生成班级!')
            return
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

        # 獲取班級和examID
        self.getID()
        if not self.dto.classID:
            QMessageBox.information(None, '提示', '请先导入学生库生成班级!')
            return
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


    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            # 獲取班級和examID
            self.getID()
            if not self.dto.classID:
                QMessageBox.information(None, '提示', '请先导入学生库生成班级!')
                return
            self.examControl.makeScoreReport()
        except:
            traceback.print_exc()


    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        """
        Slot documentation goes here.
        """
        # 獲取班級和examID
        self.getID()
        if not self.dto.nowAnswer:
            QMessageBox.information(None, '提示', '请先导入答案!')
            return
        self.examControl.makePaperReport()


    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        """
        Slot documentation goes here.
        """
        if not self.dto.failedFiles:
            QMessageBox.information(None, '提示', '尚未有阅卷失败的文件！')
            return
        direc = QFileDialog.getExistingDirectory(self, '另存为目录', r'.')
        if not direc:
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
        if self.examControl.stuDB.importStuFromXLS(file):
            try:
                self.examControl.updateClassID()
                self.updateComboBox()
            except:
                traceback.print_exc()

            QMessageBox.information(None, '消息', '结束！')


    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        """
        Slot documentation goes here.
        """
        stufile = r'data\学生库.xlsx'
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
