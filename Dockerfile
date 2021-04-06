FROM ubuntu:latest

LABEL maintainer="eleonora.belova.16@gmail.com"

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

WORKDIR /app

COPY main.py /app
COPY requirements.txt /app

RUN pip3 install -r requirements.txt

RUN python3 main.py
