# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\MyScan\PicMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1292, 892)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.line = QtWidgets.QFrame(self.centralWidget)
        self.line.setGeometry(QtCore.QRect(312, 0, 21, 871))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralWidget)
        self.line_2.setGeometry(QtCore.QRect(0, 190, 321, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralWidget)
        self.line_3.setGeometry(QtCore.QRect(0, 510, 321, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralWidget)
        self.line_4.setGeometry(QtCore.QRect(990, 0, 21, 891))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_4.sizePolicy().hasHeightForWidth())
        self.line_4.setSizePolicy(sizePolicy)
        self.line_4.setMidLineWidth(0)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_9.setGeometry(QtCore.QRect(70, 50, 161, 81))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(16)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(1020, 30, 249, 34))
        self.label_7.setObjectName("label_7")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(22, 150, 151, 20))
        self.label_2.setObjectName("label_2")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralWidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(180, 140, 71, 31))
        self.doubleSpinBox.setDecimals(2)
        self.doubleSpinBox.setMinimum(0.1)
        self.doubleSpinBox.setMaximum(1.0)
        self.doubleSpinBox.setSingleStep(0.01)
        self.doubleSpinBox.setProperty("value", 0.2)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.line_5 = QtWidgets.QFrame(self.centralWidget)
        self.line_5.setGeometry(QtCore.QRect(320, 740, 681, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(351, 804, 81, 21))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_8 = QtWidgets.QLabel(self.centralWidget)
        self.label_8.setGeometry(QtCore.QRect(330, 760, 249, 34))
        self.label_8.setObjectName("label_8")
        self.listView = QtWidgets.QListView(self.centralWidget)
        self.listView.setGeometry(QtCore.QRect(1020, 70, 261, 721))
        self.listView.setObjectName("listView")
        self.layoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 540, 251, 243))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_2.addWidget(self.pushButton_7)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_2.addWidget(self.pushButton_6)
        self.pushButton_saveas = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_saveas.setObjectName("pushButton_saveas")
        self.verticalLayout_2.addWidget(self.pushButton_saveas)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(30, 220, 251, 281))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout.addWidget(self.pushButton_8)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_1 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_1.setObjectName("pushButton_1")
        self.verticalLayout.addWidget(self.pushButton_1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setLineWidth(3)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.dateEdit = QtWidgets.QDateEdit(self.layoutWidget1)
        self.dateEdit.setProperty("showGroupSeparator", False)
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout.addWidget(self.dateEdit)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAutoFillBackground(False)
        self.label_5.setLineWidth(3)
        self.label_5.setTextFormat(QtCore.Qt.PlainText)
        self.label_5.setScaledContents(False)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.comboBox_2 = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox_2.setObjectName("comboBox_2")
        self.verticalLayout.addWidget(self.comboBox_2)
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)
        self.scrollArea.setGeometry(QtCore.QRect(490, 796, 261, 51))
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 261, 51))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralWidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.setupAction = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/tool.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setupAction.setIcon(icon)
        self.setupAction.setObjectName("setupAction")
        self.toolBar.addAction(self.setupAction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "多宝照片阅卷"))
        self.pushButton_9.setText(_translate("MainWindow", "预读答案"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#5500ff;\">进度显示：</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "全局识别精确度阈值："))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#5500ff;\">信息板：</span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#5500ff;\">功能区：</span></p></body></html>"))
        self.pushButton_3.setText(_translate("MainWindow", "阅文件"))
        self.pushButton_4.setText(_translate("MainWindow", "阅目录"))
        self.pushButton_7.setText(_translate("MainWindow", "另存失败文件"))
        self.pushButton_5.setText(_translate("MainWindow", "生成成绩报表"))
        self.pushButton_6.setText(_translate("MainWindow", "生成试卷分析"))
        self.pushButton_saveas.setText(_translate("MainWindow", "另存本次结果"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#5500ff;\">设置区：</span></p></body></html>"))
        self.pushButton_8.setText(_translate("MainWindow", "打开学生库模板"))
        self.pushButton.setText(_translate("MainWindow", "导入学生库"))
        self.pushButton_1.setText(_translate("MainWindow", "打开EXCEL录入答案"))
        self.pushButton_2.setText(_translate("MainWindow", "EXCEL导入答案"))
        self.label.setText(_translate("MainWindow", "选择考试时间（作为阅卷保存和生成报表的依据）"))
        self.label_5.setText(_translate("MainWindow", "选择阅卷班级"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.setupAction.setText(_translate("MainWindow", "设置"))
        self.setupAction.setToolTip(_translate("MainWindow", "设置卡参数"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

