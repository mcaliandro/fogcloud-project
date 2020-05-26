FROM python:alpine

RUN mkdir /opt/dashboard
COPY . /opt/dashboard
WORKDIR /opt/dashboard
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT ["python", "Dashboard.py"]
