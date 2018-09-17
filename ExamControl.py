import sys

from PyQt5.QtWidgets import QApplication

from DB import StudentDB, AnswerDB
from ExamDto import ExamDto
from ExamService import ExamService
from ScanWindow import ScanWindow


class ExamControl():
    def __init__(self):
        # 创建游戏数据源
        self.dto = ExamDto()
        # 鏈接学生數據庫
        self.stu_data = StudentDB()
        # 讀取答案
        self.ans_data = AnswerDB()
        # 加載數據
        self.reloadData()
        # 创建阅卷面板(连接游戏数据源、 安装控制器）
        self.scanWin = ScanWindow(self.dto, self)
        # 创建阅卷逻辑块（连接阅卷数据源）
        self.examServ = ExamService(self.dto)


    def reloadData(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ExamControl()
    sys.exit(app.exec_())
