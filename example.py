from gerrard import *
import time

newRobotSerial = RobotSerial("/dev/ttyUSB0")

newRobotSerial.connect()

with newRobotSerial:
    print(newRobotSerial.executeCommand("SERVO ON", True))
    time.sleep(2)

    newRobotSerial.executeCommand("JOVRD 10", True)
    newRobotSerial.executeCommand("JCOSIROP = ( 50.000, 0.000, 0.000, 0.000, 0.000, 0.000)", True)
    newRobotSerial.executeCommand("MOV J_CURR + JCOSIROP", True)

newRobot = Robot("/dev/ttyACM0")
newRobot.servoOff()

# with newRobot:
#     print(newRobot.servoOn())
#     time.sleep(1)
#     print(newRobot.servoOff())

