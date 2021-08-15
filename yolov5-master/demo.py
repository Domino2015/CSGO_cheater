import cv2
import detect

cap=cv2.VideoCapture('../VOC2020/val/1.mp4')
a=detect.detectapi(weights='runs/train/exp6/weights/best.pt')

while True:

    rec,img = cap.read()

    result,names =a.detect([img])
    img=result[0][0] #第一张图片的处理结果图片
    
    for cls,(x1,y1,x2,y2),conf in result[0][1]: #第一张图片的处理结果标签。
        print(cls,x1,y1,x2,y2,conf)
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0))
        cv2.putText(img,names[cls],(x1,y1-20),cv2.FONT_HERSHEY_DUPLEX,1.5,(255,0,0))
    
    cv2.imshow("vedio",img)

    if cv2.waitKey(1)==ord('q'):
        break