from gerrard import *
import time
import math


newRobot = Robot("/dev/ttyUSB0")

newRobot.connect()

with newRobot:
    newRobot.end()
    print(newRobot.executeCommand("SERVO ON", True))
    time.sleep(2)
    
    pos = [0,90,0,0,0,0]
    newRobot.setAcceleration(10, 10)
    # #newRobot.overrideSpeed(10)
    for i in range(1, 7):
        newRobot.torqueLimit(i, 50)

    print("HALLO")

    currentPos = AbsPos(500.15,0,638.38,5.05,81.40,4.85)

    newRobot.setVariable("COSIROP", currentPos, True)

    #newRobot.write("1;1;EXECPCOSIROP=(400.15,0,638.38,5.05,81.40,4.85)(6,0)\r", True)
    #time.sleep(1)
    newRobot.moveTo("COSIROP", True, "P")
    #newRobot.write("1;1;EXECMOV PCOSIROP\r")
    time.sleep(4)
    print(newRobot.resetError())


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
        #newRobot.moveTo("NEWPOS")
        



# with newRobot:
#     print(newRobot.servoOn())
#     time.sleep(1)
#     print(newRobot.servoOff())

