from flask import Flask, abort, request, make_response, jsonify, Blueprint
from utils.authentication import require_apikey
from utils import validators
from database.AudioSchema import Audiobook, Song, Podcast
import logging
from mongoengine import *
import yaml


# Route Blueprint
delete_blueprint = Blueprint('delete', __name__)

# Get the config definitions
with open("config.yaml") as metadata:
    loader = yaml.load(metadata, Loader=yaml.FullLoader)
    audio_file_types = loader['audio-file-types']

# API Monitoring Logger
LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(filename="../logs/requests.log",
                    level=logging.INFO, format=LOG_FORMAT)

logger = logging.getLogger()

# @route   POST /api/v1/delete_audio_file
# @desc    Delete a specific audio file by type and ID (Song, Podcast, Audiobook)
# @access  Private
# @params  audioFileType, audioFileID


@delete_blueprint.route("/api/v1/delete_audio_file", methods=["POST"])
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

            logger.info(f"Deleted song with ID: {fileID}")

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

            logger.info(f"Deleted podcast with ID: {fileID}")

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

            logger.info(f"Deleted audiobook with ID: {fileID}")

        except DoesNotExist:
            response['errors'] = "Invalid audiobook metadata"
            response['status'] = 400
            return make_response(jsonify(response), 400)

    else:
        logger.info("API returned a server error")
        abort(500, 'Internal Server Error')
