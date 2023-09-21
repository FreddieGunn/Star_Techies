from datetime import datetime, timedelta
import jwt
from api import api
import hashlib

accounts = [
    {
        "username": "TESTUSER",
        "password": "SHA256"
    },
    {
        "username": "TESTUSER2",
        "password": "SHA2567"
    }
]


# This needs to be replaced with a db query which returns the account type or None
def check_account(username, password):

    # Commented until database is implemented
    """
    expected_encrypted_password = None
    password_correct = check_encrypted_password(password, expected_encrypted_password)
    if not password_correct:
        return None
    """
    for account in accounts:
        if account["username"] == username:
            if account["password"] == password:
                # Change this!!!
                return "Admin"
    return None


# Write a function using flask-jwt that takes the username and account_type as arguments and returns a JWT token.
def get_auth_token(username, account_type):
    # Change time delta to 20 mins when finished testing
    auth_token = jwt.encode({"username": username, "account_type": account_type,
                             "exp": datetime.utcnow() + timedelta(hours=24)},
                            api.config["SECRET_KEY"], "HS256")

    return auth_token


# Function to check the auth_token provided.
def check_token(auth_token):
    # Implemented as user may not provide a token.
    if not auth_token:
        return None
    try:
        decoded = jwt.decode(auth_token, api.config["SECRET_KEY"], algorithms=["HS256"])
        if "username" not in decoded or "account_type" not in decoded:
            return None
        return decoded
    except jwt.exceptions.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None


# Function to create refresh token
def get_refresh_token(username, account_type):
    refresh_token = jwt.encode({"username": username, "account_type": account_type,
                                "exp": datetime.utcnow() + timedelta(days=3)},
                               api.config["SECRET_REFRESH_KEY"], "HS256")
    return refresh_token


# Function to get a new auth_token from a refresh token.
def refresh_auth_token(user_refresh_token):
    # Implemented as user may not provide a token.
    if not user_refresh_token:
        return None

    try:
        decoded = jwt.decode(user_refresh_token, api.config["SECRET_REFRESH_KEY"], algorithms=["HS256"])
        print(decoded)
        if "username" not in decoded or "account_type" not in decoded:
            return None
        return get_auth_token(decoded["username"], decoded["account_type"])
    except jwt.exceptions.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None


def get_account_from_token(token_result):
    return token_result["username"], token_result["account_type"]


def set_encrypted_password(password):
    # Use sha256 to encrypt password
    # Salt could be stored in db or config file
    salt = "XZDJDcwevwgvjkerWDWD3243FEDVEf"
    password += salt
    return hashlib.sha256(password.encode()).hexdigest()


def check_encrypted_password(password, expected_encrypted_password):
    salt = "XZDJDcwevwgvjkerWDWD3243FEDVEf"
    password += salt
    return hashlib.sha256(password.encode()).hexdigest() == expected_encrypted_password
