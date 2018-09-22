import cv2 as cv
import os
import numpy as np

randomBA=bytearray(os.urandom(120000))
flatNA=np.array(randomBA)

gray=flatNA.reshape(100,300,4)
cv.imshow('gray',gray)
cv.waitKey(0)

bgr=flatNA.reshape(100,400,3)
cv.imshow('bgr',bgr)
cv.waitKey(0)


img=cv.imread(r"image\model.bmp")
cv.imshow('bgr',img)
cv.waitKey(0)
print(img.shape,img.size,img.dtype)
roi=img[0:100,0:100]
img[200:300,300:400]=roi
img[:,:,1]=0
print(np.array(img))



cv.imshow('bgr',img)
cv.waitKey(0)