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
    rb.overrideSpeed(80)
    

    rb.executeCommand("SPD M_NSPD", True)
    #newRobot.executeCommand("M_NSPD", True)
    for i in range(1, 7):
        rb.torqueLimit(i, 50)

    print("Code is gestart!")
    
    #QoKX;522.13;Y;288.62;Z;215.49;A;178.59;B;-13.61;C;1.90;;7,0;100;0.00;00000000
    rb.setVariable("Start", AbsPos(490, 0, 220.49, 178.59, -13.61, 1.90, 7, 0))

    rb.moveTo("Start", mode="P")

    time.sleep(2)
    print("We zijn bij start!")

    noten = ["A", "B", "C", "D", "E", "F", "G"]

    # Piano toets is 24 breed
    # 0 pos C van oktaaf 0

    RobotY = 0
    
    def gaNaar(noot:str, oktaaf:int=-2):
        global RobotY
        oktaafbreette = 168
        OldRobotY = RobotY 
        RobotY = (0.15 + (2 * 24)) - (oktaaf * oktaafbreette) - (noten.index(noot) * 24)
        rb.setVariable("toets", AbsPos(490, RobotY, 200, 178.59, -13.61, 1.90, 7, 0))
        rb.moveTo("toets", mode="P")
        time.sleep(0.3)#abs(OldRobotY - RobotY) * 0.01)

    def druk():
        rb.setVariable("toets", AbsPos(490, RobotY, 180, 178.59, -13.61, 1.90, 7, 0))
        rb.moveTo("toets", mode="P")
        time.sleep(0.4)
        rb.setVariable("toets", AbsPos(490, RobotY, 200, 178.59, -13.61, 1.90, 7, 0))
        rb.moveTo("toets", mode="P")
        time.sleep(0.3)
    
    # while True:
    #     Letter = ""
    #     while Letter not in noten:
    #         Letter = input("Letter: ").upper()
        
    #     gaNaar(Letter)
    #     druk()

    gaNaar("C")
    time.sleep(1)

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
        (G, -2),

        (E, -2),
        (F, -2),
        (G, -2),

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
        gaNaar(item[0], item[1])
        time.sleep(0.1)
        druk()

 
    time.sleep(0.5)
    rb.end()
    rb.resetError()
    