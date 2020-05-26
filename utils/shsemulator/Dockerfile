FROM python:alpine

RUN mkdir /opt/shsemulator
COPY . /opt/shsemulator
WORKDIR /opt/shsemulator

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "emulator.py"]
