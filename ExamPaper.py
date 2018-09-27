import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import QMessageBox
from imutils import contours
from imutils.perspective import four_point_transform

ANSWER_CHAR = {0: "A", 1: "B", 2: "C", 3: "D"}


class ExamPaper():
    def __init__(self):
        self.showingImg = None

    def cv_imread(self, file_path=""):
        img = cv.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)  # 解决不能读取中文路径问题
        return img

    def initProcess(self, imgFile):
        self.img = self.cv_imread(imgFile)
        # self.showingImg=self.img
        cv.imshow('1.origin', self.img)
        cv.waitKey(0)


    def get_max_img(self, src_img):
        maxImg=None
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        # 高斯滤波，清除一些杂点
        blur = cv.GaussianBlur(gray, (3, 3), 0)
        # 自适应二值化算法
        thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 131, 1)
        image, cnts, hierarchy = cv.findContours(thresh2.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        sortcnts=sorted(cnts,key=lambda c: cv.contourArea(c),reverse=True)
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)
            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                maxImg = four_point_transform(src_img, approx.reshape(4, 2))
                ratio=maxImg.shape[1] / maxImg.shape[0]
                print(ratio)
                if ratio>1.3 and ratio<2.0 and maxImg.shape[0] >src_img.shape[0]/4 and maxImg.shape[1] >src_img.shape[1]/4:
                    return maxImg
        else:
            QMessageBox.information(None,'提示','找不到有效的答題区域！')
            return None


    def get_roi_img(self, src_img):
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        blur = cv.GaussianBlur(gray, (3, 3), 0)
        # 自适应二值化算法
        thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 131, 1)

        r_image, cnts, r_hierarchy = cv.findContours(thresh2.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        roi_img = []
        # 按面积大小对所有的轮廓排序
        listcnt = sorted(cnts, key=cv.contourArea, reverse=True)
        dstImgCount = 3  # 获取最大的4个矩形
        for cnt in listcnt:
            if dstImgCount == 0:
                break
            peri = 0.01 * cv.arcLength(cnt, True)
            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(cnt, peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取源图内容部分
                roi_img.append(four_point_transform(src_img, approx.reshape(4, 2)))
                dstImgCount = dstImgCount - 1
        return roi_img

    def test(self, imgFile):
        # 预处理获取所有轮廓
        self.initProcess(imgFile)
        # 获取最大的答题卡区域
        self.paper_img = self.get_max_img(self.img)
        cv.imshow('paper_img', self.paper_img)
        cv.waitKey(0)
        # 找到答题卡上的答题、班级和学号区域
        self.answer_img = self.get_roi_img(self.paper_img)
        for i, c in enumerate(self.answer_img):
            cv.imshow('answer_img' + str(i), c)
            cv.waitKey(0)
        # 读取答题区域的选项
        self.ans_choices_cnts = self.getChoiceContour(self.answer_img[0])
        self.stuid_choice_cnts= self.getChoiceContour(self.answer_img[1])

        self.ans_choices=self.getChoices(self.ans_choices_cnts,self.answer_img[0])
        print(self.ans_choices)


    def getChoiceContour(self, src_img):
        print('获取答题区域')
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        ret, thresh2 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        r_image, cnts, r_hierarchy = cv.findContours(thresh2.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        choiceCnts = []
        for cxx in cnts:
            # 通过矩形，标记每一个指定的轮廓
            x, y, w, h = cv.boundingRect(cxx)
            ar = w / float(h)

            if w < 50 and h < 30 and ar >= 2 and ar <= 3.5 and w > 10 and h > 5:
                # 使用红色标记，满足指定条件的图形
                cv.rectangle(src_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv.imshow('choices', src_img)
                # 把每个选项，保存下来
                choiceCnts.append(cxx)
        print('找到的选项个数为：', len(choiceCnts))
        return choiceCnts

    def getChoices(self, choiceCnts,src_img):
        cv.drawContours(self.img,choiceCnts,-1,(0,255,0),1)
        cv.imshow('choices',self.img)
        print('获取所有選項气泡')
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        ret, thresh2 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        # 按坐标从上到下排序
        print(len(choiceCnts))
        choiceCnts = contours.sort_contours(choiceCnts, method="left-to-right")[0]
        choiceCnts = contours.sort_contours(choiceCnts, method="top-to-bottom")[0]
        # 使用np函数，按5个元素，生成一个集合
        choices = []
        # questionID为題号，j为行内序号
        for (questionID, i) in enumerate(np.arange(0, len(choiceCnts), 4)):
            # 获取按从左到右的排序后的5个元素
            cnts = choiceCnts[i:i + 4]
            # 遍历每一个选项
            bubble_row = []  # 暂存每行序号和像素值
            for (inlineID, c) in enumerate(cnts):
                print(c)
                # 生成一个大小与透视图一样的全黑背景图布
                mask = np.zeros(gray.shape, dtype="uint8")
                cv.imshow('mask',mask)
                cv.waitKey(0)
                # 将指定的轮廓+白色的填充写到画板上,255代表亮度值，亮度=255的时候，颜色是白色，等于0的时候是黑色
                cv.drawContours(mask, [c], -1, 255, -1)
                cv.imshow('draw mask',mask)
                cv.waitKey(0)
                # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
                mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
                cv.imshow('bitwise',mask)
                cv.waitKey(0)
                # 获取每个答案的像素值
                total = cv.countNonZero(mask)
                # 存到一个数组里面，tuple里面的参数分别是，像素大小和行内序号
                bubble_row.append((total, inlineID))
            # 行内按像素值排序
            bubble_row = sorted(bubble_row, key=lambda x: x[0], reverse=True)
            # 將题号和选择的序号(inlineID值）存入choice_bubble
            choice_num = bubble_row[0][1]  # [0][0]為total，[0][1]為選項號
            choices.append((questionID + 1, ANSWER_CHAR[choice_num]))  # %为字符串占位操作符
        return choices
