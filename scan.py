import cv2
import pandas as pd
from cryptography.fernet import Fernet
import os


class Scan:

    def __init__(self):
        pass

    def scan(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('trainer/trainer.yml')
        cascadepath = "haarcascade_frontalface_default.xml"
        facecascade = cv2.CascadeClassifier(cascadepath)

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

        idnum = 0
        confidence = 0

        file = open("key.key", "rb")
        key = file.read()
        file.close()

        with open("data/csv/dataset.csv.encrypted", "rb") as f:
            data = f.read()

        fernet = Fernet(key)
        token = fernet.decrypt(data)

        with open("data/csv/dataset.csv.decrypted", "wb") as f:
            f.write(token)

        df = pd.read_csv("data/csv/dataset.csv.decrypted", index=False)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            confidence = round(100 - confidence)

        output_details = df.iloc[[idnum]]
        os.remove("data/csv/dataset.csv.decrypted")
        return output_details, confidence
