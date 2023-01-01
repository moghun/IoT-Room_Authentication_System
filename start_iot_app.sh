#!/bin/bash
app="server"
docker build -t ${app_iot} .
sudo docker run -it -p 80:80 -d ${app_iot}