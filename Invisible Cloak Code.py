# Importing Modules

import numpy as np
import cv2
import time

print("HELLO FRANDSSSSSSSSSSSS")

# Capturing Webcam Feed
#cap = cv2.VideoCapture('http://192.168.43.200:8080/video?640x480')
cap = cv2.VideoCapture(0)

time.sleep(3)  #providing 3 second of time to adjust

count = 0

background = 0  # capturing back image when we use cloak

# Capturing Static Background Frame

for i in range(60):  # provided 60 iteration to capturing the background
    ret, background = cap.read()

# Flip the Image

background = np.flip(background, axis=1)

while (cap.isOpened()): # till running this will executing

    ret, img = cap.read()  # capturing our image to perform operation

    if not ret:
        break

    count += 1

    img = np.flip(img, axis=1)

    # Converting from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #img=source input BGR=red,blue,green

    lower_red = np.array([0, 120, 70]) #using lower red color to determine cloak
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red) #for 170 to 180

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2  #overloading as what shade of color it will be it will segemnted(170-180) degree

    # morphology is used to remove the noise or distortions

    # mask1 is input image morph is operation we are doing np.ons willl create matrix 3,3

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2) # 2 reduce noise 

    # using dilate to thickness and smoothing the images 
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8), iterations=1)

    
    
    mask2 = cv2.bitwise_not(mask1) # except the cloak
   
    # it will give result when the background will be there
    res1 = cv2.bitwise_and(background, background, mask=mask1) # differentiate clock color wrt background
    
    # when i will be in image
    
    res2 = cv2.bitwise_and(img, img, mask=mask2) # substuting the cloak part
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0) #addition of res1 and res2 1 and 0 is a equation
    # aplha time source image 0 is gaama 
    # adding linearly image 

    cv2.imshow('HOLA HUNTER', final_output)
    k = cv2.waitKey(10)
    if k == 27: # using esacpe key  
        break

cap.release()
cv2.destroyAllWindows()
