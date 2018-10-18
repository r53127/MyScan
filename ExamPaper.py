import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMessageBox
from imutils import contours
from imutils.perspective import four_point_transform

# 选项字母表
ANSWER_CHAR = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
# 十个学号数字
NUM_BITS = 10

class ExamPaper():
    def __init__(self, dto):
        self.dto = dto
        #加载配置
        self.loadConfig()
        # 初始化試卷
        self.initPaper()

    def loadConfig(self):
        # 行數
        self.ANSWER_ROWS = self.dto.cfg.ANSWER_ROWS
        # 列数
        self.ANSWER_COLS = self.dto.cfg.ANSWER_COLS
        # 学号区excel列数
        self.Stuid_AREA_COLS = self.dto.cfg.Stuid_AREA_COLS
        # 学号区excel行数
        self.Stuid_AREA_ROWS = self.dto.cfg.Stuid_AREA_ROWS
        # 学号第一个数字起始X偏移单元格数
        self.ID_X_OFFSET = self.dto.cfg.ID_X_OFFSET
        # 学号第一个数字起始Y偏移单元格数
        self.ID_Y_OFFSET = self.dto.cfg.ID_Y_OFFSET
        # 每题选项
        self.PER_CHOICE_COUNT = self.dto.cfg.PER_CHOICE_COUNT

    def initPaper(self):
        self.stuID = None
        self.score = None
        self.showingImg = None
        self.showingImgThresh = None
        self.showingPaperThresh = None
        self.showingWrong = None
        self.showingStu = None
        self.showingChoices = None
        self.showingPaperCnts = None
        self.multiChoiceCount = 0
        self.noChoiceCount = 0

    def cv_imread(self, file_path=""):
        img = cv.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)  # 解决不能读取中文路径问题
        return img

    def initImg(self, imgFile):
        src_img = self.cv_imread(imgFile)
        self.showingImg = ExamPaper.convertImg(src_img)
        return src_img

    # 根据答题区域大小生成每个选框的绝对坐标
    def makeAnswerCnts(self, src_img, expandingFlag=True, offset=0):
        width = src_img.shape[1]
        height = src_img.shape[0]
        rows = self.ANSWER_ROWS * 2 + 1
        cols = self.ANSWER_COLS * self.PER_CHOICE_COUNT * 2 + 1
        height_scale_size = height / rows
        width_scale_size = width / cols
        answerCnts = []
        for x in range(1, 2 * self.ANSWER_COLS * self.PER_CHOICE_COUNT, 2):  # 列循环
            for y in range(1, 2 * self.ANSWER_ROWS, 2):  # 行循环
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
    def getChoicesAndScore(self, src_img):
        # processed_img = cv.medianBlur(src_img, 13)
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片

        # cv.imwrite('gray.png',gray)
        processed_img = cv.GaussianBlur(gray, (3, 3), 0)
        thresh2 = cv.adaptiveThreshold(processed_img.copy(), 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,
                                       157, 19)
        # cv.imshow('paperth2',thresh2)
        self.showingPaperThresh = ExamPaper.convertImg(thresh2)
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
        # cv.imwrite('tmp/ansImgThresh.png', thresh2)

        showingPaperCnts = src_img.copy()
        showingChoices = src_img.copy()

        choiceCnts = contours.sort_contours(choiceCnts, method="left-to-right")[0]
        choiceCnts = contours.sort_contours(choiceCnts, method="top-to-bottom")[0]

        if self.dto.nowAnswer is None:  # 如果未导入答案，标注所有的定位框
            cv.drawContours(showingPaperCnts, choiceCnts, -1, (255, 0, 0), 2)

        # 使用np函数，按5个元素，生成一个集合
        choices = []
        wrong_img = src_img.copy()
        # questionID为題号
        questionID = 0
        for col in range(self.ANSWER_COLS):  # 列循环3列
            if self.dto.nowAnswer is not None:  # 如果已导入答案，如果题号等于最大题数，也停止列循环
                if questionID == len(self.dto.nowAnswer):
                    break
            for row in range(self.ANSWER_ROWS):  # 行循环20行
                # 获取按从左到右的排序后的4个元素
                cnts = choiceCnts[
                       self.ANSWER_COLS * self.PER_CHOICE_COUNT * row + self.PER_CHOICE_COUNT * col:self.ANSWER_COLS * self.PER_CHOICE_COUNT * row + self.PER_CHOICE_COUNT + self.PER_CHOICE_COUNT * col]
                # 遍历每一个选项
                row_choices = []  # 暂存每行序号和像素值
                pixelCount = 0
                for (inlineID, c) in enumerate(cnts):  # 行内循环4个选项
                    # 生成一个大小与透视图一样的全黑背景图布
                    mask = np.zeros(gray.shape, dtype="uint8")
                    # 将指定的轮廓+白色的填充写到画板上,255代表亮度值，亮度=255的时候，颜色是白色，等于0的时候是黑色
                    cv.drawContours(mask, [c], -1, 255, -1)
                    # cv.imshow('c', mask)
                    # cv.waitKey(0)
                    maxPixel = cv.countNonZero(mask)  # 单个蒙板的像素
                    # print(maxPixel)
                    pixelCount += maxPixel  # 累加最大像素值
                    # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
                    mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
                    # cv.imshow('m', mask)
                    # cv.waitKey(0)
                    # 获取每个答案的像素值
                    total = cv.countNonZero(mask)
                    # 存到一个数组里面，tuple里面的参数分别是，像素大小和行内序号
                    row_choices.append((total, inlineID, c))  # 分别存放总像素值，行内序号，轮廓值
                    if self.dto.nowAnswer:  # 如果已导入答案，则标注相应题数的标注框
                        cv.drawContours(showingPaperCnts, [c], 0, (255, 0, 0), 2)
                # 行内按像素值排序
                CHOICE_THRESHOLD = pixelCount / self.PER_CHOICE_COUNT * self.dto.answerThreshhold  # 取阈值
                row_choices = sorted(row_choices, key=lambda x: x[0], reverse=True)
                questionID = col * self.ANSWER_ROWS + row + 1  # 计算题号
                # print('第'+str(questionID)+'题答案和阈值为：',row_choices,CHOICE_THRESHOLD)
                answerAndCnts = self.getAnswerCharsAndCnts(row_choices, CHOICE_THRESHOLD)  # 得到所选答案和轮廓

                # 显示未选
                if not answerAndCnts[0].strip():  # 如果所选答案为空，则进行画框标注，同时未涂总数+1计数
                    cv.drawContours(wrong_img, cnts, -1, (0, 0, 255), 2)
                    self.noChoiceCount += 1
                # 显示多选
                if len(answerAndCnts[0]) > 1:
                    cv.drawContours(showingChoices, answerAndCnts[1], -1, (0, 0, 255), 2)  # 红色显示多选框
                    self.multiChoiceCount += 1
                else:
                    cv.drawContours(showingChoices, answerAndCnts[1], -1, (0, 255, 255), 2)  # 黄色显示单选框

                choices.append((questionID, answerAndCnts[0]))  # 所选结果存入 题号+答案
                if self.dto.nowAnswer is not None:  # 如果已导入答案，如果题号等于最大题数，就停止行循环
                    if questionID == len(self.dto.nowAnswer):
                        break
        # 判分
        if not self.dto.testFlag:
            score = self.getScore(choices, self.dto.nowAnswer)
            self.dto.nowPaper.score = score
        # 显示图像
        self.showingPaperCnts = ExamPaper.convertImg(showingPaperCnts)  # 显示所有定位标注框图片
        self.showingWrong = ExamPaper.convertImg(wrong_img)  # 显示未涂或者未达标的选项标注框图片
        self.showingChoices = ExamPaper.convertImg(showingChoices)  # 显示已选标注框图片

        if self.dto.testFlag:
            return choices
        else:
            return choices, score

    # 根据选项 的涂色阈值换算选项字母
    # param:ANSWER_THRESHOLD 像素阈值；每行4个选项
    def getAnswerCharsAndCnts(self, row_choices, ANSWER_THRESHOLD):
        answerChars = ''
        cnts = []
        # bubble_row[0]為total，bubble_row[1]為選項號
        for b in row_choices:
            if b[0] > ANSWER_THRESHOLD:  # 大于阈值
                answerChars += ANSWER_CHAR[b[1]]  # 追加字母
                cnts.append(b[2])  # 追加轮廓
        return (''.join(sorted(list(answerChars))), cnts)  # 按字母顺序排序

    def getScore(self, choices, answers):
        # print('判分'),(answer.get(choice[0]))[0]是答案，(answer.get(choice[0]))[1]是每题分值
        score = 0
        for choice in choices:
            if (answers.get(choice[0]))[0] == choice[1]:
                score += (answers.get(choice[0]))[1]
        return round(score, 1)  # 保留一位小数

    # 生成学号绝对坐标
    def makeStuidCnts(self, src_img, expandingFlag=True, offset=0):
        ID_BITS = self.dto.cfg.CLASS_BITS + self.dto.cfg.STU_BITS#学号区总位数
        width = src_img.shape[1]
        height = src_img.shape[0]
        height_scale_size = height / self.Stuid_AREA_ROWS  # 每单元格高度
        width_scale_size = width / self.Stuid_AREA_COLS  # 每单元格宽度
        stuidCnts = []
        for x in range(ID_BITS):  # x为列相对坐标:表示2位数
            for y in range(NUM_BITS):  # y为行相对坐标:表示每位10个数字
                if expandingFlag:  # 扩大
                    top_left = [(2 * x + self.ID_X_OFFSET) * width_scale_size - offset,
                                (2 * y + self.ID_Y_OFFSET) * height_scale_size - offset]
                    top_right = [(2 * x + 1 + self.ID_X_OFFSET) * width_scale_size + offset,
                                 (2 * y + self.ID_Y_OFFSET) * height_scale_size - offset]
                    bottom_left = [(2 * x + self.ID_X_OFFSET) * width_scale_size - offset,
                                   (2 * y + self.ID_Y_OFFSET + 1) * height_scale_size + offset]
                    bottom_right = [(2 * x + 1 + self.ID_X_OFFSET) * width_scale_size + offset,
                                    (2 * y + self.ID_Y_OFFSET + 1) * height_scale_size + offset]
                else:  # 缩小
                    top_left = [(2 * x + self.ID_X_OFFSET) * width_scale_size + offset,
                                (2 * y + self.ID_Y_OFFSET) * height_scale_size + offset]
                    top_right = [(2 * x + 1 + self.ID_X_OFFSET) * width_scale_size - offset,
                                 (2 * y + self.ID_Y_OFFSET) * height_scale_size + offset]
                    bottom_left = [(2 * x + self.ID_X_OFFSET) * width_scale_size + offset,
                                   (2 * y + self.ID_Y_OFFSET + 1) * height_scale_size - offset]
                    bottom_right = [(2 * x + 1 + self.ID_X_OFFSET) * width_scale_size - offset,
                                    (2 * y + self.ID_Y_OFFSET + 1) * height_scale_size - offset]
                stuidCnts.append(np.array([[top_left], [top_right], [bottom_right], [bottom_left]], dtype=np.int32))
        return stuidCnts

    # 获取学号
    def getStuID(self, src_img):
        ID_BITS = self.dto.cfg.CLASS_BITS + self.dto.cfg.STU_BITS  # 学号区总位数
        # processed_img = cv.medianBlur(src_img, 3)
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        processed_img = cv.GaussianBlur(gray, (3, 3), 0)
        thresh2 = cv.adaptiveThreshold(processed_img.copy(), 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,
                                       157, 19)
        # 按坐标从上到下排序
        stuidCnts = self.makeStuidCnts(src_img)
        stu_Img = src_img.copy()
        cv.drawContours(stu_Img,stuidCnts,-1,(255,0,255),1)

        stu_num = []  # 生成一个二维列表暂存(序号，像素，轮廓）
        for b in range(ID_BITS):
            stu_num.append([])
        for (i, c) in enumerate(stuidCnts):
            # 生成一个大小与透视图一样的全黑背景图布
            mask = np.zeros(gray.shape, dtype="uint8")
            # 将指定的轮廓+白色的填充写到画板上,255代表亮度值，亮度=255的时候，颜色是白色，等于0的时候是黑色
            cv.drawContours(mask, [c], -1, 255, -1)
            maxPixel = cv.countNonZero(mask)  # 单个蒙板的像素
            # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
            mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
            # 获取每个答案的像素值
            total = cv.countNonZero(mask)
            # 存到一个数组里面，tuple里面的参数分别是，像素大小和行内序号
            stu_num[int(i / NUM_BITS)].append((i % NUM_BITS, total, c))
        ANSWER_THRESHOLD = maxPixel * self.dto.answerThreshhold
        stuID = ''  # 初始化学号字符串
        for n in range(ID_BITS):  # 逐位获取像素最大的数字
            tmp_num = stu_num[n]  # tmp_num第n位数字所有的选项框数据
            tmp_num = sorted(tmp_num, key=lambda x: x[1], reverse=True)  # 按像素排序
            if tmp_num[0][1] > ANSWER_THRESHOLD:  # 如果小于阈值则认为学号涂得不清晰,则学号为空
                stuID += str(tmp_num[0][0])
            cv.drawContours(stu_Img, [tmp_num[0][2]], 0, (0, 255, 255), 2)  # 显示已涂学号图
        self.showingStu = ExamPaper.convertImg(stu_Img)
        self.stuID = stuID
        return self.stuID

    # 提取答题和学号区域
    def get_roi_img(self, src_img):
        if src_img.shape[1] > 1500:  # 如果图像太大，则进行缩小
            src_img = cv.resize(src_img, (1440, int((1440 / src_img.shape[1] * src_img.shape[0]))),
                                interpolation=cv.INTER_AREA)
            # src_img=cv.resize(src_img,(0,0),fx=0.3,fy=0.3,interpolation=cv.INTER_AREA)
        # cv.imshow('src',src_img)
        gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        # 高斯滤波，清除一些杂点
        blur = cv.GaussianBlur(gray, (3, 3), 0)
        # 自适应二值化算法
        thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 131, 4)

        self.showingImgThresh = ExamPaper.convertImg(thresh2)  # 显示已选标注框图片
        # cv.imshow('th',thresh2)
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
                    # cv.imwrite('tmp/paper.png', maxImg_tmp)
                    maxImg = maxImg_tmp
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的答题卡！')
            return None, None

        # print(maxImg.shape[1]/src_img.shape[1],maxImg.shape[0]/src_img.shape[0])
        if maxImg.shape[1] < 0.8 * src_img.shape[1]:
            QMessageBox.information(None, '提示', '可能太远导致目标识别区太小！')
            return None, None

        ratio = maxImg.shape[1] / maxImg.shape[0]
        # print(ratio)
        if ratio < 1.4 or ratio > 2.0:  # 标准卡宽高比为1.7
            QMessageBox.information(None, '提示', '可能太斜导致目标识别区不准！')
            return None, None

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
                        maxImg.shape[1] and ansImg_tmp.shape[0] > maxImg.shape[0] * 2 / 3 and ansImg_tmp.shape[1] > \
                        maxImg.shape[1] / 2:
                    ansImg = ansImg_tmp
                    cv.imwrite('tmp/ansImg.png', ansImg)
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的答題区域！')
            return None, None

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
                    # cv.imwrite('tmp/stuImg.png', stuImg)
                    break
        else:
            QMessageBox.information(None, '提示', '找不到有效的学号区域！')
            return None, None

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
        # 变换彩色空间顺序
        if len(img.shape) == 2:
            cimg = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
        elif len(img.shape) == 3 and img.shape[2] == 3:
            cimg = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        elif len(img.shape) == 3 and img.shape[2] == 4:
            cimg = cv.cvtColor(img, cv.COLOR_BGRA2RGB)
        # 转为QImage对象
        height, width, bytesPerComponent = cimg.shape
        bytesPerLine = bytesPerComponent * width
        showimg = QImage(cimg.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # showpix = QPixmap.fromImage(showimg)
        return showimg
