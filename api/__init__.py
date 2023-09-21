from flask import Flask
from config import Config

api = Flask(__name__)
api.config.from_object(Config)

# Need to add db connections

from api import routes, errors