import pickle
import cvzone
import cv2
import numpy as np
from mainFiles.checkParkingSpaces_cam1 import checkParkingSpaceFor_Cam1
from mainFiles.checkParkingSpaces_cam2 import checkParkingSpaceFor_Cam2
from mainFiles.checkParkingSpaces_cam3 import checkParkingSpaceFor_Cam3
from mainFiles.checkParkingSpaces_cam4 import checkParkingSpaceFor_Cam4

cap1 = cv2.VideoCapture('Videos/carParkingSpace_cam1.mp4')
cap2 = cv2.VideoCapture('Videos/carParkingSpace_cam2.mp4')
cap3 = cv2.VideoCapture('Videos/carParkingSpace_cam3.mp4')
cap4 = cv2.VideoCapture('Videos/carParkingSpace_cam4.mp4')

# This function will preprocess each frame of the video
# so that i can free spaces available
def preprocessImage(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    return imgDilate

# This function adds the border in the image so that we can differentiate videos
def addBorders(img1, img2, img3, img4):
    horZeros = np.zeros(((6, 602, 3)), np.uint8)
    verZeros = np.zeros(((336, 6, 3)), np.uint8)

    img1 = np.hstack((img1, verZeros))
    img1 = np.vstack((img1, horZeros))

    img2 = np.hstack((verZeros, img2))
    img2 = np.vstack((img2, horZeros))

    img3 = np.hstack((img3, verZeros))
    img3 = np.vstack((horZeros, img3))

    img4 = np.hstack((verZeros, img4))
    img4 = np.vstack((horZeros, img4))

    return [img1, img2, img3, img4]


while True:
    # These if functions are making sure that if the frame is last frame
    # Then i am setting the frame position to zero so that i can play it in loop
    if(cap1.get(cv2.CAP_PROP_POS_FRAMES) == cap1.get(cv2.CAP_PROP_FRAME_COUNT)):
        cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
    if(cap2.get(cv2.CAP_PROP_POS_FRAMES) == cap2.get(cv2.CAP_PROP_FRAME_COUNT)):
        cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
    if (cap3.get(cv2.CAP_PROP_POS_FRAMES) == cap3.get(cv2.CAP_PROP_FRAME_COUNT)):
        cap3.set(cv2.CAP_PROP_POS_FRAMES, 0)
    if (cap4.get(cv2.CAP_PROP_POS_FRAMES) == cap4.get(cv2.CAP_PROP_FRAME_COUNT)):
        cap4.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img1 = cap1.read()
    success, img2 = cap2.read()
    success, img3 = cap3.read()
    success, img4 = cap4.read()

    # Preprocessing the image so that we can detect a available parking space
    processedImg1 = preprocessImage(img1)
    # This function will put rectangle on the available parking spaces in the frame
    img1 = checkParkingSpaceFor_Cam1(processedImg1, img1)

    processedImg2 = preprocessImage(img2)
    img2 = checkParkingSpaceFor_Cam2(processedImg2, img2)

    processedImg3 = preprocessImage(img3)
    img3 = checkParkingSpaceFor_Cam3(processedImg3, img3)

    processedImg4 = preprocessImage(img4)
    img4 = checkParkingSpaceFor_Cam4(processedImg4, img4)

    # We are adding borders so that we can differentiate videos
    img1, img2, img3, img4 = addBorders(img1, img2, img3, img4)

    # Stacking images so that we can view them in one single window
    temp1 = np.hstack((img1, img2))
    temp2 = np.hstack((img3, img4))

    finalImg = np.vstack((temp1, temp2))

    cv2.imshow("All Parking Zones", finalImg)

    cv2.waitKey(30)