import cv2
from flask_cors import CORS
from flask import Flask, Response
import requests
import time

import zmq
import base64
import imagezmq
import socket



sender = imagezmq.ImageSender(connect_to='tcp://*:5555', REQ_REP=False)
sender.zmq_socket.setsockopt(zmq.CONFLATE, 0)
sender.zmq_socket.setsockopt(zmq.SNDHWM, 1)


camera = cv2.VideoCapture(0)

while True:
    try:
        (grabbed, frame) = camera.read()  # grab the current frame
        sender.send_image(socket.gethostname(), frame)

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break





            




