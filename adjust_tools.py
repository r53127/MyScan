import cv2 as cv
import numpy as np
def nothing(x):
    pass
# 创建一副􅢀色图像
img=cv.imread('image/20180924121516.jpg')
cv.namedWindow('image')
cv.createTrackbar('blur kernel','image',0,10,nothing)
cv.createTrackbar('threshold kernel','image',0,300,nothing)
cv.createTrackbar('C','image',1,100,nothing)
switch='0:OFF\n1:ON'
cv.createTrackbar(switch,'image',0,1,nothing)
while(1):
    k=cv.waitKey(1)&0xFF
    if k==27:
        break
    b=cv.getTrackbarPos('blur kernel','image')
    t=cv.getTrackbarPos('threshold kernel','image')
    c=cv.getTrackbarPos('C','image')
    s=cv.getTrackbarPos(switch,'image')
    if s != 0:
        blurkernel=(2*b+3,2*b+3)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
        # 高斯滤波，清除一些杂点
        blur = cv.GaussianBlur(gray, blurkernel, 0)
        # 自适应二值化算法
        thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 2*t+3, c)
        resized=cv.resize(thresh2, None,fx=0.5,fy=0.5,interpolation=cv.INTER_AREA)
        cv.imshow('image', resized)
cv.destroyAllWindows()
