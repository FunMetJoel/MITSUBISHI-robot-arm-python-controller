from gerrard import *
import time

newRobotSerial = Robot("/dev/ttyUSB0")

newRobotSerial.connect()

with newRobotSerial:
    print(newRobotSerial.executeCommand("SERVO ON", True))
    time.sleep(2)
    newRobotSerial.setAcceleration(20, 20)

    newRobotSerial.executeCommand("JOVRD 10", True)
    newRobotSerial.executeCommand("JCOSIROP = ( 10.000, 0.000, 0.000, 0.000, 0.000, 0.000)", True)
    newRobotSerial.executeCommand("MOV J_CURR + JCOSIROP", True)



# with newRobot:
#     print(newRobot.servoOn())
#     time.sleep(1)
#     print(newRobot.servoOff())

