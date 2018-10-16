# -*- coding: utf-8 -*-

"""
Module implementing ThreshAdjust.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Ui_ThreshWindow import Ui_Dialog


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
        # 根据最优阈值存在则使用最优阈值初始化调节控件
        if self.dto.bestAnswerThreshhold is not None:
            self.doubleSpinBox.setValue(self.dto.bestAnswerThreshhold)

        self.setupPushbutton_2()#刷新计入成功按钮，阅卷失败不允许计入成功
        self.pushButton_1.clicked.connect(self.reject)
        self.pushButton_2.clicked.connect(self.accept)
    
    @pyqtSlot(str)
    def on_doubleSpinBox_valueChanged(self, p0):
        self.dto.answerThreshhold=self.doubleSpinBox.value()#获取局部阈值
        self.dto.nowPaper.multiChoiceCount=0#重置多选计数器
        self.dto.nowPaper.noChoiceCount=0#重置无选项计数器
        self.parent.markingResult = self.parent.examControl.markingControl(self.file)#重新阅卷
        self.setupPushbutton_2()#刷新计入成功按钮，阅卷失败不允许计入成功
        self.update()
        self.parent.update()

    def setupPushbutton_2(self):
        if self.parent.markingResult==0 or self.parent.markingResult==-1:
            self.pushButton_2.setDisabled(True)
        else:
            self.pushButton_2.setEnabled(True)

