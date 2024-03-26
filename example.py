from gerrard import *
import time
import math

newRobot = Robot("/dev/ttyUSB0")

newRobot.connect()

with newRobot:
    print(newRobot.executeCommand("SERVO ON", True))
    time.sleep(2)
    
    pos = [0,90,0,0,0,0]
    newRobot.setVariable("NEWPOS", tuple(pos))
    newRobot.moveTo("NEWPOS")
    newRobot.setAcceleration(3, 3)
    for i in range(6):
        newRobot.torqueLimit(i+1, 30)
    while True:
        Input = input("(a/d)> ").lower()
        if Input == "a":
            pos[0] += 10
        elif Input == "d":
            pos[0] -= 10
        elif Input == "r":
            newRobot.resetError()


        newRobot.setVariable("NEWPOS", tuple(pos))
        newRobot.moveTo("NEWPOS")
        



# with newRobot:
#     print(newRobot.servoOn())
#     time.sleep(1)
#     print(newRobot.servoOff())

