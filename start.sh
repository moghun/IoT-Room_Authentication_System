#!/bin/bash
app="iot_server-2"
docker build -t ${app} .
sudo docker run --privileged -it -p 80:80 --device="/dev/video0:/dev/video0/" -d ${app}