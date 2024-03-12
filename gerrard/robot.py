from .robot_serial import RobotSerial
from typing import Union

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
        accel = str(accel)
        decel = str(decel)
        return self.executeCommand(f"ACCEL {accel},{decel}")
    

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

    def moveTo(self, positionVarialbe:str, wait:bool = True) -> Union[str, None]:
        """Move to a posiotion variable

        Args:
            positionVarialbe (str): The name of the position variable
            wait (bool, optional): Whether to wait for a response. Defaults to False

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        self.executeCommand(f"MOV J{positionVarialbe}", wait)

        
    