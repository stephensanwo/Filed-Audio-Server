import os
from flask import Flask, Blueprint
from routes.create import create_blueprint


api = Flask(__name__)
api.register_blueprint(create_blueprint)


if __name__ == '__main__':
    api.run()
