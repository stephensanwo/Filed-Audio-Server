from mongoengine import *
from datetime import datetime
from flask import abort
import api
import os


if os.getenv("FLASK_ENV") == 'development':
    try:
        connect("filed-audio-api-dev-db",
                host="localhost",
                port=27017)
    except:
        abort(500, "Internal Server Error")

elif os.getenv("FLASK_ENV") == 'production':
    try:
        db = os.getenv("DB_NAME")
        connect(
            db=db,
            host='mongo',
            port=27017,
            username="root",
            password="root",
            authentication_source="admin",
            connect=False
        )
    except:
        abort(500, "Internal Server Error")


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

    @classmethod
    def get_all_songs(cls):
        songs = cls.objects()
        response = {"songs": []}
        for song in songs:
            response['songs'].append(song.song_data())

        return response

    @classmethod
    def get_song(cls, fileID):
        song = cls.objects(id=fileID).get()
        response = {"song": {}}
        response['song'] = song.song_data()
        return response

    @classmethod
    def create_song(cls, name_of_song, duration):
        newSong = cls(
            name_of_song=name_of_song,
            duration=duration
        )
        newSong.save()
        response = {"song": newSong.song_data()}
        return response

    @classmethod
    def update_song(cls, fileID, name_of_song, duration):
        song = cls.objects(id=fileID).get()
        song.update(
            name_of_song=name_of_song,
            duration=duration
        )
        song.reload()
        response = {"song": song.song_data()}
        return response

    @classmethod
    def delete_song(cls, fileID):
        song = cls.objects(id=fileID).get()
        song.delete()

        response = f"Song with ID: {fileID} deleted"
        return response

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

    @classmethod
    def get_all_podcasts(cls):
        podcasts = cls.objects()
        response = {"podcasts": []}
        for podcast in podcasts:
            response['podcasts'].append(podcast.podcast_data())

        return response

    @classmethod
    def get_podcast(cls, fileID):
        podcast = cls.objects(id=fileID).get()
        response = {"podcast": {}}
        response['podcast'] = podcast.podcast_data()
        return response

    @classmethod
    def create_podcast(cls, name_of_podcast, duration, host, participants):
        newPodcast = cls(
            name_of_podcast=name_of_podcast,
            duration=duration,
            host=host,
            participants=participants

        )
        newPodcast.save()
        response = {"podcast": newPodcast.podcast_data()}
        return response

    @classmethod
    def update_podcast(cls, fileID, name_of_podcast, duration, host, participants):
        podcast = cls.objects(id=fileID).get()
        podcast.update(
            name_of_podcast=name_of_podcast,
            duration=duration,
            host=host,
            participants=participants
        )
        podcast.reload()
        response = {"podcast": podcast.podcast_data()}
        return response

    @classmethod
    def delete_podcast(cls, fileID):
        podcast = cls.objects(id=fileID).get()
        podcast.delete()

        response = f"Podcast with ID: {fileID} deleted"
        return response

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

    @classmethod
    def get_all_audiobooks(cls):
        audiobooks = cls.objects()
        response = {"audiobooks": []}
        for audiobook in audiobooks:
            response['audiobooks'].append(audiobook.audiobook_data())

        return response

    @classmethod
    def get_audiobook(cls, fileID):
        audiobook = cls.objects(id=fileID).get()
        response = {"audiobook": {}}
        response['audiobook'] = audiobook.audiobook_data()
        return response

    @classmethod
    def create_audiobook(cls, title_of_audiobook, author_of_title, narrator, duration):
        newAudiobook = cls(
            title_of_audiobook=title_of_audiobook,
            author_of_title=author_of_title,
            narrator=narrator,
            duration=duration

        )
        newAudiobook.save()
        response = {"audiobook": newAudiobook.audiobook_data()}
        return response

    @classmethod
    def update_audiobook(cls, fileID, title_of_audiobook, author_of_title, narrator, duration):
        audiobook = cls.objects(id=fileID).get()
        audiobook.update(
            title_of_audiobook=title_of_audiobook,
            author_of_title=author_of_title,
            narrator=narrator,
            duration=duration
        )
        audiobook.reload()
        response = {"audiobook": audiobook.audiobook_data()}
        return response

    @classmethod
    def delete_audiobook(cls, fileID):
        audiobook = cls.objects(id=fileID).get()
        audiobook.delete()

        response = f"Audiobook with ID: {fileID} deleted"
        return response

    meta = {
        "indexes": ["title_of_audiobook"],
        "ordering": ['-uploaded_time']
    }
