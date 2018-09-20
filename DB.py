from openpyxl import load_workbook


class StudentDB():
    pass


class AnswerDB():
    @classmethod
    def importAnswer(cls, file):
        answer = {}
        wb = load_workbook(file)
        sheet = wb["Sheet1"]
        for i in range(2, sheet.max_row):
            answer[sheet["A%d" % i].value] = (sheet["B%d" % i].value, sheet['C%d' % i].value)
        return answer
