# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

LABEL maintainer="fedoravdeev3@gmail.com"
LABEL version="0.1"
LABEL description="game bot fo telegram and server fo bot"


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


COPY newbot.py newbot.py
COPY server.py server.py
COPY .env .env

CMD ['python', 'newbot.py']