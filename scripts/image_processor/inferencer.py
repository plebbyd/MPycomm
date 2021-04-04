import cv2
from threading import Thread



class Processor():

    def __init__(self):
        self.frame = None
        self.height = None
        self.width = None
        self.imageStream = None
        self.show_frames = False
        self.grabber = None

    def openStream(self, device_id=0):
        #Device id is an integer value designating which capture device to go through
        #Standard webcam uses device_id = 0
        if cv2.VideoCapture(device_id) is not None and self.imageStream is None:
            self.imageStream = cv2.VideoCapture(device_id)
            return True
        else:
            return False

    def setDimensions(self, height, width):
        self.height = height
        self.width = width

        return (self.height, self.width)

    def getFrame(self):
        if self.frame is not None:
            return self.frame
        return False

    def closeStream(self):
        if self.imageStream is not None:
            self.imageStream.release()
            self.imageStream = None
            return True

        return False

    def frameGrabber(self):
        while self.imageStream is not None:
            ret, self.frame = self.imageStream.read()

            if self.show_frames:
                cv2.imshow('Processor Frame', self.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()
        return False

    def startGrabber(self):
        self.grabber = Thread(target=self.frameGrabber()).start()

    
