import cv2
import os
import time
import pandas as pd
import numpy as np
from PIL import Image
from pymongo import MongoClient

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
camera.set(3, 640)
camera.set(4, 480)
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

idcsv = pd.read_csv('idcsv.csv')
face_id = 0

for index, row in idcsv.iterrows():
    face_id += 1

face_id += 1
first_name = input("Enter first name (and middle name if applicable): ")
second_name = input("Enter family/second name: ")

idcsv.at[face_id, "ID"] = face_id
idcsv.at[face_id, "First Name"] = first_name
idcsv.at[face_id, "Last Name"] = last_name
idcsv.to_csv("idcsv.csv")

#time.sleep(2)
count = 0

"""while True:
    ret, img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])
        cv2.imshow('image', img)
    if count >= 40:
        break
    print("[System] ", count, " pictures taken")
    time.sleep(0.2)


print("Exiting capture program")
camera.release()
cv2.destroyAllWindows()

path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def getimagesandlabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
    return faceSamples, ids


print("[System] Training dataset and optimizing ML algorithms")
faces, ids = getimagesandlabels(path)
recognizer.train(faces, np.array(ids))

recognizer.write('trainer/trainer.yml')

print("\n[System] {0} faces trained. Exiting Program".format(len(np.unique(ids))))

print("[System] Program: Success")
print("[System] Process finished with exit code 0")"""

print(face_id)
