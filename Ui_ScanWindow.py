# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MyScan\ScanWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TabWidget(object):
    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(378, 209)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(50, 40, 331, 31))
        self.label.setObjectName("label")
        self.splitter = QtWidgets.QSplitter(self.tab)
        self.splitter.setGeometry(QtCore.QRect(50, 100, 279, 28))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pushButton = QtWidgets.QPushButton(self.splitter)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_4 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_3.setObjectName("pushButton_3")
        TabWidget.addTab(self.tab, "")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        TabWidget.addTab(self.tab1, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "MyScan"))
        self.label.setText(_translate("TabWidget", "请选择需要阅卷的图片目录或文件："))
        self.pushButton.setText(_translate("TabWidget", "选择文件"))
        self.pushButton_4.setText(_translate("TabWidget", "选择目录"))
        self.pushButton_3.setText(_translate("TabWidget", "取消"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "阅卷"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab1), _translate("TabWidget", "设置"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TabWidget = QtWidgets.QTabWidget()
    ui = Ui_TabWidget()
    ui.setupUi(TabWidget)
    TabWidget.show()
    sys.exit(app.exec_())

