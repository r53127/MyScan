# -*- coding: utf-8 -*-

"""
Module implementing configDialog.
"""

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog

from Ui_CamconfigWindow import Ui_configDialog

class configDialog(QDialog, Ui_configDialog):
    """
    Class documentation goes here.
    """
    def __init__(self,dto, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(configDialog, self).__init__(parent)
        self.parent=parent
        self.dto=dto
        self.setupUi(self)
        self.init()

    def init(self):
        self.spinBox_1.setValue(self.dto.cfg.PER_CHOICE_COUNT)
        self.spinBox_2.setValue(self.dto.cfg.ANSWER_ROWS)
        self.spinBox_3.setValue(self.dto.cfg.ANSWER_COLS)
        self.spinBox_4.setValue(self.dto.cfg.Stuid_AREA_COLS)
        self.spinBox_5.setValue(self.dto.cfg.Stuid_AREA_ROWS)
        self.spinBox_6.setValue(self.dto.cfg.ID_X_OFFSET)
        self.spinBox_7.setValue(self.dto.cfg.ID_Y_OFFSET)
        self.spinBox_8.setValue(self.dto.cfg.CLASS_BITS)
        self.spinBox_9.setValue(self.dto.cfg.STU_BITS)
        self.doubleSpinBox.setValue(self.dto.cfg.PER_ANS_SCORE)
        self.doubleSpinBox_2.setValue(self.dto.cfg.PART_ANS_SCORE)
        self.comboBox.addItem(str(self.dto.cfg.CAM_ID))


    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.dto.cfg.PER_CHOICE_COUNT=self.spinBox_1.value()
        self.dto.cfg.ANSWER_ROWS=self.spinBox_2.value()
        self.dto.cfg.ANSWER_COLS=self.spinBox_3.value()
        self.dto.cfg.Stuid_AREA_COLS=self.spinBox_4.value()
        self.dto.cfg.Stuid_AREA_ROWS=self.spinBox_5.value()
        self.dto.cfg.ID_X_OFFSET=self.spinBox_6.value()
        self.dto.cfg.ID_Y_OFFSET=self.spinBox_7.value()
        self.dto.cfg.CLASS_BITS=self.spinBox_8.value()
        self.dto.cfg.STU_BITS=self.spinBox_9.value()
        self.dto.cfg.PER_ANS_SCORE=self.doubleSpinBox.value()
        self.dto.cfg.PART_ANS_SCORE=self.doubleSpinBox_2.value()
        self.dto.cfg.CAM_ID=self.comboBox.currentText()
        self.dto.cfg.saveCfg(self.dto.cfg)
        self.dto.nowPaper.loadConfig()#当前考卷重新加载配置
        self.close()
        self.parent.cap.release()
        self.parent.camera_init()
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()


