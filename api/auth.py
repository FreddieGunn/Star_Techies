from datetime import datetime, timedelta
import jwt


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


def check_account(username, password):
    for account in accounts:
        if account["username"] == username:
            if account["password"] == password:
                return True
    return False


# Write a function using flask-jwt that takes the username and account_type as arguments and returns a JWT token.
def get_auth_token(username, account_type):
    # Secret key to be replaced with app.config["SECRET_KEY"]
    # Uses HS256 to encrypt data into the token
    # Change time delta to 20 mins when finished testing
    auth_token = jwt.encode({"username": username, "account_type": account_type,
                             "exp": datetime.utcnow() + timedelta(hours=24)},
                            "SECRET_KEY", "HS256")

    return auth_token


# Function to check the auth_token provided.
def check_token(auth_token):
    # Implemented as user may not provide a token.
    if not auth_token:
        return None
    try:
        decoded = jwt.decode(auth_token, "SECRET_KEY", algorithms=["HS256"])
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
                               "SECRET_REFRESH_KEY", "HS256")
    return refresh_token


# Function to get a new auth_token from a refresh token.
def refresh_auth_token(user_refresh_token):
    # Implemented as user may not provide a token.
    if not user_refresh_token:
        return None
    try:
        decoded = jwt.decode(user_refresh_token, "SECRET_REFRESH_KEY", algorithms=["HS256"])
        if "username" not in decoded or "account_type" not in decoded:
            return None
        return get_auth_token(decoded["username"], decoded["account_type"])
    except jwt.exceptions.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None


def get_account_from_token(token_result):
    return token_result["username"], token_result["account_type"]
