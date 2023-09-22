from flask import Flask
from config import Config
from boto3 import client

api = Flask(__name__)
api.config.from_object(Config)
s3_client = client('s3')
dynamodb_client = client('dynamodb')


# Flask requires these to be imported at the bottom
from api import routes, errors, auth, decorators
