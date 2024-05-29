from flask import Flask, Blueprint, request
from Utils import Response, ResponseCode

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def user_login():
	if request.method == 'POST':
		user_request = request.get_json()
		username = user_request.get('username')
		password = user_request.get('password')

		# TEST
		return Response.response(ResponseCode.LOGIN_SUCCESS, 'Login Success', 1)