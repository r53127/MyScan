# -*- coding: utf-8 -*-

"""
Module implementing ScanWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTabWidget, QFileDialog

from Ui_ScanWindow import Ui_TabWidget


class ScanWindow(QTabWidget, Ui_TabWidget):
    """
    Class documentation goes here.
    """
    def __init__(self, dto,examControl):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ScanWindow, self).__init__()
        self.dto=dto
        self.examControl=examControl
        self.files=[]
        self.setupUi(self)
        self.show()
    

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        files,filetype=QFileDialog.getOpenFileNames(self,'打开文件',r'.',r'图片文件 (*.jpg;*.png;*.bmp)')
        if not files:
            return
        self.files=files
            
            
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        direc = QFileDialog.getExistingDirectory(self, '打开阅卷目录', r'.')
        if not dir:
            return
        self.direc=direc
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    



