class ExamService():
    def __init__(self, dto):
        self.dto = dto

    def marking(self):
        # 获取目标区域：答题区和学号区
        answer_img, stu_Img = self.dto.nowPaper.get_roi_img(self.dto.nowPaper.img)
        #获取答题结果
        choices=self.dto.nowPaper.getChoices(answer_img)
        #获取学号
        stuID=self.dto.nowPaper.getStuID(stu_Img)
        return choices,stuID


    def test(self,file):
        self.dto.nowPaper.test(file)
