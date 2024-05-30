from flask import Flask, Blueprint, request

from Config import ReturnCode, User
from Utils import Response, ResponseCode
from .user_services import UserServices

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['POST'])
def user_login():
	assert request.method == 'POST'

	user_request = request.get_json()
	username = user_request.get('username')
	password = user_request.get('password')

	# 仅在Python>=3.10可用match case
	match UserServices.login(username, password):
		case ReturnCode.SUCCESS:
			return Response.response(ResponseCode.LOGIN_SUCCESS, 'Login Success', User.query.filter_by(username=username).first().id)  # TODO:加入Session
		case ReturnCode.USER_NOT_EXIST:
			return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Username Wrong', None)
		case ReturnCode.PASSWORD_NOT_ALLOWED:
			return Response.response(ResponseCode.WRONG_PASSWORD, 'Password Wrong', None)
		case _:
			print('\033[34m[WARN]\033[0m | Controller-->Login | Unexpected Output')


@user_bp.route('/register', methods=['POST'])
def user_register():
	assert request.method == 'POST'

	user_request = request.get_json()
	match UserServices.register(user_request):
		case ReturnCode.SUCCESS:
			return Response.response(ResponseCode.SUCCESS, 'Register Success', User.query.filter_by(
				username=user_request.get('username')).first().id)
		case ReturnCode.USERNAME_NOT_ALLOWED:
			return Response.response(ResponseCode.USERNAME_NOT_ALLOW, 'Username Format Wrong', None)
		case ReturnCode.USERNAME_REPEATED:
			return Response.response(ResponseCode.USERNAME_REPEATED, 'Username Has Been Registered', None)
		case ReturnCode.PASSWORD_NOT_ALLOWED:
			return Response.response(ResponseCode.WRONG_PASSWORD, 'Password Format Wrong', None)
		case ReturnCode.MAIL_NOT_ALLOWED:
			return Response.response(ResponseCode.MAIL_NOT_ALLOW, 'Mail Format Wrong', None)
		case ReturnCode.MAIL_REPEATED:
			return Response.response(ResponseCode.MAIL_REPEATED, 'Mail Has Been Registered', None)
		case ReturnCode.INFO_NOT_ALLOWED:
			return Response.response(ResponseCode.BAD_REQUEST, 'Enter All Information', None)
		case _:
			print('\033[34m[WARN]\033[0m | Controller-->Login | Unexpected Output')


@user_bp.route('/<id>/deregister', methods=['DELETE'])
def user_deregister(id):
	if request.method == 'DELETE':
		pass


@user_bp.route('/send-code', methods=['POST'])
def user_send_code():
	if request.method == 'POST':
		pass


@user_bp.route('/<mail>/code', methods=['POST'])
def user_verify_code(mail):
	if request.method == 'POST':
		pass


@user_bp.route('/<id>/password', methods=['PUT'])
def user_change_password(id):
	if request.method == 'PUT':
		pass


@user_bp.route('/<id>', methods=['GET', 'PUT'])
def user_info(id):
	if request == 'GET':
		pass
	elif request == 'PUT':
		pass
