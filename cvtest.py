import cv2 as cv
import os
import numpy as np
from scipy import ndimage

# randomBA=bytearray(os.urandom(120000))
# flatNA=np.array(randomBA)
#
# gray=flatNA.reshape(100,300,4)
# cv.imshow('gray',gray)
# cv.waitKey(0)
#
# bgr=flatNA.reshape(100,400,3)
# cv.imshow('bgr',bgr)
# cv.waitKey(0)
#
#
# img=cv.imread(r"image\model.bmp")
# cv.imshow('bgr',img)
# cv.waitKey(0)
# print(img.shape,img.size,img.dtype)
# roi=img[0:100,0:100]
# img[200:300,300:400]=roi
# img[:,:,1]=0
# print(np.array(img))
# cv.imshow('bgr',img)
# cv.waitKey(0)
# 
# kernel_3x3 = np.array([[-1, -1, -1],
#                    [-1,  8, -1],
#                    [-1, -1, -1]])
# 
# kernel_5x5 = np.array([[-1, -1, -1, -1, -1],
#                        [-1,  1,  2,  1, -1],
#                        [-1,  2,  4,  2, -1],
#                        [-1,  1,  2,  1, -1],
#                        [-1, -1, -1, -1, -1]])
# 
# img = cv.imread(r"image\model.bmp",0)
# img1=cv.imread(r"image\model.bmp")
# k3 = ndimage.convolve(img, kernel_3x3)
# k5 = ndimage.convolve(img, kernel_5x5)
# gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
# gray1 = cv.GaussianBlur(gray, (17,17), 0)
# blurred = cv.GaussianBlur(img, (17,17), 0)
# g_hpf = img - blurred
# 
# cv.imshow("img", img)
# cv.imshow("img1", img1)
# cv.imshow("3x3", k3)
# cv.imshow("5x5", k5)
# cv.imshow("gray", gray)
# cv.imshow("blurred", blurred)
# cv.imshow("g_hpf", g_hpf)
# cv.waitKey(0)
# cv.destroyAllWindows()

img = np.zeros((200, 200), dtype=np.uint8)
img[50:150, 50:150] = 255

ret, thresh = cv.threshold(img, 127, 255, 0)
image, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
color = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
img = cv.drawContours(color, contours, -1, (0,255,0), 2)
cv.imshow("contours", color)
cv.waitKey()
cv.destroyAllWindows()