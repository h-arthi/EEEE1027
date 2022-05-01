#!/usr/bin/python3
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
rawCapture = PiRGBArray(camera,size=(162,110))
time.sleep(0.1)

basespeed = 21
KP=0.21#to make the curves easier and make it go straight when the value is smaller (0.22 works)
KD=0.0176#to oscillat eback on track >>value means more oscillation, << value means less oscillation (0.0195 kinda works)
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
pulse1=GPIO.PWM(en,25) #setting the frequency to 1kHz
pulse2=GPIO.PWM(enB,28)
pulse1.start(25) #starting duty cycle at 25%
pulse2.start(25) #starting duty cycle at 25%
#functions for the car
'''
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
        GPIO.output(4,GPIO.LOW)
def left():
        print("left")
        GPIO.output(24,GPIO.LOW) #left
        GPIO.output(25,GPIO.LOW)
        GPIO.output(22,GPIO.HIGH) #right
        GPIO.output(4,GPIO.LOW)
def brake():
        print("stop")
        GPIO.output(24,GPIO.LOW)
        GPIO.output(25,GPIO.LOW)
        GPIO.output(22,GPIO.LOW)
        GPIO.output(4,GPIO.LOW)
        '''

# Loop over all frames captured by camera indefinitely
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # Display camera input
    image = frame.array
    
#    cv2.imshow('img',image)
    
    # Create key to break for loop
    key = cv2.waitKey(1) & 0xFF

    # convert to grayscale, gaussian blur, and threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(7,7),0)
    ret,thresh1 = cv2.threshold(blur,110,255,cv2.THRESH_BINARY_INV)

    # Erode to eliminate noise, Dilate to restore eroded parts of image
    mask = cv2.erode(thresh1, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find all contours in frame
    contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

    # Find x-axis centroid of largest contour and cut power to appropriate motor
    if len(contours) > 0:
    # Find largest contour area and image moments
        c = max(contours, key = cv2.contourArea)
        M = cv2.moments(c)

    # Find x-axis centroid using image moments
        cx = int(M['m10']/M['m00'])
        print('cx =',cx)
        '''
        if cx >= 150:
            left()
        if cx < 151 and cx > 110:
            straight()
        if cx <= 110:
            right()
            '''
         
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
