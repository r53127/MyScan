# -*- coding: utf-8 -*-

"""
Module implementing ScanMainWindow.
"""
import os
import threading
import traceback
import win32api

import cv2 as cv
import numpy as np
from CamconfigWindow import configDialog
from DB import AnswerDB
from PyQt5.QtCore import pyqtSlot, QDateTime, QRect, Qt, QStringListModel, QTimer
from PyQt5.QtGui import QPainter, QIcon, QFont, QImage
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QDesktopWidget, QApplication
from Ui_CamMainWindow import Ui_MainWindow
from imutils.perspective import four_point_transform


class CamMainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, dto, examControl, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(CamMainWindow, self).__init__(parent)
        self.dto = dto
        self.examControl = examControl
        self.setupUi(self)
        self.setWindowIcon(QIcon("icons\scan.ico"))
        self.line.setFixedHeight(QDesktopWidget().screenGeometry().height())
        self.line_4.setGeometry(QDesktopWidget().screenGeometry().width() - self.line.geometry().x(), 0, 21,
                                QDesktopWidget().screenGeometry().height())
        self.line_5.setGeometry(self.line.geometry().x() + 10, QDesktopWidget().screenGeometry().height()-280,
                                self.line_4.geometry().x() - self.line.geometry().x(), 21)
        self.label_7.move(QDesktopWidget().screenGeometry().width() - self.line.geometry().x() + 30, 20)
        self.label_8.move(self.line.geometry().x() + 10, QDesktopWidget().screenGeometry().height()-270)
        self.scrollArea.setGeometry(QRect(self.line.geometry().x()+15, QDesktopWidget().screenGeometry().height()-240, self.line_4.geometry().x()-self.line.geometry().x()-10, 100))
        self.scrollArea.setWidget(self.label_4)
        self.label_4.setWordWrap(True)  # 自动换行
        self.label_4.setAlignment(Qt.AlignTop)
        self.setupAction.triggered.connect(self.openConfigDialog)
        # 初始化时间控件
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        # 刷新班级控件
        self.comboBox.addItems([str(x) for x in range(1, 11)])
        self.updateComboBox()
        #设置listview位置
        self.listView.setGeometry(QDesktopWidget().screenGeometry().width() - self.line.geometry().x()+30, 60, self.line.geometry().x()-50,QDesktopWidget().screenGeometry().height()-200)
        self.picPadding=10
        self.picWidth=(self.line_4.geometry().x()-self.line.geometry().x())/3-2*self.picPadding
        self.picHeight=self.line_5.geometry().y()/2-4*self.picPadding
        # 初始化攝像頭
        self.fps=None
        self.cap=None
        self.camera_init()
        # 显示窗体
        self.showMaximized()
        self.setFocus()



    def camera_init(self):
        self.timer_camera = QTimer(self)
        self.timer_camera.timeout.connect(self.readImgFromCamra)
        self.timer_camera.timeout.connect(self.update)
        self.cap = cv.VideoCapture()
        if len(self.dto.cfg.CAM_ID)==1:
            flag = self.cap.open(int(self.dto.cfg.CAM_ID))
        else:
            flag = self.cap.open(self.dto.cfg.CAM_ID)
        if flag:
            self.fps = self.cap.get(cv.CAP_PROP_FPS)
            if self.fps!=0:
                self.timer_camera.start(1000/self.fps)
            else:
                self.timer_camera.start(30)
            self.update()
        else:
            QMessageBox.warning(None, u"Warning", str(flag)+"请检测摄像头与电脑是否连接正确!", buttons=QMessageBox.Ok,
                                defaultButton=QMessageBox.Ok)
            return



    def readImgFromCamra(self):
        ret, cvImg = self.cap.read()
        if ret:
            show = cv.resize(cvImg,(int(self.cap.get(3)),int(self.cap.get(4))))
            show = cv.cvtColor(show, cv.COLOR_BGR2RGB)
            height, width, bytesPerComponent = show.shape
            bytesPerLine = bytesPerComponent * width
            qtImg = QImage(show.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.dto.camImg=(cvImg,qtImg)
            if self.fps!=0:
                self.timer_camera.start(1000/self.fps)
            else:
                self.timer_camera.start(30)



    def openConfigDialog(self):
        self.dialog = configDialog(self.dto,parent=self)
        self.dialog.exec_()
        return


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_S and QApplication.keyboardModifiers() == Qt.ControlModifier:
            self.examControl.startThread()
        elif event.key()==Qt.Key_R and QApplication.keyboardModifiers() == Qt.ControlModifier:
            if self.fps is not None:
                self.takePhotoAnswer(self.change_size(self.dto.camImg[0]))


    def takePhotoMarking(self,ansImg,stuImg):
        # 獲取班級和examID
        self.getID()
        if not self.dto.classname:
            QMessageBox.information(None, '提示', '请先导入学生库生成班级!')
            return
        # 未导入答案，返回
        if self.dto.nowAnswer is None:
            QMessageBox.information(None, '提示', '请先导入答案!')
            return
        # 开始阅卷
        self.dto.hideAnswerFlag = 1
        if self.examControl.startThread():
            return True

    def takePhotoAnswer(self,pic):
        if pic is None:
            return
        # 开始分析
        self.dto.nowAnswer = None
        self.dto.hideAnswerFlag = 1
        self.update()
        self.dto.nowPaper.initPaper()
        self.dto.testFlag = True
        self.dto.testFile = pic
        self.dto.markingResultView=[]
        self.dto.answerThreshhold = self.doubleSpinBox.value()
        self.examControl.test(pic)
        self.dto.hideAnswerFlag=0
        self.update()



    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        try:
            painter = QPainter(self)
            if self.dto.camImg is not None:
                painter.drawImage(QRect(5, 40, 310, 210), self.dto.camImg[1])
            self.drawImg(painter, 350, 65, self.picWidth, self.picHeight, self.picPadding)  # 显示图像
            self.drawScore()  # 显示姓名分数
            self.showAnswers()
        except Exception as e:
            QMessageBox.information(None, '提示', '显示图像失败！错误是：' + str(e))

    def showAnswers(self):
        if self.dto.hideAnswerFlag==1:
            self.label_4.clear()
        if self.dto.nowAnswer!=None and self.dto.hideAnswerFlag==0:
            self.label_4.clear()
            self.label_4.setText('目前导入的答案为（题号：答案+得分+部分得分）：'+str(self.dto.nowAnswer))

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

    def drawScore(self):
        if not self.dto.markingResultView:
            return
        score=[]
        tmp = ''
        for j, result in enumerate(self.dto.markingResultView,start=1):
            if result[2][4] <0 and result[2][4]>-4:
                tmp = '第' +  str(j) + '个失败！'
            elif result[2][4]==-5:#学号重复并且选择了计入失败
                tmp = '第' + str(j) + '个：学号：' + str(result[2][0]) + ' 分数：' + str(result[2][2]) + '不覆盖！'
            elif result[2][4] == -4:#学号重复选择了计入成功
                tmp = '第' + str(j) + '个：学号：' + str(result[2][0]) + ' 分数：' + str(result[2][2]) + '覆盖！'
            else:
                tmp = '第' + str(j) + '个：学号：' + str(result[2][0]) + ' 分数：' + str(result[2][2]) + ' 成功！'

            score.append(tmp)
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
        self.dto.examID = self.dateEdit.date().toString("yyyyMMdd")+'_'+self.comboBox.currentText()
        self.dto.classname = self.comboBox_2.currentText()


    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.takePhotoAnswer(self.change_size(self.dto.camImg[0]))


    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        self.takePhotoMarking(self.change_size(self.dto.camImg[0]))

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
            self.dto.markingResultView=[]
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


    @pyqtSlot(float)
    def on_doubleSpinBox_valueChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type float
        """
        self.dto.answerThreshhold = self.doubleSpinBox.value()
        if self.dto.testFlag:
            self.dto.hideAnswerFlag = 0
            self.dto.nowPaper.initPaper()
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
        if not self.dto.markingResultView:
            QMessageBox.information(None, '错误', "尚未阅卷！")
            return
        self.examControl.makeSaveAsReport()

    def change_size(self,image):
        # image = cv.imread(read_file, 1)  # 读取图片 image_name应该是变量
        b = cv.threshold(image, 15, 255, cv.THRESH_BINARY)  # 调整裁剪效果
        binary_image = b[1]  # 二值图--具有三通道
        binary_image = cv.cvtColor(binary_image, cv.COLOR_BGR2GRAY)
        # print(binary_image.shape)  # 改为单通道

        x = binary_image.shape[0]
        y = binary_image.shape[1]
        edges_x = []
        edges_y = []

        for i in range(x):
            for j in range(y):
                if binary_image[i][j] == 255:
                    edges_x.append(i)
                    edges_y.append(j)
        left = min(edges_x)  # 左边界
        right = max(edges_x)  # 右边界
        width = right - left  # 宽度
        bottom = min(edges_y)  # 底部
        top = max(edges_y)  # 顶部
        height = top - bottom  # 高度
        pre1_picture = image[left:left + width, bottom:bottom + height]  # 图片截取
        return pre1_picture