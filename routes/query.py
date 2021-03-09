from flask import Flask, abort, request, make_response, jsonify, Blueprint
from utils.authentication import require_apikey
from database.AudioSchema import Audiobook, Song, Podcast
import logging
from mongoengine import *
import yaml


# Route Blueprint
query_blueprint = Blueprint('query', __name__)

# Get the config definitions
with open("config.yaml") as metadata:
    loader = yaml.load(metadata, Loader=yaml.FullLoader)
    audio_file_types = loader['audio-file-types']

# API Monitoring Logger
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="./logs/requests.log",
                    level=logging.INFO, format=LOG_FORMAT)

logger = logging.getLogger()

# @route   GET /api/v1/get_audio_files
# @desc    Get all audio files of specific type from database (Song, Podcast, Audiobook)
# @access  Public
# @params  audioFileType


@query_blueprint.route("/api/v1/get_audio_files", methods=["GET"])
def get_audio_files():
    # Validate request parameters
    response = {"errors": {}, "data": {}, "status": ""}

    if not request.args['audioFileType']:
        response['errors'] = "Provide an audio file type"
        response['status'] = 400
        return make_response(jsonify(response), 400)

    elif request.args['audioFileType'] not in audio_file_types:
        response['errors'] = "Provide a valid audio file type"
        response['status'] = 400
        return make_response(jsonify(response), 400)

    else:
        fileType = request.args['audioFileType']

        if fileType == "song":
            try:
                songs = Song.objects()
                response["data"]["songs"] = []
                for song in songs:
                    response["data"]['songs'].append({
                        "id": str(song.id),
                        "name_of_song": song.name_of_song,
                        "duration": song.duration,
                        "uploaded_time": song.uploaded_time,
                    })
                    response['status'] = 200
                return make_response(jsonify(response), 200)

            except:
                abort(500, 'Server Error')

        elif fileType == "podcast":
            try:
                podcasts = Podcast.objects()
                response["data"]["podcasts"] = []
                for podcast in podcasts:
                    response["data"]['podcasts'].append({
                        "id": str(podcast.id),
                        "name_of_podcast": podcast.name_of_podcast,
                        "host": podcast.host,
                        "participants": podcast.participants,
                        "duration": podcast.duration,
                        "uploaded_time": podcast.uploaded_time,
                    })
                    response['status'] = 200
                return make_response(jsonify(response), 200)

            except:
                abort(500, 'Server Error')

        elif fileType == "audiobook":
            try:
                audiobooks = Audiobook.objects()
                response["data"]["audiobooks"] = []
                for audiobook in audiobooks:
                    response["data"]["audiobooks"].append({
                        "id": str(audiobook.id),
                        "title_of_audiobook": audiobook.title_of_audiobook,
                        "author_of_title": audiobook.author_of_title,
                        "narrator": audiobook.narrator,
                        "duration": audiobook.duration,
                        "uploaded_time": audiobook.uploaded_time,
                    })
                    response['status'] = 200
                return make_response(jsonify(response), 200)
            except:
                abort(500, 'Internal Server Error')


# @route   GET /api/v1/get_audio_file
# @desc    Get specific audio file of specific type from database (Song, Podcast, Audiobook) by ID
# @access  Public
# @params  audioFileType, audioFileID


@query_blueprint.route("/api/v1/get_audio_file", methods=["GET"])
def get_audio_file():
    # Validate request parameters
    response = {"errors": {}, "data": {}, "status": ""}

    if not (request.args['audioFileType'] or request.args['audioFileID']):
        response['errors'] = "Provide an audio file type and audio file ID"
        response['status'] = 400
        return make_response(jsonify(response), 400)

    elif request.args['audioFileType'] not in audio_file_types:
        response['errors'] = "Provide a valid audio file type"
        response['status'] = 400
        return make_response(jsonify(response), 400)

    else:
        fileType = request.args['audioFileType']
        fileID = request.args['audioFileID']

        if fileType == "song":
            try:
                song = Song.objects(id=fileID).get()
                response["data"]["song"] = []
                response["data"]['song'].append({
                    "id": str(song.id),
                    "name_of_song": song.name_of_song,
                    "duration": song.duration,
                    "uploaded_time": song.uploaded_time,
                })
                response['status'] = 200
                return make_response(jsonify(response), 200)

            except:
                response['errors'] = "Song file ID does not exist"
                response['status'] = 400
                return make_response(jsonify(response), 400)

        elif fileType == "podcast":
            try:
                podcast = Podcast.objects(id=fileID).get()
                response["data"]["podcast"] = []
                response["data"]['podcast'].append({
                    "id": str(podcast.id),
                    "name_of_podcast": podcast.name_of_podcast,
                    "host": podcast.host,
                    "participants": podcast.participants,
                    "duration": podcast.duration,
                    "uploaded_time": podcast.uploaded_time,
                })
                response['status'] = 200
                return make_response(jsonify(response), 200)

            except:
                response['errors'] = "Podcast file ID does not exist"
                response['status'] = 400
                return make_response(jsonify(response), 400)

        elif fileType == "audiobook":
            try:
                audiobook = Audiobook.objects(id=fileID).get()
                response["data"]["audiobook"] = []
                response["data"]["audiobook"].append({
                    "id": str(audiobook.id),
                    "title_of_audiobook": audiobook.title_of_audiobook,
                    "author_of_title": audiobook.author_of_title,
                    "narrator": audiobook.narrator,
                    "duration": audiobook.duration,
                    "uploaded_time": audiobook.uploaded_time,
                })
                response['status'] = 200
                return make_response(jsonify(response), 200)
            except:
                response['errors'] = "Audiobook file ID does not exist"
                response['status'] = 400
                return make_response(jsonify(response), 400)
        else:
            abort(500, "Internal Server Error")
