from flask import Blueprint, jsonify
from utils import simplify_json_response

import boto3

staff_api = Blueprint('staff_api', __name__)


dynamo_client = boto3.client('dynamodb', region_name='us-east-1')

@staff_api.route('/login/<staffID>/<residentID>')
def get_resident_details(staffID, residentID):
    dynamo_client = boto3.client('dynamodb', region_name='us-east-1')
    response = dynamo_client.get_item(
        TableName='Residents', Key={"ID": {"S":residentID}}, ProjectionExpression="#FirstName,#LastName,#AdmissionDate", ExpressionAttributeNames={"#FirstName": "First Name", "#LastName": "Last Name", "#AdmissionDate": "Admission Date"})
    low_level_data = response["Item"]
    simplified_response = simplify_json_response(low_level_data)
    return simplified_response
    