import cv2
from flask_cors import CORS
from flask import Flask, Response
import requests
import time


camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()
    print("bb")
    # Encode the frame in JPEG format
    cv2.imwrite('frame.jpg', frame)
    files = {'image': open('frame.jpg', 'rb')}
    time.sleep(1)
    try:
        requests.post("http://localhost:80/get_video", files=files)
    except Exception as err:
        print("error", err)





            




