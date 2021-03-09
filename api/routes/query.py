from flask import Flask, abort, request, make_response, jsonify, Blueprint
from database.AudioSchema import Audiobook, Song, Podcast
from mongoengine import *
from utils.configs import get_filetypes
import logging


# Route Blueprint
query_blueprint = Blueprint('query', __name__)

# Get the config definitions
audio_file_types = get_filetypes()

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
                songDB = Song()
                response['data'] = songDB.get_all_songs()
                response['status'] = 200
                return make_response(jsonify(response), 200)
            except:
                logging.error(
                    f"Inernal server error trying to access API: {request.remote_addr}"
                )
                abort(500, 'Server Error')

        elif fileType == "podcast":
            try:
                podcastDB = Podcast()
                response['data'] = podcastDB.get_all_podcasts()
                response['status'] = 200
                return make_response(jsonify(response), 200)
            except:
                logging.error(
                    f"Inernal server error trying to access API: {request.remote_addr}"
                )
                abort(500, 'Server Error')

        elif fileType == "audiobook":
            try:
                audiobookDB = Audiobook()
                response['data'] = audiobookDB.get_all_audiobooks()
                response['status'] = 200
                return make_response(jsonify(response), 200)

            except:
                logging.error(
                    f"Inernal server error trying to access API: {request.remote_addr}"
                )
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
                songDB = Song()
                response['data'] = songDB.get_song(fileID)
                response['status'] = 200
                return make_response(jsonify(response), 200)

            except:
                response['errors'] = "Song file ID does not exist"
                response['status'] = 400
                return make_response(jsonify(response), 400)

        elif fileType == "podcast":
            try:
                podcastDB = Podcast()
                response['data'] = podcastDB.get_podcast(fileID)
                response['status'] = 200
                return make_response(jsonify(response), 200)

            except:
                response['errors'] = "Podcast file ID does not exist"
                response['status'] = 400
                return make_response(jsonify(response), 400)

        elif fileType == "audiobook":
            try:
                audiobookDB = Audiobook()
                response['data'] = audiobookDB.get_audiobook(fileID)
                response['status'] = 200
                return make_response(jsonify(response), 200)
            except:
                response['errors'] = "Audiobook file ID does not exist"
                response['status'] = 400
                return make_response(jsonify(response), 400)
        else:
            logging.error(
                f"Inernal server error trying to access API: {request.remote_addr}"
            )
            abort(500, "Internal Server Error")
