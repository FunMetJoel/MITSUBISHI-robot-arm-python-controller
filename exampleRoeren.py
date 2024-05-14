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
    
    pos = [0,90,0,0,0,0]
    newRobot.setAcceleration(3, 3)
    #newRobot.overrideSpeed(100)

    newRobot.executeCommand("SPD M_NSPD", True)
    #newRobot.executeCommand("M_NSPD", True)
    for i in range(1, 7):
        newRobot.torqueLimit(i, 50)

    print("Code is gestart!")
    #newRobot.setVariable("B1", JointPos(0,0,0,0,0,0), True)
    #newRobot.moveTo("B1")


    # newRobot.setVariable("D1", AbsPos(518, 88, 403, -174, 43, -162))
    # newRobot.setVariable("D2", AbsPos(470, 255, 636, -151, 80, -123))
    # newRobot.setVariable("D3", AbsPos(521, -118, 636, -151, 80, -165))
    newRobot.setVariable("D1", JointPos(90,0,0,0,0,0))
    # # newRobot.setVariable("D2", JointPos(0,5,0,0,0,0))
    # # newRobot.setVariable("D3", JointPos(0,90,0,0,0,0))
    # # newRobot.setVariable("D4", AbsPos(695,0,485,-180,90,180)) #X;695.00;Y;0.00;Z;485.00;A;-180.00;B;90.00;C;180.00;;5,0;100;0.00;00000000
    # newRobot.setVariable("D5", AbsPos(538,158,566,0,83,14))
    # newRobot.setVariable("D6", AbsPos(538,235,665,0,83,14))
    # newRobot.setVariable("D7", AbsPos(538,76,665,0,83,14))

    # newRobot.setVariable("D8", AbsPos(337,-89,716,96,71,0))
    # newRobot.setVariable("D9", AbsPos(419,-90,590,97,7,0))
    # newRobot.setVariable("D10", AbsPos(325,-88,744,96,-23,0))

    # newRobot.setVariable("D11", AbsPos(538,158,566,0,83,14))
    # newRobot.setVariable("D12", AbsPos(538,150,558,0,83,14))
    # newRobot.setVariable("D13", AbsPos(538,150,574,0,83,14))

    newRobot.setVariable("D14", AbsPos(300,0,416,180,0,0))
    newRobot.setVariable("D15", AbsPos(400,0,416,180,0,0))
    newRobot.setVariable("D16", AbsPos(350,-50,416,180,0,0))
    # newRobot.setVariable("D17", AbsPos(192,-33,909,23,-55,129))

    # newRobot.moveTo("D14", mode="P")
    # time.sleep(2)
    # newRobot.moveTo("D15", mode="P")
    # time.sleep(2)
    # newRobot.moveTo("D16", mode="P")
    # time.sleep(2)
    while True:
        newRobot.moveTo("D14", True, "P")
        #newRobot.MoveArc("PD14", "PD15", "PD16")
        newRobot.MoveCircle("PD14", "PD15", "PD16")
    #newRobot.MoveArc("PD5", "PD6", "PD7")
    # newRobot.moveTo("D1", mode="J")
    # time.sleep(3)
    # newRobot.moveTo("D8", mode="P")
    # time.sleep(3)
    # newRobot.moveTo("D9", mode="P")
    # time.sleep(3)
    # newRobot.moveTo("D10", mode="P")
    # newRobot.executeCommand("CMPG 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5")
    # newRobot.executeCommand("CMP POS, &B111111")

    time.sleep(0.5)
    newRobot.end()
    newRobot.resetError()
    