#!/usr/bin/python
from flask import Flask, render_template
from json import load, loads
from random import randint
import requests
import os

app = Flask(__name__)

host = os.getenv('CORE_STACK_SERVICE_HOST')
port = os.getenv('CORE_STACK_SERVICE_PORT')

api_service = "http://{}:{}".format(host, port)
userslist = load(open("./list.json", "r"))

@app.route("/")
def main():
    random = randint(0, len(userslist))
    userid = userslist[random]
    url = "{}/user/{}".format(api_service, userid)
    response = requests.get(url=url)
    if response.status_code == requests.codes.get('ok'):
        data = loads(response.json())
        shsid = data.get("shsid")
        url = "{}/shs/{}".format(api_service, shsid)
        response = requests.get(url=url)
        if response.status_code == requests.codes.get('ok'):
            data = loads(response.json())
            return render_template("index.html", data=data)
        else:
            return render_template("error.html", data=response.status_code)
    else:
        return render_template("error.html", data=response.status_code)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
