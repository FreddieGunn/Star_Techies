from flask import jsonify
from api import api


@api.errorhandler(400)
def bad_request(e):
    return jsonify({"msg": "Bad request"}), 400


@api.errorhandler(401)
def unauthorized(e):
    return jsonify({"msg": "Authorization required"}), 401


@api.errorhandler(404)
def not_found(e):
    return jsonify({"msg": "Resource not found"}), 404


@api.errorhandler(500)
def internal_error(e):
    return jsonify({"msg": "Internal server error"}), 500
