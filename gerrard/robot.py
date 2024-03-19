from .robot_serial import RobotSerial
from typing import Union
from enum import Enum

class VariableType(Enum):
    JOINT = "J"
    POSITION = "P"
    NUMERIC = "M"
    CHARACTER = "C"

class RobotVariable:
    def __init__(self, type:VariableType) -> None:
        self.type = type
        self.value = None

    def __set__(self, instance, value):
        self.value = value
        instance.setVariable(self.name, value)

    def __get__(self, instance, owner):
        return self.value
    
    def __set_name__(self, owner, name):
        self.name = name
        


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

    def setVariable(self, varName:str, value , wait:bool = True) -> Union[str, None]:
        """Set the value of a variable in the robot controller.

        Args:
            varName (str): The name of the variable.
            value : The value to set.
            wait (bool, optional): Whether to wait for a response. Defaults to True.

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        return self.executeCommand(f"J{varName} = {str(value)}", wait)

    def moveTo(self, positionVariable:str, wait:bool = True) -> Union[str, None]:
        """Move to a posiotion variable

        Args:
            positionVarialbe (str): The name of the position variable
            wait (bool, optional): Whether to wait for a response. Defaults to False

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        self.executeCommand(f"MOV J{positionVariable}", wait)

    def createPos(self, name:str, jointDeg:lst, other:lst = "(0,0)"):
        """Werkt nog niet, kan uitgecomment worden
        """
        return self.executeCommand(f"DEF POS {name}")
        


        
    
