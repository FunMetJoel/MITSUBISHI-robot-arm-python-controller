import numpy as np 
import cv2 


# Capturing video through webcam 
webcam = cv2.VideoCapture(0) 

params = cv2.SimpleBlobDetector_Params()

params.filterByArea = True
params.minArea = 100
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False

detector = cv2.SimpleBlobDetector_create(params)

# Start a while loop 
while True: 
    _, imageFrame = webcam.read() 

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

    pannenkoek_lower = np.array([0, 0, 200]) 
    pannenkoek_upper = np.array([255, 200, 255]) 
    # pannenkoek_lower = np.array([240, 0, 0]) 
    # pannenkoek_upper = np.array([255, 20, 20]) 
    pannenkoek_mask = cv2.inRange(hsvFrame, pannenkoek_lower, pannenkoek_upper)

    cv2.rectangle(pannenkoek_mask , (0, 300), (639, 479), 0, -1)
    maskedImageFrame = cv2.bitwise_and(imageFrame,imageFrame, mask=pannenkoek_mask)

    kernel = np.ones((5, 5), "uint8") 

    pannenkoek_mask = cv2.dilate(pannenkoek_mask, kernel) 
    res_red = cv2.bitwise_and(imageFrame, imageFrame, 
    						mask = pannenkoek_mask) 

    # Creating contour to track red color 
    contours, hierarchy = cv2.findContours(pannenkoek_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS) 

    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        if(area > 300): 
            x, y, w, h = cv2.boundingRect(contour) 
            imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                    (x+w, y+h), 
                                    (0, 0, 255), 2) 
            
            cv2.putText(imageFrame, "Pannenkoek", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (0, 0, 255))	 

    # Detect blobs.
    keypoints = detector.detect(imageFrame)
    im_with_keypoints = cv2.drawKeypoints(maskedImageFrame, keypoints, np.array([]), (0,0,255))

            
    # Program Termination 
    cv2.imshow('Original', imageFrame)
    cv2.imshow('hsvFrame', hsvFrame)
    cv2.imshow('Masked', maskedImageFrame)
    cv2.imshow('Masked2', pannenkoek_mask)
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        webcam.release() 
        cv2.destroyAllWindows() 
        break
