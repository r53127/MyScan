from ExamPaper import ExamPaper


class ExamDto():
    def __init__(self):
        self.nowPaper=ExamPaper()
        self.nowAnswer=None
        self.nowAnswerFile=None
        self.failedFiles=[]
        self.errorMsg=''
        self.examID=''
        self.classID=''
        #暂存所有的班级名称，用以初始化和刷新班级下拉列表
        self.allClassID=set()


    def setCurrentPaper(self,file):
        self.nowPaper.initProcess(file)