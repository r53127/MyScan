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

# img = np.zeros((200, 200), dtype=np.uint8)
# img[50:150, 50:150] = 255
#
# ret, thresh = cv.threshold(img, 127, 255, 0)
# image, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# color = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
# img = cv.drawContours(color, contours, -1, (0,255,0), 2)
# cv.imshow("contours", color)
# cv.waitKey()
# cv.destroyAllWindows()

# import cv2
# # 加􄤬图像
# img1 = cv2.imread('image/20180924121516.jpg')
# img2 = cv2.imread('image/test6.jpg')
# cv.imshow('img1', img1)
# cv.waitKey(0)
# cv.imshow('img2', img2)
# cv.waitKey(0)
# # I want to put logo on top-left corner, So I create a ROI
# rows,cols,channels = img2.shape
# roi = img1[0:rows, 0:cols ]
# cv.imshow('roi', roi)
# cv.waitKey(0)
# # Now create a mask of logo and create its inverse mask also
# img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
# blur = cv.GaussianBlur(img2gray, (3, 3), 0)
# mask = cv2.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 131, 4)
# cv.imshow('mask', mask)
# cv.waitKey(0)
#
# mask_inv = cv2.bitwise_not(mask)
# cv.imshow('mask_inv', mask_inv)
# cv.waitKey(0)
# # Now black-out the area of logo in ROI
# # 取roi 中与mask 中不为􅂥的值对应的像素的值􈙽其他值为0
# # 注意􄦈􄭻必􅈪有mask=mask 或者mask=mask_inv, 其中的mask= 不能忽略
# img1_bg = cv2.bitwise_and(roi,roi,mask = mask)
# cv2.imshow('img1_bg',img1_bg)
# cv2.waitKey(0)
# # 取roi 中与mask_inv 中不为􅂥的值对应的像素的值􈙽其他值为0。
# # Take only region of logo from logo image.
# img2_fg = cv2.bitwise_and(img2,img2,mask = mask_inv)
# cv2.imshow('img2_fg',img2_fg)
# cv2.waitKey(0)
# # Put logo in ROI and modify the main image
# dst = cv2.add(img1_bg,img2_fg)
# cv2.imshow('dst',dst)
# cv2.waitKey(0)
#
# img1[0:rows, 0:cols ] = dst
# cv2.imshow('res',img1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# import numpy as np
#
# import cv2
#
# cap = cv2.VideoCapture(0)
# while (1):
#     # 获取每一帧
#     ret, frame = cap.read()
#     # 􄤛换到HSV
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     # 􄕭定蓝色的􄾷值
#     lower_blue = np.array([110, 50, 50])
#     upper_blue = np.array([130, 255, 255])
#     # 根据􄾷值构建掩模
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)
#     # 对原图像和掩模􄦊􄇻位􄥿算
#     res = cv2.bitwise_and(frame, frame, mask=mask)
#     # 显示图像
#     cv2.imshow('frame', frame)
#     cv2.imshow('mask', mask)
#     cv2.imshow('res', res)
#     k = cv2.waitKey(5) & 0xFF
#     if k == 27:
#         break
#     # 关􄾜窗口
# cv2.destroyAllWindows()
