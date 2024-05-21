## Can filp pannenkoek

from gerrard import *
import time
import math
#import pyautogui
import readkey



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

    # StartPos
    newRobot.setVariable("F1", AbsPos(570,0,400,-90,90,180))

    # Centreren
    newRobot.setVariable("F2", AbsPos(520,-50,400,-90,90,180))
    newRobot.setVariable("F3", AbsPos(620,50,400,-90,90,180))
    newRobot.setVariable("F4", AbsPos(570,0,400,-90,90,180))
    
    # Flip
    newRobot.setVariable("F5", AbsPos(470,-22,150,-90,70,180))
    newRobot.setVariable("F6", AbsPos(570,0,500,-90,113,180))
    newRobot.setVariable("F7", AbsPos(500,0,500,-90,90,180))

    # for i in range(5):
    while readkey.pressedKeys.count(readkey.keyboard.Key.pause) == 0:
        newRobot.moveTo("F1", True, "P")
        time.sleep(1)
        # newRobot.moveTo("F2", True, "P")
        # time.sleep(1)

        # newRobot.moveTo("F3", True, "P")
        # time.sleep(1)
        # newRobot.moveTo("F4", True, "P")
        #time.sleep(1)
        newRobot.moveTo("F5", True, "P")
        time.sleep(1)
        newRobot.moveTo("F6", True, "P")
        time.sleep(0.6)
        newRobot.moveTo("F7", True, "P")
        time.sleep(1)    

    newRobot.end()
    newRobot.servoOff()
    newRobot.resetError()
    print('closed')