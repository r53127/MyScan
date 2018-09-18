from ExamPaper import ExamPaper


class ExamDto():
    def __init__(self):
        self.currentPaper=ExamPaper()


    def setCurrentPaper(self,file):
        self.currentPaper.initProcess(file)