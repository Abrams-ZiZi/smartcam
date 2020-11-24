import cv2
import numpy as np


class FaceDetect:
    def __init__(
        self,
        camera=0,
        facePath="haarcascade_frontalface_default.xml",
        smilePath="haarcascade_smile.xml",
    ):
        self.__video_capture = cv2.VideoCapture(camera)
        _, self.__frame = self.__video_capture.read()

        self.__resolutionX = np.size(self.__frame, 1)
        self.__resolutionY = np.size(self.__frame, 0)
        self.__cameraX = self.__resolutionX / 2
        self.__cameraY = self.__resolutionY / 2
        self.__cameraW = 0
        self.__cameraH = 0

        self.__faceCascade = cv2.CascadeClassifier(facePath)  # detect objects
        self.__smileCascade = cv2.CascadeClassifier(smilePath)

        self.__smiles = []
        self.__screenshotCounter = 0

    def __stopDetection(self):
        self.__video_capture.release()
        cv2.destroyAllWindows()

    def readImage(self):
        _, self.__frame = self.__video_capture.read()

    def showImage(self):
        cv2.imshow("FaceDetection", self.__frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.__stopDetection()
            return False
        else:
            return True

    def drawFace(self):
        self.__grayFrame = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2GRAY)

        self.__faces = self.__faceCascade.detectMultiScale(
            self.__grayFrame,
            scaleFactor=1.1,  # specifying how much the image size is reduced at each image scale
            minNeighbors=8,  # specify how many neighbors each candidate rectangle should have
            minSize=(55, 55),  # minimum object size
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        for (x, y, w, h) in self.__faces:
            cv2.rectangle(self.__frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            self.__roi_gray = self.__grayFrame[y : y + h, x : x + w]
            self.__roi_color = self.__frame[y : y + h, x : x + w]

            self.__cameraX = x
            self.__cameraY = y
            self.__cameraW = w
            self.__cameraH = h

            self.__drawSmile()

    def __drawSmile(self):
        self.__smiles = self.__smileCascade.detectMultiScale(
            self.__roi_gray,
            scaleFactor=1.7,
            minNeighbors=35,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        for (x, y, w, h) in self.__smiles:
            cv2.rectangle(self.__roi_color, (x, y), (x + w, y + h), (255, 0, 0), 2)

    def getFaceCount(self):
        return len(self.__faces)

    def getFaceCenter(self):
        return (
            self.__cameraX + (self.__cameraW / 2),
            self.__cameraY + (self.__cameraH / 2),
        )

    def saveScreenshot(self, filename):
        if len(self.__smiles) > 0:
            self.__screenshotCounter += 1
            cv2.imwrite(filename + str(self.__screenshotCounter) + ".jpg", self.__frame)

    def getRightBorder(self):
        return self.__resolutionX * 0.7

    def getLeftBorder(self):
        return self.__resolutionX * 0.3

    def getTopBorder(self):
        return self.__resolutionY * 0.3

    def getBottomBorder(self):
        return self.__resolutionY * 0.7
