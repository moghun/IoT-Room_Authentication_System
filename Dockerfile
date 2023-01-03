FROM python:3.8

# Create app directory
WORKDIR /

# Install app dependencies
COPY ./ ./

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN apt-get install make
RUN apt-get install gcc
RUN apt-get install libelf-dev
RUN apt-get install -y v4l-utils
RUN apt-get install -y sudo
RUN sudo usermod -a -G video root
RUN pip install --upgrade setuptools
RUN pip install cmake
RUN pip install -r requirements.txt
RUN pip3 install dlib --force-reinstall --no-cache-dir --global-option=build_ext

EXPOSE 80 5555 5556 5557 5558 5559 5560 5561 5562 5563 5564 5565 5566 5567 5568 5569 5570 5571 5572 5573 5574 5575 5576

CMD [ "python3", "./app.py", "multiple_devices"]
