## Can filp pannenkoek

from gerrard import *
import time
import math
import computerVision3
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
        newRobot.torqueLimit(i, 70)

    print("Code is gestart!")

    # StartPos
    F1 = AbsPos(570,0,400,-90,90,180)
    newRobot.setVariable("F1", F1)
    
    # Flip
    newRobot.setVariable("F5", AbsPos(470,-22,150,-90,70,180))
    newRobot.setVariable("F6", AbsPos(570,0,500,-90,113,180))
    newRobot.setVariable("F7", AbsPos(500,0,500,-90,90,180))

    newRobot.moveTo("F1", True, "P")
    time.sleep(1) 
    input()

    # for i in range(5):
    while readkey.pressedKeys.count(readkey.keyboard.Key.pause) == 0:
        newRobot.moveTo("F1", True, "P")
        time.sleep(1) 

        while not computerVision3.detectingPancake():
            print(" Not Detecting Pancake ")
            pass

        print(computerVision3.afwijking())
        print(f"({computerVision3.pixelsTocm(computerVision3.afwijking()[0])}cm, {computerVision3.pixelsTocm(computerVision3.afwijking()[1])}cm)")

        goedeFlipThreshold = 2

        while computerVision3.absoluteDistance() > goedeFlipThreshold:
            newRobot.overrideSpeed(90)
            time.sleep(1) 

            print(f"({computerVision3.pixelsTocm(computerVision3.afwijking()[0])}cm, {computerVision3.pixelsTocm(computerVision3.afwijking()[1])}cm)")
            afwijking = (computerVision3.pixelsTocm(computerVision3.afwijking()[1]), computerVision3.pixelsTocm(computerVision3.afwijking()[0]))
            newRobot.setVariable("F2", F1 + AbsPos(0,0,0,0,10,0) )
            newRobot.moveTo("F2", True, "P")
            time.sleep(1) 
            newRobot.setVariable("F2", F1 + AbsPos((afwijking[0]/abs(afwijking[0]+0.000001))*50,10*afwijking[1],-100,0,-20,0) )
            newRobot.moveTo("F2", True, "P")
            time.sleep(1) 
            newRobot.moveTo("F1", True, "P")
            time.sleep(2) 
    
            while not computerVision3.detectingPancake():
                time.sleep(0.1) 
                print("Not Detecting Pankake")

        newRobot.overrideSpeed(90)
        time.sleep(1) 
        print('Ready To Flip')

        # print(computerVision3.afwijking())
        # print(f"({computerVision3.pixelsTocm(computerVision3.afwijking()[0])}cm, {computerVision3.pixelsTocm(computerVision3.afwijking()[1])}cm)")
        # input()
        # while computerVision3.absoluteDistance() > 0.25:
        #     newRobot.setVariable("F2", F1 + AbsPos(-30,0,0,0,20,0) )
        #     newRobot.moveTo("F2", True, "P")
        #     time.sleep(1) 
        #     newRobot.setVariable("F2", F1 + AbsPos(20+computerVision3.pixelsTocm(computerVision3.afwijking()[1]),0,-100,0,-20,0) )
        #     newRobot.moveTo("F2", True, "P")
        #     time.sleep(1) 
        #     newRobot.moveTo("F1", True, "P")
        #     time.sleep(2) 
        #     print(f"({computerVision3.pixelsTocm(computerVision3.afwijking()[0])}cm, {computerVision3.pixelsTocm(computerVision3.afwijking()[1])}cm)")


        input()
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