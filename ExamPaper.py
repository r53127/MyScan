import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import QMessageBox
from imutils import contours
from imutils.perspective import four_point_transform

ANSWER_CHAR = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}
#行數
ANSWER_ROWS = 20
#列数
ANSWER_COLS = 3
ANSWER_THRESHOLD=270
#每题选项
PER_CHOICE_COUNT=4


class ExamPaper():
    def __init__(self):
        self.showingImg = None

    def cv_imread(self, file_path=""):
        img = cv.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)  # 解决不能读取中文路径问题
        return img

    def initProcess(self, imgFile):
        self.img = self.cv_imread(imgFile)
        # self.showingImg=self.img
        # cv.imshow('1.origin', self.img)
        # cv.waitKey(0)

    def test(self, imgFile):
        # 预处理获取所有轮廓
        self.initProcess(imgFile)
        # 获取答题卡上的答题和学号区域
        answer_img,stu_Img = self.get_roi_img(self.img)
        cv.imshow('answer_img', answer_img)
        cv.imshow('stu_img', stu_Img)
        cv.waitKey(0)
        # 读取答题区域的选项
        ans_choices_cnts = self.makeAnswerCnts(answer_img)
        # print(ans_choices_cnts)
        # cv.drawContours(answer_img,ans_choices_cnts,-1,(255,0,0),1)
        # cv.imshow('anser',answer_img)
        # cv.waitKey(0)
        #
        ans_choices=self.getChoices(ans_choices_cnts,answer_img)
        print(ans_choices)


        #根据答题区域大小生成每个选项的绝对坐标
    def makeAnswerCnts(self,src_img,offset=0):
        width=src_img.shape[1]
        height=src_img.shape[0]
        rows= ANSWER_ROWS * 2 + 1
        cols=ANSWER_COLS*PER_CHOICE_COUNT*2+1
        height_scale_size=height/rows
        width_scale_size=width/cols
        answerCnts=[]
        for i in range(ANSWER_COLS*PER_CHOICE_COUNT):
            for j in range(ANSWER_ROWS):
                top_left=[int((2*i+1)*width_scale_size+offset),int((2*j+1)*height_scale_size+offset)]
                top_right=[int(2*(i+1)*width_scale_size+offset),int((2*j+1)*height_scale_size+offset)]
                bottom_left=[int((2*i+1)*width_scale_size+offset),int(2*(j+1)*height_scale_size+offset)]
                bottom_right=[int(2*(i+1)*width_scale_size+offset),int(2*(j+1)*height_scale_size+offset)]
                answerCnts.append(np.array([[top_left],[top_right],[bottom_right],[bottom_left]],dtype=np.int32))
        return answerCnts


    def getChoices(self, choiceCnts, src_img):
        cv.drawContours(src_img, choiceCnts, -1, (255, 0, 0), 1)
        cv.imshow('choices', src_img)
        print('获取所有選項气泡')
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        ret, thresh2 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
        # 按坐标从上到下排序
        cv.imshow('thresh2',thresh2)
        cv.waitKey(0)
        choiceCnts = contours.sort_contours(choiceCnts, method="left-to-right")[0]
        choiceCnts = contours.sort_contours(choiceCnts, method="top-to-bottom")[0]
        # 使用np函数，按5个元素，生成一个集合
        choices = []
        # questionID为題号，j为行内序号
        for col in range(ANSWER_COLS):#列循环3列
            for row in range(ANSWER_ROWS):#行循环20行
                # 获取按从左到右的排序后的4个元素
                cnts = choiceCnts[ANSWER_COLS*PER_CHOICE_COUNT*row+PER_CHOICE_COUNT*col:ANSWER_COLS*PER_CHOICE_COUNT*row + PER_CHOICE_COUNT+PER_CHOICE_COUNT*col]
                # 遍历每一个选项
                bubble_row = []  # 暂存每行序号和像素值
                for (inlineID, c) in enumerate(cnts):#行内循环4个选项
                    # 生成一个大小与透视图一样的全黑背景图布
                    mask = np.zeros(gray.shape, dtype="uint8")
                    # 将指定的轮廓+白色的填充写到画板上,255代表亮度值，亮度=255的时候，颜色是白色，等于0的时候是黑色
                    cv.drawContours(mask, [c], -1, 255, -1)
                    # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
                    mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
                    # 获取每个答案的像素值
                    total = cv.countNonZero(mask)
                    # 存到一个数组里面，tuple里面的参数分别是，像素大小和行内序号
                    bubble_row.append((total, inlineID))
                # 行内按像素值排序
                bubble_row = sorted(bubble_row, key=lambda x: x[0], reverse=True)
                # bubble_row[0][0]為total，bubble_row[0][1]為選項號
                questionID=col*ANSWER_ROWS+row+1#计算题号
                choices.append((questionID,self.getAnswerChars(bubble_row)))
        return choices

    #根据选项的涂色阈值换算选项字母
    def getAnswerChars(self, bubble_row):
        answerChars=[]
        # bubble_row[0]為total，bubble_row[1]為選項號
        for b in bubble_row:
            if b[0]>ANSWER_THRESHOLD:
                answerChars.append(ANSWER_CHAR[b[1]])
        return answerChars

    #提取答题和学号区域
    def get_roi_img(self, src_img):
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        # 高斯滤波，清除一些杂点
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        # 自适应二值化算法
        thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 9, 9)
        image, cnts, hierarchy = cv.findContours(thresh2.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        sortcnts = sorted(cnts, key=lambda c: cv.contourArea(c), reverse=True)
        #找答题卡
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)
            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                maxImg_tmp = four_point_transform(src_img, approx.reshape(4, 2))
                ratio = maxImg_tmp.shape[1] / maxImg_tmp.shape[0]  # 寬高比
                if ratio > 1.3 and ratio < 2.0 and maxImg_tmp.shape[0] > src_img.shape[0] / 4 and maxImg_tmp.shape[1] > \
                        src_img.shape[1] / 4:
                    cv.imwrite('paper.png', maxImg_tmp)
                    maxImg = maxImg_tmp
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的答题卡！')
            return None

        # 找选项区
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)
            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                ansImg_tmp = four_point_transform(src_img, approx.reshape(4, 2))
                ratio = ansImg_tmp.shape[1] / ansImg_tmp.shape[0]  # 寬高比
                if ratio > 0.9 and ratio < 1.3 and ansImg_tmp.shape[0] < maxImg.shape[0] and ansImg_tmp.shape[1] < \
                        maxImg.shape[1] and ansImg_tmp.shape[0] > maxImg.shape[0] / 2 and ansImg_tmp.shape[1] > \
                        maxImg.shape[1] / 2:
                    ansImg = ansImg_tmp
                    cv.imwrite('ansImg.png', ansImg)
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的答題区域！')
            return None

        # 找学号区
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)
            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                stuImg_tmp = four_point_transform(src_img, approx.reshape(4, 2))
                ratio = stuImg_tmp.shape[1] / stuImg_tmp.shape[0]  # 寬高比
                if ratio > 0.4 and ratio < 1 and stuImg_tmp.shape[0] < ansImg.shape[0] and stuImg_tmp.shape[1] < \
                        ansImg.shape[1] and stuImg_tmp.shape[0] > maxImg.shape[0] / 4 and stuImg_tmp.shape[1] > \
                        maxImg.shape[1] / 7:
                    stuImg = stuImg_tmp
                    cv.imwrite('stuImg.png', stuImg)
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的学号区域！')
            return None

        return ansImg,stuImg


