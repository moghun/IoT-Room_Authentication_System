# BEFORE RUNNING THE PROGRAM
# RUN THIS IN TERMINAL
# pip3 install dlib --force-reinstall --no-cache-dir --global-option=build_ext

from flask_cors import CORS
import cv2
import numpy as np
import face_recognition
import requests
import os
from flask import Flask, request, render_template, Response
from pathlib import Path
from PIL import Image
import io
import base64


app = Flask(__name__)
CORS(app)



currentFile = Path(__file__).parent
UPLOAD_FOLDER = os.path.join(currentFile, "registrations")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
room_ids = []
image = []
frame = []

for room in os.listdir(UPLOAD_FOLDER):
    room_ids.append(room)
room_ids.sort()

def allowed_file(filename):
    return '.' in filename and \
           get_extension(filename) in ALLOWED_EXTENSIONS
def get_extension(filename):
     return filename.rsplit('.', 1)[1].lower()
    

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload_file():
    global room_ids
    return render_template('upload.html', roomIDs = room_ids)


@app.route('/success', methods=['GET', 'POST'])
def success():
    global room_ids

    if 'file' not in request.files:
        # flash('No file part')
        return render_template('upload.html')
    file = request.files['file']
    username = request.form['username']
    room = request.form['room']
    if file.filename == '':
        # flash('No image selected for uploading')
        return render_template('upload.html', roomIDs = room_ids)
    if file and username and room and allowed_file(file.filename):
        filename = username + "_room-" + room + "." + get_extension(file.filename)
        print(filename)
        room_folder = "room-" + room
        
        room_path = os.path.join(app.config['UPLOAD_FOLDER'], room_folder)
        print(room_path)
        if os.path.isdir(room_path) == False:
            os.mkdir(room_path)
            room_ids.append(room_folder)
            room_ids.sort()

        file.save(os.path.join(room_path, filename))

        return render_template('upload.html', roomIDs = room_ids)
    else:
        return render_template('upload.html', roomIDs = room_ids)


@app.route('/index', methods=['GET', 'POST'])
def index():
    """Video streaming home page."""
    #rnumber = ['rns']
    print("form", request.form)
    rn = request.form["room_id"]
    formatted_rn = rn[5:]
    return render_template('index.html', room_number=formatted_rn)


def gen(room_input="ALL"):
    IMAGE_FILES = []
    filename = []
    dir_path = UPLOAD_FOLDER
    global image
    global frame
    if room_input == "ALL":
        for room in os.listdir(dir_path):
            room_path = os.path.join(dir_path, room)
            for images in os.listdir(room_path):
                img_path = os.path.join(room_path, images)
                img_path = face_recognition.load_image_file(img_path)  # reading image and append to list
                IMAGE_FILES.append(img_path)
                filename.append(images.split(".", 1)[0])
    else:
        room_fname = "room-"+str(room_input)
        room_path = os.path.join(dir_path, room_fname)
        for images in os.listdir(room_path):
            img_path = os.path.join(room_path, images)
            img_path = face_recognition.load_image_file(img_path)  # reading image and append to list
            IMAGE_FILES.append(img_path)
            filename.append(images.split(".", 1)[0])


    def encoding_img(IMAGE_FILES):
        encodeList = []
        for img in IMAGE_FILES:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListknown = encoding_img(IMAGE_FILES)


    try: 
        imgc = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        # converting image to RGB from BGR
        imgc = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        fasescurrent = face_recognition.face_locations(imgc)
        encode_fasescurrent = face_recognition.face_encodings(imgc, fasescurrent)

        # faceloc- one by one it grab one face location from fasescurrent
        # than encodeFace grab encoding from encode_fasescurrent
        # we want them all in same loop so we are using zip
        for encodeFace, faceloc in zip(encode_fasescurrent, fasescurrent):
            matches_face = face_recognition.compare_faces(encodeListknown, encodeFace)
            face_distence = face_recognition.face_distance(encodeListknown, encodeFace)

            # print(face_distence)
            # finding minimum distence index that will return best match
            matchindex = np.argmin(face_distence)

            if matches_face[matchindex]:
                name = filename[matchindex].upper()
                # print(name)
                y1, x2, y2, x1 = faceloc
                # multiply locations by 4 because we above we reduced our webcam input image by 0.25
                # y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (0, 255, 0), 2, cv2.FILLED)
                cv2.putText(image, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            else:
                y1, x2, y2, x1 = faceloc
                # multiply locations by 4 because we above we reduced our webcam input image by 0.25
                # y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 255), 5)
                cv2.rectangle(image, (x1, y2 - 35), (x2, y2), (255, 0, 255), 5, cv2.FILLED)
                cv2.putText(image, "NOT REGISTERED", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        frame = cv2.imencode('.jpg', image)[1].tobytes()
        
    except Exception as e:
        print("error:", e)
        pass


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    room_number = request.args.get('room', None)
    gen(room_number)
    frame_base64 = base64.b64encode(frame).decode('utf-8')

    return render_template("index.html", frame=frame_base64)





@app.route('/get_video', methods=['POST'], strict_slashes=False)
def get_video():
    file = request.files['image']
    data = Image.open(file.stream)
    global image
    img_rgb = np.array(data)
    data = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)

    image = data
    return "True"
    

if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0", port="80")

