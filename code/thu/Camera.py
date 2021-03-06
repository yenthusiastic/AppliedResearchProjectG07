from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import sys
import time
import cv2
import numpy as np


""" 
Class to retrieve camera stream in the background to prevent freezing of GUI
[.] +Camera()
NOTE: items with [X] means completed, [+] newly added, [.] on-going, [ ] to-do 
"""

class Camera(QThread):
    # default camera port
    default_camera_port = "/dev/tty/USB0"
    # pyqtSignal to store the camera frame of this thread to be emitted during running
    frame = None
    frame_updated = pyqtSignal(np.ndarray, name='frame_updated')
    # flag to start or stop grabbing camera frames
    camera_on = True
    def __init__(self):
        QThread.__init__(self)
        # initialize capturing
        self.cap = cv2.VideoCapture(0)
        

    def __del__(self):
        print("Stopping thread Camera")
        
        self.wait()

    def run(self):
        while self.camera_on:
            # Capture frame
            ret, self.frame = self.cap.read()
            try:
                # convert color channels
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                #cv2.imshow('frame', frame)
                # emit camera frame to the GUI thread that is calling this thread
                self.frame_updated.emit(self.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as ex:
                print("Error {}: {}".format(type(ex), ex.args))
        # When camera off, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

