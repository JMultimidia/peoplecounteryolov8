import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import Tracker
import db
import time
import os
import json
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Get the language from the environment variable
language = os.getenv("LANGUAGE", "en")

# Load translations from JSON file in the language directory
translations_path = os.path.join('lang', language, 'translations.json')
with open(translations_path, 'r') as f:
    translations = json.load(f)

# Create an instance of the Database class
db_instance = db.Database()

# Define the interval to insert the data in the database
insert_interval = int(os.getenv("INSERT_INTERVAL", 120)) # Default 120 seconds

# Dictionary to store the last insertion time for each ID
last_insertion = {}

model = YOLO('yolov8s.pt')

area1 = [(312,388),(289,390),(474,469),(497,462)]
area2 = [(279,392),(250,397),(423,477),(454,469)]

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('peoplecount1.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count=0
frame_skip = 2 # Display every n frames

tracker = Tracker()

people_entering = {}
people_exiting = {}
entering = set()
exiting = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % frame_skip != 0:
        continue
    frame = cv2.resize(frame,(1020, 500)) # Resize the frame

    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    list = []
    for index, row in px.iterrows():
        x1, y1, x2, y2, d = int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[5])
        c = class_list[d]
        if 'person' in c:
           list.append([x1, y1, x2, y2])
    bbox_id = tracker.update(list)
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        results = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
        if results >= 0:
           people_entering[id] = (x4, y4)
           cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

        if id in people_entering:
           results1 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
           if results1 >= 0:
              cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)
              cv2.circle(frame, (x4, y4), 5, (255, 0, 255), -1)
              cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, (0.5), (255, 255, 255), 1)
              entering.add(id)
              current_time = time.time()
              if id not in last_insertion or current_time - last_insertion[id] > insert_interval:
                 try:
                      db_instance.insert_entering(id)
                      last_insertion[id] = current_time
                 except Exception as e:
                      print(f"Error inserting entering ID: {e}")

        results2 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
        if results2 >= 0:
            people_exiting[id] = (x4, y4)
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)

        if id in people_exiting:
            results3 = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
            if results3 >= 0:
                cv2.rectangle(frame, (x3, y3), (x4, y4), (255, 0, 255), 2)
                cv2.circle(frame, (x4, y4), 5, (255, 0, 255), -1)
                cv2.putText(frame, str(id), (x3, y3), cv2.FONT_HERSHEY_COMPLEX, (0.5), (255, 255, 255), 1)
                exiting.add(id)
                current_time = time.time()
                if id not in last_insertion or current_time - last_insertion[id] > insert_interval:
                    try:
                        db_instance.insert_exiting(id)
                        last_insertion[id] = current_time
                    except Exception as e:
                        print(f"Error inserting exiting ID: {e}")

    cv2.polylines(frame,[np.array(area1,np.int32)],True,(255,0,0),2)
    cv2.putText(frame,str('1'),(504,471),cv2.FONT_HERSHEY_COMPLEX,(0.5),(0,0,0),1)

    cv2.polylines(frame,[np.array(area2,np.int32)],True,(255,0,0),2)
    cv2.putText(frame,str('2'),(448,480),cv2.FONT_HERSHEY_COMPLEX,(0.5),(0,0,0),1)

    i_total = (len(entering))
    o_total = (len(exiting))

    cv2.putText(frame, f"{translations['ENTERED']}: {i_total}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 255, 0), 2)
    cv2.putText(frame, f"{translations['EXITED']}: {o_total}",(20, 40), cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 0, 255), 2)

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
db_instance.close()