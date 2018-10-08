import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox
from imutils import contours
from imutils.perspective import four_point_transform

ANSWER_CHAR = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G"}
# 行數
ANSWER_ROWS = 20
# 列数
ANSWER_COLS = 3
# 学号区excel列数
Stuid_AREA_COLS = 7
# 学号区excel行数
Stuid_AREA_ROWS = 28
# 学号第一个数字起始X偏移单元格数
ID_X_OFFSET = 2
# 学号第一个数字起始Y偏移单元格数
ID_Y_OFFSET = 3
# 学号位数
ID_BITS = 2
# 十个学号数字
NUM_BITS = 10
# 每题选项
PER_CHOICE_COUNT = 4


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
        answer_img, stu_Img = self.get_roi_img(self.img)
        if answer_img is None:
            return
        # cv.imshow('answer_img', answer_img)
        # cv.imshow('stu_img', stu_Img)
        # cv.waitKey(0)
        ans_choices = self.getChoices(answer_img)
        stuID = self.getStuID(stu_Img)
        print(ans_choices)
        print(stuID)

    # 根据答题区域大小生成每个选框的绝对坐标
    def makeAnswerCnts(self, src_img, expandingFlag=True, offset=0):
        width = src_img.shape[1]
        height = src_img.shape[0]
        rows = ANSWER_ROWS * 2 + 1
        cols = ANSWER_COLS * PER_CHOICE_COUNT * 2 + 1
        height_scale_size = height / rows
        width_scale_size = width / cols
        answerCnts = []
        for x in range(1, 2 * ANSWER_COLS * PER_CHOICE_COUNT, 2):
            for y in range(1, 2 * ANSWER_ROWS, 2):
                if expandingFlag:  # 扩大
                    top_left = [x * width_scale_size - offset, y * height_scale_size - offset]
                    top_right = [(x + 1) * width_scale_size + offset, y * height_scale_size - offset]
                    bottom_left = [x * width_scale_size - offset, (y + 1) * height_scale_size + offset]
                    bottom_right = [(x + 1) * width_scale_size + offset, (y + 1) * height_scale_size + offset]
                else:  # 缩小
                    top_left = [x * width_scale_size + offset, y * height_scale_size + offset]
                    top_right = [(x + 1) * width_scale_size - offset, y * height_scale_size + offset]
                    bottom_left = [x * width_scale_size + offset, (y + 1) * height_scale_size - offset]
                    bottom_right = [(x + 1) * width_scale_size - offset, (y + 1) * height_scale_size - offset]
                answerCnts.append(np.array([[top_left], [top_right], [bottom_right], [bottom_left]], dtype=np.int32))
        return answerCnts

    # 获取选项
    def getChoices(self, src_img):
        processed_img = cv.medianBlur(src_img, 13)
        gray = cv.cvtColor(processed_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        processed_img = cv.GaussianBlur(gray, (33, 33), 0)
        thresh2 = cv.adaptiveThreshold(processed_img.copy(), 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,
                                       503, 44)

        # # 识别所涂写区域时的膨胀腐蚀的kernel
        # ANS_IMG_KERNEL = np.ones((2, 2), np.uint8)
        # # 识别所涂写区域时的二值化参数
        # ANS_IMG_THRESHOLD = (88, 255)
        # # 识别所涂写区域时的膨胀参数
        # ANS_IMG_DILATE_ITERATIONS = 9
        # # 识别所涂写区域时的腐蚀参数
        # ANS_IMG_ERODE_ITERATIONS = 0

        # gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)
        # processed_img = cv.GaussianBlur(gray, (9, 9), 0)
        # # 通过二值化和膨胀腐蚀获得填涂区域
        # thresh2 = cv.adaptiveThreshold(processed_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 41,35)
        # thresh2 = cv.dilate(thresh2, ANS_IMG_KERNEL, iterations=ANS_IMG_DILATE_ITERATIONS)
        # thresh2 = cv.erode(thresh2, ANS_IMG_KERNEL, iterations=ANS_IMG_ERODE_ITERATIONS)

        # 坐标从上到下排序
        choiceCnts = self.makeAnswerCnts(src_img)

        self.showingImg=ExamPaper.convertImg(src_img.copy())
        # cv.drawContours(self.showingImg, choiceCnts, -1, (255, 255, 255), 1)
        # cv.imshow('choices', self.showingImg)
        cv.imwrite('tmp/ansImgThresh.png', thresh2)

        choiceCnts = contours.sort_contours(choiceCnts, method="left-to-right")[0]
        choiceCnts = contours.sort_contours(choiceCnts, method="top-to-bottom")[0]
        # 使用np函数，按5个元素，生成一个集合
        choices = []
        no_answer_count=0
        wrong_img = src_img.copy()
        # questionID为題号，j为行内序号
        for col in range(ANSWER_COLS):  # 列循环3列
            for row in range(ANSWER_ROWS):  # 行循环20行
                # 获取按从左到右的排序后的4个元素
                cnts = choiceCnts[
                       ANSWER_COLS * PER_CHOICE_COUNT * row + PER_CHOICE_COUNT * col:ANSWER_COLS * PER_CHOICE_COUNT * row + PER_CHOICE_COUNT + PER_CHOICE_COUNT * col]
                # 遍历每一个选项
                row_answers = []  # 暂存每行序号和像素值
                pixelCount = 0
                for (inlineID, c) in enumerate(cnts):  # 行内循环4个选项
                    # 生成一个大小与透视图一样的全黑背景图布
                    mask = np.zeros(gray.shape, dtype="uint8")
                    # 将指定的轮廓+白色的填充写到画板上,255代表亮度值，亮度=255的时候，颜色是白色，等于0的时候是黑色
                    cv.drawContours(mask, [c], -1, 255, -1)
                    maxPixel = cv.countNonZero(mask)
                    pixelCount += maxPixel
                    # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
                    mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
                    # 获取每个答案的像素值
                    total = cv.countNonZero(mask)
                    # 存到一个数组里面，tuple里面的参数分别是，像素大小和行内序号
                    row_answers.append((total, inlineID))
                # 行内按像素值排序
                ANSWER_THRESHOLD = pixelCount / PER_CHOICE_COUNT / 4  # 取一半作为阈值
                row_answers = sorted(row_answers, key=lambda x: x[0], reverse=True)
                questionID = col * ANSWER_ROWS + row + 1  # 计算题号
                # print('第'+str(questionID)+'题答案和阈值为：',row_answers,ANSWER_THRESHOLD)
                #以下为取最大值，实现单选
                #  row_answers[0][0]為total，row_answers[0][1]為選項號
                # choices.append((questionID, ANSWER_CHAR.get(row_answers[0][1])))
                # if row_answers[0][0]>ANSWER_THRESHOLD:
                #     choices.append((questionID, ANSWER_CHAR.get(row_answers[0][1])))
                # else:
                #     choices.append((questionID, ''))
                answer=self.getAnswerChars(row_answers, ANSWER_THRESHOLD)
                if not answer.strip():
                    cv.drawContours(wrong_img,cnts,-1,(255,0,0),2)
                    no_answer_count+=1
                choices.append((questionID,answer))
        if no_answer_count:
            self.showingImg=ExamPaper.convertImg(wrong_img)
            QMessageBox.information(None,'提示','该学生共有'+str(no_answer_count)+'个题未涂或涂的不符合要求！')
        return choices

    # 根据选项 的涂色阈值换算选项字母
    # param:ANSWER_THRESHOLD 像素阈值；每行4个选项
    def getAnswerChars(self, row_answers, ANSWER_THRESHOLD):
        answerChars = ''
        # bubble_row[0]為total，bubble_row[1]為選項號
        for b in row_answers:
            if b[0] > ANSWER_THRESHOLD:
                answerChars += ANSWER_CHAR[b[1]]
        return ''.join(sorted(list(answerChars)))  # 按字母顺序排序

    # 生成学号绝对坐标
    def makeStuidCnts(self, src_img, expandingFlag=True, offset=0):
        width = src_img.shape[1]
        height = src_img.shape[0]
        height_scale_size = height / Stuid_AREA_ROWS
        width_scale_size = width / Stuid_AREA_COLS
        stuidCnts = []
        for x in range(ID_BITS):  # x为列相对坐标:表示2位数
            for y in range(NUM_BITS):  # y为行相对坐标:表示每位10个数字
                if expandingFlag:  # 扩大
                    top_left = [(2 * x + ID_X_OFFSET) * width_scale_size - offset,
                                (2 * y + ID_Y_OFFSET) * height_scale_size - offset]
                    top_right = [(2 * x + 1 + ID_X_OFFSET) * width_scale_size + offset,
                                 (2 * y + ID_Y_OFFSET) * height_scale_size - offset]
                    bottom_left = [(2 * x + ID_X_OFFSET) * width_scale_size - offset,
                                   (2 * y + ID_Y_OFFSET + 1) * height_scale_size + offset]
                    bottom_right = [(2 * x + 1 + ID_X_OFFSET) * width_scale_size + offset,
                                    (2 * y + ID_Y_OFFSET + 1) * height_scale_size + offset]
                else:  # 缩小
                    top_left = [(2 * x + ID_X_OFFSET) * width_scale_size + offset,
                                (2 * y + ID_Y_OFFSET) * height_scale_size + offset]
                    top_right = [(2 * x + 1 + ID_X_OFFSET) * width_scale_size - offset,
                                 (2 * y + ID_Y_OFFSET) * height_scale_size + offset]
                    bottom_left = [(2 * x + ID_X_OFFSET) * width_scale_size + offset,
                                   (2 * y + ID_Y_OFFSET + 1) * height_scale_size - offset]
                    bottom_right = [(2 * x + 1 + ID_X_OFFSET) * width_scale_size - offset,
                                    (2 * y + ID_Y_OFFSET + 1) * height_scale_size - offset]
                stuidCnts.append(np.array([[top_left], [top_right], [bottom_right], [bottom_left]], dtype=np.int32))
        return stuidCnts

    # 获取学号
    def getStuID(self, src_img):
        processed_img = cv.medianBlur(src_img, 3)
        gray = cv.cvtColor(processed_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        processed_img = cv.GaussianBlur(gray, (3, 3), 0)
        thresh2 = cv.adaptiveThreshold(processed_img.copy(), 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,
                                       85, 18)
        # 按坐标从上到下排序
        # cv.imshow('thresh2',thresh2)
        # cv.waitKey(0)
        stuidCnts = self.makeStuidCnts(src_img)
        # cv.drawContours(src_img, stuidCnts, -1, (255, 0, 0), 1)
        # cv.imshow('i', src_img)
        # 使用np函数，按5个元素，生成一个集合
        first_num = []
        second_num = []
        m = 0  # 十位辅助计数
        n = 0  # 个位辅助计数
        for (i, c) in enumerate(stuidCnts):
            # 生成一个大小与透视图一样的全黑背景图布
            mask = np.zeros(gray.shape, dtype="uint8")
            # 将指定的轮廓+白色的填充写到画板上,255代表亮度值，亮度=255的时候，颜色是白色，等于0的时候是黑色
            cv.drawContours(mask, [c], -1, 255, -1)
            # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
            mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
            # 获取每个答案的像素值
            total = cv.countNonZero(mask)
            # 存到一个数组里面，tuple里面的参数分别是，像素大小和行内序号
            if i < 10:
                first_num.append((m, total))
                # print('firnum is :', first_num)
                m += 1
            else:
                second_num.append((n, total))
                # print('secnum is :', second_num)
                n += 1
        # 按像素值排序
        first_num = sorted(first_num, key=lambda x: x[1], reverse=True)
        second_num = sorted(second_num, key=lambda x: x[1], reverse=True)
        return str(first_num[0][0]) + str(second_num[0][0])

    # 提取答题和学号区域
    def get_roi_img(self, src_img):
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        # 高斯滤波，清除一些杂点
        blur = cv.GaussianBlur(gray, (5, 5), 0)
        # 自适应二值化算法
        thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 9, 9)
        image, cnts, hierarchy = cv.findContours(thresh2.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        sortcnts = sorted(cnts, key=lambda c: cv.contourArea(c), reverse=True)
        # 找答题卡
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)

            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                maxImg_tmp = four_point_transform(src_img, approx.reshape(4, 2))
                # cv.drawContours(src_img,[approx.reshape(4,2)],-1,(255,0,0),1)
                # cv.imshow('approx',src_img)
                ratio = maxImg_tmp.shape[1] / maxImg_tmp.shape[0]  # 寬高比
                if ratio > 1.3 and ratio < 2.0 and maxImg_tmp.shape[0] > src_img.shape[0] / 4 and maxImg_tmp.shape[1] > \
                        src_img.shape[1] / 4:
                    cv.imwrite('tmp/paper.png', maxImg_tmp)
                    maxImg = maxImg_tmp
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的答题卡！')
            return None,None

        # print(maxImg.shape[1]/src_img.shape[1],maxImg.shape[0]/src_img.shape[0])
        if maxImg.shape[1]<0.8*src_img.shape[1]:
            QMessageBox.information(None, '提示', '可能太远导致目标识别区太小！')
            return None,None

        ratio=maxImg.shape[1]/maxImg.shape[0]
        # print(ratio)
        if ratio<1.4 or ratio>2.0:#标准卡宽高比为1.7
            QMessageBox.information(None, '提示', '可能太斜导致目标识别区不准！')
            return None,None


        # 找选项区
        for i in range(len(sortcnts)):
            peri = 0.1 * cv.arcLength(sortcnts[i], True)
            # 获取多边形的所有定点，如果是四个定点，就代表是矩形
            approx = cv.approxPolyDP(sortcnts[i], peri, True)
            if len(approx) == 4:  # 矩形
                # 透视变换提取原图内容部分
                ansImg_tmp = four_point_transform(src_img, approx.reshape(4, 2))
                ratio = ansImg_tmp.shape[1] / ansImg_tmp.shape[0]  # 寬高比
                if ratio > 0.9 and ratio < 1.8 and ansImg_tmp.shape[0] < maxImg.shape[0] and ansImg_tmp.shape[1] < \
                        maxImg.shape[1] and ansImg_tmp.shape[0] > maxImg.shape[0]*2/3 and ansImg_tmp.shape[1] > \
                        maxImg.shape[1] / 2:
                    ansImg = ansImg_tmp
                    cv.imwrite('tmp/ansImg.png', ansImg)
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的答題区域！')
            return None,None

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
                    cv.imwrite('tmp/stuImg.png', stuImg)
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的学号区域！')
            return None,None

        return ansImg, stuImg


    @staticmethod
    # 功能：把矩形框（x,y,w,h)转变为ndarray
    def rect2ndarray(rect):
        x, y, w, h = rect
        top_left = [x, y]
        top_right = [x + w, y]
        bottom_right = [x + w, y + h]
        bottom_left = [x, y + h]
        return np.array([[top_left], [top_right], [bottom_right], [bottom_left]], dtype=np.int32)

    @staticmethod
    def convertImg(img):
        height, width, bytesPerComponent = img.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cv.cvtColor(img, cv.COLOR_BGR2RGB, img)
        # 转为QImage对象
        showimg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        showpix = QPixmap.fromImage(showimg)
        return showpix
