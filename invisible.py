import cv2
import time
import numpy as np

cap = cv2.VideoCapture(0)  # Read from the web cam

time.sleep(3)  # for the system to sleep for 3 second before the webcam starts
for i in range(30):
    retval, back = cap.read()
back = np.flip(back, axis=1)


# detecting the red portion In each frame
while (cap.isOpened()):  # Read every Frame from the webcam, until the camera is open
    ret, img = cap.read()
    if not ret:
        break
    img = np.flip(img, axis=1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 70])
    upper_red = np.array([9, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([171, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(img, img, mask=mask2)
    res2 = cv2.bitwise_and(back, back, mask=mask1)

    finalOutput = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow("magic", finalOutput)
    cv2.waitKey(10)


cap.release()
cv2.destroyAllWindows()