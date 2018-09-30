import cv2 as cv
import numpy as np


# def nothing(x):
#     pass


# 创建一副􅢀色图像

img = cv.imread('ansImg.png')
# cv.namedWindow('image')

# cv.createTrackbar('blur kernel', 'image', 0, 10, nothing)
# cv.createTrackbar('bs', 'image', 0, 1, nothing)
#
# cv.createTrackbar('medianBlur ', 'image', 0, 10, nothing)
# cv.createTrackbar('ms', 'image', 0, 1, nothing)
#
# cv.createTrackbar('bilateralFilter ', 'image', 0, 10, nothing)
# cv.createTrackbar('bils', 'image', 0, 1, nothing)
#
# cv.createTrackbar('threshold kernel', 'image', 0, 300, nothing)
# cv.createTrackbar('threshold C', 'image', 1, 100, nothing)
# cv.createTrackbar('ths', 'image', 0, 1, nothing)
# # while (1):
#     k = cv.waitKey(1) & 0xFF
#     if k == 27:
#         break
b = cv.getTrackbarPos('blur kernel', 'image')
bs = cv.getTrackbarPos('bs', 'image')

m = cv.getTrackbarPos('medianBlur', 'image')
ms = cv.getTrackbarPos('ms', 'image')

bil = cv.getTrackbarPos('bilateralFilter', 'image')
bils = cv.getTrackbarPos('bils', 'image')

th = cv.getTrackbarPos('threshold kernel', 'image')
thc = cv.getTrackbarPos('threshold C', 'image')
ths = cv.getTrackbarPos('ths', 'image')

processed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
# 
# #
# processed = cv.bilateralFilter(processed, 9, 75, 75)
# 
# kernel = (2 * b + 3, 2 * b + 3)
# # 高斯滤波，清除一些杂点
processed = cv.GaussianBlur(processed, (3,3), 0)
# 
# processed = cv.medianBlur(processed, 3)
# 
processed = cv.adaptiveThreshold(processed, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,131, 4)
# processed = cv.dilate(processed,kernel,iterations = 1)
# processed = cv.erode(processed, kernel, iterations=1)
# cv.imshow('processed', processed)
# 调整图片的亮度
# processed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# processed = cv.GaussianBlur(processed, (3, 3), 0)
cv.imshow('g', processed)
cv.waitKey(0)
#
# CHOICE_IMG_KERNEL = np.ones((2, 2), np.uint8)
# ANS_IMG_KERNEL = np.ones((2, 2), np.uint8)
# # 识别所涂写区域时的膨胀参数
# ANS_IMG_DILATE_ITERATIONS = 9
#
# # 识别所涂写区域时的腐蚀参数
# ANS_IMG_ERODE_ITERATIONS = 0
# # 识别所涂写区域时的二值化参数
# ANS_IMG_THRESHOLD = (127, 255)
#
# # 通过二值化和膨胀腐蚀获得填涂区域
# # ret, ans_img = cv.threshold(processed, ANS_IMG_THRESHOLD[0], ANS_IMG_THRESHOLD[1], cv.THRESH_BINARY_INV)
# ans_img = cv.adaptiveThreshold(processed, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 41, 35)
# cv.imshow('draw',ans_img)
# cv.waitKey(0)
# ans_img = cv.dilate(ans_img, ANS_IMG_KERNEL, iterations=ANS_IMG_DILATE_ITERATIONS)
# cv.imshow('draw',ans_img)
# cv.waitKey(0)
# ans_img = cv.erode(ans_img, ANS_IMG_KERNEL, iterations=ANS_IMG_ERODE_ITERATIONS)
# cv.imshow('draw',ans_img)
# cv.waitKey(0)
# ret, ans_img = cv.threshold(ans_img, ANS_IMG_THRESHOLD[0], ANS_IMG_THRESHOLD[1], cv.THRESH_BINARY_INV)
# cv.imshow('th',ans_img)
# cv.waitKey(0)
# # processed = cv.morphologyEx(processed, cv.MORPH_OPEN, kernel)
# # processed = cv.morphologyEx(processed, cv.MORPH_CLOSE, kernel)
# r_image, cnts, r_hierarchy = cv.findContours(ans_img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
#
#
# cv.drawContours(img,cnts,-1,(255,0,0),1)
# cv.imshow('img',img)
# cv.waitKey(0)
# # 自适应二值化算法

# resized = cv.resize(processed, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)

cv.destroyAllWindows()
