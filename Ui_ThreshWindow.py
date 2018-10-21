# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MyScan\ThreshWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(435, 263)
        Dialog.setSizeGripEnabled(True)
        self.label_1 = QtWidgets.QLabel(Dialog)
        self.label_1.setGeometry(QtCore.QRect(82, 60, 181, 51))
        self.label_1.setObjectName("label_1")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBox.setGeometry(QtCore.QRect(270, 60, 101, 41))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(14)
        self.doubleSpinBox.setFont(font)
        self.doubleSpinBox.setDecimals(2)
        self.doubleSpinBox.setMinimum(0.1)
        self.doubleSpinBox.setMaximum(1.0)
        self.doubleSpinBox.setSingleStep(0.01)
        self.doubleSpinBox.setProperty("value", 0.1)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.pushButton_1 = QtWidgets.QPushButton(Dialog)
        self.pushButton_1.setGeometry(QtCore.QRect(20, 160, 101, 41))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 160, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 160, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.doubleSpinBox, self.pushButton_2)
        Dialog.setTabOrder(self.pushButton_2, self.pushButton_1)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "阈值调节"))
        self.label_1.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#0000ff;\">本张精确度阈值：</span></p></body></html>"))
        self.pushButton_1.setText(_translate("Dialog", "计入失败"))
        self.pushButton_2.setText(_translate("Dialog", "计入成功"))
        self.pushButton_3.setText(_translate("Dialog", "中止阅卷"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

