# Standard imports
import cv2
import numpy as np
import threading
import math

 
# Read image
webcam = cv2.VideoCapture(0)
 
# Set up the detector with default parameters.
params = cv2.SimpleBlobDetector_Params()

params.filterByArea = True
params.minArea = 5000
params.maxArea = 15000
params.filterByCircularity = False
params.filterByConvexity = True
params.minConvexity = 0.1
params.filterByInertia = False
params.minThreshold = 10


detector = cv2.SimpleBlobDetector_create(params)

pancakeCenter = (0,0)
pancakeCords = []

correctCenter = (312, 120)

def thread():
    global pancakeCenter
    global webcam
    global detector
    while True:
        _, imageFrame = webcam.read() 
        grayFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
        cv2.rectangle(grayFrame , (0, 220), (639, 479), 0, -1)
        cv2.rectangle(grayFrame , (400, 0), (639, 479), 0, -1)
        cv2.rectangle(grayFrame , (0, 0), (200, 220), 0, -1)
        cv2.bitwise_not(grayFrame, grayFrame)
        

        array_alpha = np.array([5])
        array_beta = np.array([-100.0])

        # add a beta value to every pixel 
        cv2.add(grayFrame, array_beta, grayFrame)                    

        # multiply every pixel value by alpha
        cv2.multiply(grayFrame, array_alpha, grayFrame) 

        blurredFrame = cv2.GaussianBlur(grayFrame, (1,1), 0)
        
        # Detect blobs.
        keypoints = detector.detect(blurredFrame)
        maxSize = 0
        biggestKeypoint = None
        pancakeCenter = (0,0)
        for keypoint in keypoints:
            center = (round(keypoint.pt[0]), round(keypoint.pt[1]))
            if keypoint.size > maxSize:
                maxSize = keypoint.size
                biggestKeypoint = keypoint
                pancakeCenter = center
            
            cv2.circle(imageFrame, center, 5, (0, 0, 255), -1)

        cv2.circle(imageFrame, correctCenter, 3, (0, 255, 0), -1)
        
        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(imageFrame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Show keypoints
        cv2.imshow("Keypoints", im_with_keypoints)
        cv2.imshow("grayFrame", grayFrame)
        cv2.imshow("blurredFrame", blurredFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'): 
            webcam.release() 
            cv2.destroyAllWindows() 
            break

cvThread = threading.Thread(target=thread)

cvThread.start()

def detectingPancake():
    global pancakeCenter
    pancakeDetected = (pancakeCenter != (0, 0))
    return pancakeDetected

def afwijking():
    global pancakeCenter
    global correctCenter
    return (
        correctCenter[0] - pancakeCenter[0],
        correctCenter[1] - pancakeCenter[1]
    )

def pixelsTocm(pixels:int):
    scaleFactor = 28.8 / 176
    return pixels * scaleFactor

def absoluteDistance():
    return math.sqrt((pixelsTocm(afwijking()[0])**2) + (pixelsTocm(afwijking()[1])**2))
