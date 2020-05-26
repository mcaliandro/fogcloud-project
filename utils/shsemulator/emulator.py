#!/usr/bin/env python3
from datetime import datetime
from json import load, dumps
import requests
import os
import time


host = os.getenv('API_HOST')
port = os.getenv('API_PORT')

baseurl = "http://{}:{}".format(host, port)
systems = load(open("./list.json", "r"))

while (True):
    response = requests.get(url=baseurl)
    if response.status_code == requests.codes.get("ok"):
        print("=== SHS EMULATOR ===")
        for shsid in systems:
            dataset = load(open("./instances/{}/template.json".format(shsid), "r"))
            shsurl = "{}/shs/{}".format(baseurl, shsid)
            dt = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            dataset['lastupdate'] = dt
            appliancesList = dataset.get('appliances')
            for appliance in appliancesList: 
                appliance['lastcheck'] = dt
            response = requests.put(url=shsurl, json=dumps(dataset))
            dt = datetime.now().strftime("%H:%M:%S")
            print("[{}] PUT {} STATUS {}".format(dt, shsurl, response.status_code))
        print()
    else:
        print("Error: GET {} STATUS {}".format(baseurl, response.status_code))
    time.sleep(5)
