import os
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
import sys
import re
import logging

load_dotenv()

MONGODB_URL = os.getenv('MONGO_DB_URL')

def validate_mongodb_url(url):
    pattern = re.compile(
        r"mongodb(\+srv)?://"
        r"(?P<sarojrailive>[^:]+):(?P<mangoSaroj25>[^@]+)@"
        r"(?P<host>[^/]+)/(?P<SAROJ>[^?]+)"
    )
    match = pattern.match(url)
    if not match:
        raise NetworkSecurityException('Invalid MongoDB URL format', 'Invalid MONGO_DB_URL', sys)

if not MONGODB_URL:
    raise NetworkSecurityException('MongoDB URL is not set in environment variables', 'Missing MONGO_DB_URL', sys)

validate_mongodb_url(MONGODB_URL)
logging.info(f"MongoDB URL: {MONGODB_URL}")
