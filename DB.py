from PyQt5.QtWidgets import QMessageBox
from openpyxl import load_workbook


class StudentDB():
    pass


class AnswerDB():
    @classmethod
    def importAnswer(cls, file):
        answer = {}
        wb = load_workbook(file)
        sheet = wb["Sheet1"]
        # for i in range(2, sheet.max_row):
        #     answer[sheet["A%d" % i].value] = (sheet["B%d" % i].value, sheet['C%d' % i].value) ## 第一种方法：%字符串占位操作符
        if sheet['A1'].value !='题号':
            QMessageBox.information(None, '提示', '这不是有效的答案文件！')
            return None
        for row in sheet.rows: #第二种方法使用rows属性
            if row[0].value=='题号':
                continue
            if row[0].value is not None:
                answer[row[0].value]=(row[1].value,row[2].value)
        return answer
