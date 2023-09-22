from flask import Blueprint, jsonify
from utils import simplify_json_response

import boto3

staff_api = Blueprint('staff_api', __name__)


dynamo_client = boto3.client('dynamodb', region_name='us-east-1')

@staff_api.route('/login/<staffID>/<residentID>')
def get_resident_details(staffID, residentID):
    response = dynamo_client.get_item(
        TableName='Residents', Key={"ID": {"S":residentID}}, ProjectionExpression="#FirstName,#LastName,#AdmissionDate,Goal_ID", ExpressionAttributeNames={"#FirstName": "First Name", "#LastName": "Last Name", "#AdmissionDate": "Admission Date"})
    low_level_data = response["Item"]
    simplified_response_residents = simplify_json_response(low_level_data)
    
    goal_response = {"goals":[]}
    for goal_id in simplified_response_residents['Goal_ID']:
        response = dynamo_client.get_item(
            TableName='Goals', Key={"ID": {"S":goal_id}}, ProjectionExpression="ID,Goal_Name,Goal_Description")
        low_level_data = response["Item"]
        simplified_response_goals = simplify_json_response(low_level_data)
        goal_response["goals"].append(simplified_response_goals)
        
    del simplified_response_residents['Goal_ID']
        
    simplified_response_residents.update(goal_response)
    return simplified_response_residents
    
@staff_api.route('/login/<staffID>')
def get_staff_details(staffID):
    response = dynamo_client.get_item(
        TableName='accounts', Key={"account_id": {"S":staffID}}, ProjectionExpression="FirstName,surname,ID")
    low_level_data = response["Item"]
    simplified_response_accounts = simplify_json_response(low_level_data)
    
    response = dynamo_client.get_item(
        TableName='Staff', Key={"ID": {"S":staffID}}, ProjectionExpression="Staff_type")
    low_level_data = response["Item"]
    simplified_response_staff = simplify_json_response(low_level_data)
    
    simplified_response_accounts.update(simplified_response_staff)
    
    return simplified_response_accounts
    

    
    
    