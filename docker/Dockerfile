FROM python:3.9.5-slim-buster
ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app/
WORKDIR /app/

COPY . /app/
RUN apt update
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
