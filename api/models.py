from api import dynamodb_client
from api.auth import check_encrypted_password, set_encrypted_password
import uuid
import boto3


class AccountManager:
    def __init__(self):
        self.dynamo_db = dynamodb_client
        self.table_name = "accounts"
        self.key_name = "account_id"
        self.key_type = "S"

    # Function to retrieve a user from the database.
    def check_account_db(self, username, password):
        try:
            response = self.dynamo_db.get_item(TableName=self.table_name,
                                               Key={self.key_name: {self.key_type: username}})
            # Below if we could not find the user in the db.
            if "Item" not in response or len(response['Item']) == 0:
                return None
            hashed_password = response['Item']['password']['S']

            # Below means the user has no password set.
            if not hashed_password or hashed_password == "":
                return None

            # Below means the user has a password set, but it doesn't match the one provided.
            if not check_encrypted_password(password, hashed_password):
                return None

            if 'account_type' not in response['Item']:
                return None
            return response['Item']['account_type']['S']

        except KeyError:
            return None

    def delete_account_db(self, username):
        try:
            response = self.dynamo_db.delete_item(TableName=self.table_name,
                                                  Key={self.key_name: {self.key_type: username}})
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return None
            return True
        except KeyError:
            return None

    def get_account_db(self, username):
        try:
            response = self.dynamo_db.get_item(TableName=self.table_name,
                                               Key={self.key_name: {self.key_type: username}})
            # Below if we could not find the user in the db.
            if "Item" not in response or len(response['Item']) == 0:
                return None
            return response['Item']
        except KeyError:
            return None

    def create_account_db(self, data):
        try:
            data['password'] = set_encrypted_password(data['password'])
            data["account_id"] = data.pop("username")
            account = {}
            for key, value in data.items():
                account[key] = {self.key_type: str(value)}

            response = self.dynamo_db.put_item(TableName=self.table_name, Item=account)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return None
            return True
        except KeyError:
            return None

    def update_account_password_db(self, account_id, password):
        try:
            password = set_encrypted_password(password)
            response = self.dynamo_db.update_item(TableName=self.table_name,
                                                  Key={self.key_name: {self.key_type: account_id}},
                                                  UpdateExpression="SET password = :password",
                                                  ExpressionAttributeValues={":password": {self.key_type: password}})

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return None

            return True
        except KeyError:
            return None


class OrganizationManager:
    def __init__(self):
        self.dynamo_db = dynamodb_client
        self.table_name = "organizations"
        self.key_name = "organization_id"
        self.key_type = "S"

    def get_all_organizations(self):
        try:
            response = self.dynamo_db.scan(TableName=self.table_name)
            print(response)
            if "Items" not in response or len(response['Items']) == 0:
                return None
            items = response['Items']

            # Used if more results still to return (Unlikely for this table)+
            while "LastEvaluatedKey" in response:
                response = self.dynamo_db.scan(TableName=self.table_name,
                                               ExclusiveStartKey=response['LastEvaluatedKey'])

                items.extend(response['Items'])

            return items
        except KeyError:
            return None

    def create_organization(self, data):
        try:
            data["organization_id"] = str(uuid.uuid4())
            organization = {}
            for key, value in data.items():
                organization[key] = {self.key_type: str(value)}
            response = self.dynamo_db.put_item(TableName=self.table_name, Item=organization)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return None
            return data["organization_id"]
        except KeyError:
            return None

    def get_organization(self, organization_id):
        try:
            response = self.dynamo_db.scan(TableName=self.table_name,
                                           key={self.key_name: {self.key_type: organization_id}})
            if "Item" not in response or len(response['Item']) == 0:
                return None
            return response['Item']
        except KeyError:
            return None


class MessageManager:
    def __init__(self):
        self.dynamo_db = dynamodb_client
        self.table_name = "messages"
        self.key_name = "message_id"
        self.key_type = "S"

    def create_message(self, message):
        try:
            message["message_id"] = message["user_id"] + "_" + message["gen_goal_id"] + "_" + str(uuid.uuid4())
            new_message = {}
            for key, value in message.items():
                new_message[key] = {self.key_type: str(value)}
            print("Running")
            response = self.dynamo_db.put_item(TableName=self.table_name, Item=new_message)
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                return None
            return message["message_id"]

        except KeyError:
            return None

    def get_messages(self, user_id, gen_goal_id):
        try:
            response = self.dynamo_db.scan(TableName=self.table_name,
                                           FilterExpression="user_id = :user_id AND gen_goal_id = :gen_goal_id",
                                           ExpressionAttributeValues={":user_id": {self.key_type: user_id},
                                                                      ":gen_goal_id": {self.key_type: gen_goal_id}})
            if "Items" not in response or len(response['Items']) == 0:
                return None
            return response['Items']
        except KeyError:
            return None
