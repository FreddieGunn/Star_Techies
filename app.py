from flask import Flask, jsonify
import boto3


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"
    
@app.route('/get-items/<ID>')
def get_items(ID):
    dynamo_client = boto3.client('dynamodb', region_name='us-east-1')
    return dynamo_client.get_item(
        TableName='Residents', Key={"ID": {"S":ID}})
    

if __name__ == "__main__":
    app.run(debug=True, port=8080)