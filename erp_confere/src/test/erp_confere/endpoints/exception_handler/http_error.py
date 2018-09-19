from flask import jsonify


def forbidden(message):

	return jsonify({'message': message}), 403