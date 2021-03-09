import os
import logging
from flask import Flask, Blueprint
from routes.create import create_blueprint
from routes.query import query_blueprint
from routes.update import update_blueprint
from routes.delete import delete_blueprint


api = Flask(__name__)

logging.basicConfig(filename='logs/request-logs.log', level=logging.WARNING,
                    format=f'%(asctime)s %(levelname)s %(name)s: %(message)s')

api.register_blueprint(create_blueprint)
api.register_blueprint(query_blueprint)
api.register_blueprint(update_blueprint)
api.register_blueprint(delete_blueprint)


if __name__ == '__main__':
    api.run()
