import cv2 as cv
import numpy as np


def nothing(x):
    pass


# 创建一副􅢀色图像

img = cv.imread('tmp/ansImg.png')
cv.namedWindow('image',0)


cv.createTrackbar('medianBlur', 'image', 1, 100, nothing)

cv.createTrackbar('GaussianBlur', 'image', 0, 100, nothing)

cv.createTrackbar('aTh Block', 'image', 0, 255, nothing)
cv.createTrackbar('aTh C', 'image', 0, 255, nothing)


cv.createTrackbar('threshold low', 'image', 88, 255, nothing)
cv.createTrackbar('threshold high', 'image', 255, 255, nothing)

cv.createTrackbar('DILATE kernel', 'image', 0, 255, nothing)

cv.createTrackbar('ERODE num', 'image', 0, 255, nothing)
cv.createTrackbar('DILATE num', 'image', 0, 255, nothing)


while (1):
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break

    m = cv.getTrackbarPos('medianBlur', 'image')

    b = cv.getTrackbarPos('GaussianBlur', 'image')

    thl = cv.getTrackbarPos('threshold low', 'image')
    thh = cv.getTrackbarPos('threshold high', 'image')

    B = cv.getTrackbarPos('aTh Block', 'image')
    C = cv.getTrackbarPos('aTh C', 'image')


    kernel=cv.getTrackbarPos('DILATE kernel', 'image')
    d=cv.getTrackbarPos('DILATE num', 'image')
    e=cv.getTrackbarPos('ERODE num', 'image')

    # processed = cv.bilateralFilter(processed, 9, 75, 75)

    # processed = cv.Sobel(processed, -1, 0,1, ksize=5)
    # processed=cv.Scharr(processed,-1,0,1)
    # processed = cv.Scharr(processed, -1, 1,0)

    processed_img = cv.medianBlur(img, 2*m+1)
    processed_img = cv.cvtColor(processed_img, cv.COLOR_BGR2GRAY)

    processed_img = cv.GaussianBlur(processed_img, (2*b+3,2*b+3), 0)

    ANS_IMG_KERNEL = np.ones((kernel,kernel), np.uint8)
    # 识别所涂写区域时的膨胀参数
    ANS_IMG_DILATE_ITERATIONS = 9
    # 识别所涂写区域时的腐蚀参数
    ANS_IMG_ERODE_ITERATIONS = 0
    # 识别所涂写区域时的二值化参数
    ANS_IMG_THRESHOLD = (88, 255)


    # 通过二值化和膨胀腐蚀获得填涂区域
    # ret, ans_img = cv2.threshold(processed_img, ANS_IMG_THRESHOLD[0], ANS_IMG_THRESHOLD[1], cv2.THRESH_BINARY_INV)
    # ans_img = cv.adaptiveThreshold(processed_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 41, 35)
    # ans_img = cv.erode(processed_img, ANS_IMG_KERNEL, iterations= e)
    # ans_img= cv.dilate(ans_img,ANS_IMG_KERNEL,iterations = d)
    ans_img = cv.adaptiveThreshold(processed_img.copy(), 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 2*B+3, C)
    # ans_img = cv.erode(ans_img, ANS_IMG_KERNEL, iterations= e)
    # ans_img= cv.dilate(ans_img,ANS_IMG_KERNEL,iterations = d)

    # ret, ans_img = cv.threshold(ans_img, thl, thh, cv.THRESH_BINARY)
    # ret, ans_img1 = cv.threshold(ans_img.copy(), 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)



    cv.imshow('i', ans_img)
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



cv.destroyAllWindows()
