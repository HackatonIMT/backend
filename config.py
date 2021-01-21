import os


class Config(object):
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_DATABASE_URL'),
    }
