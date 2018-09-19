ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}
ANSWER_CHAR = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}


class ExamService():
    def __init__(self, dto):
        self.dto = dto

    def marking(self):
        # 获取最大轮廓
        maxcnt = self.dto.currentPaper.getMaxContour()

        # 获取答题区域
        choiceCnts = self.dto.currentPaper.getChoiceContour(maxcnt)

        # 获取所有答题气泡
        choices = self.dto.currentPaper.getChoices(choiceCnts)

        # 进行答案比对、判分
        print(self.getScore(choices))

    def getScore(self, choices):
        print('判分')
        correct_count = 0
        for choice in choices:
            if ANSWER_KEY.get(choice[0]) == choice[1]:
                correct_count += 1
        return correct_count / len(ANSWER_KEY) * 100
