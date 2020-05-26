#!/usr/bin/python
from flask import Flask, render_template
from json import load, loads
from random import randint
import requests
import os

app = Flask(__name__)

host = os.getenv('CORESTACK_HOST')
port = os.getenv('CORESTACK_PORT')

api_service = "http://{}:{}".format(host, port)
shslist = load(open("./list.json", "r"))

@app.route("/")
def main():
    random = randint(0, len(shslist))
    shs = shslist[random]
    url = "{}/shs/{}".format(api_service, shs)
    response = requests.get(url)
    if response.status_code == requests.codes.get("ok"):
        data = loads(response.json())
        return render_template("index.html", data=data)
    else:
        return render_template("error.html", data=response)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
