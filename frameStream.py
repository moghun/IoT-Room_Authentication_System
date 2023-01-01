import cv2
from flask_cors import CORS
from flask import Flask, Response
import requests
import time

import zmq
import base64
import imagezmq
import socket
from threading import Thread


class frameStream():
    def __init__(self, room_id=0):
        self.video_stream_widget = VideoStreamWidget(room_id)

    def start(self):
        while True:
            try:
                self.video_stream_widget.send_frame()
            except AttributeError:
                pass


 
class VideoStreamWidget(object):
    def __init__(self, src=0, onRPI=False):
        self.sender = imagezmq.ImageSender(connect_to='tcp://*:5555', REQ_REP=False)
        #sender.zmq_socket.connect('tcp://*:5555')
        self.sender.zmq_socket.setsockopt(zmq.CONFLATE, 1)
        self.sender.zmq_socket.setsockopt(zmq.SNDHWM, 1)
        self.sender.zmq_socket.setsockopt( zmq.LINGER, 0 )

        if onRPI == False:
            src = 0

        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 25)
        self.capture.set(3, 160)
        self.capture.set(4,120)
        time.sleep(2)

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()


    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            (self.status, self.frame) = self.capture.read()
    
    def send_frame(self):
        # Display frames in main program
        self.sender.send_image(socket.gethostname(), cv2.resize(self.frame, (640, 480), fx=0, fy= 0,interpolation = cv2.INTER_CUBIC))
        cv2.waitKey(int(200))

if __name__ == '__main__':
    video_stream_widget = VideoStreamWidget()
    while True:
        try:
            video_stream_widget.send_frame()
        except AttributeError:
            pass





# camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_BUFFERSIZE, 25)
# camera.set(3, 160)
# camera.set(4,120)


# while True:
#     try:
#         (grabbed, frame) = camera.read()  # grab the current frame
#         #frame = cv2.GaussianBlur(frame, (5,5), 0)
#         sender.send_image(socket.gethostname(), cv2.resize(frame, (560, 420), fx=0, fy= 0,interpolation = cv2.INTER_CUBIC))
#         cv2.waitKey(int(200))

#     except KeyboardInterrupt:
#         camera.release()
#         cv2.destroyAllWindows()
#         break