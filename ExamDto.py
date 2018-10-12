from ExamPaper import ExamPaper


class ExamDto():
    def __init__(self):
        self.nowAnswer=None#标准答案
        self.failedFiles=[]
        self.errorMsg=''
        self.examID=''
        self.classID=''
        #暂存所有的班级名称，用以初始化和刷新班级下拉列表
        self.allClassID=set()
        self.answerThreshhold=None
        self.testFile=''
        self.testFlag=False #调试模式
        self.nowPaper=ExamPaper(self)
