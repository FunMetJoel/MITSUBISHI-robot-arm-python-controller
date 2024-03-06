from libname import *
import time

newRobotSerial = RobotSerial("/dev/ttyUSB0")

newRobotSerial.connect()

with newRobotSerial:
    print(newRobotSerial.sendAndWait("GETCNTL"))
    print(newRobotSerial.sendAndWait("RELEASECNTL"))

# newRobot = Robot("/dev/ttyACM0")

# with newRobot:
#     print(newRobot.servoOn())
#     time.sleep(1)
#     print(newRobot.servoOff())

