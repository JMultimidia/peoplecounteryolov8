# main.py
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
import ast

# Load the environment variables
load_dotenv()

# Get the language from the environment variable
language = os.getenv("LANGUAGE", "en")

# Load translations from JSON file in the language directory
translations_path = os.path.join('lang', language, 'translations.json')
with open(translations_path, 'r') as f:
    translations = json.load(f)

# Use the factory function to create a Database instance
# This centralizes the database connection logic in db.py
db_instance = db.create_database_instance()

# Load the video capture URL from the environment variable
video_capture_url = os.getenv("VIDEO_CAPTURE", "rtsp://nortrix:Nortrix123@45.189.227.221:5000/cam/realmonitor?channel=1&subtype=0")

# Define the interval to insert the data in the database
insert_interval = int(os.getenv("INSERT_INTERVAL", 120)) # Default 120 seconds

# Dictionary to store the last insertion time for each ID
last_insertion = {}

model = YOLO('yolov8s.pt')

area1_str = os.getenv("AREA1", "[(312,388),(289,390),(474,469),(497,462)]")
area2_str = os.getenv("AREA2", "[(279,392),(250,397),(423,477),(454,469)]")
position_number_one_str = os.getenv("POSITON_NUMBER1", "71,322")
position_number_two_str = os.getenv("POSITION_NUMBER2", "71,322")

# Convert the strings to lists of tuples using ast.literal_eval
area1 = ast.literal_eval(area1_str)
area2 = ast.literal_eval(area2_str)

# Convert the string to a tuple of integers
position_number_one = tuple(map(int, position_number_one_str.split(',')))
position_number_two = tuple(map(int, position_number_two_str.split(',')))

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

#cap = cv2.VideoCapture('peoplecount1.mp4')
cap = cv2.VideoCapture(video_capture_url)

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")
#print(class_list)

count = 0

tracker = Tracker()

resize_w = int(os.getenv("RESIZE_WIDTH", 1020))
resize_h = int(os.getenv("RESIZE_HEIGHT", 500))

people_entering = {}
people_exiting = {}
entering = set()
exiting = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 2 != 0:
        continue
    frame = cv2.resize(frame,(resize_w, resize_h)) # Resize the frame
    # frame=cv2.flip(frame,1)
    results = model.predict(frame)
    # print(results)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    print(px) # SHOW POSITION OF MOUSE
    list = []
    for index, row in px.iterrows():
        # print(row)
        x1, y1, x2, y2, d = int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[5])
        c = class_list[d]
        if 'person' in c:
           list.append([x1, y1, x2, y2])
    bbox_id = tracker.update(list)
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        results = cv2.pointPolygonTest(np.array(area2, np.int32), (x4, y4), False)
        # print(results)
        if results >= 0:
           people_entering[id] = (x4, y4)
           cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

        if id in people_entering:
           results1 = cv2.pointPolygonTest(np.array(area1, np.int32), (x4, y4), False)
           # print(results1)
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
        # print(results2)
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
    cv2.putText(frame,str('1'),position_number_one,cv2.FONT_HERSHEY_COMPLEX,(0.5),(0,0,0),1)

    cv2.polylines(frame,[np.array(area2,np.int32)],True,(255,0,0),2)
    cv2.putText(frame,str('2'),position_number_two,cv2.FONT_HERSHEY_COMPLEX,(0.5),(0,0,0),1)

    # print(people_entering) #print the people (id) entering the area
    # print(entering) #print the people (id) entering the area
    # print(len(entering)) #print the number of people entering the area
    # print(len(exiting)) #print the number of people exiting the area
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