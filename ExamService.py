class ExamService():
    def __init__(self, dto):
        self.dto = dto

    def marking(self,imgFile):
        # 获取目标区域：答题区和学号区
        src_img=self.dto.nowPaper.initImg(imgFile)
        answer_img, stu_Img = self.dto.nowPaper.get_roi_img(src_img)
        if answer_img is None:
            return None,None,None

        # 获取学号
        stuID = self.dto.nowPaper.getStuID(stu_Img)
        # 获取答题结果
        choices,score = self.dto.nowPaper.getChoicesAndScore(answer_img)

        return stuID,choices,score

    def test(self, imgFile):
        # 预处理获取所有轮廓
        src_img=self.dto.nowPaper.initImg(imgFile)
        # 获取答题卡上的答题和学号区域
        answer_img, stu_Img = self.dto.nowPaper.get_roi_img(src_img)
        if answer_img is None or stu_Img is None:
            return
        self.dto.nowPaper.getStuID(stu_Img)
        self.dto.nowPaper.getChoicesAndScore(answer_img)
        return
