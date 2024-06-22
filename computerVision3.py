import numpy as np 
import cv2 
import threading
import math

pancakeCenter = (0,0)
pancakeCords = []

correctCenter = (312, 120)

def thread():
    global pancakeCenter
    # Capturing video through webcam 
    webcam = cv2.VideoCapture(0) 

    # Start a while loop 
    while True: 
        _, imageFrame = webcam.read() 
        
        detectionFrame = imageFrame.copy()

        blurredImageFrame = cv2.GaussianBlur(imageFrame, (13,13), 8)

        # [Blue Green Red]
        pannenkoek_rage = [30, 20, 20]
        pr = pannenkoek_rage
        pannenkoek_color = [170, 205, 205]
        pc = pannenkoek_color
        # pannenkoek_lower = np.array([90, 150, 150]) 
        # pannenkoek_upper = np.array([140, 180, 181]) 
        pannenkoek_lower = np.array([pc[0]-pr[0], pc[1]-pr[1], pc[2]-pr[2]]) 
        pannenkoek_upper = np.array([pc[0]+pr[0], pc[1]+pr[1], pc[2]+pr[2]]) 
        
        colorMask = cv2.inRange(blurredImageFrame, pannenkoek_lower, pannenkoek_upper)
        cv2.rectangle(colorMask , (0, 300), (639, 479), 0, -1)
        cv2.rectangle(colorMask , (450, 0), (639, 479), 0, -1)

        # redColorMask = cv2.inRange(blurredImageFrame, (0,0,150), (255,255,181))
        # greenColorMask = cv2.inRange(blurredImageFrame, (0,150,0), (255,180,255))
        # blueColorMask = cv2.inRange(blurredImageFrame, (80,0,0), (140,255,255))

        
        kernel = np.ones((5, 5), "uint8") 

        kerneldColorMask = cv2.dilate(colorMask, kernel) 
        res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = colorMask) 

        # Creating contour to track red color 
        contours, hierarchy = cv2.findContours(colorMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS) 


        
        cv2.circle(detectionFrame, correctCenter, 3, (0, 255, 0), -1)

        pancakeCords = []
        for pic, contour in enumerate(contours): 
            
            area = cv2.contourArea(contour) 
            if(area > 300): 
                x, y, w, h = cv2.boundingRect(contour) 
                detectionFrame = cv2.rectangle(
                    detectionFrame, 
                    (x, y), 
                    (x+w, y+h), 
                    (0, 0, 255), 
                    2
                ) 
                
                cv2.putText(
                    detectionFrame, 
                    "Pannenkoek", 
                    (x, y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                    (0, 0, 255)
                )
                
                
                center = (round(x + (0.5 * w)), round(y + (0.5 * h)))
                size = w * h
                pancakeCords.append((center, size))
                cv2.circle(detectionFrame, center, 5, (0, 0, 255), -1)
        
        if len(pancakeCords) > 0:
            biggestPancake = ((0,0), 0)
            for pancake in pancakeCords:
                if pancake[1] > biggestPancake[1]:
                    biggestPancake = pancake

            pancakeCenter = biggestPancake[0]
        else:
            pancakeCenter = (0, 0)
                
        # Program Termination 
        cv2.imshow('Detection', detectionFrame)
        cv2.imshow('Original', imageFrame)
        cv2.imshow('Blurr', blurredImageFrame)
        cv2.imshow('ColorMask', colorMask)
        cv2.imshow('kerneldColorMask', kerneldColorMask)

        # cv2.imshow('redColorMask', redColorMask)
        # cv2.imshow('greenColorMask', greenColorMask)
        # cv2.imshow('blueColorMask', blueColorMask)

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