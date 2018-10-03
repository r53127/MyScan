import sys
import traceback
from datetime import date

from PyQt5.QtWidgets import QApplication, QMessageBox

from DB import StudentDB, AnswerDB, ScanDB, ScoreDB
from ExamDto import ExamDto
from ExamService import ExamService
from ScanWindow import ScanWindow
from error import PaperRegionCountError


class ExamControl():
    def __init__(self):
        # 创建数据源
        self.dto = ExamDto()
        # 鏈接学生數據庫
        self.stuDB = StudentDB()
        #连接答案库
        self.answerDB=AnswerDB()
        #连接阅卷结果库
        self.scanDB=ScanDB()
        #连接成绩库
        self.scoreDB=ScoreDB()
        # 创建阅卷面板(连接数据源、 安装控制器）
        self.scanWin = ScanWindow(self.dto, self)
        # 创建阅卷逻辑块（连接数据源）
        self.examServ = ExamService(self.dto)

    def startMarking(self):
        choices, stuID=self.examServ.marking()
        stuClass='高三一班'
        #根据学号查姓名
        result=self.stuDB.checkData(stuID,stuClass)
        if not result:
            QMessageBox.information(None,'TIP','未找到该学生！')
            return False
        stuName=result[0][2]
        # 答案入库
        for choice in choices:
            self.scanDB.insertDB(stuClass,stuID,stuName,choice[0],choice[1])
        #判分
        if len(choices)>len(self.dto.nowAnswer):
            QMessageBox.information(None,'提示','学生选项比答案多，题有'+str(len(choices))+'个，答案有'+str(len(self.dto.nowAnswer))+'个！')
            return False
        score = self.getScore(choices, self.dto.nowAnswer)
        examid=date.today()
        #分数入库
        self.scoreDB.insertDB(stuClass,stuID,stuName,score,str(examid))
        return True


    def getScore(self, choices, answer):
        # print('判分')
        correct_count = 0
        score = 0
        for choice in choices:
            if (answer.get(choice[0]))[0] == choice[1]:
                correct_count += 1
                score += (answer.get(choice[0]))[1]
        return score


    def test(self,file):
        try:
            self.examServ.test(file)
        except PaperRegionCountError as e:
            self.dto.errorMsg = '错误！找到的选项个数为：' + str(e.errorValue) + e.errorMsg
            self.scanWin.update()
            return
        except:
            traceback.print_exc()
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ExamControl()
    sys.exit(app.exec_())
