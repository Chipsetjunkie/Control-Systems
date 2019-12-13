import cv2
import numpy as np
import time
#import pyautogui as pgi
from km import Kalman_Filter


k = Kalman_Filter(4,1)
x_pos=0
y_pos=0


def Mouse(event,x,y,flags,params):
    global x_pos,y_pos,image,k
    image = np.zeros((500,500,3), np.uint8)

    k.predict()
    corr_pos = k.Update()
    x_k,y_k = corr_pos[0],corr_pos[1]
    cv2.circle(image,(x_k,y_k),10,(255,128,0))#corrected pos
    x_pos,y_pos = x,y
    k.set_measure([x_pos,y_pos,0,0])
    cv2.circle(image,(x,y),10,(0,0,255))

image = np.zeros((500,500,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',Mouse)


while(1):


    cv2.imshow('image',image)
    if cv2.waitKey(2) & 0xFF == 27:
        break




cv2.destroyAllWindows()
