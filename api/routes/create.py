from flask import Flask, abort, request, make_response, jsonify, Response, Blueprint
from utils.authentication import require_apikey
from utils import validators
from database.AudioSchema import Audiobook, Song, Podcast
from mongoengine import *
import logging


# Route Blueprint
create_blueprint = Blueprint('create', __name__)

# @route   POST /api/v1/create
# @desc    Create new audio file (Song, Podcast, Audiobook)
# @access  Private
# @params  audioFileType, audioFileMatadata


@create_blueprint.route("/api/v1/create", methods=["POST"])
@require_apikey
def create():
    response = {"errors": {}, "data": {}, "status": ""}

    req = request.get_json()
    audioFileType = req["audioFileType"]
    audioFileMetadata = req["audioFileMetadata"]

    # Validate Audio Input
    errors, valid = validators.validateAudioInput(
        audioFileType, audioFileMetadata)

    if not valid:
        response['errors'] = errors
        response['status'] = 400
        return make_response(jsonify(response), 400)

    if audioFileType == "song":

        errors, valid = validators.validateSongMetadata(audioFileMetadata)

        if not valid:
            response['errors'] = errors
            response['status'] = 400
            return make_response(jsonify(response), 400)

        try:
            songDB = Song()
            response['data'] = songDB.create_song(
                audioFileMetadata['name_of_song'], audioFileMetadata['duration'])
            response['status'] = 200
            return make_response(jsonify(response), 200)
        except:
            abort(400, 'Invalid song metadata')

    elif audioFileType == "podcast":
        errors, valid = validators.validatePodcastMetadata(audioFileMetadata)

        if not valid:
            response['errors'] = errors
            response['status'] = 400
            return make_response(jsonify(response), 400)

        try:
            podcastDB = Podcast()
            response['data'] = podcastDB.create_podcast(
                audioFileMetadata['name_of_podcast'], audioFileMetadata['duration'], audioFileMetadata['host'], audioFileMetadata['participants'])
            response['status'] = 200
            return make_response(jsonify(response), 200)

        except:
            abort(400, 'Invalid podcast metadata')

    elif audioFileType == "audiobook":
        errors, valid = validators.validateAudiobookMetadata(audioFileMetadata)

        if not valid:
            response['errors'] = errors
            response['status'] = 400
            return make_response(jsonify(response), 400)

        newAudiobook = Audiobook(
            title_of_audiobook=audioFileMetadata['title_of_audiobook'],
            author_of_title=audioFileMetadata['author_of_title'],
            narrator=audioFileMetadata['narrator'],
            duration=audioFileMetadata['duration']
        )

        try:
            audiobookDB = Audiobook()
            response['data'] = audiobookDB.create_audiobook(
                audioFileMetadata['title_of_audiobook'], audioFileMetadata['author_of_title'], audioFileMetadata['narrator'], audioFileMetadata['duration'])
            response['status'] = 200
            return make_response(jsonify(response), 200)

        except:
            abort(400, 'Invalid audiobook metadata')

    else:
        logging.error(
            f"Inernal server error trying to access API: {request.remote_addr}")

        abort(500, 'Internal Server Error')
