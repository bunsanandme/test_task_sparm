import os


class Config(object):
    SECRET_KEY = "really bad secret key"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "mysql://root:admin@localhost:3306/test"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_APP = "run.py"
