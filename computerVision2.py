# Standard imports
import cv2
import numpy as np;
 
# Read image
webcam = cv2.VideoCapture(0)
 
# Set up the detector with default parameters.
params = cv2.SimpleBlobDetector_Params()

# params.filterByArea = True
# params.minArea = 600
# params.maxArea = 1000
# params.filterByCircularity = False
# params.filterByConvexity = False
# params.filterByInertia = False
params.minThreshold = 70


detector = cv2.SimpleBlobDetector_create(params)

pannenkoek_lower = np.array([120, 150, 100]) 
pannenkoek_upper = np.array([150, 190, 130]) 

pannenkoek_lower = np.array([80, 130, 100]) 
pannenkoek_upper = np.array([150, 210, 170]) 

while True:
    _, imageFrame = webcam.read() 
    imageFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2GRAY)
    imageFrame = cv2.GaussianBlur(imageFrame, (3,3), 0)
    # Detect blobs.
    keypoints = detector.detect(imageFrame)
    
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(imageFrame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    # Show keypoints
    cv2.imshow("Keypoints", im_with_keypoints)
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        webcam.release() 
        cv2.destroyAllWindows() 
        break