from datetime import datetime
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


# Write a function using flask-jwt that takes the username and accountType as arguments and returns a JWT token.
def get_auth_token(username, accountType):
    # Secret key to be replaced with app.config["SECRET_KEY"]
    # Uses HS256 to encrypt data into the token

    auth_token = jwt.encode({"username": username, "accountType": accountType,
                             "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=20)},
                            "SECRET_KEY", "HS256")

    return auth_token


# Function to check the auth_token provided.
def check_token(auth_token):
    # Implemented as user may not provide a token.
    if not auth_token:
        return None
    try:
        decoded = jwt.decode(auth_token, "SECRET_KEY", algorithms=["HS256"])
        if "username" not in decoded or "accountType" not in decoded:
            return None
        return {"username": decoded["username"], "accountType": decoded["accountType"]}
    except jwt.exceptions.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None


# Function to create refresh token
def get_refresh_token(username, accountType):
    refresh_token = jwt.encode({"username": username, "accountType": accountType,
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=3)},
                               "SECRET_REFRESH_KEY", "HS256")
    return refresh_token


# Function to get a new auth_token from a refresh token.
def refresh_auth_token(user_refresh_token):
    # Implemented as user may not provide a token.
    if not user_refresh_token:
        return None
    try:
        decoded = jwt.decode(user_refresh_token, "SECRET_REFRESH_KEY", algorithms=["HS256"])
        if "username" not in decoded or "accountType" not in decoded:
            return None
        return get_auth_token(decoded["username"], decoded["accountType"])
    except jwt.exceptions.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
