import cv2
import numpy as np
import default2

###################################
webcam = True
path = 'image2.jpg'  # Path to the image if webcam is not used
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cap.set(10, 160)  # Brightness
cap.set(3, 1920)  # Width
cap.set(4, 1080)  # Height

scale = 3  # Scale factor for measurement
wP = 630 # Width of the A4 paper in pixels
hP = 891  # Height of the A4 paper in pixels
###################################

while True:
    if webcam:
        success, img = cap.read()
        if not success:
            print("Error: Could not read frame.")
            break
    else:
        img = cv2.imread(path)

    imgContours, conts = default2.getContours(img, minArea=50000, filter=4)

    if len(conts) != 0:
        biggest = conts[0][2]
        imgWarp = default2.warpImg(img, biggest, wP, hP)

        imgContours2, conts2 = default2.getContours(imgWarp, minArea=2000, filter=4, cThr=[50, 50], draw=False)

        if len(conts) != 0:  # Ensure there are contours to process
            for obj in conts2:
                cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
                nPoints = default2.reorder(obj[2])
                nW = round((default2.findDis(nPoints[0][0] // scale, nPoints[1][0] // scale) / 10), 1)
                nH = round((default2.findDis(nPoints[0][0] // scale, nPoints[2][0] // scale) / 10), 1)

                # Draw arrows for width and height
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                (nPoints[1][0][0], nPoints[1][0][1]), (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                (nPoints[2][0][0], nPoints[2][0][1]), (255, 0, 255), 3, 8, 0, 0.05)

                # Get bounding box coordinates
                x, y, w, h = obj[3]
                cv2.putText(imgContours2, '{}cm'.format(nW), (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(imgContours2, '{}cm'.format(nH), (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)

        cv2.imshow('A4', imgContours2)

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow('Original', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Allow exit with 'q'
        break

cap.release()  # Release the webcam
cv2.destroyAllWindows()  # Close all OpenCV windows