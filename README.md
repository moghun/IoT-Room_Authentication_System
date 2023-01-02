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
