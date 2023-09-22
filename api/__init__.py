from flask import Flask
from config import Config
from boto3 import client
import sys
sys.path.insert(0, '/home/ec2-user/environment/Star_Techies')
from resident.resident_home import resident_api
from staff.staff_view_endpoints import staff_api

api = Flask(__name__)
api.config.from_object(Config)
s3_client = client('s3')
dynamodb_client = client('dynamodb')

api.register_blueprint(resident_api)
api.register_blueprint(staff_api)

# Flask requires these to be imported at the bottom
from api import routes, errors, auth, decorators
