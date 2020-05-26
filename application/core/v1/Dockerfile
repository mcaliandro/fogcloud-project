FROM python:alpine

RUN mkdir /opt/corestack
COPY . /opt/corestack
WORKDIR /opt/corestack
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "CoreService.py"]
