from flask import Flask, request
from apilogic import API

import configparser
import json
import sys

def readConfig(file):
    config = configparser.ConfigParser()
    config.read(file)

    # Check if needed sections are in config
    if ('GENERAL' or 'RESOURCES') not in config:
        print ("Invalid Config found, could not find section GENERAL")
        sys.exit(-1)

    return config


def setup(data):
    # Create app and call route constructor
    app = Flask("")
    app.debug = True

    constructRoutes(app, data)

    return app

def constructRoutes(app, data):
    api = API(data)

    base_api = "/{}/".format(api.version)

    @app.route("/")
    def root():
        return json.dumps(
            api.getAPIInfo()
            )

    @app.route(base_api + "createvm", methods=["POST"])
    def createvm():
        return api.createVM(byteToJson(request.data))

    @app.route(base_api + "reboot", methods=["POST"])
    def rebootvm():
        return api.rebootVM(byteToJson(request.data))

    @app.route(base_api + "list", methods=["GET"])
    def getInfo():
        return api.listVM()

    

def start(app):
    app.run()

def byteToJson(bytecode):
    data = bytecode.decode("UTF-8")
    return json.loads(data)

if __name__ == "__main__":
    data = readConfig("config.ini")
    app = setup(data)
    start(app)
