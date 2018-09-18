class ExamService():
    def __init__(self, dto):
        self.dto = dto

    def marking(self):
        #获取最大轮廓
        maxcnt=self.dto.currentPaper.getMaxContour()

        #获取答题区域
        qus_cnt=self.dto.currentPaper.getAnswerContour(maxcnt)


        #获取所有答题气泡
        answers=self.dto.currentPaper.getAnswers(qus_cnt)

        #进行答案比对
        right_answers=self.dto.currentPaper.checkAnswer(answers)

        #判分
        self.dto.currentPaper.getScore(right_answers)


