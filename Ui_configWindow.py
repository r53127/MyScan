# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MyScan\configWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_configDialog(object):
    def setupUi(self, configDialog):
        configDialog.setObjectName("configDialog")
        configDialog.resize(614, 324)
        configDialog.setSizeGripEnabled(True)
        self.pushButton = QtWidgets.QPushButton(configDialog)
        self.pushButton.setGeometry(QtCore.QRect(150, 250, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(configDialog)
        self.pushButton_2.setGeometry(QtCore.QRect(370, 250, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.layoutWidget = QtWidgets.QWidget(configDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(300, 20, 231, 185))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 5, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.layoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 6, 0, 1, 1)
        self.spinBox_7 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_7.setMinimum(1)
        self.spinBox_7.setMaximum(10)
        self.spinBox_7.setSingleStep(1)
        self.spinBox_7.setProperty("value", 3)
        self.spinBox_7.setDisplayIntegerBase(10)
        self.spinBox_7.setObjectName("spinBox_7")
        self.gridLayout.addWidget(self.spinBox_7, 4, 1, 1, 1)
        self.spinBox_9 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_9.setMinimum(2)
        self.spinBox_9.setMaximum(10)
        self.spinBox_9.setSingleStep(1)
        self.spinBox_9.setProperty("value", 2)
        self.spinBox_9.setDisplayIntegerBase(10)
        self.spinBox_9.setObjectName("spinBox_9")
        self.gridLayout.addWidget(self.spinBox_9, 6, 1, 1, 1)
        self.spinBox_8 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_8.setMinimum(0)
        self.spinBox_8.setMaximum(5)
        self.spinBox_8.setSingleStep(1)
        self.spinBox_8.setProperty("value", 0)
        self.spinBox_8.setDisplayIntegerBase(10)
        self.spinBox_8.setObjectName("spinBox_8")
        self.gridLayout.addWidget(self.spinBox_8, 5, 1, 1, 1)
        self.spinBox_4 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_4.setMinimum(1)
        self.spinBox_4.setMaximum(10)
        self.spinBox_4.setProperty("value", 7)
        self.spinBox_4.setObjectName("spinBox_4")
        self.gridLayout.addWidget(self.spinBox_4, 1, 1, 1, 1)
        self.spinBox_5 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_5.setMinimum(1)
        self.spinBox_5.setProperty("value", 28)
        self.spinBox_5.setObjectName("spinBox_5")
        self.gridLayout.addWidget(self.spinBox_5, 2, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.spinBox_6 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_6.setMinimum(1)
        self.spinBox_6.setMaximum(10)
        self.spinBox_6.setSingleStep(1)
        self.spinBox_6.setProperty("value", 2)
        self.spinBox_6.setDisplayIntegerBase(10)
        self.spinBox_6.setObjectName("spinBox_6")
        self.gridLayout.addWidget(self.spinBox_6, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(configDialog)
        self.label.setGeometry(QtCore.QRect(30, 20, 60, 16))
        self.label.setObjectName("label")
        self.layoutWidget1 = QtWidgets.QWidget(configDialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 42, 171, 111))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.spinBox_1 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBox_1.setMinimum(2)
        self.spinBox_1.setMaximum(8)
        self.spinBox_1.setProperty("value", 4)
        self.spinBox_1.setObjectName("spinBox_1")
        self.gridLayout_2.addWidget(self.spinBox_1, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(100)
        self.spinBox_2.setSingleStep(1)
        self.spinBox_2.setProperty("value", 20)
        self.spinBox_2.setDisplayIntegerBase(10)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout_2.addWidget(self.spinBox_2, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(10)
        self.spinBox_3.setProperty("value", 3)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout_2.addWidget(self.spinBox_3, 2, 1, 1, 1)

        self.retranslateUi(configDialog)
        QtCore.QMetaObject.connectSlotsByName(configDialog)

    def retranslateUi(self, configDialog):
        _translate = QtCore.QCoreApplication.translate
        configDialog.setWindowTitle(_translate("configDialog", "参数设置"))
        self.pushButton.setText(_translate("configDialog", "保存"))
        self.pushButton_2.setText(_translate("configDialog", "关闭"))
        self.label_10.setText(_translate("configDialog", "<html><head/><body><p>班级位数：</p></body></html>"))
        self.label_5.setText(_translate("configDialog", "学号区："))
        self.label_6.setText(_translate("configDialog", "学号区excel Y轴总格数："))
        self.label_7.setText(_translate("configDialog", "学号起始X轴偏移格数："))
        self.label_9.setText(_translate("configDialog", "<html><head/><body><p>学号起始Y轴偏移格数：</p></body></html>"))
        self.label_11.setText(_translate("configDialog", "<html><head/><body><p>学号位数：</p></body></html>"))
        self.label_8.setText(_translate("configDialog", "学号区excel X轴总格数："))
        self.label.setText(_translate("configDialog", "答题区："))
        self.label_4.setText(_translate("configDialog", "选项个数："))
        self.label_3.setText(_translate("configDialog", "题总行数："))
        self.label_2.setText(_translate("configDialog", "题总列数："))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    configDialog = QtWidgets.QDialog()
    ui = Ui_configDialog()
    ui.setupUi(configDialog)
    configDialog.show()
    sys.exit(app.exec_())

