from __future__ import annotations
from .robot_serial import RobotSerial
from typing import Union, List, Tuple
from .customtypes import JointPos, AbsPos
            
class Robot(RobotSerial):
    def __init__(self, port:str, baudrate:int=9600, robotSlot:int=1, controllerSlot:int=1) -> None:
        super().__init__(port, baudrate, robotSlot, controllerSlot)

    def servoOn(self, wait:bool = False) -> Union[str, None]:
        """Turn on the servo of the robot.

        Args:
            wait (bool, optional): Whether to wait for a response. Defaults to False.

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        return self.executeCommand("SERVO ON", wait)
    
    def servoOff(self, wait:bool = False) -> Union[str, None]:
        """Turn off the servo of the robot.

        Args:
            wait (bool, optional): Whether to wait for a response. Defaults to False.

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        return self.executeCommand("SERVO OFF", wait)
    
    def setAcceleration(self, accel:int = 100, decel:int = 100) -> None:
        """Set maximum acceleration and deceleration in percentages

        Args:
            accel (int, 0 to 100): Maximum acceleration in %
            decel (int, 0 to 100): Maximum deceleration in %
        """
        accel = str(accel)
        decel = str(decel)
        return self.executeCommand(f"ACCEL {accel},{decel}")
        
    def torqueLimit(self, axisNr:int = 0, limitPercentage:int = 100):
        """Set maximum torque on specified axis
        
        Args:
            axisNr (int): axis number (1 to 6)
            limitPercentage (int): maximum torque allowed on specified axis
        """
        self.executeCommand(f"TORQ {axisNr},{limitPercentage}")    

    def setVariable(self, varName:str, value, wait:bool = True) -> Union[str, None]:
        """Set the value of a variable in the robot controller.

        Args:
            varName (str): The name of the variable.
            value : The value to set.
            wait (bool, optional): Whether to wait for a response. Defaults to True.

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        if type(value) == JointPos or type(value) == tuple:
            varType = "J"
        elif type(value) == AbsPos:
            varType = "P"
        elif type(value) == int | type(value) == float:
            varType = "M"
        elif type(value) == str:
            varType = "C"
        else:
            raise TypeError(f"Type {type(value)} is not supported")
        
        return self.executeCommand(f"{varType}{varName} = {str(value)}", wait)

    def moveTo(self, positionVariable:str, wait:bool = True, mode:str = "J",) -> Union[str, None]:
        """Move to a posiotion variable

        Args:
            positionVarialbe (str): The name of the position variable
            mode (str): J or P
            wait (bool, optional): Whether to wait for a response. Defaults to False

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        self.executeCommand(f"MOV {mode}{positionVariable}", wait)
    
    def resetError(self, wait:bool = True):
        return self.send("RSTALRM", wait)

    def maxSpeed(self, speed:int):
        """Set maximum movement speed"""
        return self.executeCommand(f"SPD {speed}")
    
    def overrideSpeed(self, speed:int):
        """Set override speed"""
        return self.executeCommand(f"OVRD {speed}")
    
    def end(self):
        return self.executeCommand("END")
    
    def getPos(self):
        return self.send("PPOSF", True)
    
    def MoveCircle(self, start, point1, point2):
        return self.executeCommand(f"MVC {start},{point1},{point2}")
    
    def MoveArc(self, pos1, pos2, pos3):
        return self.executeCommand(f"MVR {pos1}, {pos2}, {pos3}")

        
    
