import cv2
import numpy as np

def getContours(img,cThr=[100,100],showCanny=False,minArea=1000,filter=0,draw =False):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,cThr[0],cThr[1])
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=3)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    if showCanny: cv2.imshow('Canny', imgThre)
    contours, hiearchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append([len(approx), area, approx, bbox, i])
            else:
                finalCountours.append([len(approx), area, approx, bbox, i])
    finalCountours = sorted(finalCountours, key=lambda x: x[1], reverse=True)
    if draw:
        for con in finalCountours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)
    return img, finalCountours

def reorder(myPoints):         #This is for if for example the images' coordinates are mixed up for example 1,4,2,3 or 1,3,2,4, we need to
                                #reorder in the cases to get 1,2,3,4, and not have an inverted image
    myPointsNew = np.zeros_like(myPoints)
    myPoints = myPoints.reshape((4, 2))
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]  # Top-left
    myPointsNew[3] = myPoints[np.argmax(add)]  # Bottom-right
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # Top-right
    myPointsNew[2] = myPoints[np.argmax(diff)]  # Bottom-left
    return myPointsNew

def warpImg(img, pts, wP, hP): #This is for the warping the image to only consider the background be able to map the
                                #image with its background so its able to identify its dimensions.
    pts = reorder(pts)
    pts1 = np.float32(pts)
    pts2 = np.float32([[0, 0], [wP, 0], [0, hP], [wP, hP]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (wP, hP))
    return imgWarp

def findDis(pts1, pts2):     #This is for objects that are at a slanted position, so we use Pythagorean theorem formula
    return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5