# import the pyautogui library to test and use it to do initial cursor movement
import pyautogui
import cv2
import time
import numpy as np
import HandTrackingModule as HTM
import math


# find the size of the screen
print(pyautogui.size())

###
wCam, hCam = pyautogui.size().width, pyautogui.size().height
###

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = HTM.handDetector(mode=False, maxHands=2, detectionCon=0.7, trackCon=0.5)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList[0]) != 0:
        # print(lmList[0][4], lmList[0][8], lmList[1])
        x1, y1 = lmList[0][4][1], lmList[0][4][2]
        x2, y2 = lmList[0][8][1], lmList[0][8][2]
        cX, cY = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cX, cY), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        if length < 50:
            cv2.circle(img, (cX, cY), 15, (0, 255, 255), cv2.FILLED)
            print(cX, cY)
            # pyautogui.moveTo(cX, cY)
            # pyautogui.click(cX, cY)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Img", img)
    cv2.waitKey(1)

    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)


# move the cursor to a specified location over a period of time
pyautogui.moveTo(1000, 100, duration=1)

# move the cursor relative to its current position over a period of time
pyautogui.moveRel(0, 50, duration=1)

# print out the current position of the cursor
print(pyautogui.position())

# click at a specified location
pyautogui.click(100, 100)