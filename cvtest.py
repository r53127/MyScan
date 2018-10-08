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
# # cv2.destroyAllWindows()
# import numpy as np
# import cv2
# #create a black use numpy,size is:512*512
# img = np.zeros((512,512,3), np.uint8)
# #fill the image with white
# # img.fill(255)
# ###########################################
# ####Main Function                      ####
# #draw
# #        start x  y end x    y      color
# cv2.line(img, (10,50), (511, 511), (255,0,0), 5)
# cv2.rectangle(img, (384,0), (510, 128), (0, 255, 0), 3)
# cv2.circle(img, (447, 63), 63, (0,0,255), -1)
# cv2.ellipse(img, (256,256), (100,50),45,0,290,(0,0,255),-1)
# font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(img, 'Hello', (10,500), font, 4, (255,2,255), 2)
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# import cv2 as cv
# from imutils import contours
# import numpy as np
# from ExamPaper import ANSWER_COLS, ANSWER_ROWS
#
# src_img=cv.imread('stuImg.png')
# cv.imshow('stuid', src_img)
# gray = cv.cvtColor(src_img, cv.COLOR_BGR2GRAY)  # 转化成灰度图片
# blur = cv.GaussianBlur(gray, (5, 5), 0)
# # 自适应二值化算法
# thresh2 = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 403, 40)
# cv.imshow('thresh2', thresh2)
# cv.waitKey(0)
# image, cnts, hierarchy = cv.findContours(thresh2.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# sortcnts = sorted(cnts, key=lambda c: cv.contourArea(c), reverse=True)
# stuCnts = []
# stuBoudingCnts=[]
# # 找填凃框
# for c in sortcnts:
#     x, y, w, h = cv.boundingRect(c)
#     # cv.rectangle(src_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
#     # cv.imshow('e', src_img)
#     # cv.waitKey(0)
#     ratio = w / float(h)
#     if ratio > 1.5 and ratio < 3.0 and w > 30 and h > 10:
#         stuCnts.append(c)
#         top_left=[x,y]
#         top_right=[x+w,y]
#         bottom_right=[x+w,y+h]
#         bottom_left=[x,y+h]
#         stuBoudingCnts.append(np.array([[top_left],[top_right],[bottom_right],[bottom_left]],dtype=np.int32))
# # 按坐标从上到下排序
# stuBoudingCnts= contours.sort_contours(stuBoudingCnts, method="left-to-right")[0]
# stuBoudingCnts= contours.sort_contours(stuBoudingCnts, method="top-to-bottom")[0]
# print(stuBoudingCnts)
# for s in stuBoudingCnts:
#     cv.drawContours(src_img, [s], -1, (255, 0, 0), 1)
#     cv.imshow('i',src_img)
#     cv.waitKey(0)
# # 使用np函数，按5个元素，生成一个集合
# first_num=[]
# second_num=[]
# m=0#十位辅助计数
# n=0#个位辅助计数
# for (i, c) in enumerate(stuBoudingCnts):
#     # 生成一个大小与透视图一样的全黑背景图布
#     mask = np.zeros(gray.shape, dtype="uint8")
#     # 将指定的轮廓+白色的填充写到画板上,255代表亮度值，亮度=255的时候，颜色是白色，等于0的时候是黑色
#     cv.drawContours(mask, [c], -1, 255, -1)
#     # 做两个图片做位运算，把每个选项独自显示到画布上，为了统计非0像素值使用，这部分像素最大的其实就是答案
#     mask = cv.bitwise_and(thresh2, thresh2, mask=mask)
#     # 获取每个答案的像素值
#     total = cv.countNonZero(mask)
#     # 存到一个数组里面，tuple里面的参数分别是，像素大小和行内序号
#     if i%2==0:
#         first_num.append((m,total))
#         print('firnum is :',first_num)
#         m+=1
#     else:
#         second_num.append((n,total))
#         print('secnum is :',second_num)
#         n+=1
# # 按像素值排序
# first_num = sorted(first_num, key=lambda x: x[1], reverse=True)
# second_num = sorted(second_num, key=lambda x: x[1], reverse=True)
#
# print('学号是：',str(first_num[0][0])+str(second_num[0][0]))
import cv2
video="http://admin:admin@192.168.31.34:8081/"  #ip摄像头的地址
cap = cv2.VideoCapture(video)
while(1):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
