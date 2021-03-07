from mongoengine import *
from datetime import datetime


connect("filed-audio-api-dev-db",
        host="localhost",
        port=27017)


class Song(Document):
    """
    Desc: Audio Schema for DB
    """

    name_of_song = StringField(required=True, max_length=100)
    duration = IntField(required=True, min_value=0)
    uploaded_time = DateTimeField(default=datetime.utcnow)

    def song_data(self):
        song_dict = {
            "id": str(self.id),
            "name_of_song": self.name_of_song,
            "duration": self.duration,
            "uploaded_time": self.uploaded_time,
        }
        return song_dict

    meta = {
        "indexes": ["name_of_song"],
        "ordering": ['-uploaded_time']
    }


class Podcast(Document):
    """
    Desc: Podcast Schema for DB
    """

    name_of_podcast = StringField(required=True, max_length=100)
    duration = IntField(required=True, min_value=0)
    uploaded_time = DateTimeField(default=datetime.utcnow)
    host = StringField(required=True, max_length=100)
    participants = ListField(StringField(max_length=100))

    def podcast_data(self):
        podcast_dict = {
            "id": str(self.id),
            "name_of_podcast": self.name_of_podcast,
            "duration": self.duration,
            "uploaded_time": self.uploaded_time,
            "host": self.host,
            "participants": self.participants
        }
        return podcast_dict

    meta = {
        "indexes": ["name_of_podcast"],
        "ordering": ['-uploaded_time']
    }


class Audiobook(Document):
    """
    Desc: Audiobook Schema for DB
    """

    title_of_audiobook = StringField(required=True, max_length=100)
    author_of_title = StringField(required=True, max_length=100)
    narrator = StringField(required=True, max_length=100)
    duration = IntField(required=True, min_value=0)
    uploaded_time = DateTimeField(default=datetime.utcnow)

    def audiobook_data(self):
        audiobook_dict = {
            "id": str(self.id),
            "title_of_audiobook": self.title_of_audiobook,
            "author_of_title": self.author_of_title,
            "narrator": self.narrator,
            "duration": self.duration,
            "uploaded_time": self.uploaded_time
        }
        return audiobook_dict

    meta = {
        "indexes": ["title_of_audiobook"],
        "ordering": ['-uploaded_time']
    }
