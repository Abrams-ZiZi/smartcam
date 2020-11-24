import serial


class CameraControl:
    def __init__(self, port, baudrate=9600):
        self.__servoX = 0
        self.__servoY = 0

        self.__ser = serial.Serial()
        self.__ser.port = port
        self.__ser.baudrate = baudrate
        self.__ser.timeout = 0.1
        self.__ser.open()

    def __readResponse(self):
        self.__b = bytearray(b"                   ")
        self.__ser.readinto(self.__b)
        return self.__b

    def getPosition(self):
        self.__ser.write(b":RP\x0D")
        self.__position = self.__readResponse()
        self.__servoX = self.__position[0]
        self.__servoY = self.__position[1]
        return self.__servoX, self.__servoY

    def getFaces(self):
        self.__ser.write(b":RF\x0D")
        self.__faceCount = self.__readResponse()
        return self.__faceCount[0]

    def setPosition(self, servoX, servoY):
        self.__servoX = servoX
        self.__servoY = servoY
        self.__ser.write(
            b":SP" + bytes([self.__servoX]) + bytes([self.__servoY]) + b"\x0D"
        )

    def setFaces(self, faceCount):
        self.__faceCount = faceCount
        self.__ser.write(b":SF" + bytes([self.__faceCount]) + b"\x0D")

    def ping(self):
        self.__ser.write(b":@\x0D")
        if self.__readResponse() == "@":
            return True
        else:
            return False

    def moveRight(self):
        self.__ser.write(b":MR\x0D")

    def moveLeft(self):
        self.__ser.write(b":ML\x0D")

    def moveUp(self):
        self.__ser.write(b":MU\x0D")

    def moveDown(self):
        self.__ser.write(b":MD\x0D")
