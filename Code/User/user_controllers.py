from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, g
import requests

from Config import ReturnCode, User, UserConfig, db
from Utils import Response, ResponseCode, Helper
from .user_services import UserServices
from .Mail import SendMail

user_bp = Blueprint('user', __name__)

@user_bp.before_request
def user_login_interceptor():
	if request.path.startswith('/user'):
		if request.path in UserConfig.ALLOW_PATH:
			return
		if request.path.startswith('/user/') and request.path.endswith('/code'):
			# 验证码
			return
		if session.get('user_login') is None:
			return redirect(url_for('user.user_login'))  # 重新导航到/login视图函数，需要包含蓝图名称


@user_bp.route('/test')
def test():
	return render_template('login.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def user_login():
	if request.method == 'GET':
		return render_template('login.html')

	elif request.method == 'POST':
		user_request = request.form
		username = user_request.get('username')
		password = user_request.get('password')
		remember_me = user_request.get('remember_me')

		print('\033[35m[DEBUG]\033[0m | Login | Session : ', session)

		if session.get('user_login'):
			return Response.response(ResponseCode.LOGIN_SUCCESS, 'Login Success', User.query.filter_by(username=username).first().id)

		# 仅在Python>=3.10可用match case
		match UserServices.login(username, password):
			case ReturnCode.SUCCESS:
				if remember_me is not None:
					session['user_login'] = username
					session.permanent = True  # 启用Config的Session清空时间
				return Response.response(ResponseCode.LOGIN_SUCCESS, 'Login Success', User.query.filter_by(username=username).first().id)  # TODO:加入Session
			case ReturnCode.USER_NOT_EXIST:
				return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Username Wrong', None)
			case ReturnCode.PASSWORD_NOT_ALLOWED:
				return Response.response(ResponseCode.WRONG_PASSWORD, 'Password Wrong', None)
			case _:
				print('\033[34m[WARN]\033[0m | Controller-->Login | Unexpected Output')


@user_bp.route('/register', methods=['GET', 'POST'])
def user_register():
	if request.method == 'GET':
		print('Register Get')
		session.clear()  # 清空前者注册信息
		return render_template('register.html')

	elif request.method == 'POST':
		print(session)
		if session.get('username') is None:
			user_request = request.form
			if user_request['password'] != user_request['repassword']:
				return Response.response(ResponseCode.WRONG_PASSWORD, 'Password Not Same', None)
			for key in user_request.keys():
				if user_request[key] == '':
					return Response.response(ResponseCode.BAD_REQUEST, 'Enter All Information', None)
				session[key] = user_request[key]

			return redirect(url_for('user.user_send_code'))

		else:
			match UserServices.register(session, commit=True):
				case ReturnCode.SUCCESS:
					# return Response.response(ResponseCode.SUCCESS, 'Register Success', User.query.filter_by(
					# 	username=user_request.get('username')).first().id)
					return redirect(url_for('user.user_login'))
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


@user_bp.route('/send-code', methods=['GET', 'POST'])
def user_send_code():
	if request.method == 'GET':
		match UserServices.send_mail(session['mail']):
			case ReturnCode.SUCCESS:
				# return Response.response(ResponseCode.SUCCESS, 'Send Mail Success', mail)
				return redirect(url_for('user.user_verify_code', mail=session['mail']))
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, 'Send Mail FAIL', None)
			case ReturnCode.MAIL_NOT_ALLOWED:
				return Response.response(ResponseCode.FAILED, 'Mail Wrong', None)

	elif request.method == 'POST':
		mail = request.form.get('mail')
		match UserServices.send_mail(mail):
			case ReturnCode.SUCCESS:
				return Response.response(ResponseCode.SUCCESS, 'Send Mail Success', mail)
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, 'Send Mail FAIL', None)
			case ReturnCode.MAIL_NOT_ALLOWED:
				return Response.response(ResponseCode.FAILED, 'Mail Wrong', None)


@user_bp.route('/<mail>/code', methods=['GET', 'POST'])
def user_verify_code(mail):
	if request.method == 'GET':
		return render_template('check-code.html')

	elif request.method == 'POST':

		match UserServices.check_code(mail, request.form.get('code'), need_user_check=False):
			case ReturnCode.SUCCESS:

				response = requests.post('http://127.0.0.1:5000/user/register', json={'test':'test'})
				return redirect(url_for('user.user_login'))
			# return Response.response(ResponseCode.SUCCESS, 'Check Code Success', User.query.filter_by(mail=mail).first().id)
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, 'Check Code Fail', None)
			case ReturnCode.MAIL_NOT_ALLOWED:
				return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Mail Wrong', None)


@user_bp.route('/<id>/password', methods=['PUT'])
def user_change_password(id):
	assert request.method == 'PUT'

	user_request = request.get_json()
	match UserServices.change_password(id, user_request.get('password')):
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
	if request.method == 'GET':
		db_user = User.query.get(id)
		if db_user is None:
			return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Could Not Find The User', None)

		return Response.response(ResponseCode.SUCCESS, 'Get Info Success', Helper.to_dict(db_user))

	elif request.method == 'PUT':
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
