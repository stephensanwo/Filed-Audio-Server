from flask import Flask, abort, request, make_response, jsonify, Blueprint
from utils.authentication import require_apikey
from utils import validators
from database.AudioSchema import Audiobook, Song, Podcast
from mongoengine import *
from utils.configs import get_filetypes
import logging


# Route Blueprint
delete_blueprint = Blueprint('delete', __name__)

# Get the config definitions

audio_file_types = get_filetypes()

# @route   POST /api/v1/delete_audio_file
# @desc    Delete a specific audio file by type and ID (Song, Podcast, Audiobook)
# @access  Private
# @params  audioFileType, audioFileID


@delete_blueprint.route("/api/v1/delete_audio_file", methods=["POST"])
@require_apikey
def delete_audio_file():
    response = {"errors": {}, "message": "", "status": ""}

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

    if fileType == "song":
        try:
            # Find song if it exists
            song = Song.objects(id=fileID).get()
            song.delete()

            response['message'] = (f"Song with ID: {fileID} deleted")
            response['status'] = 200
            return make_response(jsonify(response), 200)

        except DoesNotExist:
            response['errors'] = "Invalid song metadata"
            response['status'] = 400
            return make_response(jsonify(response), 400)

    elif fileType == "podcast":

        try:
            # Find podcast if it exists
            podcast = Podcast.objects(id=fileID).get()
            podcast.delete()

            response['message'] = (f"Podcast with ID: {fileID} deleted")
            response['status'] = 200
            return make_response(jsonify(response), 200)

        except DoesNotExist:
            response['errors'] = "Invalid podcast metadata"
            response['status'] = 400
            return make_response(jsonify(response), 400)

            return make_response(jsonify(response), 400)

    elif fileType == "audiobook":

        try:
            # Find audiobook if it exists
            audiobook = Audiobook.objects(id=fileID).get()
            audiobook.delete()

            response['message'] = (f"Audiobook with ID: {fileID} deleted")
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
