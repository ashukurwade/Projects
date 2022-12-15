import cv2
import numpy as np
import time

#capturing a output video
video = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',video,20.0, (640,480))

#reads from webcam
cap = cv2.VideoCapture(0)

#sleep a system for a while to start a webcam
time.sleep(3)
count = 0
background = 0

#capture the background
for i in range(60):
	ret,background = cap.read()
background = np.flip(background,axis=1)

#reading a video frame by frame from the webcam
while cap.isOpened():
    ret,img = cap.read()
    if not ret:
        break
    count+=1
    img = np.flip(img,axis=1)
    
    #convert color frame from BGR to HSV
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    #detect red color
    lower_red = np.array([0,120,70])
    upper_red = np.array([100,255,255])
    mask1 = cv2.inRange(hsv,lower_red,upper_red)
    
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
    
    mask1 = mask1+mask2
    # open and large mask image
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    
    # Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1)
    
    # Segment the red color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img,img,mask=mask2)
    
    # Create image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(background,background,mask=mask1)
    
    # Generating the final output 
    finalOutput = cv2.addWeighted(res1,1,res2,1,0)
    out.write(finalOutput)
    cv2.imshow("Invisible Cloak",finalOutput)
    cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()