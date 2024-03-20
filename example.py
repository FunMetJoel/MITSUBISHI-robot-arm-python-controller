from gerrard import *
import time
import math

newRobot = Robot("/dev/ttyUSB0")

newRobot.connect()

with newRobot:
    print(newRobot.executeCommand("SERVO ON", True))
    time.sleep(2)
    
    pos = [0,90,0,0,0,0]
    newRobot.setAcceleration(10, 10)
    while True:
        Input = input("(a/d)> ").lower()
        if Input == "a":
            pos[0] += 10
        elif Input == "d":
            pos[0] -= 10

        newRobot.setVariable("NEWPOS", tuple(pos))
        newRobot.moveTo("NEWPOS")
        



# with newRobot:
#     print(newRobot.servoOn())
#     time.sleep(1)
#     print(newRobot.servoOff())

