import cv2
import pandas as pd
from cryptography.fernet import Fernet
import os


class Scan:
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath("..\\data\\key.key", cur_path)
    with open(new_path, "rb") as file:
        key = file.read()
    file.close()

    new_path = os.path.relpath("..\\data\\csv\\dataset.encrypted.csv", cur_path)
    with open(new_path, "rb") as f:
        data = f.read()

    fernet = Fernet(key)
    token = fernet.decrypt(data)

    with open("..\\data\\csv\\dataset.decrypted.csv", "wb") as f:
        f.write(token)

    def __init__(self, ):
        path = "..\\data\\csv\\dataset.decrypted.csv"
        self.df = pd.read_csv(path, index=False)

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

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            confidence = round(100 - confidence)

        output_details = self.df.iloc[[idnum]]
        output_details = output_details.values.tolist()
        os.remove("data/csv/dataset.csv.decrypted")
        return output_details, confidence
