import os
import cv2
import pandas as pd


class Command:
    def __init__(self):
        pass

    def display_cam_data(self, date):
        path = "..\\data\\detected_faces\\" + date
        list_of_img_names = os.listdir(path)

        for img_name in list_of_img_names:
            path = "..\\data\\detected_faces\\" + date + "\\" + img_name
            cv2.imshow(img_name, path)

        return len(list_of_img_names)

    def totals(self):
        path = "..\\data\\csv\\totals.csv"
        totals = pd.read_csv(path, index=False)
        output_details = totals.values.tolist()
        return output_details

    def cam_hits_per_day(self, date):
        path = "..\\data\\csv\\img_taken_per_day.csv"
        df = pd.read_csv(path, index=False)
        cam_hits = df.iloc[[date]]
        output_details = cam_hits.values.tolist()
        return output_details
