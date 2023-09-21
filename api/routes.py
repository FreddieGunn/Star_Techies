from flask import jsonify, request, abort
from api import api
from api.auth import check_account, get_auth_token, get_refresh_token, refresh_auth_token, set_encrypted_password
from api.decorators import admin_required, springboard_required, auth_required

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


# May need to change the auth_required decorator to remove Residents accessing other residents' data.
@api.route("/api/residents", methods=["GET"])
@auth_required
def get_residents(username, account_type):
    # Retrieve all residents here
    # Mock data for now
    return jsonify({"residents": users}), 200


@api.route("/api/residents/<resident_id>", methods=["GET"])
@auth_required
def get_resident(resident_id, username, account_type):
    # Retrieve the user here
    # Need to add filtering and check account type
    # Mock filter
    if int(resident_id) != 1 and int(resident_id) != 2:
        abort(404)

    # Mock data for now
    return jsonify({"residents": users[0]}), 200


@api.route("/api/residents/<resident_id>", methods=["DELETE"])
@admin_required
def delete_resident(resident_id, username, account_type):
    # Check the user exists
    # Replace with actual check function
    if int(resident_id) != 1 and int(resident_id) != 2:
        abort(404)

    # Delete the user from the db here

    return jsonify({"msg": "Resident deleted"}), 200


@api.route("/api/residents", methods=["POST"])
@springboard_required
def create_resident(username, account_type):
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

    account_type = check_account(username, password)
    if not account_type:
        abort(401)

    # X needs to be replaced with the account type. This will come from the db.
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


@api.route("/api/accounts", methods=["DELETE"])
@admin_required
def delete_account(username, account_type):
    data = request.get_json()
    account_to_delete = data.get("username")
    if not account_to_delete:
        abort(400)

    # Check the user exists in db
    account_exists = False
    if not account_exists:
        abort(404)

    # Delete the user from the db here

    return jsonify({"msg": "Account deleted"}), 200


@api.route("/api/accounts", methods=["POST"])
@springboard_required
def create_account(username, account_type):
    data = request.get_json()
    account_to_create = data.get("username")
    if not account_to_create:
        abort(400)

    # Check the username doesn't already exist in db

    # Get all values from data and write to db

    password = data.get("password")
    encrypted_password = set_encrypted_password(password)
    print(encrypted_password)
    return jsonify({"msg": "Account created"}), 201