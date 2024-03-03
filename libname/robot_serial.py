import serial
from typing import Union

class RobotSerial:
    """Class for communication with the robot controller via serial port.

    Args:
        port (str): The serial port to connect to the robot controller.
        baudrate (int): The baudrate of the serial port. Defaults to 9600.
        robotSlot (int): The slot number of the robot. Defaults to 1.
        controllerSlot (int): The slot number of the controller. Defaults to 1.
    """
    def __init__ (self, port:str, baudrate:int=9600, robotSlot:int=1, controllerSlot:int=1) -> None:
        self.ser = serial.Serial(port, baudrate)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.timeout = 5

        self.robotSlot = robotSlot
        self.controllerSlot = controllerSlot

    def connect(self) -> None:
        """Connect to the robot controller."""
        self.ser.open()
    
    def __enter__(self):
        self.sendAndWait("CNTLON") # TODO: check if correct

    def __exit__(self, exc_type, exc_value, traceback):
        self.sendAndWait("CNTLOFF") # TODO: check if correct

    def __del__(self):
        self.ser.close()

    def write(self, data:str, wait:bool = False) -> None:
        """Write data to the robot controller.

        Args:
            data (str): The data to write.
            wait (bool, optional): Whether to wait for a response. Defaults to False.

        Returns:
            str: The response from the robot controller if wait is True, otherwise None.
        """
        self.ser.write(str.encode(data))
        if wait:
            return self.ser.read_until(b"\r").decode("utf-8")

    def send(self, data:str, wait:bool = False) -> None:
        """Send data to the robot controller.

        Args:
            data (str): The data to send.
            wait (bool, optional): Whether to wait for a response. Defaults to False.

        Returns:
            str: The response from the robot controller if wait is True, otherwise None.
        """
        prefix = f"{self.robotSlot};{self.controllerSlot};"
        suffix = "\r"
        return self.write((prefix + data + suffix), wait)
    
    def executeCommand(self, command:str, wait:bool = False) -> Union[str, None]:
        """Execute a command on the robot controller.

        Args:
            command (str): The command to execute.
            wait (bool, optional): Whether to wait for a response. Defaults to False.

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        prefix = "EXEC"
        return self.send(prefix + command, wait)

    def parceResponse(self, response:str) -> str:
        """Parce the response from the robot controller.

        Args:
            response (str): The response from the robot controller.

        Returns:
            str: The parsed response.
        """
        return response # TODO: implement