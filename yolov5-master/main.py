# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 04:52:32 2021

@author: wangw
"""

import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
import detect

import argparse

import keyboard

from ctypes import *



screen_width=1280
screen_height=720


width_net=int(screen_width/8)
height_net=int(screen_height/6)

roi_width=width_net*6
roi_height=height_net*4

#计算中心点时候补偿像素
gap=5


index=0;
loop_time = time()


dd_dll = windll.LoadLibrary('DD94687.64.dll')
print("Load DD success!")
st = dd_dll.DD_btn(0) #DD Initialize
# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

##load model
a=detect.detectapi(weights='runs/train/exp6/weights/best.pt')
print("Load model success!")
# initialize the WindowCapture class
wincap = WindowCapture('Counter-Strike: Global Offensive')
print("Load  Capture Window success!")





while(True):
    # get an updated image of the game
    #screenshot = wincap.get_screenshot()
    #[height_net:height_net*5,width_net:width_net*7]
    
    img =  wincap.get_screenshot()[height_net:height_net*5,width_net:width_net*7]
    
    
    result,_ =a.detect([img]);
    #img=result[0][0] #第一张图片的处理结果图片
    sorted(result[0][1],key=lambda x:x[1][2]);
    for cls,(x1,y1,x2,y2),conf in result[0][1][0:1]: #第一张图片的处理结果标签。
        if conf>0.55:
            print("头坐标：",x1,y1,"-",x2,y2,conf)
            #移动相对坐标计算
            yy=(y2-y1)/2 +y1+height_net
            xx=(x2-x1)/2 +x1+width_net
            
            ##相对位移 实际值+补偿值
            row=int((screen_width/2)-xx)-gap
            col=int((screen_height/2)-yy)-gap
            
            #keyboard.wait("c") 
            if keyboard.is_pressed('c')==True:
                dd_dll.DD_movR(-row,-col)##+4
                #print("Mouse move rel.",-row,-col)
                if abs(int((roi_width/2)-(x1+(x2-x1)/2)))<(x2-x1)/1.5:
                    #静步并开枪
                    dd_dll.DD_key(500, 1)
                    dd_dll.DD_btn(1)
                    dd_dll.DD_btn(2)
                    dd_dll.DD_key(500, 2)
                    index=index+1;
                    print('开火!!',index)

            cv.rectangle(img,(x1,y1),(x2,y2),(255,00,0))
            #cv.putText(img,names[cls],(x1,y1-10),cv.FONT_HERSHEY_DUPLEX,1.5,(255,255,0))
            #cv.putText(img,names[cls],(x1,y1-20),cv.FONT_HERSHEY_DUPLEX,1.5,(255,0,0))
    
    cv.imshow("vedio",img)

    if cv.waitKey(1)==ord('q'):
        cv.destroyAllWindows()
        break
        
#cv.destroyAllWindows()
print('Done.')




