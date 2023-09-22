from functools import wraps
from flask import request, abort
from api.auth import check_token, get_account_from_token


# All route decorators return the username and account_type which need to be arguments in routes.py functions.

# Custom decorator to check auth_token valid and account_type is Admin
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            abort(401)
        token_result = check_token(auth_token)
        if not token_result or token_result['account_type'] != 'Admin':
            abort(401)
        username, account_type = get_account_from_token(token_result)
        return func(*args, username=username, account_type=account_type, **kwargs)

    return wrapper


# Custom decorator to check auth_token valid and account_type is Admin or Springboard
def springboard_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            abort(401)
        token_result = check_token(auth_token)
        if not token_result or token_result['account_type'] not in ['Admin', 'Springboard']:
            abort(401)
        username, account_type = get_account_from_token(token_result)
        return func(*args, username=username, account_type=account_type, **kwargs)

    return wrapper


# Custom decorator to check auth_token is valid with any account_type
def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get("Authorization")
        if not auth_token:
            abort(401)
        token_result = check_token(auth_token)
        if not token_result:
            abort(401)
        username, account_type = get_account_from_token(token_result)
        return func(*args, username=username, account_type=account_type, **kwargs)

    return wrapper
