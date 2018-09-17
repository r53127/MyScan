# -*- coding: utf-8 -*-

"""
Module implementing ScanWindow.
"""
import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTabWidget, QFileDialog, QApplication, QMessageBox

from Ui_ScanWindow import Ui_TabWidget


class ScanWindow(QTabWidget, Ui_TabWidget):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ScanWindow, self).__init__(parent)
        self.files=[]
        self.setupUi(self)
    

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        files,filetype=QFileDialog.getOpenFileNames(self,'打开文件',r'.',r'图片文件 (*.jpg;*.png;*.bmp)')
        if files:
            self.files=files
            
            
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        direc = QFileDialog.getExistingDirectory(self, '打开阅卷目录', r'.')
        if dir:
            self.direc=direc
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ScanWindow()
    win.show()
    sys.exit(app.exec_())
