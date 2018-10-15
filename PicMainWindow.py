# -*- coding: utf-8 -*-

"""
Module implementing ScanMainWindow.
"""

import logging
import os
import shutil
import traceback
import win32api

from PyQt5.QtCore import pyqtSlot, QDateTime, QRect, Qt
from PyQt5.QtGui import QPainter, QIcon, QFont
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QDesktopWidget

from DB import AnswerDB
from ThreshWindow import ThreshWindow
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
        self.markingResultView = []
        self.dto = dto
        self.examControl = examControl
        self.setupUi(self)
        self.setWindowIcon(QIcon("scan.ico"))
        self.line.setFixedHeight(QDesktopWidget().screenGeometry().height())
        self.line_4.setGeometry(QDesktopWidget().screenGeometry().width() - self.line.geometry().x(), 0, 21,
                                QDesktopWidget().screenGeometry().height())
        self.line_5.setGeometry(self.line.geometry().x() + 10, 800,
                                self.line_4.geometry().x() - self.line.geometry().x(), 21)
        self.label_7.move(QDesktopWidget().screenGeometry().width() - self.line.geometry().x() + 30, 20)
        self.label_8.move(self.line.geometry().x() + 30, 820)
        self.label_4.setGeometry(QRect(self.line.geometry().x() + 50, 860, 1250, 138))
        self.label_4.setWordWrap(True)  # 自动换行
        self.label_4.setAlignment(Qt.AlignTop)

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
            self.drawImg(painter, 350, 20, 400, 350, 20)  # 显示图像
            self.drawScore(painter, QDesktopWidget().screenGeometry().width() - self.line.geometry().x() + 20,
                           70)  # 显示姓名分数
            self.showFailedfiles()
        except Exception as e:
            QMessageBox.information(None, '提示', '显示图像失败！错误是：' + str(e))

    def showFailedfiles(self):
        if len(self.dto.failedFiles) != 0:
            filenames = []
            for file in self.dto.failedFiles:
                filename = os.path.basename(file)
                filenames.append(filename)
            self.label_4.setText(str(filenames))

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
            painter.drawText(x + (w + padding) * 2, y, '所涂学号：')
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
        if not self.markingResultView:
            return
        tmp = ''
        for j, result in enumerate(self.markingResultView):
            if result[2] == 0 or result[2] == -1:
                tmp = '第' + str(result[0]) + '个失败！'
            else:
                tmp = '第' + str(result[0]) + '个：学号：' + str(result[2][0]) + ' 分数：' + str(result[2][2]) + ' 成功！'
            painter.drawText(startX + 5, startY + 20 * j, tmp)

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
        # print(self.dto.nowAnswer)

        STAND_ANSWER_LEN = []  # 算出所选每一个标准答案的长度
        for i in range(len(self.dto.nowAnswer)):
            ans = self.dto.nowAnswer[i + 1][0]
            STAND_ANSWER_LEN.append(len(ans))
        self.dto.testFlag = False  # 关闭测试开关
        self.dto.failedFiles = []  # 重置错误文件记录
        self.label_4.clear()  # 清除错误文件显示
        failedCount = 0  # 重置错误文件计数
        successedCount = 0  # 重置正确文件计数
        self.markingResultView = []  # 记录本次所有阅卷结果
        for i, file in enumerate(files, start=1):
            try:
                # 初始化一张试卷
                self.dto.nowPaper.initPaper()
                # 刷新显示
                self.update()
                # 根据界面全局参数初始化精确度阈值
                self.dto.answerThreshhold = self.doubleSpinBox.value()
                # s试探性阅卷
                self.markingResult = self.examControl.markingControl(file)
                if self.markingResult == 0:  # 如果无法识别图片，直接计入失败跳过调节阈值
                    failedCount += 1
                    self.dto.failedFiles.append(file)
                    QMessageBox.information(None, '提示', '找不到答题区，直接计入失败！')
                elif self.markingResult == -1:
                    QMessageBox.information(None, '提示', '请确认学号是否涂的有问题，可通过调节阈值重试，如果确实有问题，建议直接计入失败！')
                    failedCount, successedCount = self.confirmMarking(file, failedCount, successedCount)
                else:
                    retry_flag = 1  # 重试标识
                    for a in range(2, 10):  # 程序自行尝试调节阈值
                        self.dto.answerThreshhold = a / 10  # 获取阈值
                        self.dto.nowPaper.multiChoiceCount = 0  # 重置多选计数器
                        self.dto.nowPaper.noChoiceCount = 0  # 重置无选项计数器
                        self.markingResult = self.examControl.markingControl(file)  # 重新阅卷
                        choice_answer_len = []
                        for ans in self.markingResult[1]:  # 算出所选每一个所选答案的长度
                            choice_answer_len.append(len(ans[1]))
                        print(choice_answer_len,STAND_ANSWER_LEN)
                        if choice_answer_len == STAND_ANSWER_LEN:
                            successedCount += 1
                            retry_flag = 0
                            break
                    if retry_flag == 1:
                        # 如果程序调节失败，操作者自行调节阈值
                        failedCount, successedCount = self.confirmMarking(file, failedCount, successedCount)
                # 记录该文件阅卷结果
                self.markingResultView.append([i, file, self.markingResult])
                # QApplication.processEvents()
                # time.sleep(10)
            except Exception as e:
                failedCount += 1
                self.dto.failedFiles.append(file)
                logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
                logging.debug(traceback.format_exc())
                # traceback.print_exc()
                QMessageBox.information(None, '提示', '此图片阅卷失败！错误是：' + str(e))
                continue
        self.statusBar().showMessage(
            '已全部结束！本次共阅' + str(len(files)) + '份，成功' + str(successedCount) + '份，失败' + str(failedCount) + '份！')

    # 调节阈值窗口
    def confirmMarking(self, file, failedCount, successedCount):
        dialog = ThreshWindow(self.dto, file, self)
        result = dialog.exec_()
        if result:
            successedCount += 1
        else:
            failedCount += 1
            self.dto.failedFiles.append(file)
        return failedCount, successedCount

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
            ext = os.path.splitext(filename)[1]
            ext = ext.lower()
            if ext != '.jpg' and ext != '.png' and ext != '.bmp' and ext != '.jpeg':
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
            QMessageBox.information(None, '提示:', '共导入' + str(len(answers)) + '个题答案！')
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
            self.examControl.test(self.dto.testFile)
        self.update()
