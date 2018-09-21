class ExamService():
    def __init__(self, dto):
        self.dto = dto

    def marking(self):
        # 获取最大轮廓
        maxcnt = self.dto.nowPaper.getMaxContour()

        # 获取答题区域
        choiceCnts = self.dto.nowPaper.getChoiceContour(maxcnt)

        # 获取所有答题气泡
        choices = self.dto.nowPaper.getChoices(choiceCnts)

        # 进行答案比对、判分
        score = self.getScore(choices, self.dto.nowAnswer)

        # 答案、得分入库

    def getScore(self, choices, answer):
        print('判分')
        correct_count = 0
        score = 0
        for choice in choices:
            if (answer.get(choice[0]))[0] == choice[1]:
                correct_count += 1
                score += (answer.get(choice[0]))[1]
        return score
