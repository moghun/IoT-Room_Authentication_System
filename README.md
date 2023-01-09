# IoT-Face-Recognition-Room-Authentication-System

Real-time room authentication system that manages multiple cameras with Flask, face-recognition and imagezmq libraries.

System uses ZMQ PUB-SUB sockets to stream video from multiple devices and authenticate on the server. (requires slight adjustments)

## Authentication with local camera

### Initialization on the server computer (works with local webcam)

```bash
> python3 install -r requirements.txt
> python3 app.py
```


## Authentication with multiple cameras

### Initializing the server

```bash
> python3 install -r requirements.txt
> python3 app.py multiple_devices
```

### Initializing remote camera (on each device)

```bash
> python3 install -r requirements.txt
> python3 frameServer.py <room_number>
```
### Docker container currently not working

## In case of dlib error, try this
```bash
> pip3 install dlib --force-reinstall --no-cache-dir --global-option=build_ext
```


## User flow

- Upload a photograph and enter credientials of the person for register a room
- Select a room for real-time authentication
- Return to admin panel for new registration or authenticate another room

<img width="1433" alt="2" src="https://user-images.githubusercontent.com/89805772/210205596-d9d5215d-4093-4ee1-a7d8-9cba2940346b.png">

<img width="1433" alt="3" src="https://user-images.githubusercontent.com/89805772/210205989-e62c14f5-37a4-4e25-8246-d1eb5f56bd07.png">
