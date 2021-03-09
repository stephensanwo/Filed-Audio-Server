from mongoengine import *
from datetime import datetime


connect("filed-audio-api-dev-db", host="localhost", port=27017)


class Auth(Document):
    """
    Desc: Auth Schema for DB
    """
    client_email = StringField(required=True)
    api_key = StringField(required=True)
    date_created = DateTimeField(default=datetime.utcnow)

    def auth_data(self):
        auth_dict = {
            "client_email": self.client_email,
            "date_created": self.date_created,
        }
        return auth_dict

    meta = {"indexes": ["client_email"], "ordering": ["-date_created"]}
