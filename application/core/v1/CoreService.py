import os
from json import loads
from flask import Flask, request
from flask_restplus import Api, Resource
from flask_mongoengine import MongoEngine
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, ListField, StringField


coreService = Flask(__name__)
api = Api(coreService, version='1.0', title='CoreService', description='SmartHomeSystem application')

coreService.config['MONGODB_SETTINGS'] = {
    'db': os.getenv('DB_NAME'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT'))
}

dbService = MongoEngine()
dbService.init_app(coreService)


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


@api.route("/user/<id>")
@api.doc(params={'id': 'House Owner unique identifier'})
class HouseOwner(Resource):
    def get(self, id):
        userData = User.objects(userid=id).first()
        if not userData: api.abort(403)
        shsid = userData.shsid
        shsData = SmartHomeSystem.objects(shsid=shsid).first()
        if not shsData: api.abort(404)
        return shsData, 200


@api.route("/shs/<id>")
@api.doc(params={'id': 'SmartHomeSytem device unique identifier'})
class SHS(Resource):
    def get(self, id):
        shsData = SmartHomeSystem.objects(shsid=id).first()
        if not shsData: api.abort(404)
        return shsData, 200

    def put(self, id): 
        data = loads(request.get_json())
        if not data: api.abort(400)
        if not id == data.get("shsid"): api.abort(400)
        result = SmartHomeSystem.objects(shsid=id).first()
        if not result: api.abort(500)
        result.update(**data)
        return {"message": "SUCCESS"}, 200


if __name__ == "__main__":
    coreService.run(host='0.0.0.0', port='5000', debug=True)
