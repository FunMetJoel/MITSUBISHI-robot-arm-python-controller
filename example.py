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
    #newRobot.setAcceleration(10, 10)
    #newRobot.overrideSpeed(100)

    newRobot.executeCommand("SPD M_NSPD", True)
    #newRobot.executeCommand("M_NSPD", True)
    for i in range(1, 7):
        newRobot.torqueLimit(i, 50)

    print("Code is gestart!")

    pos1 = AbsPos(-40,0,950,0,0,-0)
    #pos2 = AbsPos(500,0,500.38,0,90,0)
    #pos3 = AbsPos(377,2,500.38,0,90,0)
    # pos1 = AbsPos(500,200,400.38,0,90,0)
    # pos2 = AbsPos(500,0,500.38,0,90,0)
    # pos3 = AbsPos(500,-200,400.38,0,90,0)

    #pos4 = AbsPos(-555.70,72.60,576.22,11.74,35.06,-20.25)
    #pos5 = AbsPos(-555.70,72.60,576.22,11.74,35.06,-20.25)
    #pos6 = AbsPos(600,0,500.38,0,90,0)

    
    newRobot.setVariable("A1", pos1, True)
    #newRobot.setVariable("A2", pos2, True)
    #newRobot.setVariable("A3", pos6, True)

    #newRobot.moveTo("A1", True, "P")
    newRobot.setVariable("B1", JointPos(90,0,0,0,0,0), True)
    newRobot.moveTo("B1")
    time.sleep(1)
    newRobot.moveTo("A1", True, "P")

    # while True:
    #     pass
        #newRobot.executeCommand("MVR3 PA1, PA3, PA2 TYPE 0, 1", True)
        # newRobot.executeCommand("MVS PA1", True)
        # time.sleep(1)
        # newRobot.executeCommand("MOV PA3", True)
        # time.sleep(1)
        # newRobot.executeCommand("MVR PA1, PA2, PA3 ", True)
        # time.sleep(1)
        # newRobot.executeCommand("MVR PA3, PA2, PA1", True)
        # time.sleep(1)
        #print(newRobot.getPos())


    # while True:
    #     # print(pyautogui.position(), pos[0], pos[1])

    #     # # Gets scroll wheel input and moves the robot accordingly
    #     # scrollAmount = pyautogui.scroll()

                
    #     # pos[0] = 0 + ((pyautogui.position()[0] - 800) / -10)
    #     # pos[1] = 90 + ((pyautogui.position()[1] - 540) / 10)
    #     Input = input("(a/d)> ").lower()
    #     if Input == "a":
    #         pos[0] += 10
    #     elif Input == "d":
    #         pos[0] -= 10

    #     #newRobot.setVariable("NEWPOS", JointPos(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]))
            
    #     # QoKX;179.12;Y;11.94;Z;955.42;A;-0.28;B;30.77;C;1.63;;5,0;100;0.00;0000000
    #     #newRobot.setVariable("NEWPOS", AbsPos(179, 12, 955, 0, 30, 1))
    #     print(newRobot.executeCommand("P1234 = (203.00,368.84,872.01,0.00,44.60,61.10)(7,0)", True))
    #     time.sleep(2)
    #     print(newRobot.executeCommand("MOV P1234", True))
    #     newRobot.moveTo("NEWPOS")
        



# with newRobot:
#     print(newRobot.servoOn())
#     time.sleep(1)
#     print(newRobot.servoOff())

