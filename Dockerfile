FROM python:3.7-stretch

# Install ffmpeg for music functionality
RUN apt install ffmpeg

# Setup project and install dependencies
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run senko bot
CMD [ "python", "./senko.py" ]