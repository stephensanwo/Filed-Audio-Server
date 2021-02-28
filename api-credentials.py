import sys
import bcrypt
import logging
import uuid
from database.AuthSchema import Auth

LOG_FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(
    filename="./logs/api-credentials.log",
    level=logging.INFO,
    format=LOG_FORMAT,
)

logger = logging.getLogger()


def create_api_credentials():
    client_email = str(sys.argv[1])
    api_key = str(uuid.uuid4())

    print(
        f"""
        Your Credentials
        ------------------
        Email: {client_email}  
        API Key: {api_key}
        ------------------
        Please keep your crednetials safe
        """
    )
    logger.info(f"API credentials generated for {client_email}")

    # Hashing API credentials for the DB
    api_key = bcrypt.hashpw(api_key.encode("utf-8"), bcrypt.gensalt())

    logger.info(f"API Key Hashed: {api_key}")

    api_credentials = Auth(
        client_email=client_email, api_key=api_key,
    )
    api_credentials.save()

    logger.info("API Credentials stored in Auth databse successfully")
    return "API Credentials Created Successfully"


create_api_credentials()

# Example in CLI
# python credentials.py admin-stephen-sanwo stephen.sanwo@icloud.com admin
