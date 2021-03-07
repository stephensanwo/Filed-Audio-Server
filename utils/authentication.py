from flask import Blueprint, jsonify, make_response, request, abort
from functools import wraps
import bcrypt
import logging
from database.AuthSchema import Auth


LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(
    filename="./logs/api-authentication.log", level=logging.INFO, format=LOG_FORMAT
)

logger = logging.getLogger()


def vaidate_api_credentials(api_key, api_client):
    """
    Match API key
    @param api_key: API key from request
    @param api_client: API Client from request.
    @return: boolean
    """
    if api_key is None or api_client is None:

        return False
    try:
        # Find the client ID provided in the Auth DB
        client = Auth.objects(client_email=api_client).get()

        # Get the Hashed API key for the client_id from the DB and unhash with bcrypt
        hashed_api_key = client.api_key
        user = client.client_email
    except:
        return False

    ip = request.remote_addr()
    if bcrypt.checkpw(api_key.encode("utf-8"), hashed_api_key.encode("utf-8")):
        logger.info(f"API Key Authenticated for user: {user}, ip: {ip}")
        return True

    logger.error(
        f"API Key Authentication failed, Wrong API Key provided by user: {ip}")
    return False


# Decorator for requiring api key on routes
def require_apikey(function):
    """
    @param function: function
    @return: decorator, return the wrapped function or abort json object.
    """

    @wraps(function)
    def decorated_function(*args, **kwargs):
        api_key = request.headers["api_key"]
        api_client = request.headers["api_client"]

        if vaidate_api_credentials(api_key, api_client):
            return function(*args, **kwargs)
        else:
            logger.warning(
                f"Unauthorized address trying to use API: {request.remote_addr}"
            )
            abort(401)

    return decorated_function
