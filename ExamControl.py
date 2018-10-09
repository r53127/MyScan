import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox

from DB import StudentDB, ScanDB, ScoreDB, ScoreReportForm, PaperReportForm
from ExamDto import ExamDto
from ExamService import ExamService
from PicMainWindow import PicMainWindow
from ScanMainWindow import ScanMainWindow
from ScanWindow import ScanWindow
from error import PaperRegionCountError


class ExamControl():
    def __init__(self):
        # 创建数据源
        self.dto = ExamDto()
        # 鏈接学生數據庫
        self.stuDB = StudentDB()
        self.updateClassID()
        # 连接阅卷结果库
        self.scanDB = ScanDB()
        # 连接成绩库
        self.scoreDB = ScoreDB()
        # 创建阅卷面板(连接数据源、 安装控制器）
        self.scanWin = PicMainWindow(self.dto, self)
        # self.scanWin = ScanMainWindow(self.dto, self)
        # self.scanWin = ScanWindow(self.dto, self)
        # 创建阅卷逻辑块（连接数据源）
        self.examServ = ExamService(self.dto)

    def updateClassID(self):
        self.dto.allClassID = self.stuDB.queryClassID()

    def startMarking(self):
        choices, stuID = self.examServ.marking()

        classID = self.dto.classID
        examID = self.dto.examID

        # 根据学号查姓名
        result = self.stuDB.checkData(stuID, classID)
        if not result:
            QMessageBox.information(None, '提示', '未找到该学生！')
            return 0 #计入失败
        stuName = result[0][2]
        # 检查阅卷是否重复
        result = self.scanDB.checkData(stuID, examID, classID)
        if result:
            QMessageBox.information(None, '提示', '重复阅卷，该学号已阅过！')
            return -1  #重复，不计入失败

        # 阅卷结果为空
        if choices is None:
            return 0 #计入失败
        # 少答案
        if len(choices) > len(self.dto.nowAnswer):
            QMessageBox.information(None, '提示',
                                    '学生选项比答案多，题有' + str(len(choices)) + '个，答案有' + str(len(self.dto.nowAnswer)) + '个！')
            return 0 #计入失败

        # 判分
        score = self.getScore(choices, self.dto.nowAnswer)
        # 答案入库，choice[0]是题号，choice[1]是填涂选项
        for choice in choices:
            self.scanDB.insertDB(examID, classID, stuID, stuName, choice[0], choice[1])
        # 分数入库
        self.scoreDB.insertDB(classID, stuID, stuName, score, examID)

        return 1  #成功

    def makeScoreReport(self):
        # 初始化报表文件
        try:
            reportFile = ScoreReportForm()
            #查询分数
            result=self.scoreDB.queryData(self.dto.classID,self.dto.examID)
            if result:
                reportFile.makeScoreReport(result)
            else:
                QMessageBox.information(None, '提示', '没有查询到对应班级和日期的阅卷数据！')
        except:
            traceback.print_exc()

    def makePaperReport(self):
        # 初始化报表文件
        try:
            reportFile = PaperReportForm()
            stu_count=self.scanDB.queryPersonCount(self.dto.examID,self.dto.classID)
            if not stu_count:
                QMessageBox.information(None, '提示', '没有查询到对应班级和日期的阅卷数据！')
                return
            ques_count=len(self.dto.nowAnswer)
            paperResult=[]
            for quesid in range(1,ques_count+1):
                correct_ans=self.dto.nowAnswer.get(quesid)[0]
                correct_count=len(self.scanDB.queryData(self.dto.classID,self.dto.examID,quesid,correct_ans))/stu_count
                A_count = len(self.scanDB.queryData(self.dto.classID, self.dto.examID, quesid, 'A'))/stu_count
                B_count = len(self.scanDB.queryData(self.dto.classID, self.dto.examID, quesid, 'B'))/stu_count
                C_count = len(self.scanDB.queryData(self.dto.classID, self.dto.examID, quesid, 'C'))/stu_count
                D_count = len(self.scanDB.queryData(self.dto.classID, self.dto.examID, quesid, 'D'))/stu_count
                #根据模板存放需要的数据：考试时间，班级，题号，正确答案，正确率，A选项率，B选项率，C选项率，D选项率,总人数，总题数
                paperResult.append([self.dto.examID,self.dto.classID,quesid,correct_ans,correct_count,A_count,B_count,C_count,D_count,stu_count,ques_count])
            reportFile.makePaperReport(paperResult)
        except:
            traceback.print_exc()

    def getScore(self, choices, answer):
        # print('判分'),(answer.get(choice[0]))[0]是答案，(answer.get(choice[0]))[1]是每题分值
        correct_count = 0
        score = 0
        for choice in choices:
            if (answer.get(choice[0]))[0] == choice[1]:
                correct_count += 1
                score += (answer.get(choice[0]))[1]
        return score

    def test(self, file):
        try:
            self.examServ.test(file)
        except PaperRegionCountError as e:
            self.dto.errorMsg = '该学生共有'+str(e.errorValue)+'个题未涂或涂的不符合要求！'
            self.scanWin.update()
            return
        except:
            traceback.print_exc()
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ExamControl()
    sys.exit(app.exec_())
