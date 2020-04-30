import cv2
import time
from datetime import datetime


class Detect:
    name = ""
    cam_names_dict = {}

    def __init__(self, name):
        self.name = name
        self.cam_names_dict = {}

    def setup(self, cam_location_names):
        count = 0
        cam_location_names = cam_location_names
        for location in cam_location_names:
            count = str(count)
            globals()["Cam"+count] = cv2.VideoCapture(count, cv2.CAP_DSHOW)
            self.cam_names_dict["Cam"+count] = location
            count = int(count)
            count += 1

    def begin_scan(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        facecascade = cv2.CascadeClassifier("cascade/haarcascade_frontalface_default.xml")
        len_of_cam_names_dict = len(self.cam_names_dict)

        while True:
            for i in range(len_of_cam_names_dict):
                i = str(i)
                cam = globals()["Cam" + i]
                ret, img = cam.read()
                minw = 0.1 * cam.get(3)
                minh = 0.1 * cam.get(4)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = facecascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(int(minw), int(minh)),
                )

                for (x, y, w, h) in faces:
                    time_of_capture = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cv2.imwrite(
                        "data/detected_faces/" + self.cam_names_dict["Cam"+i] + "/" + time_of_capture + ".jpg",
                        gray[y:y + h, x:x + w]
                    )
                    yield "Face detected at " + self.cam_names_dict["Cam"+i] + "camera on " + time_of_capture + "."
                i = int(i)
                i += 1
                time.sleep(0.25)
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                break
