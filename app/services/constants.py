import os
from loguru import logger 

HOST_URL = os.getenv("HOST_URL")
CREATE_API_KEY = os.getenv("CREATE_API_KEY")
logger.info(f"create apikey {CREATE_API_KEY}")

TIME_EXPIRATION_URL= 7