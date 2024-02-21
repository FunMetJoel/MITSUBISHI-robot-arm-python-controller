import serial

class robotSerial:
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

        self.robotSlot = robotSlot
        self.controllerSlot = controllerSlot
    
    def __enter__(self):
        self.sendAndWait("GETCNTL") # TODO: check if correct

    def __exit__(self, exc_type, exc_value, traceback):
        self.sendAndWait("RELEASECNTL") # TODO: check if correct

    def __del__(self):
        self.ser.close()

    def send(self, data:str) -> None:
        """Send data to the robot controller.

        Args:
            data (str): The data to send.
        """
        prefix = f"{self.robotSlot};{self.controllerSlot};"
        suffix = "\r"
        self.ser.write(str.encode(prefix + data + suffix))


    def sendAndWait(self, data:str) -> str:
        """Send data to the robot controller and wait for a response.

        Args:
            data (str): The data to send.

        Returns:
            str: The response from the robot controller.
        """
        
        self.send(data)
        return self.ser.read_until(b"\r").decode("utf-8")
    
    def executeCommand(self, command:str, wait:bool = False) -> str|None:
        """Execute a command on the robot controller.

        Args:
            command (str): The command to execute.
            wait (bool, optional): Whether to wait for a response. Defaults to False.

        Returns:
            str|None: The response from the robot controller if wait is True, otherwise None.
        """
        prefix = "EXEC"
        if wait:
            return self.sendAndWait(prefix + command)
        else:
            self.send(prefix + command)

    def parceResponse(self, response:str) -> str:
        """Parce the response from the robot controller.

        Args:
            response (str): The response from the robot controller.

        Returns:
            str: The parsed response.
        """
        return response # TODO: implement
    
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
    