from flask import Blueprint, jsonify, make_response, request, abort
from functools import wraps
import logging
from database.AuthSchema import Auth
import logging


def vaidate_api_credentials(api_key):
    """
    Match API key
    @param api_key: API key from request
    @param api_client: API Client from request.
    @return: boolean
    """
    if api_key is None:
        return False

    try:
        # Find the client ID provided in the Auth DB
        client = Auth.objects(api_key=api_key).get()
        # Get the API key from the DB
        api_key_db = client.api_key

    except:
        return False

    ip = request.remote_addr

    if api_key_db == api_key:
        return True

    logging.error(
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
        api_key = request.args["api_key"]

        if vaidate_api_credentials(api_key):
            return function(*args, **kwargs)
        else:
            logging.warning(
                f"Unauthorized address trying to use API: {request.remote_addr}"
            )
            abort(401)

    return decorated_function
