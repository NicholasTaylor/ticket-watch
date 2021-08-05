FROM python:3.9.6-alpine

RUN mkdir -p /opt/ticket-watch
WORKDIR /opt/ticket-watch

COPY requirements.txt /opt/ticket-watch/
RUN pip install -r /opt/ticket-watch/requirements.txt