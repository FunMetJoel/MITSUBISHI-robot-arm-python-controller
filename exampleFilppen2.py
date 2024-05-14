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
    
    #newRobot.setAcceleration(3, 3)
    newRobot.overrideSpeed(100)

    newRobot.executeCommand("SPD M_NSPD", True)
    #newRobot.executeCommand("M_NSPD", True)
    for i in range(1, 7):
        newRobot.torqueLimit(i, 100)

    print("Code is gestart!")
    
    newRobot.setVariable("D14", AbsPos(281,9,417,180,-20,180))
    newRobot.setVariable("D15", AbsPos(395,10,385,180,0,180))
    newRobot.setVariable("D16", AbsPos(570,32,452,180,45,180))

    newRobot.setVariable("E1", AbsPos(570,32,400,180,0,90))
    newRobot.setVariable("E2", AbsPos(500,32,150,180,0,90))
    newRobot.setVariable("E3", AbsPos(570,32,150,180,0,90))
    newRobot.setVariable("E4", AbsPos(570,32,500,180,0,90))
    newRobot.setVariable("E5", AbsPos(570,32,500,180,0,90))


    # StartPos
    newRobot.setVariable("F1", AbsPos(570,0,400,-90,90,180))

    # Centreren
    newRobot.setVariable("F2", AbsPos(520,-50,400,-90,90,180))
    newRobot.setVariable("F3", AbsPos(620,50,400,-90,90,180))
    newRobot.setVariable("F4", AbsPos(570,0,400,-90,90,180))
    
    # Flip
    newRobot.setVariable("F5", AbsPos(470,-22,150,-90,60,180))
    newRobot.setVariable("F6", AbsPos(570,0,500,-90,120,180))
    newRobot.setVariable("F7", AbsPos(500,0,500,-90,90,180))


    newRobot.setVariable("G1", AbsPos(500,32,150,-180,90,90))
    newRobot.setVariable("G2", AbsPos(500,32,150,-90,70,180))

    for i in range(5):
        newRobot.moveTo("F1", True, "P")
        input()#time.sleep(1)
        # newRobot.moveTo("F2", True, "P")
        # time.sleep(1)
        
        # newRobot.moveTo("F3", True, "P")
        # time.sleep(1)
        # newRobot.moveTo("F4", True, "P")
        time.sleep(1)
        newRobot.moveTo("F5", True, "P")
        time.sleep(1)
        newRobot.moveTo("F6", True, "P")
        time.sleep(0.6)
        newRobot.moveTo("F7", True, "P")
        time.sleep(1)


    time.sleep(0.5)
    newRobot.end()
    newRobot.servoOff()
    newRobot.resetError()
    