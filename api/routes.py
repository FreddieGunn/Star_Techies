from flask import jsonify, request, abort
from api import api
from api.auth import get_auth_token, get_refresh_token, refresh_auth_token
from api.decorators import admin_required, springboard_required, auth_required
from api.bucket import get_bucket
from api.models import AccountManager

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

# Initialise the account manager
account_manager = AccountManager()


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

    account_type = account_manager.check_account_db(username, password)
    if not account_type:
        abort(401)

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


@api.route("/api/accounts/<account_id>", methods=["DELETE"])
@admin_required
def delete_account(account_id, username, account_type):
    if account_id == username:
        return jsonify({"msg": "Cannot delete your own account"}), 400

    # Check the account exists
    if not account_manager.get_account_db(account_id):
        abort(404)

    # Delete the account
    if not account_manager.delete_account_db(account_id):
        abort(400)
    return jsonify({"msg": "Account deleted"}), 200


@api.route("/api/accounts", methods=["POST"])
@springboard_required
def create_account(username, account_type):
    data = request.get_json()
    mandatory_fields = ["username", "password", "account_type", "name", "surname"]

    # Check all mandatory fields are present
    for mandatory_field in mandatory_fields:
        if mandatory_field not in data:
            return jsonify({"msg": f"Missing mandatory field {mandatory_field}"}), 400

    # Check the username doesn't already exist in db
    if account_manager.get_account_db(data["username"]):
        return jsonify({"msg": "Username already exists"}), 400

    # Check the account type is valid
    if data["account_type"] not in ["Admin", "Springboard", "Resident", "External"]:
        return jsonify({"msg": "Invalid account type"}), 400

    # Only Admin can create Admin accounts
    if data["account_type"] == "Admin" and account_type != "Admin":
        return jsonify({"msg": "Only Admin can create Admin accounts"}), 400

    # Check the password is valid
    if len(data["password"]) < 8:
        return jsonify({"msg": "Password must be at least 8 characters"}), 400

    # Get all values from data and write to db
    if not account_manager.create_account_db(data):
        abort(400)

    return jsonify({"msg": "Account created", "username": data["account_id"]}), 201


# Test route to check bucket retrieval
@api.route("/api/get_bucket", methods=["GET"])
def get_buck():
    get_bucket()
    return jsonify({"msg": "Bucket retrieved"}), 200


# Change password route
@api.route("/api/change_password/<account_id>", methods=["POST"])
@auth_required
def change_password(account_id, username, account_type):
    data = request.get_json()
    password = data.get("password")
    if not password:
        return jsonify({"msg": "Missing password"}), 400

    # Only admin can change others passwords
    if account_id != username and account_type != "Admin":
        return jsonify({"msg": "Only Admin can change other users' passwords"}), 400

    # Check the username exists in db
    if not account_manager.get_account_db(account_id):
        return jsonify({"msg": "Username does not exist"}), 400

    # Check the password is valid
    if len(password) < 8:
        return jsonify({"msg": "Password must be at least 8 characters"}), 400

    # Update the password
    if not account_manager.update_account_password_db(account_id, password):
        abort(400)
    return jsonify({"msg": "Password updated"}), 200
