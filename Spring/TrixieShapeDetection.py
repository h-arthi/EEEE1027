import numpy as np
import cv2

cap = cv2.VideoCapture(0)



while True:
    ret, frame = cap.read() #getting input frm the camera
    frame = frame[100:500, 100:600]
    width = int(cap.get(3)) #setting the width of the display frame
    height = int(cap.get(4))#setting the height of the display frame
    #making the image gray and applying thresh
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    _, thresh = cv2.threshold(blur, 125, 255, cv2.THRESH_BINARY_INV)
    canny = cv2.Canny(thresh, 127, 175)
    contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    circle = 0
    quadrilateral = 0
    triangle = 0
    pentagon = 0
    other = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 700:
            approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True) #gets the vertices
            cv2.drawContours(frame, [contour], 0, (0, 0, 255), 5) #draws contours
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
                if len(approx) == 3:
                    cv2.putText(frame, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    triangle += 1
                elif len(approx) == 4:
                    cv2.putText(frame, "Quadrilateral", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    quadrilateral+=1
                elif len(approx) == 5:
                    cv2.putText(frame, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    pentagon+=1
                else:
                    cv2.putText(frame, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
                    circle+=1

    cv2.putText(frame, "Number of Shapes:"+ str(len(contours)),(10,25),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0))                
    #cv2.imshow("gray", gray)
    cv2.imshow("thresh", thresh)
    cv2.imshow('Canny', frame)
    print("-----")
    print("Number of Circles = ",circle/2)                
    print("Number of Quadrilaterals = ",quadrilateral/2)
    print("Number of Pentagon = ",pentagon/2)
    print("Number of Triangles = ",triangle/2)
    print("Total Number of Shapes = ",circle/2+quadrilateral/2+pentagon/2+triangle/2)
    print("-----")

    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()       

    