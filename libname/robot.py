from .robot_serial import robotSerial

class robot(robotSerial):
    def __init__(self, port:str, baudrate:int=9600, robotSlot:int=1, controllerSlot:int=1) -> None:
        super().__init__(port, baudrate, robotSlot, controllerSlot)

    def servoOn(self, wait:bool = False) -> str|None:
        """Turn on the servo of the robot.

        Args:
            wait (bool, optional): Whether to wait for a response. Defaults to False.

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        return self.executeCommand("SERVO ON", wait)
    
    def servoOff(self, wait:bool = False) -> str|None:
        """Turn off the servo of the robot.

        Args:
            wait (bool, optional): Whether to wait for a response. Defaults to False.

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        return self.executeCommand("SERVO OFF", wait)
    