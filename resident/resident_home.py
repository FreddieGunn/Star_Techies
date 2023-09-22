from flask import Blueprint, jsonify
from utils import simplify_json_response

import boto3

resident_api = Blueprint('resident_api', __name__)


dynamo_client = boto3.client('dynamodb', region_name='us-east-1')

@resident_api.route('/get-items/<ID>')
def get_items(ID):
    dynamo_client = boto3.client('dynamodb', region_name='us-east-1')
    response = dynamo_client.get_item(
        TableName='Residents', Key={"ID": {"S":ID}})
    low_level_data = response["Item"]
    return simplify_json_response(low_level_data)
    
    

    
    
        
    
    
    