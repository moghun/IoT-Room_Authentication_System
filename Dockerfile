FROM python:3.8

# Create app directory
WORKDIR /

# Install app dependencies
COPY requirements.txt ./

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install cmake
RUN pip install -r requirements.txt
RUN pip3 install dlib --force-reinstall --no-cache-dir --global-option=build_ext

EXPOSE 80
CMD [ "python3", "./iot_app.py"]
