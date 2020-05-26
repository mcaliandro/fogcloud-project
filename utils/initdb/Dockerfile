FROM python:alpine

RUN mkdir /opt/initdb
COPY . /opt/initdb
WORKDIR /opt/initdb
RUN pip install -r requirements.txt
