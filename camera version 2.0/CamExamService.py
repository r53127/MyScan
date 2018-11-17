class ExamService():
    def __init__(self, dto):
        self.dto = dto

    def marking(self,ansImg,stuImg):
        # # 获取目标区域：答题区和学号区
        # src_img=self.dto.nowPaper.initImg(imgFile)
        # answer_img, stu_Img = self.dto.nowPaper.get_roi_img(src_img)

        if ansImg is None:
            return None,None,None

        # 获取学号
        ID = self.dto.nowPaper.getStuID(stuImg)
        # 获取答题结果
        choices,score = self.dto.nowPaper.getChoicesAndScore(ansImg)

        return ID,choices,score

    def test(self, imgFile):
        # 初始化一张试卷
        self.dto.nowPaper.initPaper()
        # 读图
        src_img=self.dto.nowPaper.initImg(imgFile)
        # 获取答题卡上的答题和学号区域
        answer_img, stu_Img = self.dto.nowPaper.get_roi_img(src_img)
        if answer_img is None or stu_Img is None:
            return
        self.dto.nowPaper.getStuID(stu_Img)
        choices=self.dto.nowPaper.getChoicesAndScore(answer_img)
        return choices
