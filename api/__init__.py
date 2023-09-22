from flask import Flask
from config import Config
from boto3 import client

api = Flask(__name__)
api.config.from_object(Config)
s3_client = client('s3', aws_access_key_id=api.config['AWS_ACCESS_KEY_ID'],
                   aws_secret_access_key=api.config['AWS_SECRET_ACCESS_KEY'],
                   region_name=api.config['AWS_REGION'])
dynamodb_client = client('dynamodb', aws_access_key_id=api.config['AWS_ACCESS_KEY_ID'],
                         aws_secret_access_key=api.config['AWS_SECRET_ACCESS_KEY'],
                         region_name=api.config['AWS_REGION'])


# Flask requires these to be imported at the bottom
from api import routes, errors, auth, decorators
