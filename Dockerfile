FROM python:3.8

WORKDIR /src
COPY notify.py slack.py requirements.txt /src
RUN pip install -r requirements.txt