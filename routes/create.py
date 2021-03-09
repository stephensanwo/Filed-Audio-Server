from flask import Flask, abort, request, make_response, jsonify, Response, Blueprint
from utils.authentication import require_apikey
from utils import validators
from database.AudioSchema import Audiobook, Song, Podcast
import logging
from mongoengine import *


# Route Blueprint
create_blueprint = Blueprint('create', __name__)

# API Monitoring Logger
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="./logs/requests.log",
                    level=logging.INFO, format=LOG_FORMAT)

logger = logging.getLogger()

# @route   POST /api/v1/create
# @desc    Create new audio file (Song, Podcast, Audiobook)
# @access  Private
# @params  audioFileType, audioFileMatadata

# @require_apikey


@create_blueprint.route("/api/v1/create", methods=["POST"])
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

            logger.info("Created new Song")

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
            logger.info("Created new Podcast")

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
            logger.info("Created new Audiobook")

        except:
            abort(400, 'Invalid audiobook metadata')

    else:
        logger.info("API returned a server error")
        abort(500, 'Internal Server Error')
