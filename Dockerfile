FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive 

# dependencies for tesseract
RUN apt-get update && apt-get install -y \
    software-properties-common \
    tzdata \
    ffmpeg \
    libsm6 \
    libxext6 \
    python3-pip \
    && apt-get clean

# installing tesseract from repo
RUN add-apt-repository ppa:alex-p/tesseract-ocr5
RUN apt install -y tesseract-ocr

# add timezone for telethon
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python packages
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/src/"

WORKDIR /
COPY . .
