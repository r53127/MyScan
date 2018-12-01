import logging
import os
import sys
import traceback

from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox
from imutils.perspective import four_point_transform

from DB import StudentDB, ScanDB, ScoreDB, ScoreReportForm, PaperReportForm, SaveAsReport
from CamExamDto import ExamDto
from CamExamService import ExamService
from CamMainWindow import CamMainWindow
from CamThreshWindow import ThreshWindow
import cv2 as cv

class WorkThread(QThread):
    trigger = pyqtSignal()

    def __int__(self,parent=None):
        super(WorkThread, self).__init__()


    def run(self):
        try:
            global exam
            cv.imwrite('cam.jpg',exam.dto.camImg[0])
            while(1):
                self.sleep(0.5)
                ansImg, stuImg=self.get_roi_img(exam.dto.camImg[0])
                if ansImg is not None:
                    exam.startMarking(ansImg,stuImg)
                    # 循环完毕后发出信号
                    self.trigger.emit()

        except:
            traceback.print_exc()

    # 提取答题和学号区域
    def get_roi_img(self, src_img):
        if src_img.shape[1] > 1500:  # 如果图像太大，则进行缩小
            src_img = cv.resize(src_img, (1440, int((1440 / src_img.shape[1] * src_img.shape[0]))),
                                interpolation=cv.INTER_AREA)
            # src_img=cv.resize(src_img,(0,0),fx=0.3,fy=0.3,interpolation=cv.INTER_AREA)
        # cv.imshow('src',src_img)
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        # 高斯滤波，清除一些杂点
        blur = cv.GaussianBlur(gray, (3, 3), 0)
        # 自适应二值化算法
        thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 131, 4)

        # self.showingImgThresh = ExamPaper.convertImg(thresh2)  # 显示已选标注框图片
        # cv.imshow('th',thresh2)
        image, cnts, hierarchy = cv.findContours(thresh2.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # cv.drawContours(src_img, cnts, -1, (255, 0, 0), 1)
        # cv.imshow('src', src_img)
        sortcnts = sorted(cnts, key=lambda c: cv.contourArea(c), reverse=True)
        # 找答题卡
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)

            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                maxImg_tmp = four_point_transform(src_img, approx.reshape(4, 2))
                # cv.drawContours(src_img,[approx.reshape(4,2)],-1,(255,0,0),1)
                # cv.imshow('approx',maxImg_tmp)
                ratio = maxImg_tmp.shape[1] / maxImg_tmp.shape[0]  # 寬高比
                if ratio > 1.3 and ratio < 2.0 and maxImg_tmp.shape[0] > src_img.shape[0] / 4 and maxImg_tmp.shape[1] > \
                        src_img.shape[1] / 4:
                    cv.imwrite('tmp/paper.png', maxImg_tmp)
                    maxImg = maxImg_tmp
                    break
        else:
            # QMessageBox.information(None, '提示', '找不到有效的答题卡！')
            exam.dto.errorMsg='找不到有效的答题卡！'
            return None, None

        # print(maxImg.shape[1]/src_img.shape[1],maxImg.shape[0]/src_img.shape[0])
        if maxImg.shape[1] < 0.5 * src_img.shape[1]:
            # QMessageBox.information(None, '提示', '可能太远导致目标识别区太小！')
            exam.dto.errorMsg='可能太远导致目标识别区太小！'
            return None, None
        #
        ratio = maxImg.shape[1] / maxImg.shape[0]
        # print(ratio)
        if ratio < 1.4 or ratio > 2.0:  # 标准卡宽高比为1.7
            # QMessageBox.information(None, '提示', '可能太斜导致目标识别区不准！')
            exam.dto.errorMsg='可能太斜导致目标识别区不准！'
            return None, None

        # 找选项区
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)
            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                ansImg_tmp = four_point_transform(src_img, approx.reshape(4, 2))
                ratio = ansImg_tmp.shape[1] / ansImg_tmp.shape[0]  # 寬高比
                if ratio > 0.9 and ratio < 1.8 and ansImg_tmp.shape[0] < maxImg.shape[0] and ansImg_tmp.shape[1] < \
                        maxImg.shape[1] and ansImg_tmp.shape[0] > maxImg.shape[0] * 2 / 3 and ansImg_tmp.shape[1] > \
                        maxImg.shape[1] / 2:
                    ansImg = ansImg_tmp
                    cv.imwrite('tmp/ansImg.png', ansImg)
                    break
        else:
            # QMessageBox.information(None, '提示', '找不到有效的答題区域！')
            exam.dto.errorMsg = '找不到有效的答題区域！'
            return None, None

        # 找学号区
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)
            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                stuImg_tmp = four_point_transform(src_img, approx.reshape(4, 2))
                ratio = stuImg_tmp.shape[1] / stuImg_tmp.shape[0]  # 寬高比
                if ratio > 0.4 and ratio < 1 and stuImg_tmp.shape[0] < ansImg.shape[0] and stuImg_tmp.shape[1] < \
                        ansImg.shape[1] and stuImg_tmp.shape[0] > maxImg.shape[0] / 4 and stuImg_tmp.shape[1] > \
                        maxImg.shape[1] / 7:
                    stuImg = stuImg_tmp
                    # cv.imwrite('tmp/stuImg.png', stuImg)
                    break
        else:
            exam.dto.errorMsg ='找不到有效的学号区域！'
            # QMessageBox.information(None, '提示', '找不到有效的学号区域！')
            return None, None

        return ansImg, stuImg

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
        self.updateClassname()
        # 连接阅卷结果库
        self.scanDB = ScanDB()
        # 连接成绩库
        self.scoreDB = ScoreDB()
        # 创建阅卷面板(连接数据源、 安装控制器）
        self.scanWin = CamMainWindow(self.dto, self)
        # 创建阅卷逻辑块（连接数据源）
        self.examServ = ExamService(self.dto)

    def updateClassname(self):
        self.dto.allClassname = self.stuDB.queryClassname()

    def startThread(self):
        self.workThread=WorkThread()
        self.workThread.start()
        self.workThread.trigger.connect(self.threadStop)

    def threadStop(self):
        self.workThread.quit()
        QMessageBox.information(None, '提示', '线程已结束！')


    def startMarking(self, ansImg,stuImg):#自适应阈值批量阅卷并做各种记录和保存处理
        self.scanWin.statusBar().showMessage('')#清除状态栏信息
        self.dto.testFlag = False  # 关闭测试开关
        self.scanWin.label_4.clear()  # 清除错误文件显示
        failedCount = 0  # 重置错误文件计数
        successedCount = 0  # 重置正确文件计数
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
            failedCount, successedCount,self.markingResult,confirmResult= self.autoScan(ansImg,stuImg, failedCount, successedCount)
            # 记录该文件阅卷结果
            if confirmResult==0 and self.markingResult[4]==-4:#重复，选择了计入失败，不覆盖，改变标志为-5
                self.markingResult[4]=-5
                self.dto.markingResultView.append([0,'來自拍照',self.markingResult])
            elif self.markingResult!=0:
                self.dto.markingResultView.append([0,'來自拍照',self.markingResult])
            QApplication.processEvents()  # 停顿刷新界面
            return True
        except Exception as e:
            logging.basicConfig(filename='error.log', filemode='w', level=logging.DEBUG)
            logging.debug(traceback.format_exc())
            # traceback.print_exc()
            QMessageBox.information(None, '提示', '此图片阅卷失败！错误是：' + str(e))

    def marking(self, ansImg,stuImg):  # 阅单卡
        ID, choices, score = self.examServ.marking(ansImg,stuImg)

        # 无法识别图片，直接返回0
        if ID is None and choices is None and score is None:
            return 0  # 无法识别

        classname = self.dto.classname
        examID = self.dto.examID

        if ID != '':
            stuID = int(ID[self.dto.cfg.CLASS_BITS:(self.dto.cfg.CLASS_BITS + self.dto.cfg.STU_BITS)])  ##按位截取学号并转换成数字
        else:
            return [0, choices, score, '未识别出学号',-1 ]  # 未识别出学号

        got_classID = ID[0:self.dto.cfg.CLASS_BITS]  # 按位截取班级

        if len(self.stuDB.queryClassnameByClassID(got_classID))>1:
            QMessageBox.information(None, '提示', '班级库有错，一个班级代号不能对应多个班级！')
            return 0

        if got_classID != '':  # 对比班级
            if {(classname,)} != self.stuDB.queryClassnameByClassID(got_classID):
                return [stuID, choices, score, '班级有错',-2]  # 班级冲突或无法识别

        # 根据班級查姓名
        result = self.stuDB.checkDataByClassname(stuID, classname)
        if not result:
            return [ stuID, choices, score, '姓名未查到',-3]  # 学号不存在
        stuName = result[0][2]

        result = self.scanDB.checkData(stuID, examID, classname)
        if result:
            return [stuID, choices, score, stuName,-4 ]  # 重复阅卷或者学号涂重

        return [ stuID, choices, score, stuName,1]  # 成功

    def autoScan(self, ansImg,stuImg, failedCount, successedCount):#自适应阈值扫描
        confirmResult=1#手动确认结果，无需手动调节的都默认计入成功！
        retry_flag = 1  # 重试标识
        for a in range(2, 8):  # 程序自行尝试调节阈值
            self.dto.answerThreshhold = a / 10  # 获取阈值
            self.dto.nowPaper.multiChoiceCount = 0  # 重置多选计数器
            self.dto.nowPaper.noChoiceCount = 0  # 重置无选项计数器
            self.markingResult = self.marking(ansImg,stuImg)  # 阅卷
            QApplication.processEvents()  # 停顿刷新界面
            if self.markingResult == 0:  # 无法识别图片，直接计入失败跳过调节阈值
                retry_flag=0#不再重试
                break
            if self.markingResult[4] == -2:# 班级冲突
                retry_flag=0#不再重试
                failedCount += 1
                # QMessageBox.information(None, '提示', '学生涂的班级和老师选的班级不一致，直接计入失败！')
                break
            if self.markingResult[4] == -1 or self.markingResult[4]==-3:  # 学号无法识别或学号查不到，则跳出循环，手动调节
                retry_flag = 1  # 重试
                # QMessageBox.information(None, '提示', '请确认班级或学号是否涂的有问题，可通过调节阈值重试，如果确实有问题，建议直接计入失败！')
                break
            if self.comparison(self.markingResult[1]):  # 比对所有单选的序号是否一致，如果一致说明阈值适合则结束
                if self.markingResult[4] == -4:  # 重复阅卷或者学号涂重
                    self.dto.bestAnswerThreshhold = a / 10  # 保存最优阈值
                    retry_flag = 1  # 重试
                    # QMessageBox.information(None, '提示', '该学号已阅过，请确实此学生是否错涂别人的学号，计入成功则覆盖，计入失败则不保存！')
                else:
                    successedCount += 1
                    retry_flag = 0
                    self.dto.bestAnswerThreshhold = a / 10  # 保存最优阈值
                    self.saveMarkingData(*self.markingResult)#成功则保存数据
                break
        if retry_flag == 1:#手动调节阈值
            # 如果程序调节失败，操作者自行调节阈值
            confirmResult= self.confirmMarking(ansImg,stuImg)
            if confirmResult==1:#计入成功
                successedCount += 1
                self.saveMarkingData(*self.markingResult)  # 选择计入成功则保存数据
            elif confirmResult==0 :#计入失败
                failedCount += 1
        return failedCount, successedCount,self.markingResult,confirmResult

    def comparison(self,choices):#对比标准答案和读卡结果所有单选的序号是否一致
        for n in self.dto.STAND_ONE_ANSWER_ORDER:
            if len(choices[n-1][1]) ==1:#判断选项长度是否也为1个
                continue
            else:
                return False#有一个不一样就认为不一致
        else:
            return True

    # 调节阈值窗口
    def confirmMarking(self, ansImg,stuImg):
        dialog = ThreshWindow(self.dto, ansImg,stuImg, self.scanWin)
        result = dialog.exec_()
        return result

    # 保存阅卷数据
    def saveMarkingData(self, stuID, choices, score, stuName,flag):
        classname = self.dto.classname
        examID = self.dto.examID
        # 阅卷重复
        if flag==-4:
            # 更新数据
            for choice in choices:
                self.scanDB.updateDB(stuID, choice[0], choice[1])  # 学号，题号，答案
            # 分数更新
            self.scoreDB.updateDB(stuID, score)  # 学号，分数
        else:
            # 答案入库，choice[0]是题号，choice[1]是填涂选项
            for choice in choices:
                self.scanDB.insertDB(examID, classname, stuID, stuName, choice[0], choice[1])
            # 分数入库
            self.scoreDB.insertDB(classname, stuID, stuName, score, examID)

    def makeScoreReport(self):
        # 初始化报表文件
        try:
            reportFile = ScoreReportForm()
            #查询分数
            scoreList=self.scoreDB.queryScore(self.dto.classname, self.dto.examID)#根据班级，考试时间查成绩
            if not scoreList:
                QMessageBox.information(None, '提示', '没有查询到对应班级和日期的阅卷数据！')
                return
            stuList=self.stuDB.queryStuByClassname(self.dto.classname)#根据班级查名单
            for stu in stuList:#stu内数据分别为userid INTEGER  primary key AUTOINCREMENT ,stuid int,name varchar(20),gender varchar(4),classid varchar(20))
                for scor in scoreList:#score内数据分别为scoreID ,classID varchar(20),stuID int,name varchar(20),score int,examID varchar(8))
                    if stu[1]==scor[2] and stu[2]==scor[3]: #如果姓名和学号一致
                        break
                else:
                    scoreList.append([0,self.dto.classname,stu[1],stu[2],0,self.dto.examID])
            reportFile.makeScoreReport(scoreList)
        except Exception as e:
            QMessageBox.information(None, '错误:', "意外错误！错误是：" + str(e) + "！")

    def makePaperReport(self):
        # 初始化报表文件
        try:
            reportFile = PaperReportForm()
            stu_count=self.scanDB.queryPersonCount(self.dto.examID,self.dto.classname)
            if not stu_count:
                QMessageBox.information(None, '提示', '没有查询到对应班级和日期的阅卷数据！')
                return
            ques_count=len(self.dto.nowAnswer)
            paperResult=[]
            for quesid in range(1,ques_count+1):
                correct_ans=self.dto.nowAnswer.get(quesid)[0]
                correct_count=len(self.scanDB.queryCorrectData(self.dto.classname,self.dto.examID,quesid,correct_ans))/stu_count
                A_count = len(self.scanDB.queryData(self.dto.classname, self.dto.examID, quesid, 'A'))/stu_count
                B_count = len(self.scanDB.queryData(self.dto.classname, self.dto.examID, quesid, 'B'))/stu_count
                C_count = len(self.scanDB.queryData(self.dto.classname, self.dto.examID, quesid, 'C'))/stu_count
                D_count = len(self.scanDB.queryData(self.dto.classname, self.dto.examID, quesid, 'D'))/stu_count
                #转换成百分数
                correct_count = "{:.2%}".format(correct_count)
                A_count = "%.2f%%" % (A_count * 100)
                B_count = "%.2f%%" % (B_count * 100)
                C_count = "%.2f%%" % (C_count * 100)
                D_count = "%.2f%%" % (D_count * 100)
                #根据模板存放需要的数据：考试时间，班级，题号，正确答案，正确率，A选项率，B选项率，C选项率，D选项率,总人数，总题数
                paperResult.append([self.dto.examID,self.dto.classname,quesid,correct_ans,correct_count,A_count,B_count,C_count,D_count,stu_count,ques_count])
            reportFile.makePaperReport(paperResult)
        except Exception as e:
            # traceback.print_exc()
            QMessageBox.information(None, '错误:', "意外错误！错误是：" + str(e) + "！")

    def makeSaveAsReport(self):
        # 初始化报表文件
        try:
            reportFile = SaveAsReport()
            reportFile.makeSaveAsReport(self.dto.markingResultView,self.dto.classname,self.dto.examID)
        except Exception as e:
            # traceback.print_exc()
            QMessageBox.information(None, '错误:', "意外错误！错误是：" + str(e) + "！")



    def test(self, file):
        try:
            choices=self.examServ.test(file)

            if choices is None:
                return
            answer = {}

            while 1:#删除末尾答案为空的题目
                if choices[-1][1]=='':
                    choices.pop()
                else:
                    break

            for c in choices:
                answer[c[0]] = (c[1], self.dto.cfg.PER_ANS_SCORE, self.dto.cfg.PART_ANS_SCORE)

            self.dto.nowAnswer = answer
            self.dto.STAND_ONE_ANSWER_ORDER=[]#计算并保存标准答案长度为1的题号
            for i in range(len(self.dto.nowAnswer)):
                ans = self.dto.nowAnswer[i + 1][0]
                if len(ans)==1:
                    self.dto.STAND_ONE_ANSWER_ORDER.append(i+1)
        except Exception as e:
            # traceback.print_exc()
            QMessageBox.information(None, '错误:', "意外错误！错误是：" + str(e) + "！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exam=ExamControl()
    sys.exit(app.exec_())
