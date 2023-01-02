# IoT-Face-Recognition-Room-Authentication-System

Real-time room authentication system that manages multiple cameras with Flask, face-recognition and imagezmq libraries.

System uses ZMQ PUB-SUB sockets to stream video from multiple devices and authenticate on the server. (requires slight adjustments)

## Initialization on the server computer (works with local webcam)
```bash
> python3 install -r requirements.txt
> python3 app.py
```

## Initialization on a IoT camera device
```bash
> python3 install -r requirements.txt
> python3 frameServer.py
```

## User flow

* Upload a photograph and enter credientials of the person for register a room
* Select a room for real-time authentication
* Return to admin panel for new registration or authenticate another room

<img width="1433" alt="2" src="https://user-images.githubusercontent.com/89805772/210205596-d9d5215d-4093-4ee1-a7d8-9cba2940346b.png">

<img width="1433" alt="1" src="https://user-images.githubusercontent.com/89805772/210205620-768bfb94-2214-46ba-874c-467202e8e2a8.png">
