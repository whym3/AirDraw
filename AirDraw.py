import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
""" Output Window Dimensions"""
cap = cv2.VideoCapture(0)
""" Input from webcam """
cap.set(3, frameWidth)
cap.set(3, frameHeight)

myColor = [[5, 107, 0, 19, 255, 255], [133, 56, 0, 159, 156, 255], [57, 76, 0, 100, 255, 255]]
""" My marker Colors 
 User can add more Values as per need"""

myColorValues = [[51, 153, 255], [255, 0, 255], [0, 255, 0]]
""" Color values of the markers in BGR 
   User can add values as per need these color are printed on the output screen"""

myPoints = []  # [x, y, colorid]

""" This function identifies the marker color
    and displays a circle on the tip of the marker for user assistance"""


def findColor(img, myColor, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []

    # For each of the color a mask is detected and contour is created for each of it
    for color in myColor:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED) # draws a circle on the tip of the pen
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1;       # for giving the right value of color in myColorValues
        # cv2.imshow(str(color[0]), mask)
    return newPoints


""" This function identifies and draws the contour of the object detected """


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0;  # if area < 500 then function returns 0
    for cnt in contours:
        area = cv2.contourArea(cnt)  # if the area is bigger than 500px it draws contour on the image
        if area > 500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y            # returns the value of the tip of the pen, if area < 500 then it returns 0


def AirDraw(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()  # Reads Video from the webcam
    imgResult = img.copy()  # Final image on which all the results are displayed
    newPoints = findColor(img, myColor, myColorValues)  # These 3 values are passed in the function

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)  # new points are added to the list

    """ Appends newly discovered points on the output Screen """
    if len(myPoints) != 0:
        AirDraw(myPoints, myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
