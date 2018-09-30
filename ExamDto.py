from ExamPaper import ExamPaper


class ExamDto():
    def __init__(self):
        self.nowPaper=ExamPaper()
        self.nowAnswer=None
        self.nowAnswerFile=None
        self.failedFiles=[]
        self.errorMsg=''


    def setCurrentPaper(self,file):
        self.nowPaper.initProcess(file)