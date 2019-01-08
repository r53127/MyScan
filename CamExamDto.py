from CamExamPaper import ExamPaper
from CamconfigFile import Config


class ExamDto():
    def __init__(self):
        self.cfg=Config()
        self.nowAnswer=None#标准答案
        self.errorMsg=''
        self.examID=''
        self.classname=''
        #暂存所有的班级名称，用以初始化和刷新班级下拉列表
        self.allClassname=set()
        self.answerThreshhold=None#全局答案阈值
        self.bestAnswerThreshhold=None#最优答案阈值
        self.testFile=None
        self.testFlag=False #调试模式
        self.nowPaper=ExamPaper(self)
        self.STAND_ONE_ANSWER_ORDER = None#标准答案为单选的题号
        self.hideAnswerFlag=0#消息区隐藏导入答案标识
        self.markingResultView=[]
        self.camImg=None
        self.ansImg=None
        self.stuImg=None
        self.isReading=False

