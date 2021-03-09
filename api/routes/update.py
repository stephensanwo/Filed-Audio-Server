from flask import Flask, abort, request, make_response, jsonify, Blueprint
from utils.authentication import require_apikey
from utils import validators
from database.AudioSchema import Audiobook, Song, Podcast
from mongoengine import *
from utils.configs import get_filetypes
import logging


# Route Blueprint
update_blueprint = Blueprint('update', __name__)

# Get the config definitions

audio_file_types = get_filetypes()

# @route   POST /api/v1/update_audio_file
# @desc    Update a specific audio file by type and ID (Song, Podcast, Audiobook)
# @access  Private
# @params  audioFileType, audioFileID


@update_blueprint.route("/api/v1/update_audio_file", methods=["POST"])
@require_apikey
def update_audio_file():
    response = {"errors": {}, "data": {}, "status": ""}

    # Validate request parameters
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

    # Validate request body

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

    # Param and Body must be the same file type
    if audioFileType == "song" and fileType == "song":
        errors, valid = validators.validateSongMetadata(audioFileMetadata)

        if not valid:
            response['errors'] = errors
            response['status'] = 400
            return make_response(jsonify(response), 400)

        try:
            # Find song if it exists
            song = Song.objects(id=fileID).get()
            song.update(
                name_of_song=audioFileMetadata['name_of_song'], duration=audioFileMetadata['duration']
            )
            song.reload()

            response['data'] = (song.song_data())
            response['status'] = 200
            return make_response(jsonify(response), 200)

        except DoesNotExist:
            response['errors'] = "Invalid song metadata"
            response['status'] = 400
            return make_response(jsonify(response), 400)

        # Param and Body must be the same file type
    elif audioFileType == "podcast" and fileType == "podcast":
        errors, valid = validators.validatePodcastMetadata(audioFileMetadata)

        if not valid:
            response['errors'] = errors
            response['status'] = 400
            return make_response(jsonify(response), 400)

        try:
            # Find podcast if it exists
            podcast = Podcast.objects(id=fileID).get()
            podcast.update(
                name_of_podcast=audioFileMetadata['name_of_podcast'],
                duration=audioFileMetadata['duration'],
                host=audioFileMetadata['host'],
                participants=audioFileMetadata['participants']
            )
            podcast.reload()

            response['data'] = (podcast.podcast_data())
            response['status'] = 200
            return make_response(jsonify(response), 200)

        except DoesNotExist:
            response['errors'] = "Invalid podcast metadata"
            response['status'] = 400
            return make_response(jsonify(response), 400)

     # Param and Body must be the same file type
    elif audioFileType == "audiobook" and fileType == "audiobook":
        errors, valid = validators.validateAudiobookMetadata(audioFileMetadata)

        if not valid:
            response['errors'] = errors
            response['status'] = 400
            return make_response(jsonify(response), 400)

        try:
            # Find audiobook if it exists
            audiobook = Audiobook.objects(id=fileID).get()
            audiobook.update(
                title_of_audiobook=audioFileMetadata['title_of_audiobook'],
                author_of_title=audioFileMetadata['author_of_title'],
                narrator=audioFileMetadata['narrator'],
                duration=audioFileMetadata['duration']
            )
            audiobook.reload()

            response['data'] = (audiobook.audiobook_data())
            response['status'] = 200
            return make_response(jsonify(response), 200)

        except DoesNotExist:
            response['errors'] = "Invalid audiobook metadata"
            response['status'] = 400
            return make_response(jsonify(response), 400)

    else:
        logging.error(
            f"Inernal server error trying to access API: {request.remote_addr}"
        )
        abort(500, 'Internal Server Error')
