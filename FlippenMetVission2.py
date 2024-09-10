from gerrard import *
import time
import math
import computerVision2 as comVis
import readkey
import numpy as np

bot = Robot("/dev/ttyUSB0")

totalFlips = 0

OverallSpeed = 70
TorqueLimit = 70
goedeFlipThreshold = 2
HOMEPOS = AbsPos(570,0,400,-90,90,180)

def setup():
    bot.end()
    bot.resetError()
    print(bot.executeCommand("SERVO ON", True))
    time.sleep(2)

    bot.executeCommand("SPD M_NSPD", True)
    #bot.executeCommand("M_NSPD", True)
    for i in range(1, 7):
        bot.torqueLimit(i, TorqueLimit)

    bot.setVariable("HOMEPOS", HOMEPOS)

    print("-- Homing --")
    bot.overrideSpeed(0.1 * OverallSpeed)
    bot.moveTo("HOMEPOS", True, "P")
    time.sleep(5)
    bot.overrideSpeed(OverallSpeed)

    bot.setVariable("DOWNPOS", AbsPos(470,-22,150,-90,60,180))
    bot.setVariable("FLIPPOS", AbsPos(570,0,500,-90,115,180))
    bot.setVariable("VANGPOS", AbsPos(500,0,500,-90,90,180))

def goedLegAlgoritme():
    speedMultiplier = 0.1
    lastAfwijking = (0,0)
    while True:
        bot.moveTo("HOMEPOS", True, "P")
        time.sleep(0.5 + (0.04 / speedMultiplier) )

        while not comVis.detectingPancake():
            print("-! Not Detecting Pancake !-")
            time.sleep(1)

        afwijking = comVis.afwijking()
        
        print(f"({comVis.pixelsTocm(afwijking[0]):.2f}cm, {comVis.pixelsTocm(afwijking[1]):.2f}cm)")

        if comVis.absoluteDistance() < goedeFlipThreshold:
            break

        #Speed berekenen
        if (lastAfwijking != (0,0)):
            hoeveelBewogen = (
                lastAfwijking[0] - afwijking[0],
                lastAfwijking[1] - afwijking[1]
            )

            verhouding = (
                hoeveelBewogen[0]/lastAfwijking[0],
                hoeveelBewogen[1]/lastAfwijking[1]
            )

            # absHoeveelBewogen = math.sqrt(hoeveelBewogen[0]**2 + hoeveelBewogen[1] ** 2)

            # abslastAfwijking = math.sqrt(lastAfwijking**2, lastAfwijking**2)

            # verhouding = (absHoeveelBewogen/abslastAfwijking)

        lastAfwijking = afwijking

        bot.overrideSpeed(speedMultiplier * OverallSpeed)
        time.sleep(0.1)

        
        bot.setVariable("CORRPOS", HOMEPOS + AbsPos(
            0,#(afwijking[0]/abs(afwijking[0]+0.000001))*50,
            0,#10*afwijking[1],
            0,#-100,
            0,
            min(max(abs(afwijking[0])*7,5),20) * np.sign(afwijking[0]),
            min(max(abs(afwijking[1])*4,4),20) * -np.sign(afwijking[1])
        ))
        bot.moveTo("CORRPOS", True, "P")
        time.sleep(0.5 + (0.04 / speedMultiplier) )

def flip():
    global totalFlips
    print(f'Ready To Flip #{totalFlips}')

    #input()
    bot.moveTo("DOWNPOS", True, "P")
    time.sleep(1)
    bot.moveTo("FLIPPOS", True, "P")
    time.sleep(0.6)
    bot.moveTo("VANGPOS", True, "P")
    time.sleep(1)    

    totalFlips += 1


def main():
    bot.moveTo("HOMEPOS", True, "P")
    time.sleep(1)

    goedLegAlgoritme()

    flip()

if __name__ == "__main__":
    print(f"-- Starting file --")
    print(f"-- {__file__} --")

    bot.connect()

    with bot:
        print("-- Setting up Robot --")
        setup()
        print("-- Robot ready --")

        stopCondition = (readkey.pressedKeys.count(readkey.keyboard.Key.pause) != 0)
        while not stopCondition:
            main()

        print("-- Stopped --")
