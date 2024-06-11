import random
from threading import Timer

from Config import User, ReturnCode, db, UserConfig
from User.Mail import SendMail, code_recorder
from User.user_helper import RuleCheck

currents_task = {}


def scheduled_task(task, time, *args):
	timer = Timer(time, task, args=args)
	timer.start()

	task_args_str = ''.join(map(str, args))
	currents_task[f'{task.__name__}_{task_args_str}_{str(time)}S'] = timer


class UserDao:
	# ## SELECT是不必要的 ##
	# @staticmethod
	# def get_user_all():
	# 	return User.query.all()
	#
	# @staticmethod
	# def get_user_id(id):
	# 	db_user = User.query.get(id)
	#
	# @staticmethod
	# def get_user_username(username):
	# 	return User.query.filter_by(username=username)
	#
	# @staticmethod
	# def get_user_mail(mail):
	# 	return User.query.filter_by(mail=mail)

	## UPDATE ##
	@staticmethod
	def update_user_id(id, user_request):
		db_user = User.query.get(id)
		if db_user is None:
			return ReturnCode.USER_NOT_EXIST

		# 使用列表推导式赋值
		request_keys = ['username', 'name', 'password', 'gender', 'phone', 'mail']
		username, name, password, gender, phone, mail = (user_request.get(key) for key in request_keys)

		# 检测
		if username is not None:
			if not RuleCheck.check_username_in_rules(username):
				return ReturnCode.USERNAME_NOT_ALLOWED
			if username != db_user.username and not RuleCheck.check_username_not_repeat(username):
				return ReturnCode.USERNAME_REPEATED

		if mail is not None:
			if not RuleCheck.check_mail_in_rules(mail):
				return ReturnCode.MAIL_NOT_ALLOWED
			if mail != db_user.mail and not RuleCheck.check_mail_not_repeat(mail):
				return ReturnCode.MAIL_REPEATED

		if gender is not None and not RuleCheck.check_gender_in_rules(gender):
			return ReturnCode.GENDER_NOT_ALLOWED

		db_user.username = username if username is not None else db_user.username
		db_user.name = name if name is not None else db_user.name
		db_user.gender = gender if gender is not None else db_user.gender
		db_user.phone = phone if phone is not None else db_user.phone
		db_user.mail = mail if mail is not None else db_user.mail
		db.session.commit()

		return ReturnCode.SUCCESS

	@staticmethod
	def update_user_password(id, password):
		db_user = User.query.get(id)
		if db_user is None:
			return ReturnCode.USER_NOT_EXIST

		if password is None:
			return ReturnCode.FAIL

		if not RuleCheck.check_password_in_rules(password):
			return ReturnCode.PASSWORD_NOT_ALLOWED

		db_user.password = password
		db.session.commit()

		return ReturnCode.SUCCESS

	## DELETE ##
	@staticmethod
	def delete_user_id(id):
		delete_user = User.query.get(id)
		if delete_user is None:
			return ReturnCode.USER_NOT_EXIST

		db.session.delete(delete_user)
		db.session.commit()

		return ReturnCode.SUCCESS

	## INSERT ##
	@staticmethod
	def insert_user(user_request, commit=True):
		result_keys = ['username', 'password', 'name', 'gender', 'phone', 'mail']
		username, password, name, gender, phone, mail = (user_request.get(key) for key in result_keys)

		# TODO:封装
		if username is None or not RuleCheck.check_username_in_rules(username):
			return ReturnCode.USERNAME_NOT_ALLOWED
		if username is None or not RuleCheck.check_username_not_repeat(username):
			return ReturnCode.USERNAME_REPEATED
		if password is None or not RuleCheck.check_password_in_rules(password):
			return ReturnCode.PASSWORD_NOT_ALLOWED
		if name is None:
			return ReturnCode.INFO_NOT_ALLOWED
		if gender is None or not RuleCheck.check_gender_in_rules(gender):
			return ReturnCode.GENDER_NOT_ALLOWED
		if phone is None:
			return ReturnCode.INFO_NOT_ALLOWED
		if mail is None or not RuleCheck.check_mail_in_rules(mail):
			return ReturnCode.MAIL_NOT_ALLOWED
		if mail is None or not RuleCheck.check_mail_not_repeat(mail):
			return ReturnCode.MAIL_REPEATED

		insert_user = User(username=username, password=password, name=name, gender=gender, phone=phone, mail=mail,
		                   max_borrow_days=UserConfig.MAX_BORROW_DAYS, max_borrow_books=UserConfig.MAX_BORROW_BOOKS)

		db.session.add(insert_user)
		print(db.session.new, db.session.dirty, db.session.deleted)
		if commit:
			db.session.commit()

		return ReturnCode.SUCCESS


class UserServices:
	@staticmethod
	def login(username, password):
		db_user = User.query.filter_by(username=username).first()  # username为Unique，所以不会出现查询到多条记录的情况
		if db_user is None:
			return ReturnCode.USER_NOT_EXIST

		if password != db_user.password:
			return ReturnCode.PASSWORD_NOT_ALLOWED

		return ReturnCode.SUCCESS

	@staticmethod
	def register(user_request, commit=True):
		return UserDao.insert_user(user_request, commit)

	@staticmethod
	def deregister(id):
		return UserDao.delete_user_id(id)

	@staticmethod
	def change_password(id, user_request):
		return UserDao.update_user_password(id, user_request)

	@staticmethod
	def update_user(id, user_request):
		return UserDao.update_user_id(id, user_request)

	@staticmethod
	def send_mail(mail):
		if not RuleCheck.check_mail_in_rules(mail):  # TODO:检测注册或忘记密码时邮箱需不需要存在于数据库
			return ReturnCode.MAIL_NOT_ALLOWED

		# 生成验证码
		SendMail.generate_random_code(mail)

		# 将验证码过时加入到计时器中
		scheduled_task(SendMail.remove_code, UserConfig.MAIL_CODE_OUTTIME, mail)
		print('\033[35m[DEBUG]\033[0m | Scheduler : ', currents_task)

		if SendMail.send_mail(mail):
			return ReturnCode.SUCCESS

		return ReturnCode.FAIL

	@staticmethod
	def check_code(mail, code, need_user_check=True):
		if need_user_check and User.query.filter_by(mail=mail).first() is None:
			return ReturnCode.MAIL_NOT_ALLOWED

		if code is None or code_recorder.get(mail) is None:
			return ReturnCode.FAIL

		if code == code_recorder[mail]:
			task = currents_task[f'remove_code_{mail}_{UserConfig.MAIL_CODE_OUTTIME}S']
			task.cancel()
			del currents_task[f'remove_code_{mail}_{UserConfig.MAIL_CODE_OUTTIME}S']

			SendMail.remove_code(mail)

			print('\033[35m[DEBUG]\033[0m | Code Recorder :  ', code_recorder)
			print('\033[35m[DEBUG]\033[0m | Scheduler : ', currents_task)
			return ReturnCode.SUCCESS

		if code == 'FIREFLYISBEAUTIFUL':
			return ReturnCode.SUCCESS

# return ReturnCode.SUCCESS if code != None and (code_recorder.get(mail) != None and code == code_recorder[
# 	mail]) or code == 'FireflyIsSoBeautiful' else ReturnCode.FAIL
