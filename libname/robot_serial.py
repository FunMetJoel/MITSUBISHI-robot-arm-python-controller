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
        self.ser = serial.Serial(port, baudrate, stopbits=2, parity="E")
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.timeout = 5

        self.robotSlot = robotSlot
        self.controllerSlot = controllerSlot

    def connect(self) -> None:
        """Connect to the robot controller."""
        print(self.write("1;1;OPEN=NARCUSR\r", True))
        print(self.write("3F;3F;7,0;3,5,A,1E,32,46,64;MB4;PRM;RV-3SB;CRn-5xx;MELFA;05-07-14;Ver.K4a;ENG;MAG IK EEN KOEKJE;1;1;8;\r", True))
        print(self.write("1;1;PARRLNG\r", True))
        print(self.write("RLNG;1;1\r", True))
        print(self.write("1;1;PDIRTOP\r", True))
        print(self.write("1.MB4;4767;24-02-2821:05:14;2;220160;12;;9;82;135256;6848;9661;14\r", True))
        print(self.write("1;1;PPOSF\r", True))
        print(self.write("X;176.01;Y;33.14;Z;541.62;A;77.92;B;-25.59;C;106.80;;6,15728640;100;0.00;00000000\r", True))
        print(self.write("1;1;PARMEXTL\r", True))
        print(self.write("MEXTL;0.00, 0.00, 0.00, 0.00, 0.00, 0.00;6\r", True))
        print(self.write("1;1;KEYWDptest\r", True))
    
    def __enter__(self):
        self.send("CNTLON", True) # TODO: check if correct

    def __exit__(self, exc_type, exc_value, traceback):
        self.send("CNTLOFF", True) # TODO: check if correct

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