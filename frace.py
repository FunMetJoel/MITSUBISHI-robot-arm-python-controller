from gerrard import *
import time
import math
#import pyautogui

newRobot = Robot("/dev/ttyUSB0")

newRobot.connect()

with newRobot:
    newRobot.end()
    newRobot.resetError()
    print(newRobot.executeCommand("SERVO ON", True))
    time.sleep(2)
    
    #newRobot.setAcceleration(50, 50)
    newRobot.overrideSpeed(50)

    newRobot.executeCommand("SPD M_NSPD", True)
    #newRobot.executeCommand("M_NSPD", True)
    for i in range(1, 7):
        newRobot.torqueLimit(i, 100)

    print("Code is gestart!")

    xbounds = (270, 570)
    ybounds = (-200, 200)
    
    newRobot.setVariable("E1", AbsPos(xbounds[0],ybounds[0],400,180,0,180))
    newRobot.setVariable("E2", AbsPos(xbounds[1],ybounds[1],400,180,0,180))

    newRobot.setVariable("H1", AbsPos(xbounds[0],ybounds[0],400,180,0,180))
    newRobot.setVariable("H2", AbsPos(xbounds[0],ybounds[1],400,180,0,180))
    newRobot.setVariable("H3", AbsPos(xbounds[1],ybounds[1],400,180,0,180))
    newRobot.setVariable("H4", AbsPos(xbounds[1],ybounds[0],400,180,0,180))


    

    while True:
        newRobot.moveLinearTo("H1", True, "P")
        print("H1")
        time.sleep(2)
        newRobot.moveLinearTo("H2", True, "P")
        print("H2")
        time.sleep(2)
        newRobot.moveLinearTo("H3", True, "P")
        print("H3")
        time.sleep(2)
        newRobot.moveLinearTo("H4", True, "P")
        print("H4")
        time.sleep(2)

        


    time.sleep(0.5)
    newRobot.end()
    newRobot.resetError()
    