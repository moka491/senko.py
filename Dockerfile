FROM ubuntu:19.04

# Install python3, curl and pip
RUN apt-get update
RUN apt-get -y install python3 curl python3-distutils git
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

# Install ffmpeg for music functionality
RUN apt-get -y install ffmpeg libffi-dev libnacl-dev python3-dev

# Setup project and install dependencies
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run senko bot
CMD [ "python3", "./senko.py" ]