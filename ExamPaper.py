import numpy as np

import cv2 as cv
from imutils import contours
from imutils.perspective import four_point_transform




class ExamPaper():
    def __init__(self):
        self.showingImg=None

    def initProcess(self, imgFile):
        self.img = cv.imread(imgFile)
        self.showingImg=self.img
        self.gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)        # 转化成灰度图片
        self.gaussian_bulr = cv.GaussianBlur(self.gray, (5, 5), 0)  # 高斯模糊
        self.edged = cv.Canny(self.gaussian_bulr, 75, 200)  # 边缘检测,灰度值小于2参这个值的会被丢弃，大于3参这个值会被当成边缘，在中间的部分，自动检测

    def getMaxContour(self):
        print('获取最大轮廓')
        image, cnts, hierarchy = cv.findContours(self.edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        maxcnt = max(cnts, key=lambda c: cv.contourArea(c))
        return maxcnt


    def getChoiceContour(self, cnt):
        print('获取答题区域')
        peri = 0.01 * cv.arcLength(cnt, True)
        # 获取多边形的所有定点，如果是四个定点，就代表是矩形
        approx = cv.approxPolyDP(cnt, peri, True)
        if len(approx) == 4:  # 矩形
            # 透视变换提取灰度图内容部分
            self.tx_sheet = four_point_transform(self.gray, approx.reshape(4, 2))
            # 使用ostu二值化算法对灰度图做一个二值化处理
            self.ret,self.thresh2 = cv.threshold(self.tx_sheet, 0, 255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
            # 继续寻找轮廓
            r_image, r_cnt, r_hierarchy = cv.findContours(self.thresh2.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            print("找到轮廓个数：",len(r_cnt))
            choiceCnts = []
            for cxx in r_cnt:
                # 通过矩形，标记每一个指定的轮廓
                x, y, w, h = cv.boundingRect(cxx)
                ar = w / float(h)

                if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
                    # 使用红色标记，满足指定条件的图形
                    # cv.rectangle(ox_sheet, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # 把每个选项，保存下来
                    choiceCnts.append(cxx)
        return choiceCnts

    def getChoices(self, choiceCnts):
        print('获取所有選項气泡')
        # 按坐标从上到下排序
        choiceCnts = contours.sort_contours(choiceCnts, method="top-to-bottom")[0]
        # 使用np函数，按5个元素，生成一个集合
        choices=[]
        #q为行号，j为行内序号
        for (q, i) in enumerate(np.arange(0, len(choiceCnts), 5)):
            # 获取按从左到右的排序后的5个元素
            cnts = contours.sort_contours(choiceCnts[i:i + 5])[0]
            # 遍历每一个选项
            bubble_row = []#暂存每行序号和像素值
            for (j, c) in enumerate(cnts):
                # 生成一个大小与透视图一样的全黑背景图布
                mask = np.zeros(self.tx_sheet.shape, dtype="uint8")
                # 将指定的轮廓+白色的填充写到画板上,255代表亮度值，亮度=255的时候，颜色是白色，等于0的时候是黑色
                cv.drawContours(mask, [c], -1, 255, -1)
                # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
                mask = cv.bitwise_and(self.thresh2, self.thresh2, mask=mask)
                # 获取每个答案的像素值
                total = cv.countNonZero(mask)
                # 存到一个数组里面，tuple里面的参数分别是，像素大小和行内序号
                bubble_row.append((total, j))
            #行内按像素值排序
            bubble_row=sorted(bubble_row,key=lambda x: x[0],reverse=True)
            # 將题号和选择的序号(j值）存入choice_bubble
            choice_num=bubble_row[0][1]
            choices.append((q,choice_num))
        return choices







