#!/bin/bash
app="server"
docker build -t ${app_local} .
sudo docker run -it -p 80:80 -d ${app_local}