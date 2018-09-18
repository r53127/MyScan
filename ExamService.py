class ExamService():
    def __init__(self, dto):
        self.dto = dto

    def marking(self):
        #获取最大轮廓
        self.dto.currentPaper.getMaxContour()

        #获取答题区域
        self.dto.currentPaper.getAnswerContour()


        #获取所有答题气泡
        answers=self.dto.currentPaper.getAnswers()

        #进行答案比对
        right_answers=self.checkAnswer(answers)

        #判分
        self.getScore(right_answers)


    def checkAnswer(self, answers):
        print('进行答案比对')

    def getScore(self, right_answers):
        print('判分')

