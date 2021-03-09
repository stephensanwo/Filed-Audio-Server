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

        newSong = Song(
            name_of_song=audioFileMetadata['name_of_song'],
            duration=audioFileMetadata['duration']
        )

        try:
            newSong.save()
            response['data'] = (newSong.song_data())
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

        newPodcast = Podcast(
            name_of_podcast=audioFileMetadata['name_of_podcast'],
            duration=audioFileMetadata['duration'],
            host=audioFileMetadata['host'],
            participants=audioFileMetadata['participants']
        )

        try:
            newPodcast.save()
            response['data'] = (newPodcast.podcast_data())
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
            newAudiobook.save()
            response['data'] = (newAudiobook.audiobook_data())
            response['status'] = 200
            return make_response(jsonify(response), 200)

        except:
            abort(400, 'Invalid audiobook metadata')

    else:
        logging.error(
            f"Inernal server error trying to access API: {request.remote_addr}")

        abort(500, 'Internal Server Error')
