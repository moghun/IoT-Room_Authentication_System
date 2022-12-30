#!/bin/bash
app="server"
docker build -t ${app} .
sudo docker run -it -p 80:80 -d ${app}  
