import cvzone
import cv2
import pickle

with open('positions/carParkPosition_cam2', 'rb') as f:
    posList = pickle.load(f)

width, height = 37, 78


# This function will check available parking spaces in the car parking zone
def checkParkingSpaceFor_Cam2(imgPro, img):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 300:
            spaceCounter += 1
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0, 255, 0), 1)

    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (12, 12), scale=1,
                       thickness=1, offset=10, colorR=(0, 200, 0))
    return img
