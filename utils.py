import boto3
def simplify_json_response(response):
    boto3.resource('dynamodb', region_name = 'us-east-1')
    deserializer = boto3.dynamodb.types.TypeDeserializer()
    python_data = {k: deserializer.deserialize(v) for k,v in response.items()}
    return python_data
    