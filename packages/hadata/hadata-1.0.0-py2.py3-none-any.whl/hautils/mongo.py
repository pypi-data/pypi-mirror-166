import os
from mongoengine import connect
from dotenv import load_dotenv

from hautils import logger

load_dotenv(override=False)

DATABASE_HOST = os.getenv('MONGO_HOST')
DATABASE_NAME = os.getenv('MONGO_DB')
DATABASE_USER = os.getenv("MONGO_USER")
DATABASE_PASS = os.getenv("MONGO_PASS")


def create_db():
    db_str = "mongodb://%s:%s@%s:27017/%s" % (DATABASE_USER, DATABASE_PASS, DATABASE_HOST, DATABASE_NAME)
    logger.info("connecting to database string %s" % (db_str,))
    connect(host=db_str)