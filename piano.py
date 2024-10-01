from gerrard import *
import time
import math
#import pyautogui

rb = Robot("/dev/ttyUSB0")

rb.connect()

with rb:
    
    rb.end()
    rb.resetError()
    print(rb.executeCommand("SERVO ON", True))
    time.sleep(2)
    rb.overrideSpeed(30)
    

    rb.executeCommand("SPD M_NSPD", True)
    #newRobot.executeCommand("M_NSPD", True)
    for i in range(1, 7):
        rb.torqueLimit(i, 50)

    print("Code is gestart!")
    
    #QoKX;522.13;Y;288.62;Z;215.49;A;178.59;B;-13.61;C;1.90;;7,0;100;0.00;00000000
    rb.setVariable("Start", AbsPos(490, 0, 220.49, 178.59, -13.61, 1.90, 7, 0))

    rb.moveLinearTo("Start", mode="P")

    time.sleep(1)
    print("We zijn bij start!")

    noten = ["A", "B", "C", "D", "E", "F", "G"]

    # Piano toets is 24 breed
    # 0 pos C van oktaaf 0

    RobotY = 0
    
    def gaNaar(noot:str, oktaaf:int=-2):
        global RobotY
        oktaafbreette = 168
        RobotY = (0.15 + (2 * 24)) - (oktaaf * oktaafbreette) - (noten.index(noot) * 24)
        rb.setVariable("toets", AbsPos(490, RobotY, 190, 178.59, -13.61, 1.90, 7, 0))
        rb.moveLinearTo("toets", mode="P")
        time.sleep(0.25)#abs(OldRobotY - RobotY) * 0.01)

    def gaMetArcNaar(noot:str, oktaaf:int=-2):
        global RobotY
        oldRobotY = RobotY
        oktaafbreette = 168
        RobotY = (0.15 + (2 * 24)) - (oktaaf * oktaafbreette) - (noten.index(noot) * 24)
        rb.setVariable("t1", AbsPos(490, oldRobotY, 182, 178.59, -13.61, 1.90, 7, 0))
        time.sleep(0.1)
        rb.setVariable("t2", AbsPos(490, oldRobotY + 0.5 * (RobotY - oldRobotY), 200, 178.59, -13.61, 1.90, 7, 0))
        time.sleep(0.1)
        rb.setVariable("t3", AbsPos(490, RobotY, 182, 178.59, -13.61, 1.90, 7, 0))
        time.sleep(0.1)
        rb.MoveArc("t1", "t2", "t3")
        time.sleep(1)


    def druk(nootlengteMultiplier = 1):
        rb.setVariable("toets", AbsPos(490, RobotY, 180, 178.59, -13.61, 1.90, 7, 0))
        rb.moveLinearTo("toets", mode="P")
        time.sleep(0.25 * nootlengteMultiplier)
        rb.setVariable("toets", AbsPos(490, RobotY, 195, 178.59, -13.61, 1.90, 7, 0))
        rb.moveLinearTo("toets", mode="P")
        time.sleep(0.25)
    
    # while True:
    #     Letter = ""
    #     while Letter not in noten:
    #         Letter = input("Letter: ").upper()
        
    #     gaNaar(Letter)
    #     druk()
    gaNaar("C")
    time.sleep(4)
    rb.overrideSpeed(20)

    # VaderJacob = "CDECCDECEFGEFG"
    A,B,C,D,E,F,G = "A","B","C","D","E","F","G"
    VaderJacob = [
        (C, -2),
        (D, -2),
        (E, -2),
        (C, -2),

        (C, -2),
        (D, -2),
        (E, -2),
        (C, -2),

        (E, -2),
        (F, -2),
        (G, -2, 4),

        (E, -2),
        (F, -2),
        (G, -2, 4),

        (G, -2),
        (A, -1),
        (G, -2),
        (F, -2),
        (E, -2),
        (C, -2),

        (G, -2),
        (A, -1),
        (G, -2),
        (F, -2),
        (E, -2),
        (C, -2),

        (C, -2),
        (G, -3),
        (C, -2),

        (C, -2),
        (G, -3),
        (C, -2),
    ]
    

    for item in VaderJacob:
        multiplier = 1
        if len(item) > 2:
            multiplier = item[2]
        gaMetArcNaar(item[0], item[1])
        # time.sleep(0.1)
        # druk(multiplier)

 
    time.sleep(0.5)
    rb.end()
    rb.resetError()
    