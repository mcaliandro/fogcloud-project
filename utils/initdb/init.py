#!/usr/bin/env python3
from json import load, dumps
from mongoengine import *
import os


class User(Document):
    userid = StringField(required=True)
    shsid = StringField(required=True)
    username = StringField(required=True)

class Appliance(EmbeddedDocument):
    name = StringField(required=True)
    status = StringField(required=True)
    lastcheck = StringField(required=True)
    consumption = StringField(required=True)

class Areas(EmbeddedDocument):
    name = StringField(required=True)
    consumption = StringField(required=True)
    rate = StringField(required=True)

class SmartHomeSystem(Document):
    shsid = StringField(required=True)
    lastupdate = StringField(required=True)
    appliances = ListField(EmbeddedDocumentField(Appliance))
    areas = ListField(EmbeddedDocumentField(Areas))


host = os.getenv('DB_HOST')
port = int(os.getenv('DB_PORT'))
name = os.getenv('DB_NAME')

try:
    connect(name, host=host, port=port)
except Exception as exc:
    print("Error connecting {}:{}".format(host, port))
    print(exc)
else:
    users = load(open("./users/list.json", "r"))
    systems = load(open("./shs/list.json", "r"))

    print("=== USER ===")
    for user in users:
        data = load(open("./users/instances/{}/template.json".format(user), "r"))
        result = User(**data)
        result.save()
        print(data)

    print("=== SHS ===")
    for shs in systems:
        data = load(open("./shs/instances/{}/template.json".format(shs), "r"))
        result = SmartHomeSystem(**data)
        result.save()
        print(data)

    disconnect()
