import serial

class robotSerial:
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
        prefix = f"{self.robotSlot};{self.controllerSlot};"
        suffix = "\r"
        self.ser.write(str.encode(prefix + data + suffix))

    def sendAndWait(self, data:str) -> str:
        self.send(data)
        return self.ser.read_until(b"\r").decode("utf-8")
    
    def executeCommand(self, command:str, wait:bool = False) -> str|None:
        prefix = "EXEC"
        if wait:
            return self.sendAndWait(prefix + command)
        else:
            self.send(prefix + command)

    def parceResponse(self, response:str) -> str:
        return response # TODO: implement
    
class robot(robotSerial):
    def __init__(self, port:str, baudrate:int=9600, robotSlot:int=1, controllerSlot:int=1) -> None:
        super().__init__(port, baudrate, robotSlot, controllerSlot)

    def servoOn(self, wait:bool = False) -> str|None:
        return self.executeCommand("SERVO ON", wait)
    
    def servoOff(self, wait:bool = False) -> str|None:
        return self.executeCommand("SERVO OFF", wait)
    
    
    
    

    