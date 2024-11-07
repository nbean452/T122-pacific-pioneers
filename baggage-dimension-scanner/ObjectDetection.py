import cv2
import test2utlis

###################################
webcam = False
path = 'image4.jpg'
cap = cv2.VideoCapture(0)
cap.set(10, 160)  # Brightness
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height
scale = 3  # Adjust this based on your setup
wP = 210 * scale  # Width for warping
hP = 297 * scale  # Height for warping

while True:
    if webcam:
        success, img = cap.read()  # Read from webcam
    else:
        img = cv2.imread(path)  # Read from file

    imgContours, conts = test2utlis.getContours(img, minArea=100000, filter=4)
    if len(conts) != 0:
        biggest = conts[0][2]  # Get the largest contour
        nPoints = test2utlis.reorder(biggest)
        imgWarp = test2utlis.warpImg(img, nPoints, wP, hP)

        imgContours2, conts2 = test2utlis.getContours(imgWarp, minArea=2000, filter=4, cThr=[50, 50], draw=False)
        if len(conts2) != 0:  # Check if any contours found after warping
            for obj in conts2:
                cv2.polylines(imgContours2, [obj[2]], True, (0, 255, 0), 2)
                nPoints = test2utlis.reorder(obj[2])  # Reorder points

                # Calculate width and height
                nW = round((test2utlis.findDis(nPoints[0][0], nPoints[1][0]) / scale), 1)  # Width
                nH = round((test2utlis.findDis(nPoints[0][0], nPoints[2][0]) / scale), 1)  # Height

                # Draw arrows and dimensions on the image
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                (nPoints[1][0][0], nPoints[1][0][1]), (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgContours2, (nPoints[0][0][0], nPoints[0][0][1]),
                                (nPoints[2][0][0], nPoints[2][0][1]), (255, 0, 255), 3, 8, 0, 0.05)

                # Get bounding box for text placement
                x, y, w, h = obj[3]
                cv2.putText(imgContours2, '{}cm'.format(nW), (x + 30, y - 10),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 0, 255), 2)
                cv2.putText(imgContours2, '{}cm'.format(nH), (x - 70, y + h // 2),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5, (255, 0, 255), 2)

        cv2.imshow('A4', imgContours2)

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)  # Resize original image for display
    cv2.imshow('Original', img)
    cv2.waitKey(1)