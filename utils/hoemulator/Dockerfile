FROM python:alpine

RUN mkdir /opt/hoemulator
COPY . /opt/hoemulator
WORKDIR /opt/hoemulator

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "emulator.py"]
