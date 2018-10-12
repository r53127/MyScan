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
        self.markingResultView=[]
        self.dto = dto
        self.examControl = examControl
        self.setupUi(self)
        self.setWindowIcon(QIcon("scan.ico"))
        self.line.setFixedHeight(QDesktopWidget().screenGeometry().height())
        self.line_4.setGeometry(QDesktopWidget().screenGeometry().width()-self.line.geometry().x(), 0, 21, QDesktopWidget().screenGeometry().height())


        # 设置错误消息label_4的字体
        errorFont = QFont()
        errorFont.setBold(True)
        errorFont.setPointSize(20)
        errorPal = QPalette()
        errorPal.setColor(QPalette.WindowText, Qt.red)
        self.label_4.setFont(errorFont)
        self.label_4.setPalette(errorPal)
        self.label_4.move(350,860)
        self.label_7.setFont(errorFont)
        self.label_7.setPalette(errorPal)
        self.label_7.move(QDesktopWidget().screenGeometry().width()-self.line.geometry().x()+50,20)

        # 初始化时间控件
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        # 刷新班级控件
        self.updateComboBox()
        # 显示窗体
        self.showMaximized()


    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        try:
            painter = QPainter(self)
            self.drawImg( painter, 350,20,400,350,20)#显示图像
            self.drawScore(painter, QDesktopWidget().screenGeometry().width()-self.line.geometry().x()+10, 100)  # 显示姓名分数
            self.label_4.setText(self.dto.errorMsg)
            self.label_4.adjustSize()
        except Exception as e:
            QMessageBox.information(None, '提示', '显示图像失败！错误是：' + str(e))

    def drawImg(self, painter, x, y,w, h, padding):#显示图片
        if self.dto.nowPaper.showingImg is not None:
            painter.drawImage(QRect(x, y, w, h), self.dto.nowPaper.showingImg)
        if self.dto.nowPaper.showingPaper is not None:
            painter.drawImage(QRect(x + w + padding, y, w, h), self.dto.nowPaper.showingPaper)
        if self.dto.nowPaper.showingPaperCnts is not None:
            painter.drawImage(QRect(x + (w + padding) * 2, y, w, h), self.dto.nowPaper.showingPaperCnts)
        if self.dto.nowPaper.showingThresh is not None:
            painter.drawImage(QRect(x, y + h + padding, w, h), self.dto.nowPaper.showingThresh)
        if self.dto.nowPaper.showingWrong is not None:
            painter.drawImage(QRect(x + w + padding, y + h + padding, w, h), self.dto.nowPaper.showingWrong)
        if self.dto.nowPaper.showingStu is not None:
            painter.drawImage(QRect(x + (w + padding) * 2, y + h + padding, w / 2, h), self.dto.nowPaper.showingStu)

    def drawScore(self,painter,startX,startY):
        if not self.markingResultView:
            return
        tmp=''
        for j,result in enumerate(self.markingResultView):
            i=int((startY+20*j)/(QDesktopWidget().screenGeometry().height() - 50))#换列
            tmp='学号：'+str(result[0])+' 分数：'+str(result[1])
            painter.drawText(startX+140*i+5,startY+20*j,tmp)

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
        self.dto.answerThreshhold=self.doubleSpinBox.value()


    def startScan(self, files):
        self.dto.testFlag = False
        failedCount = 0
        successedCount=0
        self.markingResultView=[]#本次所有阅卷结果
        for i,file in enumerate(files,start=1):
            try:
                # 初始化一张试卷
                self.dto.nowPaper.initPaper()
                self.update()
                markingResult = self.examControl.markingControl(file)
                if not markingResult:
                    failedCount += 1
                    self.dto.failedFiles.append(file)
                else:
                    self.markingResultView.append(markingResult)
                    successedCount+=1
                    self.update()
            except Exception as e:
                failedCount += 1
                self.dto.failedFiles.append(file)
                logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
                logging.debug(traceback.format_exc())
                # traceback.print_exc()
                QMessageBox.information(None, '提示', '此图片阅卷失败！错误是：' + str(e))
                continue
        self.statusBar().showMessage('已全部结束！本次共阅'+str(len(files))+'份，成功'+str(successedCount)+'份，失败'+str(failedCount) + '份！')


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
        self.dto.answerThreshhold=self.doubleSpinBox.value()
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
