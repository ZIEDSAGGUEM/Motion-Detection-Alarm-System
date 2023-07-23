import threading
import winsound

import cv2
import imutils



cap =cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


success,frame=cap.read()

frame=imutils.resize(frame,width=500)
frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
frame=cv2.GaussianBlur(frame,(21,21),0)

alarm=False
alarm_mode=False
alarm_counter=0


def beep_alarm():
    global alarm
    for success in range(5):
        if not alarm_mode:
            break
        print("Alarm")
        winsound.Beep(2500,1000)

    alarm=False


while True:

    success,img=cap.read()
    img=imutils.resize(img,width=500)

    if alarm_mode:
        frame_bw= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        frame_bw= cv2.GaussianBlur(frame_bw,(5,5),0)

        difference = cv2.absdiff(frame_bw,frame)
        threshold=cv2.threshold(difference,25,255,cv2.THRESH_BINARY)[1]
        frame=frame_bw


        if threshold.sum()>30000000:
            alarm_counter+=1
        else:
            if alarm_counter>0:
                alarm_counter-=1


        cv2.imshow("Cam",threshold)
    else:
        cv2.imshow("Cam",img)



    if alarm_counter>20:
        if not alarm:
            alarm =True
            threading.Thread(target=beep_alarm).start()



    key_pressed= cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode=not alarm_mode
        alarm_counter=0
    if key_pressed==ord("q"):
        alarm_mode=False
        break


cap.release()
cv2.destroyAllWindows()