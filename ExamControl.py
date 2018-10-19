import logging
import os
import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox

from DB import StudentDB, ScanDB, ScoreDB, ScoreReportForm, PaperReportForm
from ExamDto import ExamDto
from ExamService import ExamService
from PicMainWindow import PicMainWindow
from ThreshWindow import ThreshWindow

CLASS_ID={31:'高三1班',32:'高三2班'}

class ExamControl():
    def __init__(self):
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        if not os.path.exists('image'):
            os.mkdir('image')
        # 创建数据源
        self.dto = ExamDto()
        # 鏈接学生數據庫
        self.stuDB = StudentDB()
        #刷新班级列表
        self.updateClassID()
        # 连接阅卷结果库
        self.scanDB = ScanDB()
        # 连接成绩库
        self.scoreDB = ScoreDB()
        # 创建阅卷面板(连接数据源、 安装控制器）
        self.scanWin = PicMainWindow(self.dto, self)
        # 创建阅卷逻辑块（连接数据源）
        self.examServ = ExamService(self.dto)
        #阅卷进度视图
        self.markingResultView = []

    def updateClassID(self):
        self.dto.allClassID = self.stuDB.queryClassID()

    def marking(self, imgFile):#阅单卡
        ID, choices, score = self.examServ.marking(imgFile)

        # 无法识别图片，直接返回0
        if ID is None and choices is None and score is None:
            return 0  # 无法识别

        classID = self.dto.classID

        got_classID = ID[0:self.dto.cfg.CLASS_BITS]  # 按位截取班级
        if ID!='':
            stuID = int(ID[self.dto.cfg.CLASS_BITS:(self.dto.cfg.CLASS_BITS + self.dto.cfg.STU_BITS)])  ##按位截取学号并转换成数字
        else:
            return -1#未识别出学号

        if got_classID != '':  # 对比班级
            if CLASS_ID[int(got_classID)] != classID:
                return -1 #班级冲突

        # 根据学号查姓名
        result = self.stuDB.checkData(stuID, classID)
        if not result:
            return -1  #学号不存在
        stuName = result[0][2]

        return (stuID, choices, score, stuName)  # 成功

    def startMarking(self, files):#自适应阈值批量阅卷并做各种记录和保存处理
        self.scanWin.statusBar().showMessage('')#清除状态栏信息
        self.dto.testFlag = False  # 关闭测试开关
        self.dto.failedFiles = []  # 重置错误文件记录
        self.scanWin.label_4.clear()  # 清除错误文件显示
        failedCount = 0  # 重置错误文件计数
        successedCount = 0  # 重置正确文件计数
        self.markingResultView = []  # 记录本次所有阅卷结果
        for i, file in enumerate(files, start=1):
            try:
                # 初始化一张试卷
                self.dto.nowPaper.initPaper()
                # 刷新显示
                self.scanWin.update()

                # 根据最优阈值存在使用最优阈值，如果不存在使用全局阈值初始化精确度阈值
                if self.dto.bestAnswerThreshhold is not None:
                    self.dto.answerThreshhold=self.dto.bestAnswerThreshhold
                else:
                    self.dto.answerThreshhold = self.scanWin.doubleSpinBox.value()

                #自动适应阈值阅卷
                failedCount, successedCount,self.markingResult,confirmResult= self.autoScan(file, failedCount, successedCount)
                # 记录该文件阅卷结果
                if confirmResult:#计入成功，记录结果
                    self.markingResultView.append([i, file, self.markingResult])
                else:#计入失败，markingResult记录为-1
                    self.markingResultView.append([i, file, -1])
                self.scanWin.update()
                QApplication.processEvents()#停顿刷新界面
            except Exception as e:
                failedCount += 1
                self.dto.failedFiles.append(file)
                logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
                logging.debug(traceback.format_exc())
                # traceback.print_exc()
                QMessageBox.information(None, '提示', '此图片阅卷失败！错误是：' + str(e))
                continue
        self.scanWin.statusBar().showMessage(
            '已全部结束！本次共阅' + str(len(files)) + '份，成功' + str(successedCount) + '份，失败' + str(failedCount) + '份！')


    def autoScan(self, file,failedCount, successedCount):#自适应阈值扫描
        confirmResult=1#手动确认结果，无需手动调节的都默认计入成功！
        retry_flag = 1  # 重试标识
        for a in range(2, 8):  # 程序自行尝试调节阈值
            self.dto.answerThreshhold = a / 10  # 获取阈值
            self.dto.nowPaper.multiChoiceCount = 0  # 重置多选计数器
            self.dto.nowPaper.noChoiceCount = 0  # 重置无选项计数器
            self.markingResult = self.marking(file)  # 阅卷
            if self.markingResult == 0:  # 无法识别图片，直接计入失败跳过调节阈值
                retry_flag=0#不再重试
                failedCount += 1
                self.dto.failedFiles.append(file)
                QMessageBox.information(None, '提示', '找不到答题区，直接计入失败！')
                break
            if self.markingResult == -1:  # 学号无法识别，则跳出循环，手动调节
                retry_flag = 1  # 重试
                QMessageBox.information(None, '提示', '请确认班级或学号是否涂的有问题，可通过调节阈值重试，如果确实有问题，建议直接计入失败！')
                break
            choice_answer_len = []  # 暂存本次所阅的答案长度
            for choice in self.markingResult[1]:  # 算出所选每一个所选答案的长度
                choice_answer_len.append(len(choice[1]))
            if choice_answer_len == self.dto.STAND_ANSWER_LEN:  # 比对所涂答案长度和标准答案的长度，如果一致说明阈值适合则结束
                successedCount += 1
                retry_flag = 0
                self.dto.bestAnswerThreshhold = a / 10  # 保存最优阈值
                self.saveMarkingData(*self.markingResult)#成功则保存数据
                break
        if retry_flag == 1:#手动调节阈值
            # 如果程序调节失败，操作者自行调节阈值
            confirmResult= self.confirmMarking(file)
            if confirmResult:#计入成功
                successedCount += 1
                self.saveMarkingData(*self.markingResult)  # 选择计入成功则保存数据
            else:#计入失败
                failedCount += 1
                self.dto.failedFiles.append(file)
        return failedCount, successedCount,self.markingResult,confirmResult

    # 调节阈值窗口
    def confirmMarking(self, file):
        dialog = ThreshWindow(self.dto, file, self.scanWin)
        result = dialog.exec_()
        return result

    # 保存阅卷数据
    def saveMarkingData(self, stuID, choices, score, stuName):
        classID = self.dto.classID
        examID = self.dto.examID
        # 检查阅卷是否重复
        result = self.scanDB.checkData(stuID, examID, classID)
        if result:
            reply = QMessageBox.question(None, "提示",
                                         "已经阅过，数据已存在，是否覆盖？",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply != 16384:
                return
            # 更新数据
            for choice in choices:
                self.scanDB.updateDB(stuID, choice[0], choice[1])  # 学号，题号，答案
            # 分数更新
            self.scoreDB.updateDB(stuID, score)  # 学号，分数
        else:
            # 答案入库，choice[0]是题号，choice[1]是填涂选项
            for choice in choices:
                self.scanDB.insertDB(examID, classID, stuID, stuName, choice[0], choice[1])
            # 分数入库
            self.scoreDB.insertDB(classID, stuID, stuName, score, examID)



    def makeScoreReport(self):
        # 初始化报表文件
        try:
            reportFile = ScoreReportForm()
            #查询分数
            scoreList=self.scoreDB.queryScore(self.dto.classID, self.dto.examID)#根据班级，考试时间查成绩
            if not scoreList:
                QMessageBox.information(None, '提示', '没有查询到对应班级和日期的阅卷数据！')
                return
            stuList=self.stuDB.queryStuByClassID(self.dto.classID)#根据班级查名单
            for stu in stuList:#stu内数据分别为userid INTEGER  primary key AUTOINCREMENT ,stuid int,name varchar(20),gender varchar(4),classid varchar(20))
                for scor in scoreList:#score内数据分别为scoreID ,classID varchar(20),stuID int,name varchar(20),score int,examID varchar(8))
                    if stu[1]==scor[2] and stu[2]==scor[3]: #如果姓名和学号一致
                        break
                else:
                    scoreList.append([0,self.dto.classID,stu[1],stu[2],0,self.dto.examID])
            reportFile.makeScoreReport(scoreList)
        except Exception as e:
            QMessageBox.information(None, '错误:', "意外错误！错误是：" + str(e) + "！")

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
        except Exception as e:
            QMessageBox.information(None, '错误:', "意外错误！错误是：" + str(e) + "！")



    def test(self, file):
        try:
            self.examServ.test(file)
        except Exception as e:
            QMessageBox.information(None, '错误:', "意外错误！错误是：" + str(e) + "！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ExamControl()
    sys.exit(app.exec_())
