import os
from flask import Flask, Blueprint
from routes.create import create_blueprint
from routes.query import query_blueprint
from routes.update import update_blueprint
from routes.delete import delete_blueprint


api = Flask(__name__)
api.register_blueprint(create_blueprint)
api.register_blueprint(query_blueprint)
api.register_blueprint(update_blueprint)
api.register_blueprint(delete_blueprint)


if __name__ == '__main__':
    api.run()
