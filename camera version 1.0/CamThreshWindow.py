# -*- coding: utf-8 -*-

"""
Module implementing ThreshAdjust.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Ui_CamThreshWindow import Ui_Dialog


class ThreshWindow(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, dto,file,parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ThreshWindow, self).__init__(parent)
        self.file=file
        self.dto=dto
        self.parent=parent
        self.setupUi(self)
        # 根据最优阈值存在则使用最优阈值初始化调节控件,如果doubleSpinBox设置的默认值和此处的初始化值不一致，该界面加载的时候会执行一次on_doubleSpinBox_valueChanged刷新
        if self.dto.bestAnswerThreshhold is not None:
            self.doubleSpinBox.setValue(self.dto.bestAnswerThreshhold)#如果最优阈值存在则使用最优阈值
        else:
            self.doubleSpinBox.setValue(self.parent.doubleSpinBox.value())#如果最优阈值存在则使用全局阈值

        self.setupPushbutton_2()#刷新计入成功按钮，阅卷失败不允许计入成功
        self.pushButton_1.clicked.connect(self.reject)
        self.pushButton_2.clicked.connect(self.accept)
    
    @pyqtSlot(str)
    def on_doubleSpinBox_valueChanged(self, p0):
        self.dto.answerThreshhold=self.doubleSpinBox.value()#获取局部阈值
        self.dto.nowPaper.multiChoiceCount=0#重置多选计数器
        self.dto.nowPaper.noChoiceCount=0#重置无选项计数器
        self.parent.examControl.markingResult = self.parent.examControl.marking(self.file)#重新阅卷
        self.setupPushbutton_2()#刷新计入成功按钮，阅卷失败不允许计入成功
        self.update()
        self.parent.update()


    def setupPushbutton_2(self):
        if self.parent.examControl.markingResult!=0:
            if self.parent.examControl.markingResult[4]==-1 or self.parent.examControl.markingResult[4]==-3:
                self.pushButton_2.setDisabled(True)
            else:
                self.pushButton_2.setEnabled(True)
        else:
            self.pushButton_2.setDisabled(True)

