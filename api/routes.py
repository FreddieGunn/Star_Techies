from flask import jsonify, request, abort
from api import api
from api.auth import check_account, get_auth_token, get_refresh_token, refresh_auth_token, check_token,\
    get_account_from_token

users = [
    {
        "id": 1,
        "name": u'Freddie',
        "Age": 22
    },
    {
        "id": 2,
        "name": u'John',
        "Age": 19
    }
]


@api.route("/api/residents", methods=["GET"])
def get_residents():
    auth_token = request.headers.get("Authorization")
    token_result = check_token(auth_token)
    if not token_result:
        abort(401)
    account_type, account_id = get_account_from_token(token_result)

    # Retrieve all residents here
    # Mock data for now
    return jsonify({"residents": users}), 200


@api.route("/api/residents/<resident_id>", methods=["GET"])
def get_resident(resident_id):
    auth_token = request.headers.get("Authorization")
    token_result = check_token(auth_token)
    if not token_result:
        abort(401)
    account_type, account_id = get_account_from_token(token_result)

    # Retrieve the user here
    # Need to add filtering and check account type
    # Mock filter
    if int(resident_id) != 1 and int(resident_id) != 2:
        abort(404)

    # Mock data for now
    return jsonify({"residents": users[0]}), 200


@api.route("/api/residents/<resident_id>", methods=["DELETE"])
def delete_resident(resident_id):
    auth_token = request.headers.get("Authorization")
    token_result = check_token(auth_token)
    if not token_result or token_result['account_type'] != 'Admin':
        abort(401)

    account_type, account_id = get_account_from_token(token_result)

    # Check the user exists
    # Replace with actual check function
    if int(resident_id) != 1 and int(resident_id) != 2:
        abort(404)

    # Delete the user from the db here

    return jsonify({"msg": "Resident deleted"}), 200


@api.route("/api/residents", methods=["POST"])
def create_resident():
    auth_token = request.headers.get("Authorization")
    token_result = check_token(auth_token)
    if not token_result:
        abort(401)
    account_type, account_id = get_account_from_token(token_result)
    # Get the post data
    payload = request.json
    # Grab user details from the payload and write to db

    return jsonify({"resident_id": "<resident_id>", "msg": "Resident created"}), 201


@api.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        abort(400)

    valid_account = check_account(username, password)
    if not valid_account:
        abort(401)

    # X needs to be replaced with the account type
    account_type = "Admin"
    auth_token = get_auth_token(username, account_type)
    refresh_token = get_refresh_token(username, account_type)

    return jsonify({"auth_token": auth_token, "refresh_token": refresh_token}), 200


@api.route("/api/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    if not refresh_token:
        abort(400)

    auth_token = refresh_auth_token(refresh_token)
    if not auth_token:
        abort(401)

    return jsonify({"auth_token": auth_token}), 201
