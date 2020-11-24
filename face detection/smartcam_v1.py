import facedetect
import cameracontrol
import time


def main():
    smartCamControl = cameracontrol.CameraControl("COM7")
    smartCamVideo = facedetect.FaceDetect(camera=1)

    time.sleep(3)

    smartCamControl.setPosition(90, 60)

    time1Move = time.clock()
    time1Screenshot = time.clock()
    time1Faces = time.clock()

    while smartCamVideo.showImage() is True:
        smartCamVideo.readImage()
        smartCamVideo.drawFace()

        time2Screenshot = time.clock()
        if time2Screenshot - time1Screenshot > 1:
            smartCamVideo.saveScreenshot("smile")
            time1Screenshot = time.clock()

        time2Move = time.clock()
        if time2Move - time1Move > 0.5:
            if smartCamVideo.getFaceCenter()[0] > smartCamVideo.getRightBorder():
                smartCamControl.moveRight()
            if smartCamVideo.getFaceCenter()[0] < smartCamVideo.getLeftBorder():
                smartCamControl.moveLeft()
            if smartCamVideo.getFaceCenter()[1] < smartCamVideo.getTopBorder():
                smartCamControl.moveUp()
            if smartCamVideo.getFaceCenter()[1] > smartCamVideo.getBottomBorder():
                smartCamControl.moveDown()
            time1Move = time.clock()

        time2Faces = time.clock()
        if time2Faces - time1Faces > 0.25:
            if smartCamVideo.getFaceCount() != smartCamControl.getFaces():
                smartCamControl.setFaces(smartCamVideo.getFaceCount())
                time1Faces = time.clock()


main()