import pyautogui
import cv2
import time
import numpy as np
import HandTrackingModule as HTM
import math

# Find the size of the screen
screen_width, screen_height = pyautogui.size()

# Set the camera resolution
camera_width, camera_height = 1280, 720

# Calculate the scaling factors
x_scale = screen_width / camera_width
y_scale = screen_height / camera_height

# Initialize camera capture
cap = cv2.VideoCapture(0)
cap.set(3, camera_width)
cap.set(4, camera_height)

# Initialize mouse position to the center of the screen
pyautogui.moveTo(screen_width // 2, screen_height // 2)

# Initialize other variables
pTime = 0
detector = HTM.handDetector(mode=False, maxHands=2, detectionCon=0.9, trackCon=0.5)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList[0]) != 0:
        # print(lmList[0][8])

        # Thumb (4)
        x1, y1 = lmList[0][4][1], lmList[0][4][2]
        # Pointer Finger (8)
        x2, y2 = lmList[0][8][1], lmList[0][8][2]
        # Middle Finger (12)
        x3, y3, = lmList[0][12][1], lmList[0][12][2]
        # Center of Thumb and Middle Finger
        cX1, cY1 = (x1 + x3) // 2, (y1 + y3) // 2

        # Scale the hand coordinates to the screen resolution
        scaled_cX = int(x2 * x_scale)
        scaled_cY = int(y2 * y_scale)

        # Circle on thumb
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        # Circle on middle finger
        cv2.circle(img, (x3, y3), 15, (255, 0, 255), cv2.FILLED)
        # Circle on the center line
        cv2.circle(img, (cX1, cY1), 15, (255, 0, 255), cv2.FILLED)
        # Line between middle finger and thumb
        cv2.line(img, (x1, y1), (x3, y3), (255, 0, 255), 3)

        # Length between 4 and 8
        length = math.hypot(x2 - x1, y2 - y1)
        # Length between 4 and 12
        length2 = math.hypot(x3 - x1, y3 - y1)

        # Move mouse to pointer finger
        pyautogui.moveTo(scaled_cX, scaled_cY + 50)

        if int(length2) >= 100:
            print(int(length2))
            # print(cX1, cY1)
        else:
            cv2.circle(img, (cX1, cY1), 15, (0, 255, 255), cv2.FILLED)
            pyautogui.click(scaled_cX, scaled_cY)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Img", img)
    cv2.waitKey(1)

    cv2.putText(img, f"FPS: {int(fps)}", (200, 500), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
