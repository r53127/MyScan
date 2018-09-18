import cv2 as cv

class ExamPaper():
    def __init__(self):
        self.img=None

    def init(self, imgFile):
        self.img = cv.imread(imgFile)


    def getMaxContour(self):
        print('获取最大轮廓')


    def getAnswerContour(self):
        print('获取答题区域')

    def getAnswers(self):
        print('获取所有答题气泡')






