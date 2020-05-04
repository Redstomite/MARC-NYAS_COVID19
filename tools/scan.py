import cv2.cv2
import time


class Scan:

    def __init__(self, ):
        self.idnum = 0

    def scan(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("..\\trainer\\trainer.yml")
        cascadepath = "..\\cascade\\haarcascade_frontalface_default.xml"
        facecascade = cv2.CascadeClassifier(cascadepath)

        yield "Initialized."

        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)

        minw = 0.1 * cam.get(3)
        minh = 0.1 * cam.get(4)

        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = facecascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minw), int(minh)),
        )

        confidence = 0
        face_detected = False

        yield "Beginning Scan."
        while True:
            if face_detected:
                yield "Face detected."
                break
            else:
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    self.idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
                    confidence = round(100 - confidence)
                    face_detected = True
                yield "Not detected yet"
                time.sleep(0.5)


        yield "Returning details."
        yield output_details, confidence

    def pin_location(self, cur_loc):
        yield "Adding " + cur_loc + " to data."



        return "Added " + cur_loc + " to " + self.name + "'s data."
