# -*- coding: utf-8 -*-

"""
Module implementing ScanMainWindow.
"""

import os
import shutil
import win32api

from PyQt5.QtCore import pyqtSlot, QDateTime, QRect, Qt, QStringListModel
from PyQt5.QtGui import QPainter, QIcon, QFont
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QDesktopWidget

from DB import AnswerDB
from Ui_PicMainWindow import Ui_MainWindow
from configWindow import configDialog


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
        self.setWindowIcon(QIcon("icons\scan.ico"))
        self.line.setFixedHeight(QDesktopWidget().screenGeometry().height())
        self.line_4.setGeometry(QDesktopWidget().screenGeometry().width() - self.line.geometry().x(), 0, 21,
                                QDesktopWidget().screenGeometry().height())
        self.line_5.setGeometry(self.line.geometry().x() + 10, 800,
                                self.line_4.geometry().x() - self.line.geometry().x(), 21)
        self.label_7.move(QDesktopWidget().screenGeometry().width() - self.line.geometry().x() + 30, 20)
        self.label_8.move(self.line.geometry().x() + 10, 810)
        self.scrollArea.setGeometry(QRect(self.line.geometry().x()+15, 840, self.line_4.geometry().x()-self.line.geometry().x()-10, 100))
        self.scrollArea.setWidget(self.label_4)
        self.label_4.setWordWrap(True)  # 自动换行
        self.label_4.setAlignment(Qt.AlignTop)
        self.setupAction.triggered.connect(self.openConfigDialog)
        # 初始化时间控件
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        # 刷新班级控件
        self.updateComboBox()
        #设置listview位置
        self.listView.setGeometry(QDesktopWidget().screenGeometry().width() - self.line.geometry().x()+30, 60, self.line.geometry().x()-50,QDesktopWidget().screenGeometry().height()-200)
        # 显示窗体
        self.showMaximized()

    def openConfigDialog(self):
        dialog = configDialog(self.dto)
        dialog.exec_()
        return

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        try:
            painter = QPainter(self)
            self.drawImg(painter, 350, 65, 400, 350, 20)  # 显示图像
            self.drawScore(painter, QDesktopWidget().screenGeometry().width() - self.line.geometry().x() + 20,
                           110)  # 显示姓名分数
            self.showFailedfiles()
            # if self.dto.testFlag:
            self.showAnswers()
        except Exception as e:
            QMessageBox.information(None, '提示', '显示图像失败！错误是：' + str(e))

    def showFailedfiles(self):
        if len(self.dto.failedFiles) != 0:
            filenames = []
            for file in self.dto.failedFiles:
                filename = os.path.basename(file)
                filenames.append(filename)
            self.label_4.clear()
            self.label_4.setText('失败文件名：'+str(filenames))

    def showAnswers(self):
        if self.dto.nowAnswer!=None and self.dto.hideAnswerFlag==0:
            self.label_4.clear()
            self.label_4.setText('导入的答案为（题号：答案+得分+部分得分）：'+str(self.dto.nowAnswer))

    def drawImg(self, painter, x, y, w, h, padding):  # 显示图片
        if self.dto.nowPaper.showingImg is not None:
            painter.drawText(x, y, '原图：')
            painter.drawImage(QRect(x, y + 10, w, h), self.dto.nowPaper.showingImg)
        if self.dto.nowPaper.showingChoices is not None:
            if self.dto.nowPaper.multiChoiceCount > 0:
                painter.setFont(QFont('Mine', 14))
                painter.setPen(Qt.red)
                painter.drawText(x + w + padding, y, '请注意：有' + str(self.dto.nowPaper.multiChoiceCount) + '个多选！')
                painter.setPen(Qt.black)
                painter.setFont(QFont('Mine', 9))
            else:
                painter.drawText(x + w + padding, y, '所涂选项:')
            painter.drawImage(QRect(x + w + padding, y + 10, w, h), self.dto.nowPaper.showingChoices)
        if self.dto.nowPaper.showingStu is not None:
            if self.dto.nowPaper.stuID !='':
                painter.drawText(x + (w + padding) * 2, y, '所涂学号：')
            else:
                painter.setFont(QFont('Mine', 14))
                painter.setPen(Qt.red)
                painter.drawText(x + (w + padding) * 2, y, '无法识别学号！')
                painter.setPen(Qt.black)
                painter.setFont(QFont('Mine', 9))
            painter.drawImage(QRect(x + (w + padding) * 2, y + 10, w / 2, h), self.dto.nowPaper.showingStu)
        if self.dto.nowPaper.showingWrong is not None and self.dto.nowPaper.noChoiceCount != 0:
            painter.setFont(QFont('Mine', 14))
            painter.setPen(Qt.red)
            painter.drawText(x, y + h + padding * 3, '未作答题目有' + str(self.dto.nowPaper.noChoiceCount) + '个！')
            painter.drawImage(QRect(x, y + h + padding * 3 + 10, w, h), self.dto.nowPaper.showingWrong)
            painter.setPen(Qt.black)
            painter.setFont(QFont('Mine', 9))
        if self.dto.testFlag:
            if self.dto.nowPaper.showingImgThresh is not None:
                painter.drawText(x + w + padding, y + h + padding * 3, '原图二值化：')
                painter.drawImage(QRect(x + w + padding, y + h + padding * 3 + 10, w, h),
                                  self.dto.nowPaper.showingImgThresh)
            if self.dto.nowPaper.showingPaperThresh is not None:
                painter.drawText(x + (w + padding) * 2, y + h + padding * 3, '答题区二值化：')
                painter.drawImage(QRect(x + (w + padding) * 2, y + h + padding * 3 + 10, w, h),
                                  self.dto.nowPaper.showingPaperThresh)

    def drawScore(self, painter, startX, startY):
        if not self.examControl.markingResultView:
            return
        score=[]
        tmp = ''
        for j, result in enumerate(self.examControl.markingResultView):
            if result[2] == 0 or (result[2][4] <0 and result[2][4]>-4):
                tmp = '第' + str(result[0]) + '个失败！'
            elif result[2][4]==-5:
                tmp = '第' + str(result[0]) + '个：学号：' + str(result[2][0]) + ' 分数：' + str(result[2][2]) + '不覆盖！'
            elif result[2][4] == -4:
                tmp = '第' + str(result[0]) + '个：学号：' + str(result[2][0]) + ' 分数：' + str(result[2][2]) + '覆盖！'
            else:
                tmp = '第' + str(result[0]) + '个：学号：' + str(result[2][0]) + ' 分数：' + str(result[2][2]) + ' 成功！'
            score.append(tmp)
            # painter.drawText(startX + 5, startY + 20 * j, tmp)
            slm=QStringListModel()
            slm.setStringList(score)
            self.listView.setModel(slm)
    # 刷新班级控件
    def updateComboBox(self):
        self.comboBox_2.clear()
        if self.dto.allClassname is not None:
            for i in self.dto.allClassname:
                for j in i:
                    self.comboBox_2.addItem(j)

    def getID(self):
        self.dto.examID = self.dateEdit.date().toString("yyyyMMdd")
        self.dto.classname = self.comboBox_2.currentText()


    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        # 獲取班級和examID
        self.getID()
        if not self.dto.classname:
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
        self.dto.hideAnswerFlag = 1
        self.examControl.startMarking(files)


    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        # 獲取班級和examID
        self.getID()
        if not self.dto.classname:
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
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext != '.jpg' and ext != '.png' and ext != '.bmp' and ext != '.jpeg':
                continue
            files.append(os.path.join(direc + '/', filename))
        # 开始阅卷
        self.dto.hideAnswerFlag = 1
        self.examControl.startMarking(files)

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
            self.dto.testFlag = False
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
            self.dto.STAND_ONE_ANSWER_ORDER=[]#计算并保存标准答案长度为1的题号
            for i in range(len(self.dto.nowAnswer)):
                ans = self.dto.nowAnswer[i + 1][0]
                if len(ans)==1:
                    self.dto.STAND_ONE_ANSWER_ORDER.append(i+1)
            QMessageBox.information(None, '提示:', '共导入' + str(len(answers)) + '个题答案！')
            self.dto.hideAnswerFlag = 0
            self.dto.nowPaper.initPaper()
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
            if not self.dto.classname:
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
            i=self.examControl.stuDB.importStuFromXLS(file)
            if i:
                self.examControl.updateClassname()
                self.updateComboBox()
                QMessageBox.information(None, '消息', '共导入'+str(i)+'个学生！')
        except Exception as e:
            QMessageBox.information(None, '提示', '导入失败！错误是：' + str(e) + '，请选择正确的学生库文件！')

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
        self.dto.nowAnswer=None
        self.dto.testFlag = True
        self.dto.testFile = file
        self.dto.answerThreshhold = self.doubleSpinBox.value()
        self.examControl.test(file)
        self.update()

    @pyqtSlot(float)
    def on_doubleSpinBox_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type float
        """
        self.dto.answerThreshhold = self.doubleSpinBox.value()
        if self.dto.testFlag:
            self.dto.nowAnswer = None
            self.examControl.test(self.dto.testFile)
        self.update()
    
    @pyqtSlot()
    def on_pushButton_saveas_clicked(self):
        """
        Slot documentation goes here.
        """
        # 獲取班級和examID
        self.getID()
        if not self.examControl.markingResultView:
            QMessageBox.information(None, '错误', "尚未阅卷！")
            return
        self.examControl.makeSaveAsReport()