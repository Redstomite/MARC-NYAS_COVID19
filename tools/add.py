import cv2
import os
import pandas as pd
import numpy as np
from PIL import Image
import pylevenshtein as pylev
from cryptography.fernet import Fernet


class Add:
    """
    Class to deal with new users.
    """

    nationality = ""
    first_name = ""
    middle_name = ""
    last_name = ""
    gender = ""
    age = 0
    lev = 0
    confidence = 0
    details = []
    df = pd.DataFrame()
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    file = open("key.key", "rb")
    key = file.read()
    file.close()

    with open("data/csv/dataset.csv.encrypted", "rb") as f:
        data = f.read()

    fernet = Fernet(key)
    token = fernet.decrypt(data)

    with open("data/csv/dataset.csv.decrypted", "wb") as f:
        f.write(token)
    """
    Uses the Fernet key of the encrypted csv file to decrypt its contents and
    create a new temporary file.
    """


    def __init__(self):
        self.nationality = ""
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.gender = ""
        self.age = 0
        self.lev = 0
        self.confidence = 0
        self.df = pd.DataFrame()
        self.details = []
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.travelled = "No"

    def load(self, details):
        """
        Loads data and sets values within the class.

        Parameters
        ----------
        details : list
            A list of details of the user.
        """
        self.nationality = details[0]
        self.nationality = details[1]
        self.first_name = details[2]
        self.middle_name = details[3]
        self.last_name = details[4]
        self.gender = details[5]
        self.age = details[6]
        self.travelled = details[7]
        self.df = pd.read_csv("data/csv/dataset.csv.decyrpted", index=False)

    def check(self):
        """
        Checks if user is in database.
        """
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("trainer/trainer.yml")
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

        output_details = []
        idnum = 0
        confidence = 0

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            idnum, self.confidence = recognizer.predict(gray[y:y + h, x:x + w])
            output_details = self.df.iloc[[idnum]]
            self.confidence = round(100 - confidence)

        if output_details[1] is None:
            output_name = output_details[0] + " " + output_details[2]
        else:
            output_name = output_details[0] + " " + output_details[1] + "" + output_details[2]
        if self.middle_name is None:
            input_name = self.first_name + " " + self.last_name
        else:
            input_name = self.first_name + " " + self.middle_name + " " + self.last_name

        lev = pylev.levenshtein.distc(output_name, input_name)
        return_output = [idnum, self.confidence, output_details, lev]

        return return_output

    def user_add(self, confirm):
        """
        Adds user to database.
        """
        if self.lev >= 2 and self.confidence <= 45 and confirm == "yes":
            face_id = 0
            for row in self.df.iterrows():
                face_id = row

            count = 0
            for val in self.details:
                self.df.at[face_id, count] = val

            camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            camera.set(3, 640)
            camera.set(4, 480)
            face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            count = 0

            while True:
                ret, img = camera.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    count += 1
                    cv2.imwrite(self.nationality + "/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h,
                                                                                                        x:x + w])
                    cv2.imshow('image', img)
                if count >= 40:
                    break

            camera.release()
            cv2.destroyAllWindows()

            return "Added" + self.first_name + " to the database. Train model."
        else:
            raise NotImplementedError("Model output 'user in database'. If not checked user, please do.")

    def getimagesandlabels(self, path):
        """
        System function. No calling.
        """
        imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
        facesamples = []
        idnum = 0
        ids = []
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        for imagePath in imagepaths:
            pil_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(pil_img, 'uint8')
            idnum = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                facesamples.append(img_numpy[y:y + h, x:x + w])
        ids.append(idnum)
        return facesamples, ids

    def train(self):
        """
        Trains yml model.
        """
        path = self.nationality
        faces, ids = self.getimagesandlabels(path)
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.write('trainer/trainer.yml')
        return ids

    def flush(self):
        """
        Resets all values and destroys decrypted csv file.
        """
        self.nationality = ""
        self.first_name = ""
        self.middle_name = ""
        self.last_name = ""
        self.gender = ""
        self.age = 0
        self.lev = 0
        self.confidence = 0
        self.df = pd.DataFrame()
        self.details = []
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.travelled = "No"
        os.remove("data/csv/dataset.csv.decrypted")
