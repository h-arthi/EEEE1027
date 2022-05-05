#hithere
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO
import time
import cv2
import picamera
import numpy as np

# Initialize camera
camera = picamera.PiCamera()
camera.resolution = (192,112)
camera.framerate = 20
rawCapture = PiRGBArray(camera,size=(162,112))
time.sleep(0.1)

basespeed = 23
KP=0.22#to make the curves easier and make it go straight when the value is smaller (0.2 works)
KD=0.015#to oscillat eback on track >>value means more oscillation, << value means less oscillation (0.0095 kinda works)
last_error=0

# setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
en = 17
enB = 23
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
pulse1=GPIO.PWM(en,68)#setting the frequency to 1kHz
pulse2=GPIO.PWM(enB,71)
pulse1.start(25) #starting duty cycle at 25%
pulse2.start(25) #starting duty cycle at 25%
#functions for the car

def straight():
         print("straight")
         GPIO.output(24,GPIO.HIGH)
         GPIO.output(25,GPIO.LOW)
         GPIO.output(22,GPIO.HIGH)
         GPIO.output(4,GPIO.LOW)
         print("forward")
def back():
        print("backward")
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(22,GPIO.LOW)
        GPIO.output(4,GPIO.HIGH)
def right():
        print("right")
        GPIO.output(24,GPIO.HIGH)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(22,GPIO.LOW)
        GPIO.output(4,GPIO.HIGH)
def left():
        print("left")
        GPIO.output(24,GPIO.LOW) #left
        GPIO.output(25,GPIO.HIGH)
        GPIO.output(22,GPIO.HIGH) #right
        GPIO.output(4,GPIO.LOW)
def brake():
        print("stop")
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(22,GPIO.LOW)
        GPIO.output(4,GPIO.LOW)
        

# Loop over all frames captured by camera indefinitely
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # Display camera input
    image = frame.array
    
    cv2.imshow('img',image)
    
    # Create key to break for loop
    key = cv2.waitKey(1) & 0xFF

    # convert to grayscale, gaussian blur, and threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(7,7),0)
    ret,thresh1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY_INV)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #picking a lower and upper bound colour to extract pixels from
    lower_blue = np.array([100,75,2],np.uint8)
    upper_blue = np.array([120, 255,255],np.uint8)
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([40,255,255])
    red_lower = np.array([160, 50, 50], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
    green_lower = np.array([48, 170, 60], np.uint8)
    green_upper = np.array([90, 255, 255], np.uint8)
    mask4 = cv2.inRange(hsv, green_lower, green_upper)
    mask3 = cv2.inRange(hsv, red_lower, red_upper)
    kernal = np.ones((5,5),"uint8")
    mask1 = cv2.inRange(hsv, lower_blue, upper_blue)
    blueMask = cv2.dilate(mask1, kernal)
    mask2 = cv2.inRange(hsv, lower_yellow, upper_yellow)
    results = cv2.bitwise_and(image, image, mask = blueMask)
    results1 = cv2.bitwise_and(image, image, mask = mask2)
    redMask = cv2.dilate(mask3, kernal)
    results2 = cv2.bitwise_and(image, image, mask = redMask)
    greenMask = cv2.dilate(mask4, kernal)
    results3 = cv2.bitwise_and(image, image, mask = greenMask)
    # Erode to eliminate noise, Dilate to restore eroded parts of image
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    
    contours1,_ = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours2,_ = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours3,_ = cv2.findContours(redMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours4,_ = cv2.findContours(greenMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.imshow("green mask",results3)    
    cv2.imshow("blue mask",results)
    cv2.imshow("yellow mask",results1)
    cv2.imshow("red mask",results2)


    

    # Find all contours in frame
    contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

    # Find x-axis centroid of largest contour and cut power to appropriate motor

    if len(contours1) > 0:
        cn = max(contours1, key = cv2.contourArea)
        if (cv2.contourArea(cn)) < 7800 and (cv2.contourArea(cn)) < 8300:
            M1 = cv2.moments(cn)
            blueCn = cv2.drawContours(image, contours, -1,(0,255,0),3)
            if M1 != 0.0:
                x = int(M1['m10'])
                y = int(M1['m00'])
                if x & y != 0:
                    cxB = int(x/y)
                    if cxB > 0:
                        cx = cxB
                        print('cxB =' ,cxB)
    if len(contours3) > 0:
                cn3 = max(contours3, key = cv2.contourArea)
                if (cv2.contourArea(cn3)) < 7000 and (cv2.contourArea(cn3)) < 8300:
                    M3 = cv2.moments(cn3)
                    redCn = cv2.drawContours(image, contours, -1,(0,255,0),3)
                    if M3 != 0.0:
                        x2 = int(M3['m10'])
                        y2 = int(M3['m00'])
                        if x2 & y2 != 0:
                            cxR = int(x2/y2)
                            if cxR > 0:
                                cx = cxR
                                print('cxR =' ,cxR)
    if len(contours2) > 0:
        cn2 = max(contours2, key = cv2.contourArea)
        M2 = cv2.moments(cn2)
        #print(cv2.contourArea(cn2))
        if (cv2.contourArea(cn2)) > 700:
            yellowCn = cv2.drawContours(image, contours, -1,(0,255,0),3)
            if M2 != 0.0:
                x1 = int(M2['m10'])
                y1 = int(M2['m00'])
                if x1 & y1 != 0:
                    cxY = int(x1/y1)
                    if cxY > 0:
                        cx = cxY
                        print('cxY =', cxY)           
                   
            
    if len(contours4) > 0:
        cn4 = max(contours4, key = cv2.contourArea)
        if (cv2.contourArea(cn4)) >500:
            M4 = cv2.moments(cn4)
            #print(cv2.contourArea(cn4))
            greenCn = cv2.drawContours(image, contours, -1,(0,255,0),3)
            if M4 != 0.0:
                x4 = int(M4['m10'])
                y4 = int(M4['m00'])
                if x4 & y4 != 0:
                    cxG = int(x4/y4)
                    if cxG > 0:
                        cx = cxG
                        print('cxG =', cxG)

    if len(contours) > 0:
        # Find largest contour area and image moments
            c = max(contours, key = cv2.contourArea)
            M = cv2.moments(c)
            # Find x-axis centroid using image moments
            cx = int(M['m10']/M['m00'])
            print("cx =",cx)
                                           
    error = 100 - cx
    derivative = error - last_error
    speedL = basespeed - (error * KP + derivative * KD)
    speedR = basespeed + (error * KP + derivative * KD)
    if speedL <= 0:
        speedL = 0
    if speedR <= 0:
        speedR = 0
    last_error = error
    
    pulse1.ChangeDutyCycle(speedR)
    pulse2.ChangeDutyCycle(speedL)
    GPIO.output(24,GPIO.HIGH)
    GPIO.output(25,GPIO.LOW)
    GPIO.output(22,GPIO.HIGH)
    GPIO.output(4,GPIO.LOW)

    if key == ord("q"):
            
            break

    rawCapture.truncate(0)

GPIO.output(24, GPIO.LOW)
GPIO.output(25, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(4, GPIO.LOW)

GPIO.cleanup()
cv2.destroyAllWindows()
