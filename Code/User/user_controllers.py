from flask import Flask, Blueprint, request, session, redirect, url_for, render_template

import User
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
	return render_template('reset-password.html')


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
	# POST请求分为两种
	# 1.查询session是否存储着用户信息，若有，则直接载入到数据库并清空Session内容，然后返回至Login
	# 2.若无，则显示Register的页面信息
	if request.method == 'GET':
		if session.get('register') is not None and session['register']:
			match UserServices.register(session, commit=True):
				case ReturnCode.SUCCESS:
					print('\033[35m[DEBUG]\033[0m | Register GET | Session Clear')
					session.clear()  # 清空注册信息
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
		else:
			return render_template('register.html')


	# POST请求则用于将Register的页面信息存入Session里
	elif request.method == 'POST':
		print('\033[35m[DEBUG]\033[0m | Register POST Before Loading | Session : ', session)

		# 对Session进行赋值操作
		user_request = request.form
		if user_request['password'] != user_request['repassword']:
			return Response.response(ResponseCode.WRONG_PASSWORD, 'Password Not Same', None)
		for key in user_request.keys():
			if user_request[key] == '':
				return Response.response(ResponseCode.BAD_REQUEST, 'Enter All Information', None)
			session[key] = user_request[key]
		session['register'] = True  # 启用注册状态

		print('\033[35m[DEBUG]\033[0m | Register POST After Loading | Session : ', session)
		return redirect(url_for('user.user_send_code'))  # GET请求，因为从Session中获取信息



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
	# GET请求负责两种情况：
	# 1. Session里存有Mail内容，直接处理
	# 2. Session里无Mail内容，则返回HTML并通过POST请求进行处理
	if request.method == 'GET':
		if session.get('mail') is not None:
			match UserServices.send_mail(session['mail']):
				case ReturnCode.SUCCESS:
					return redirect(url_for('user.user_verify_code', mail=session['mail']))  # 由于该URL带有参数，需要显式传入
				case ReturnCode.FAIL:
					return Response.response(ResponseCode.FAILED, 'Send Mail FAIL', None)
				case ReturnCode.MAIL_NOT_ALLOWED:
					return Response.response(ResponseCode.FAILED, 'Mail Wrong', None)
		else:
			return render_template('reset-password-mail.html')

	elif request.method == 'POST':
		mail = request.form.get('mail')
		match UserServices.send_mail(mail):
			case ReturnCode.SUCCESS:
				return redirect(url_for('user.user_verify_code', mail=mail))  # 由于该URL带有参数，需要显式传入
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
				print('\033[35m[DEBUG]\033[0m | Verify Code POST | Session : ', session)

				session['user_login'] = mail  # 验证状态——通过
				session.permanent = True  # 启用Config的Session清空时间

				# 当Session存有Register信息时，则代表此时为注册状态
				# 若无，则代表此时在重置密码阶段
				# 注意，这种写法较为暴力，但在验证码使用场景较少时简单有效
				if session.get('register') is not None and session.get('register'):
					return redirect(url_for('user.user_register'))
				else:
					return redirect(url_for('user.user_change_password',  id=User.query.filter_by(mail=mail).first().id))
				# return ReturnCode.
			# return Response.response(ResponseCode.SUCCESS, 'Check Code Success', User.query.filter_by(mail=mail).first().id)
			case ReturnCode.FAIL:
				return Response.response(ResponseCode.FAILED, 'Check Code Fail', None)
			case ReturnCode.MAIL_NOT_ALLOWED:
				return Response.response(ResponseCode.ACCOUNT_NOT_EXIST, 'Mail Wrong', None)


@user_bp.route('/<id>/password', methods=['GET', 'POST'])
def user_change_password(id):
	# 该视图函数需要验证状态
	if request.method == 'GET':
		return render_template('reset-password.html')

	# 为何更新信息时不使用PUT？
	# 因为Jinja2的HTML表单仅仅支持POST和GET :)
	elif request.method == 'POST':
		user_request = request.form
		if user_request['password'] != user_request['repassword']:
			return Response.response(ResponseCode.WRONG_PASSWORD, 'Password Not Same', None)

		match UserServices.change_password(id, user_request.get('password')):
			case ReturnCode.SUCCESS:    # TODO:实际上并没有对密码是否和原先的密码重复做判断
				print('\033[35m[DEBUG]\033[0m | Reset Password | Success : ', id)
				return redirect(url_for('user.user_login'))
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
