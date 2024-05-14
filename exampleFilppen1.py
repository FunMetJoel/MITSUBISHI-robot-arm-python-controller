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
    newRobot.overrideSpeed(100)

    newRobot.executeCommand("SPD M_NSPD", True)
    #newRobot.executeCommand("M_NSPD", True)
    for i in range(1, 7):
        newRobot.torqueLimit(i, 100)

    print("Code is gestart!")
    
    newRobot.setVariable("D14", AbsPos(281,9,417,180,-20,180))
    newRobot.setVariable("D15", AbsPos(395,10,385,180,0,180))
    newRobot.setVariable("D16", AbsPos(570,32,452,180,45,180))

    newRobot.setVariable("E1", AbsPos(570,32,400,180,0,180))
    newRobot.setVariable("E2", AbsPos(500,32,150,180,-30,180))
    newRobot.setVariable("E3", AbsPos(570,32,150,180,-30,180))
    newRobot.setVariable("E4", AbsPos(570,32,500,180,30,180))
    newRobot.setVariable("E5", AbsPos(570,32,500,180,0,180))

    while True:
        newRobot.moveTo("E1", True, "P")
        time.sleep(1)
        newRobot.moveTo("E2", True, "P")
        time.sleep(1)
        newRobot.moveTo("E3", True, "P")
        time.sleep(1)
        newRobot.moveTo("E4", True, "P")
        time.sleep(1)
        newRobot.moveTo("E5", True, "P")
        time.sleep(1)

    time.sleep(0.5)
    newRobot.end()
    newRobot.resetError()
    