#!/usr/bin/env python3
from datetime import datetime
from json import load, dumps
import requests
import os
import time


host = os.getenv('WEB_HOST')
port = os.getenv('WEB_PORT')

baseurl = "http://{}:{}".format(host, port)
users = load(open("./list.json", "r"))

while (True):
    response = requests.get(url=baseurl)
    if response.status_code == requests.codes.get("ok"):
        print("=== HO EMULATOR ===")
        for userid in users:
            url = "{}/user/{}".format(baseurl, userid)
            response = requests.get(url=url)
            dt = datetime.now().strftime("%H:%M:%S")
            print("[{}] GET {} STATUS {}".format(dt, url, response.status_code))
        print()
    else:
        print("Error: GET {} STATUS {}".format(baseurl, response.status_code))
    time.sleep(1)
