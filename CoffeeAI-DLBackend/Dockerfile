FROM python:3.9.16-bullseye

WORKDIR usr/src/flask_app

RUN pip install flask
RUN pip install gunicorn
RUN pip install tensorflow
RUN pip install keras
RUN pip install pillow

COPY . .