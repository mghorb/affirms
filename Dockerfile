# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
RUN mkdir -pv $APP_HOME
WORKDIR $APP_HOME
COPY . $APP_HOME

RUN python3 --version

RUN apt-get update && apt-get upgrade -y
RUN apt-get install espeak -y
RUN apt-get install ffmpeg -y
RUN apt-get install gunicorn -y
RUN apt-get install libespeak1 -y
RUN apt-get install portaudio19-dev -y
RUN apt-get install python3-pyaudio -y

RUN echo "Installed dependencies"

# Install production dependencies.
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip list

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
