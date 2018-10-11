# -*- coding: utf-8 -*-

"""
Module implementing ScanMainWindow.
"""

import logging
import os
import shutil
import traceback
import win32api

from PyQt5.QtCore import pyqtSlot, Qt, QDateTime, QRect
from PyQt5.QtGui import QPainter, QPalette, QFont, QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QDesktopWidget

from DB import AnswerDB
from Ui_PicMainWindow import Ui_MainWindow


class PicMainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, dto, examControl, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(PicMainWindow, self).__init__(parent)
        self.dto = dto
        self.examControl = examControl
        self.setupUi(self)
        self.setWindowIcon(QIcon("scan.ico"))
        self.line.setFixedHeight(QDesktopWidget().screenGeometry().height())

        # 设置错误消息label_4的字体
        errorFont = QFont()
        errorFont.setBold(True)
        errorFont.setPointSize(14)
        errorPal = QPalette()
        errorPal.setColor(QPalette.WindowText, Qt.red)
        self.label_4.setFont(errorFont)
        self.label_4.setPalette(errorPal)
        self.label_4.move(350,860)
        #设置学号和分数label字体
        IDFont = QFont("华文楷体")
        IDFont.setBold(True)
        IDFont.setPointSize(25)
        IDPal = QPalette()
        IDPal.setColor(QPalette.WindowText, Qt.red)
        self.stuID_label.setFont(IDFont)
        self.score_label.setFont(IDFont)
        self.stuID_label.setPalette(IDPal)
        self.score_label.setPalette(IDPal)

        # 初始化时间控件
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        # 刷新班级控件
        self.updateComboBox()
        # 显示窗体
        self.showMaximized()


    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        try:
            x,y,w,h,padding=350,20,450,400,20
            painter = QPainter(self)
            self.label_4.setText(self.dto.errorMsg)
            self.label_4.adjustSize()
            if self.dto.nowPaper.stuID:
                self.stuID_label.setText('学号：'+self.dto.nowPaper.stuID)
                self.stuID_label.adjustSize()
            else:
                self.stuID_label.setText('')
            if self.dto.nowPaper.score:
                self.score_label.setText('分数：'+str(self.dto.nowPaper.score))
                self.score_label.adjustSize()
            else:
                self.score_label.setText('')
            if (self.dto.nowPaper is not None) and (self.dto.nowPaper.showingImg is not None):
                painter.drawImage(QRect(x, y,w, h),self.dto.nowPaper.showingImg)
            if self.dto.nowPaper.showingPaper is not None:
                painter.drawImage(QRect(x+w+padding, y, w, h), self.dto.nowPaper.showingPaper)
            if self.dto.nowPaper.showingPaperCnts is not None:
                painter.drawImage(QRect(x+(w+padding)*2, y, w, h), self.dto.nowPaper.showingPaperCnts)
            if self.dto.nowPaper.showingThresh is not None:
                painter.drawImage(QRect(x, y+h+padding, w, h), self.dto.nowPaper.showingThresh)
            if self.dto.nowPaper.showingWrong is not None:
                painter.drawImage(QRect(x+w+padding, y+h+padding, w, h), self.dto.nowPaper.showingWrong)
            if self.dto.nowPaper.showingStu is not None:
                painter.drawImage(QRect(x+(w+padding)*2, y+h+padding, w/2, h), self.dto.nowPaper.showingStu)
        except Exception as e:
            QMessageBox.information(None, '提示', '显示图像失败！错误是：' + str(e))


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
        self.dto.testFlag = False
        failedCount = 0
        for i,file in enumerate(files,start=1):
            try:
                # 初始化一张试卷
                self.dto.nowPaper.initPaper()
                self.update()
                markingFlag = self.examControl.markingControl(file)
                if markingFlag==0:
                    failedCount += 1
                    self.dto.failedFiles.append(file)
                if i<len(files):
                    reply = QMessageBox.question(self, "提示",
                                                 "是否继续下一个？",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if reply != 16384:
                        break
            except Exception as e:
                failedCount += 1
                self.dto.failedFiles.append(file)
                logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
                logging.debug(traceback.format_exc())
                traceback.print_exc()
                QMessageBox.information(None, '提示', '此图片阅卷失败！错误是：' + str(e))
                continue
        else:
            if failedCount != 0:
                QMessageBox.information(None, "提示", "本次共有" + str(failedCount) + '张图片阅卷失败！')
            self.statusBar().showMessage('已全部结束！')


    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        # 獲取班級和examID
        self.getID()
        if not self.dto.classID:
            QMessageBox.information(None, '提示', '请先导入学生库生成班级!')
            return
        # 未导入答案，返回
        if not self.dto.nowAnswer:
            QMessageBox.information(None, '提示', '请先导入答案!')
            return
        files, filetype = QFileDialog.getOpenFileNames(self, '打开文件', r'.', r'图片文件 (*.jpg;*.png;*.bmp;*.jpeg)')
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
            ext=os.path.splitext(filename)[1]
            ext=ext.lower()
            if ext!='.jpg' and ext!='.png' and ext!='.bmp' and ext!='.jpeg':
                continue
            files.append(os.path.join(direc + '/', filename))
        # 开始阅卷
        self.startScan(files)

    @pyqtSlot()
    def on_pushButton_1_clicked(self):
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
            self.dto.testFlag=False
            file, filetype = QFileDialog.getOpenFileName(self, '导入答案文件', r'.\data', r'EXCEL文件 (*.xlsx)')
            # 如果未选择，返回
            if not file:
                return
            # 读取答案
            answers = AnswerDB.importAnswerFromXLS(file)
            # 如果答案为空，返回
            if answers is None:
                return
            self.dto.nowAnswer = answers
            QMessageBox.information(None, '提示:', '共导入'+str(len(answers))+'个题答案！')
        except BaseException as e:
            QMessageBox.information(None, '错误:', "错误是：" + str(e) + "，请导入有效的答案文件！")


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
        except Exception as e:
            QMessageBox.information(None, '提示', '错误是：' + str(e))


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
        try:
            if self.examControl.stuDB.importStuFromXLS(file):
                self.examControl.updateClassID()
                self.updateComboBox()
                QMessageBox.information(None, '消息', '结束！')
        except Exception as e:
            QMessageBox.information(None, '提示', '导入失败！错误是：' + str(e)+'，请选择正确的学生库文件！')

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
        self.dto.testFlag=True
        self.dto.testFile=file
        # 初始化一张试卷
        self.dto.nowPaper.initPaper()
        self.update()
        self.examControl.test(file)
    
    @pyqtSlot(float)
    def on_doubleSpinBox_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type float
        """
        self.dto.answerThreshhold=p0
        if self.dto.testFlag:
            self.examControl.test(self.dto.testFile)
        self.update()
