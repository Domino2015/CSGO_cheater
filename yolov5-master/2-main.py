# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 12:36:14 2021

@author: wangw
"""
import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture
import detect
import argparse
import keyboard
from ctypes import *
import math


dd_dll = windll.LoadLibrary('DD94687.64.dll')
print("Load DD success!")
st = dd_dll.DD_btn(0) #DD Initialize
#Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
##load model
a=detect.detectapi(weights='runs/train/exp12/weights/best.pt')
print("Load model success!")
# initialize the WindowCapture class
wincap = WindowCapture('Counter-Strike: Global Offensive')
#wincap = WindowCapture('Left 4 Dead 2 - Direct3D 9')
print("Load  Capture Window success!")


screen_width=1280
screen_height=720
width_net=int(screen_width/8)
height_net=int(screen_height/6)
'''
screen_width=1920
screen_height=1080
width_net=int(screen_width/16)
height_net=int(screen_height/9)
'''
roi_width=width_net*6
roi_height=height_net*4
#计算中心点时候补偿像素
gap=4

#origin_x=width_net
#origin_y=height_net

loop_time = time.time()

while(True):
    # get an updated image of the game
    #screenshot = wincap.get_screenshot()
    #[height_net:height_net*5,width_net:width_net*7]
    
    #检测网格区域划分
    origin_x=width_net*2
    origin_y=height_net*2

    end_x=width_net*6
    end_y=height_net*4
    # get an updated image of the game
    img =  wincap.get_screenshot()[origin_y:end_y,origin_x:end_x]

    result,_ =a.detect([img]);
    #img=result[0][0] #第一张图片的处理结果图片
    sorted(result[0][1],key=lambda x:x[1][2]);
    
    text1='Target Num:'+str(len(result[0][1]))
    cv.putText(img, text1, (10, 30), cv.FONT_HERSHEY_COMPLEX, .4, (0, 255, 0), 1,8)
    
    index=1
    for cls,(x1,y1,x2,y2),conf in result[0][1]: #第一张图片的处理结果标签。
        if conf>0.85:
            #print(x1,y1,x2,y2,conf)
            #计算在绝对坐标系中目标头位置
            xx=(x2-x1)/2 +x1+origin_x
            yy=(y2-y1)/2 +y1+origin_y
            #print("绝对坐标-头：",xx,yy,"-",conf)
            ##相对位移 实际值+补偿值
            row=round((screen_width/2)-xx)-gap
            col=round((screen_height/2)-yy)-gap
            #print("Mouse will move rel.",-row,-col)
            
            ##等待“c”键按下开火
            if keyboard.is_pressed('c')==True:
                dd_dll.DD_movR(-row,-col)
                ##更新同一图像，下一个检测目标左上角坐标
                origin_x=origin_x+row
                origin_y=origin_y+col
                ##增加延迟 确保 鼠标移动到位
                #鼠标灵敏度5.5
                time.sleep(0.015)
                #静步 left shift 并 开枪
                dd_dll.DD_key(500, 1)
                dd_dll.DD_btn(1)
                dd_dll.DD_btn(2)
                dd_dll.DD_key(500, 2)
                cv.putText(img, 'Attack!!', (100,15), cv.FONT_HERSHEY_COMPLEX,  .4, (0, 255, 0), 1,8)
                #print('开火!!')
                #print("Mouse move rel.",-row,-col)
            text2='Target '+str(index)+' ('+str(int(xx))+','+str(int(yy))+') CI:'+str(round(conf, 2))
            cv.putText(img, text2, (10,15*(2+index)), cv.FONT_HERSHEY_COMPLEX,  .4, (0, 255, 0), 1,8)
            
            cv.putText(img,str(index), (x1+3,y1-2), cv.FONT_HERSHEY_COMPLEX,.4, (0, 255, 0), 1,8)
            index=index+1;
            '''
                if abs(int((roi_width/2)-(x1+(x2-x1)/2)))<(x2-x1)/1.5:
                    #静步并开枪
                    dd_dll.DD_key(500, 1)
                    dd_dll.DD_btn(1)
                    dd_dll.DD_btn(2)
                    dd_dll.DD_key(500, 2)
                    print('开火!!')
            '''
            #框出头部，输出信息
            cv.rectangle(img,(x1,y1),(x2,y2),(255,00,0))
        
       
        
    # debug the loop rate
    text3='FPS {}'.format(round(1 / (time.time() - loop_time),1))
    cv.putText(img, text3, (10,15), cv.FONT_HERSHEY_COMPLEX,  .4, (0, 255, 0), 1,8)
    
    loop_time = time.time()
    
    cv.imshow("Counter-Strike: Global Offensive",img)
    if cv.waitKey(1)==ord('q'):
           cv.destroyAllWindows()
           break
#cv.destroyAllWindows()
#print('Done.')
