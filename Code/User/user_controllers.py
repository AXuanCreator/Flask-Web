from flask import Flask, Blueprint, request

from Config import ReturnCode, User
from Utils import Response, ResponseCode
from .user_services import UserServices
from .Mail import SendMail

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
			return Response.response(ResponseCode.BAD_REQUEST, 'Username Format Wrong', None)
		case ReturnCode.USERNAME_REPEATED:
			return Response.response(ResponseCode.USERNAME_REPEATED, 'Username Has Been Registered', None)
		case ReturnCode.PASSWORD_NOT_ALLOWED:
			return Response.response(ResponseCode.WRONG_PASSWORD, 'Password Format Wrong', None)
		case ReturnCode.MAIL_NOT_ALLOWED:
			return Response.response(ResponseCode.BAD_REQUEST, 'Mail Format Wrong', None)
		case ReturnCode.MAIL_REPEATED:
			return Response.response(ResponseCode.BAD_REQUEST, 'Mail Has Been Registered', None)
		case ReturnCode.INFO_NOT_ALLOWED:
			return Response.response(ResponseCode.BAD_REQUEST, 'Enter All Information', None)
		case _:
			print('\033[34m[WARN]\033[0m | Controller-->Login | Unexpected Output')


@user_bp.route('/<id>/deregister', methods=['DELETE'])
def user_deregister(id):
	assert request.method == 'DELETE'

	match UserServices.deregister(id):
		case ReturnCode.SUCCESS:
			return Response.response(ResponseCode.SUCCESS, 'Deregister Success', id)
		case ReturnCode.USER_NOT_EXIST:
			return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Could Not Find The User', None)



@user_bp.route('/send-code', methods=['POST'])
def user_send_code():
	if request.method == 'POST':
		match UserServices.send_mail(request.get_json().get('mail')):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, 'Send Mail Success', None)
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, 'Send Mail FAIL', None)




@user_bp.route('/<mail>/code', methods=['POST'])
def user_verify_code(mail):
	if request.method == 'POST':
		pass


@user_bp.route('/<id>/password', methods=['PUT'])
def user_change_password(id):
	assert request.method == 'PUT'

	user_request = request.get_json()
	match UserServices.change_password(id, user_request):
		case ReturnCode.SUCCESS:
			return Response.response(ResponseCode.SUCCESS, 'Update Password Success', id)
		case ReturnCode.USER_NOT_EXIST:
			return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Could Not Find The User', None)
		case ReturnCode.FAIL:
			return Response.response(ResponseCode.BAD_REQUEST, 'Password Null', None)
		case ReturnCode.PASSWORD_NOT_ALLOWED:
			return Response.response(ResponseCode.WRONG_PASSWORD, 'Password Format Wrong', None)


@user_bp.route('/<id>', methods=['GET', 'PUT'])
def user_info(id):
	if request == 'GET':
		db_user = User.query.get(id)
		if db_user is None:
			return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Could Not Find The User', None)

		return Response.response(ResponseCode.SUCCESS, 'Get Info Success', db_user)

	elif request == 'PUT':
		user_request = request.get_json()
		match UserServices.update_user(id, user_request):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, 'Update Info Success', id)
			case ReturnCode.USER_NOT_EXIST:
				return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Could Not Find The User', None)
			case ReturnCode.USERNAME_NOT_ALLOWED:
				return Response.response(ResponseCode.BAD_REQUEST, 'Username Format Wrong', None)
			case ReturnCode.USERNAME_REPEATED:
				return Response.response(ResponseCode.USERNAME_REPEATED, 'Username Has Been Registered', None)
			case ReturnCode.GENDER_NOT_ALLOWED:
				return Response.response(ResponseCode.BAD_REQUEST, 'Enter True Gender', None)
			case ReturnCode.MAIL_NOT_ALLOWED:
				return Response.response(ResponseCode.BAD_REQUEST, 'Mail Format Wrong', None)
			case ReturnCode.MAIL_REPEATED:
				return Response.response(ResponseCode.BAD_REQUEST, 'Mail Has Been Registered', None)

